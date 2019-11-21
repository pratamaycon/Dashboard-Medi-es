import requests
import sys
import time


link = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
file_name = "downloaded.png"
start = time.clock()
response = requests.get(link, stream=True)
with open(file_name, "wb") as f:
    print("Downloading %s" % file_name)
    response = requests.get(link, stream=True)
    total_length = int(response.headers.get('content-length'))
    print(response.headers["content-type"])
    print(total_length / 1024, "Kb")
    print(int(response.headers["Age"]) * (10 ** -6), "Sec")
    print(response.headers["date"])

    if total_length is None: # no content length header
        f.write(response.content)
    else:
        dl = 0
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r[%s%s] %s bps" % ('=' * done, ' ' * (50-done), dl//(time.clock() - start)))
            sys.stdout.flush()