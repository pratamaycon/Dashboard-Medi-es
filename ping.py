import os
import sys
import socket
import struct
import select
import time
import signal

if sys.platform == "win32":     # Identificador do SO 
    default_timer = time.clock  # No Windows, o melhor timer é o time.clock ()
else:
    default_timer = time.time   # Na maioria das outras plataformas, o melhor timer é o time.time ()

NUM_PACKETS = 4    # números de pacotes
PACKET_SIZE = 64   # Tamanho de pacotes
WAIT_TIMEOUT = 3.0  

#=============================================================================#
# ICMP parameters

ICMP_ECHOREPLY = 0  # Echo reply (per RFC792)
ICMP_ECHO = 8  # Echo request (per RFC792)
ICMP_MAX_RECV = 2048  # Max size of incoming buffer

MAX_SLEEP = 1000


class MyStats:
    thisIP = "0.0.0.0"  # Máscara do IP
    pktsSent = 0    # pacotes enviados
    pktsRcvd = 0    # pacotes recebidos
    minTime = 999999999 # tempo mínimo
    maxTime = 0     # tempo máximo
    totTime = 0     # tempo total
    avrgTime = 0    # tempo médio
    fracLoss = 1.0  # pacotes que fracassaram


myStats = MyStats  # Minhas estatísticas

#=============================================================================#


def checksum(source_string): # verificar a integridade de dados transmitidos
    """Se um arquivo é exatamente o mesmo arquivo depois de uma transferência. 
    Para verificar se não foi alterado por terceiros ou se não está corrompido."""
    countTo = (int(len(source_string)/2))*2 # tamanho do bytes de dados
    suma = 0   # soma de verificacao
    count = 0  # contador

    loByte = 0 # bit menos significativo
    hiByte = 0 # bit mais significativo
    while count < countTo:
        """Um indicador da ordem de bytes nativa. Isso terá o valor 
        'big' em plataformas big-endian (primeiro byte mais significativo) e 
        'little' em plataformas little-endian (menos significativo primeiro byte)."""
        if (sys.byteorder == "little"):
            loByte = source_string[count]     # bit menos significativo
            hiByte = source_string[count + 1] # bit mais significativo
        else:
            loByte = source_string[count + 1] # bit menos significativo
            hiByte = source_string[count]     # bit mais significativo
    
        suma = suma + (hiByte * 256 + loByte) # soma de verificacao com os bytes 
        count += 2

    if countTo < len(source_string):  # Check for odd length
        loByte = source_string[len(source_string)-1]
        print(loByte)
        suma += loByte

    # Truncate suma to 32 bits (a variance from ping.c, which
    suma &= 0xffffffff
    # uses signed ints, but overflow is unlikely in ping)

    suma = (suma >> 16) + (suma & 0xffff)    # Add high 16 bits to low 16 bits
    suma += (suma >> 16)                    # Add carry from above (if any)
    answer = ~suma & 0xffff                # Invert and truncate to 16 bits
    answer = socket.htons(answer)

    return answer

#=============================================================================#


def do_one(myStats, destIP, hostname, timeout, mySeqNumber, packet_size, quiet=False):
    """
    Returns either the delay (in ms) or None on timeout.
    """
    delay = None

    try:  # One could use UDP here, but it's obscure
        mySocket = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    except socket.error as e:
        print("failed. (socket error: '%s')" % e.args[1])
        raise  # raise the original error

    my_ID = os.getpid() & 0xFFFF

    sentTime = send_one_ping(mySocket, destIP, my_ID, mySeqNumber, packet_size)
    if sentTime == None:
        mySocket.close()
        return delay

    myStats.pktsSent += 1

    recvTime, dataSize, iphSrcIP, icmpSeqNumber, iphTTL = receive_one_ping(
        mySocket, my_ID, timeout)

    mySocket.close()

    if recvTime:
        delay = (recvTime-sentTime)*1000
        if not quiet:
            print("%d bytes from %s: icmp_seq=%d ttl=%d time=%d ms" % (
                dataSize, socket.inet_ntoa(struct.pack("!I", iphSrcIP)), icmpSeqNumber, iphTTL, delay)
            )
        myStats.pktsRcvd += 1
        myStats.totTime += delay
        if myStats.minTime > delay:
            myStats.minTime = delay
        if myStats.maxTime < delay:
            myStats.maxTime = delay
    else:
        delay = None
        print("Request timed out.")

    return delay

