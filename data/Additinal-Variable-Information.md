## **Additional Variable Information**

The dataset consists of 10,000 data points stored as rows with 14 features in columns.

**UID:** unique identifier ranging from 1 to 10000

**product ID:** consisting of a letter *L*, *M*, or *H* for low (50% of all products), medium (30%) and high (20%) as product quality variants and a variant-specific serial number

**air temperature [K]:** generated using a random walk process later normalized to a standard deviation of 2 K around 300 K

**process temperature [K]:** generated using a random walk process normalized to a standard deviation of 1 K, added to the air temperature plus 10 K.

**rotational speed [rpm]:** calculated from a power of 2860 W, overlaid with a normally distributed noise

**torque [Nm]:** torque values are normally distributed around 40 Nm with a Ïƒ = 10 Nm and no negative values. 

**tool wear [min]:** The quality variants H/M/L add 5/3/2 minutes of tool wear to the used tool in the process. and a

**'machine failure':** label that indicates, whether the machine has failed in this particular datapoint for any of the following failure modes are true.

## **The machine failure consists of five independent failure modes.**

**tool wear failure (TWF):** the tool will be replaced of fail at a randomly selected tool wear time between 200 â€“ 240 mins (120 times in our dataset). At this point in time, the tool is replaced 69 times, and fails 51 times (randomly assigned). <u> **##** *Observando o dataset, pode-se constatar que na verdade existem **43 casos** de falha nessas condições.* **##** </u>



**heat dissipation failure (HDF):** heat dissipation causes a process failure, if the difference between air - and process temperature is below 8.6 K and the toolâ€™s rotational speed is below 1380 rpm. This is the case for 115 data points.

**power failure (PWF):** the product of torque and rotational speed (in rad/s) equals the power required for the process. If this power is below 3500 W or above 9000 W, the process fails, which is the case 95 times in our dataset.

**overstrain failure (OSF):** if the product of tool wear and torque exceeds 11,000 minNm for the L product variant (12,000 M, 13,000 H), the process fails due to overstrain. This is true for 98 datapoints.

**random failures (RNF):** each process has a chance of 0,1 % to fail regardless of its process parameters. This is the case for only 5 datapoints, less than could be expected for 10,000 datapoints in our dataset. <u> **##** *Observando o dataset, pode-se constatar que na verdade existem **19 casos** de falha nessas condições.* **##** </u>

**If at least one of the above failure modes is true, the process fails and the 'machine failure' label is set to 1. It is therefore not transparent to the machine learning method, which of the failure modes has caused the process to fail.**

---

*Versão emp portugês*

## **Informações Adicionais sobre as Variáveis** 

O conjunto de dados consiste em 10.000 pontos de dados armazenados como linhas com 14 recursos (variáveis) em colunas. 

**UID:** identificador único que varia de 1 a 10000 

**product ID (ID do produto):** consiste em uma letra *L*, *M* ou *H* para baixa (*low* - 50% de todos os produtos), média (*medium* - 30%) e alta (*high* - 20%) qualidade, servindo como variantes de qualidade do produto, seguidas por um número de série específico da variante 

**air temperature [K] (temperatura do ar):** gerada por meio de um processo de passeio aleatório (*random walk*), posteriormente normalizada para um desvio padrão de 2 K em torno de 300 K 

**process temperature [K] (temperatura do processo):** gerada por meio de um processo de passeio aleatório, normalizada para um desvio padrão de 1 K, adicionada à temperatura do ar mais 10 K 

**rotational speed [rpm] (velocidade de rotação):** calculada a partir de uma potência de 2860 W, sobreposta por um ruído normalmente distribuído 

**torque [Nm]:** os valores de torque são normalmente distribuídos em torno de 40 Nm com um σ = 10 Nm e sem valores negativos 

**tool wear [min] (desgaste da ferramenta):** as variantes de qualidade H/M/L adicionam 5/3/2 minutos de desgaste à ferramenta utilizada no processo 

**'machine failure' (falha da máquina):** rótulo (*label*) que indica se a máquina falhou nesse ponto de dados específico para qualquer um dos modos de falha listados a seguir. 

## **A falha da máquina consiste em cinco modos de falha independentes.** 

**tool wear failure (TWF - falha por desgaste da ferramenta):** a ferramenta será substituída ou falhará em um tempo de desgaste de ferramenta selecionado aleatoriamente entre 200 e 240 minutos (120 vezes em nosso conjunto de dados). Neste momento, a ferramenta é substituída 69 vezes e falha 51 vezes (atribuído aleatoriamente). <u> **##** *Observando o dataset, pode-se constatar que na verdade existem **43 casos** de falha nessas condições.* **##** </u>


**heat dissipation failure (HDF - falha por dissipação de calor):** a dissipação de calor causa uma falha no processo se a diferença entre a temperatura do ar e a do processo for inferior a 8,6 K e a velocidade de rotação da ferramenta for inferior a 1380 rpm. Este é o caso de 115 pontos de dados. 

**power failure (PWF - falha de energia/potência):** o produto do torque pela velocidade de rotação (em rad/s) é igual à potência necessária para o processo. Se essa potência for inferior a 3500 W ou superior a 9000 W, o processo falha, o que ocorre 95 vezes em nosso conjunto de dados. 

**overstrain failure (OSF - falha por sobreesforço):** se o produto do desgaste da ferramenta pelo torque exceder 11.000 minNm para a variante de produto L (12.000 para M, 13.000 para H), o processo falha devido a sobreesforço. Isso é verdadeiro para 98 pontos de dados. 

**random failures (RNF - falhas aleatórias):** cada processo tem uma chance de 0,1% de falhar, independentemente de seus parâmetros de processo. Este é o caso de apenas 5 pontos de dados, menos do que o esperado para os 10.000 pontos de dados em nosso conjunto de dados. <u> **##** *Observando o dataset, pode-se constatar que na verdade existem **19 casos** de falha nessas condições.* **##** </u>

**Se pelo menos um dos modos de falha acima for verdadeiro, o processo falha e o rótulo 'machine failure' é definido como 1. Portanto, não é transparente para o método de aprendizado de máquina qual dos modos de falha fez o processo falhar.**
