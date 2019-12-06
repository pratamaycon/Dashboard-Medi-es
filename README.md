# Trabalho Redes de Computadores 1 2019.1

## Título
<h3>Medição de desempenho de rede.</h3>

## Descrição
<<<<<<< HEAD
<p>Nosso objetivo é medir o desempenho da rede de ip pré definidos, acima criamos uma ferramenta que simula um ping igual do CMD Windows que dá além de informar se aquele ip está funcional ou não, ele dá algumas informações estatísticas que não ajudam entender o que está acontencendo com cada de um nossos pacotes que foram enviados.</p>
=======

<p>
 
Nosso objetivo é medir o desempenho da rede de ips pré definidos, enviamos pacotes para os ips especificados e escutamos suas respostas se o ips estiverem ativos, recebemos uma resposta do solicitando e se não,isso irá gerar diferentes exceções de acordo 
com os possíveis problemas, como por exemplo, ip destino ou host que não existe. O solicitante irá nos retornar uma mensagem assim 

**"A solicitação ping não pôde encontrar o (Nome do Host). Verifique o nome e tente novamente."**.

Além disso, após essa verificação o programa exibe prints no console exibindo dados referentes ao solicitante esses dados são referentes ao tamanho do pacotes, ip destino, número de sequência, tempo de vida e a latência que seriam todos os tempos dados em milisegundos. Essa informações de latência posteriormente são usadas para gerar um arquivo csv que é gerado toda vez após a execução do ping, e esse arquivo será utilizado como um dataset para a construção de um dashboard referente ao tempo de Minimo, Médio e Máximo de cada envio e sua resposta.

</p>

<p></p>
>>>>>>> 25914ff9e5bd86694d44bc225d9c7d8c2d77d9b9

## Pré-requisitos
* Para a execução é necessário utilizar Python 3 na versão inferior a 3.8
* Versão Recomedada _Python 3.6_
* Para plotar o gráfico necessário baixar _pip install matplotlib_ **mais informações** em: [Módulo matplotlib](https://pypi.org/project/matplotlib/)
* Baixar Módulo _numpy_ com o comando _pip install numpy_ **mais informações** em: [Módulo numpy](https://pypi.org/project/numpy/)
* Baixar Módulo _pandas_ com o comando _pip install pandas_ **mais informações** em: [Módulo pandas](https://pypi.org/project/pandas/)


## Instruções de Execução
**Dependendo da Configuração da sua Váriavel de Ambiente pode se usar _python_ ou _py_ para rodar os programas em python 3**
* Rodar o comando _py ping_.py
* Rodar o comando _py dash_.py

## Autoria e Contribuições
<p>Nomes:</p>

* Maycon Prata
* Rafael Oliveira Neto
* Yuan Stewart Pereira Cardoso
* Wagner Rangel Junior





