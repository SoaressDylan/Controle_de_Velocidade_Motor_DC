import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar o arquivo txt
file_path = 'Dados para gráfico de Resposta ao Degrau.txt'  # Caminho do seu arquivo

# Ler o arquivo usando pandas
df = pd.read_csv(file_path, sep=';')

# Extrair as colunas
tempo = df.iloc[:, 0]
entrada = df.iloc[:, 1]
saida = df.iloc[:, 2]
rpm_medio = df.iloc[:, 3]

# Obter os títulos das colunas
titulo_tempo = df.columns[0]
titulo_entrada = df.columns[1]
titulo_saida = df.columns[2]
titulo_rpm_medio = df.columns[3]

# Parâmetros da equação modelada
#ganho_do_degrau = 2108.57142857143
#ganho_da_exponencial = 1834.2857142857158
#deslocamento_em_t = 0.9875
#constante_de_tempo = 0.03890500000000019
ganho_do_degrau=  2108.5714
ganho_da_exponencial=  1829.314288
deslocamento_em_t=  0.9875
constante_de_tempo=  0.039595000597916874

# Calcular os valores da equação modelada para cada instante de tempo
equacao_modelada = ganho_do_degrau - ganho_da_exponencial * np.exp(-(tempo - deslocamento_em_t) / constante_de_tempo)
equacao_modelada[tempo < deslocamento_em_t] = ganho_do_degrau - ganho_da_exponencial  # Aplicar a condição

# Calcular o erro entre o modelo e o RPM médio
erro_absoluto = rpm_medio-equacao_modelada
erro_relativo = (erro_absoluto / rpm_medio)*100

# Criar um DataFrame com os dados do erro absoluto e do tempo
df_erro_tempo = pd.DataFrame({'Tempo': tempo, 'Erro Absoluto': erro_absoluto})

# Salvar os dados em um arquivo de texto
df_erro_tempo.to_csv('erro_absoluto_tempo.txt', index=False, sep=';')

# Imprimir o maior e o menor valor do erro
print("Maior valor do erro:", max(erro_relativo))
print("Menor valor do erro:", min(erro_relativo))


# Plotar o gráfico
fig, ax1 = plt.subplots()

# Configuração do primeiro eixo Y (lado esquerdo) - RPM
ax1.set_xlabel(titulo_tempo)
ax1.set_ylabel('Velocidade (RPM)', color='tab:blue')
ax1.plot(tempo, rpm_medio, label=titulo_rpm_medio, color='tab:blue')
ax1.plot(tempo, equacao_modelada, label='Equação Modelada', linestyle='--', color='red')  # Adicionando a curva da equação modelada
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_ylim(-150, 2550)
ax1.set_yticks(range(-150, 2551, 450))  # Definir marcações de 450 em 450 RPM

# Configuração do segundo eixo Y (lado direito) - Erro
ax2 = ax1.twinx()
ax2.set_ylabel('Erro relativo (%)', color='tab:orange')
ax2.plot(tempo, erro_relativo, label='Erro', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')
ax2.set_ylim(-60, 60)
ax2.set_yticks([x/10 for x in range(-600, 601, 200)])  # Definir marcações de 450 em 450 RPM

# Ajustar o eixo x para variar de 0.7375 a 1.8625 segundos
ax1.set_xlim(0.7375, 1.8625)
ax1.set_xticks([x/10000 for x in range(7375, 18626, 1250)])  # Marcação de 0,2 em 0,2 segundos


# Título e legenda
plt.title('Curva Experimental x  Curva Modelada')
fig.tight_layout()  # Para ajustar o layout

# Configurar legendas uma ao lado da outra
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper right', bbox_to_anchor=(1, 1), ncol=3)

# Adicionar linhas de grade baseadas no eixo x
ax1.grid(True, which='both', axis='x', linestyle='-')
ax2.grid(True)

# Mostrar o gráfico
plt.show()