#=============================================================================#


def send_one_ping(mySocket, destIP, myID, mySeqNumber, packet_size):
    """
    Send one ping to the given >destIP<.
    """
    #destIP  =  socket.gethostbyname(destIP)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    # (packet_size - 8) - Remove header size from packet size
    myChecksum = 0

    # Make a dummy heder with a 0 checksum.
    header = struct.pack(
        "!BBHHH", ICMP_ECHO, 0, myChecksum, myID, mySeqNumber
    )

    padBytes = []
    startVal = 0x42
    # 'cose of the string/byte changes in python 2/3 we have
    # to build the data differnely for different version
    # or it will make packets with unexpected size.
    if sys.version[:1] == '2':
        bytes = struct.calcsize("d")
        data = ((packet_size - 8) - bytes) * "Q"
        data = struct.pack("d", default_timer()) + data
    else:
        for i in range(startVal, startVal + (packet_size-8)):
            padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
        #data = bytes(padBytes)
        data = bytearray(padBytes)

    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)  # Checksum is in network order

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "!BBHHH", ICMP_ECHO, 0, myChecksum, myID, mySeqNumber
    )

    packet = header + data

    sendTime = default_timer()

    try:
        # Port number is irrelevant for ICMP
        mySocket.sendto(packet, (destIP, 1))
    except socket.error as e:
        print("General failure (%s)" % (e.args[1]))
        return

    return sendTime

#=============================================================================#


