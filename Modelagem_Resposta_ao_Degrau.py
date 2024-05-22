#BIBLIOTECAS
import tkinter as tk            #Para o pop-up de escolher o txt com os dados
from tkinter import filedialog  #Para o pop-up de escolher o txt com os dados
import matplotlib.pyplot as plt #Para o plot dos gráficos
import math                     #Para gerar as curvas modeladas
import os                       #Para criar uma pasta com os gráficos
import sympy as sp              #Para enccontrar a função de transferência
import control as ctrl

#VARIÁVEIS GLOBAIS
SerieTemporal = []
deslocamento_em_t = None
linha_deslocamento_em_t = None

#FUNÇÕES

def ler_arquivo(arquivo): #Abre o txt e salva os dados no vetor SerieTemporal
    global SerieTemporal
    try:                                    #Tenta abrir e ler o txt
        with open(arquivo, "r") as f:           #Abre o txt e fecha no final
            for line in f:                      #Varre as linhas do txt
                linha = line.strip().split(';') #Divide cada linha em colunas de acordo com o separador ";"
                SerieTemporal.append(linha)     #Salva no vetor
        print("Arquivo lido com sucesso.")
    except FileNotFoundError:               #Caso tenha dado erro
        print("Arquivo não encontrado.")
        abrir_arquivo()                         #Abre a janela pra escolher o arquivo

def abrir_arquivo():    #Exibe a janela pra escolher o arquivo
    arquivo = filedialog.askopenfilename(title="Selecione o arquivo") #Exibe o pop-up

    if arquivo:             #Se o arquivo existe, lê
        ler_arquivo(arquivo)
    else:                   # Finaliza a prog se nenhum arquivo for selecionado
        print("Nenhum arquivo selecionado.")
        exit()

def inicio_degrau(): #BUSCA ONDE OCORRE O DEGRAU (acha o deslocamento em t)
    for i in range(1,len(SerieTemporal)-2): #Procura a primeira derivada maior que zero e retorna o índice do dado seguinte
        derivada = (float(SerieTemporal[i+1][1]) - float(SerieTemporal[i][1])) / (float(SerieTemporal[i+1][0]) - float(SerieTemporal[i][0]))
        if derivada > 0:
            return i+1
    return -1 #Caso não tenha encontrado o degrau

#BUSCA O PRIMEIRO VALOR QUE ATENDE AOS CRITÉRIOS DE ESTABILIDADE
def buscar_regime_permanente():    #Procura o instante de tempo t' que a função está em estado permamente
    global SerieTemporal                #Chama a variável global pra dentro da função

    for i in range(50, len(SerieTemporal)): #Varre o vetor apartir do 50º dado

        valores = [float(SerieTemporal[i-j][2]) for j in range(20)] #Cria um vetor de amostra com os 50 dados anteriores a t'
        media = sum(valores) / 20       #Calcula a média da amostra                      
        diferenca = max(valores) - min(valores) #Calcula a amplitude da amostra

        if diferenca < 0.007 * media:   #Caso a aplitude desta amostra seja menor que 0,7% da média é estado permanente
            return i                    # retorna o índice da primeira linha que atende às condições
        
    return -1                           # se não encontrar nenhuma linha que atenda às condições (Código de Erro)



#BUSCA O VALOR MAIS PRÓXIMO DE 62,3% DO REGIME PERMANENTE (seu t correspondente é o tal)
def buscar_primeiro_tal(valor_referencia):
    global SerieTemporal                #Chama a variável global pra dentro da função

    menor_diferenca = float('inf')      #Fala que a menor diferença é infinito
    linha_mais_proxima = None           #Declara a variável local
    
    for i, linha in enumerate(SerieTemporal[1:], start=1): #Varre o vetor
        diferenca = abs(float(linha[2]) - valor_referencia) #Calcula a diferença do dado com o 62,3%
        if diferenca < menor_diferenca: #Caso seja a menor diferença encontrada, salva o indice da linha
            menor_diferenca = diferenca #Atualiza o valor da menor diferença
            linha_mais_proxima = linha  #Atualiza o índice da linha do dado com a menor diferença

    if linha_mais_proxima:
        return linha_mais_proxima # retorna o índice da linha do dado mais próximo de 62,3%
    else:
        return None  # se não encontrar nenhuma linha (Código de Erro)

