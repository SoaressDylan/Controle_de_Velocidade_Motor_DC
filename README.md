# Controle de Velocidade Motor DC
 O Código está dividido entre Arduino, Python e Matlab.
# Arduíno:
   Em primeira instância, o calculo de furos(N) foi calculado, com N sendo apresentado a partir de uma medição com o auxílio de um tacômetro, chegamos em N = 400 , em sequência foi calculado seu alfa, através da seguinte relação:
V(rpm) =  ((cont/n)/(delta(T)*10^-6)) . 60 , onde n*delta(T) = alfa.
Assim , chegamos a relação de alfa = 60;
o Código foi implementado a partir da saída PWM (Modulação por Largura de Pulso), não foi necessário bibliotecas a serem incluídas.
# Python:
 Os Arquivos para a leitura e a obtenção de gráficos e sua Função de Transferência em Malha Aberta , foram realizadas pelo python, aqui foram necessária a inclusão de algumas bibliotecas como:
 