def receive_one_ping(mySocket, myID, timeout):
    """
    Receive the ping from the socket. Timeout = in ms
    """
    timeLeft = timeout/1000

    while True:  # Loop while waiting for packet or timeout
        startedSelect = default_timer()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (default_timer() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return None, 0, 0, 0, 0

        timeReceived = default_timer()

        recPacket, addr = mySocket.recvfrom(ICMP_MAX_RECV)

        ipHeader = recPacket[:20]
        iphVersion, iphTypeOfSvc, iphLength, \
            iphID, iphFlags, iphTTL, iphProtocol, \
            iphChecksum, iphSrcIP, iphDestIP = struct.unpack(
                "!BBHHHBBHII", ipHeader
            )

        icmpHeader = recPacket[20:28]
        icmpType, icmpCode, icmpChecksum, \
            icmpPacketID, icmpSeqNumber = struct.unpack(
                "!BBHHH", icmpHeader
            )

        if icmpPacketID == myID:  # Our packet
            dataSize = len(recPacket) - 28
            #print (len(recPacket.encode()))
            return timeReceived, (dataSize+8), iphSrcIP, icmpSeqNumber, iphTTL

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return None, 0, 0, 0, 0

#=============================================================================#


def dump_stats(myStats):
    """
    Show stats when pings are done
    """
    print("\n----%s PYTHON PING Statistics----" % (myStats.thisIP))

    if myStats.pktsSent > 0:
        myStats.fracLoss = (myStats.pktsSent -
                            myStats.pktsRcvd)/myStats.pktsSent

    print("%d packets transmitted, %d packets received, %0.1f%% packet loss" % (
        myStats.pktsSent, myStats.pktsRcvd, 100.0 * myStats.fracLoss
    ))

    if myStats.pktsRcvd > 0:
        print("round-trip (ms)  min/avg/max = %d/%0.1f/%d" % (
            myStats.minTime, myStats.totTime/myStats.pktsRcvd, myStats.maxTime
        ))

    print("")
    return

#=============================================================================#


def signal_handler(signum, frame):
    """
    Handle exit via signals
    """
    dump_stats()
    print("\n(Terminated with signal %d)\n" % (signum))
    sys.exit(0)

#=============================================================================#


def verbose_ping(hostname, timeout=WAIT_TIMEOUT, count=NUM_PACKETS,
                 packet_size=PACKET_SIZE, path_finder=False):
    """
    Send >count< ping to >destIP< with the given >timeout< and display
    the result.
    """
    signal.signal(signal.SIGINT, signal_handler)   # Handle Ctrl-C
    if hasattr(signal, "SIGBREAK"):
        # Handle Ctrl-Break e.g. under Windows
        signal.signal(signal.SIGBREAK, signal_handler)

    myStats = MyStats()  # Reset the stats

    mySeqNumber = 0  # Starting value

    try:
        destIP = socket.gethostbyname(hostname)
        print("\nPYTHON PING %s (%s): %d data bytes" %
              (hostname, destIP, packet_size))
    except socket.gaierror as e:
        print(hostname)
        print()
        return

    myStats.thisIP = destIP

    for i in range(count):
        delay = do_one(myStats, destIP, hostname,
                       timeout, mySeqNumber, packet_size)

        if delay == None:
            delay = 0

        mySeqNumber += 1

        # Pause for the remainder of the MAX_SLEEP period (if applicable)
        if (MAX_SLEEP > delay):
            time.sleep((MAX_SLEEP - delay)/1000)

    dump_stats(myStats)

#=============================================================================#


def quiet_ping(hostname, timeout=WAIT_TIMEOUT, count=NUM_PACKETS,
               packet_size=PACKET_SIZE, path_finder=False):
    """
    Same as verbose_ping, but the results are returned as tuple
    """
    myStats = MyStats()  # Reset the stats
    mySeqNumber = 0  # Starting value

    try:
        destIP = socket.gethostbyname(hostname)
    except socket.gaierror as e:
        return False

    myStats.thisIP = destIP

    # This will send packet that we dont care about 0.5 seconds before it starts
    # acrutally pinging. This is needed in big MAN/LAN networks where you sometimes
    # loose the first packet. (while the switches find the way... :/ )
    if path_finder:
        fakeStats = MyStats()
        do_one(fakeStats, destIP, hostname, timeout,
               mySeqNumber, packet_size, quiet=True)
        time.sleep(0.5)

    for i in range(count):
        delay = do_one(myStats, destIP, hostname, timeout,
                       mySeqNumber, packet_size, quiet=True)

        if delay == None:
            delay = 0

        mySeqNumber += 1

        # Pause for the remainder of the MAX_SLEEP period (if applicable)
        if (MAX_SLEEP > delay):
            time.sleep((MAX_SLEEP - delay)/1000)

    if myStats.pktsSent > 0:
        myStats.fracLoss = (myStats.pktsSent -
                            myStats.pktsRcvd)/myStats.pktsSent
    if myStats.pktsRcvd > 0:
        myStats.avrgTime = myStats.totTime / myStats.pktsRcvd

    # return tuple(max_rtt, min_rtt, avrg_rtt, percent_lost)
    return myStats.maxTime, myStats.minTime, myStats.avrgTime, myStats.fracLoss

#=============================================================================#

def verificaHost(hostname):
 resultado = "" # String vazia
 try:
  socket.gethostbyname(hostname)  # Retorna o endereço de ip
  return hostname
 except socket.error:
  resultado = "A solicitação ping não pôde encontrar o host %s. Verifique o nome e tente novamente."%(hostname)
  return resultado

#=============================================================================#


def main():

    ping = verbose_ping 
    ping(verificaHost('www.wikipedia.org'), timeout=3000) # tentativa de ping no wikipedia
    ping(verificaHost('172.217.29.100'), timeout=3000) # tentativa de ping no google via ip
    ping(verificaHost('www.google.com'), timeout=3000) # tentativa de ping no google
    ping(verificaHost('localhost'), timeout=3000) # tentativa de ping no localhost
    ping(verificaHost('fla2019.com'), timeout=3000) # pingando em sites que não existem 
    ping(verificaHost('ZeldaGOT.com'), timeout=3000) # pingando em sites que não existem

if __name__ == '__main__':
    main()