#BUSCA O INTERVALO QUE COMTÉM O VALOR 62,3% DO REGIME PERMANENTE E INTERPOLA O t CORRESPONDENTE
def buscar_primeiro_tal_interpolado(valor_referencia):
    global SerieTemporal                            #Chama a variável global SerieTemporal pra dentro da função
    global deslocamento_em_t                        #Chama a variável global eslocamento_em_t pra dentro da função
    linha_anterior = None                           #Declara a variável local
    valor_anterior = float(SerieTemporal[1][2])     #Inicializa a variável local

    for i, linha_atual in enumerate(SerieTemporal[2:], start=2):      #Varre a série
        valor_atual = float(linha_atual[2])                           #Obtém o valor atual
        if valor_anterior < valor_referencia <= valor_atual:    #Verifica se o valor de 62,3% está entre o dado atual e o anterior
            
            #Realiza a interpolação
            x1 = float(linha_anterior[0])
            y1 = float(linha_anterior[2])
            x2 = float(linha_atual[0])
            y2 = float(linha_atual[2])
            constante_de_tempo = (x1 + (valor_referencia - y1) * (x2 - x1) / (y2 - y1)) - deslocamento_em_t

            return constante_de_tempo   #Retorna o valor da constante interpolada (e sai do for)
        
        valor_anterior = valor_atual    #Atualiza qual é o valor anterior
        linha_anterior = linha_atual    #Atualiza qual é o indice da linha anterior
            
    return -1 # se não encontrar o intervalo que contém o valor de 62,3% (Código de Erro)



#CRIA OS DADOS DO GRÁFICO DE ACORDO COM OS PARÂMETROS E ADICIONA NO VETOR SERIETEMPORAL
def curva_modelada(constante_de_tempo, ganho_da_exponencial, indice,titulo):
    global SerieTemporal                                #Chama a variável global pra dentro da função
    ganho_do_degrau = float(SerieTemporal[indice][2])   #Obtém o valor em regime permanente da função
    global deslocamento_em_t                            #Chama a variável global deslocamento_em_t pra dentro da função
    global linha_deslocamento_em_t                      #Chama a variável global linha_deslocamento_em_t pra dentro da função

    SerieTemporal[0].append(titulo)     # Adiciona o nome da nova série na primeira linha

    for linha in SerieTemporal[1:linha_deslocamento_em_t]:    #Cria dados antes do degrau
        valor_nova_coluna = float(SerieTemporal[indice][2])*1-ganho_da_exponencial #Cálcula o valor inicial da função
        linha.append(valor_nova_coluna) #Salva o valor inicial da curva no vetor
              
    for linha in SerieTemporal[linha_deslocamento_em_t:]:     #Varre cada linha após o degrau e cálcula o valor da função
        tempo = float(linha[0])
        valor_nova_coluna = ganho_do_degrau*1-ganho_da_exponencial*math.exp(-(tempo-deslocamento_em_t) / constante_de_tempo)
        linha.append(valor_nova_coluna)
    print("")    
    print("Modelagem de ",titulo)
    print("TIPO DA EQUAÇÃO:")
    print("ganho_do_degrau*1-ganho_da_exponencial*e^(-(t-deslocamento_em_t) / constante_de_tempo)")
    print("VALORES DOS PARÂMETROS:")
    print("ganho_do_degrau: ",ganho_do_degrau)
    print("ganho_da_exponencial: ",ganho_da_exponencial)
    print("deslocamento_em_t: ",deslocamento_em_t)
    print("constante_de_tempo: ",constante_de_tempo)



#INÍCIO DO ALGORITMO

# GERANDO O VETOR COM AS SÉRIES TEMPORAIS
try:                                    # Tenta abrir o arquivo pra salvar os dados
    ler_arquivo("yfjhgf.txt")
except FileNotFoundError:               # Se o arquivo não for encontrado, abre a caixa de diálogo para selecionar manualmente
    print("Arquivo não encontrado.")    
    abrir_arquivo()

#Obtém onde a exponencial deve começar (onde ocorre o degrau)
linha_deslocamento_em_t = inicio_degrau()      
if linha_deslocamento_em_t!=-1:
    deslocamento_em_t = float(SerieTemporal[linha_deslocamento_em_t][0])
    print("Deslocamento em t igual a ",deslocamento_em_t)
else:
    print("Não foi possível determinar o deslocamento em t. Algumas funções não serão acionadas.")

#DETERMINAÇÃO DO REGIME PERMANENTE
indice_RP = buscar_regime_permanente() #Índice da linha onde entra em regime permanente
if indice_RP != -1:
    print("Regime permanente em: ", SerieTemporal[indice_RP])
else:
    print("Nenhum valor que atenda às condições especificadas de regime permanente foi encontrado.")


if indice_RP != -1:

    #DETERMINAÇÃO DO VALOR DE TAL    
    valor_referencia = (float(SerieTemporal[indice_RP][2])-float(SerieTemporal[1][2])) * 0.632 + float(SerieTemporal[1][2])

    #Método Aproximado
    linha_mais_proxima = buscar_primeiro_tal(valor_referencia)
    if linha_mais_proxima:
        print("Resultado mais proximo de 1 tal:", linha_mais_proxima)
    else:
        print("Não foi possível encontrar um resultado proximo de 1 tal.")

    #Método Interpolado
    if deslocamento_em_t:
        constante_de_tempo = buscar_primeiro_tal_interpolado(valor_referencia)
        if constante_de_tempo != -1:
            print("Valor da constante de tempo interpolado para", valor_referencia, "->", constante_de_tempo)
        else:
            print("Erro: não foi possível encontrar as duas linhas para interpolação.")

    #GERAÇÃO DA CURVA A PARTIR DOS PARÂMETROS    
    ganho_da_exponencial = float(SerieTemporal[indice_RP][2])-float(SerieTemporal[1][2]) #Calcula o ganho da componente exponencial
    if linha_mais_proxima and deslocamento_em_t:
        curva_modelada(float(linha_mais_proxima[0])-deslocamento_em_t,ganho_da_exponencial,indice_RP,"aproximado")
    if constante_de_tempo != -1 and deslocamento_em_t:
        curva_modelada(float(constante_de_tempo),ganho_da_exponencial,indice_RP,"interpolado")

        # Definindo as variáveis
        t, s = sp.symbols('t s')
        trava=1
        if trava:
            KD, KE, CT = sp.symbols('KD KE CT')
        else:
            KD = float(SerieTemporal[indice_RP][2]) 
            KE = ganho_da_exponencial
            CT=constante_de_tempo         
        
        # Definindo a função no domínio do tempo
        y_t = KD*1-KE*sp.exp(-t/ CT)

        # Fazendo a Transformada de Laplace
        Y_s = sp.laplace_transform(y_t, t, s)
        X_s = KD*1/s
        print('A X(s) é: ',X_s)
        print('A Y(s) é: ',Y_s)

        FTMA = sp.simplify(Y_s[0]/ X_s)
        print('A FTMA é: ',FTMA)

# Criação do gráfico com todas as curvas
nomes_funcoes = SerieTemporal[0][1:]
dados = [[float(valor) for valor in linha] for linha in SerieTemporal[1:]]
dados_transpostos = list(map(list, zip(*dados)))
tempo = dados_transpostos[0]



# Criação do diretório para salvar os gráficos
if not os.path.exists('plots'):
    os.makedirs('plots')

plt.figure()  # Cria uma nova figura para todas as séries
for i, nome in enumerate(nomes_funcoes):
    if i != 0:
        plt.plot(tempo, dados_transpostos[i + 1], label=nome)

plt.xlabel('Tempo')
plt.ylabel('Valor')
plt.title('Gráfico de Séries Temporais')
plt.legend()
plt.grid(True)
plt.savefig(f'plots/Gráfico_de_Séries_Temporais.png')  # Salva o gráfico com todas as séries
plt.close()  # Fecha a figura para evitar sobrecarga de memória

# Plota cada série separadamente e salva como PNG
for i, nome in enumerate(nomes_funcoes):
    plt.figure()  # Cria uma nova figura para cada série
    plt.plot(tempo, dados_transpostos[i + 1])
    plt.xlabel('Tempo')
    plt.ylabel('RPM')
    plt.title(f'Gráfico de {nome}')
    plt.grid(True)
    plt.savefig(f'plots/SerieTemporal_{nome}.png')
    plt.close()  # Fecha a figura para evitar sobrecarga de memória

print("Gráficos salvos com sucesso na pasta 'plots'.")



