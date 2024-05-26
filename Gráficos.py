import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo txt
file_path = 'Dados para gráfico de 1000Hz.txt'  # Caminho do seu arquivo

# Ler o arquivo usando pandas
df = pd.read_csv(file_path, sep=';')

# Verificar se os dados foram carregados corretamente
print(df.head())

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

# Plotar o gráfico
fig, ax1 = plt.subplots()

# Configuração do primeiro eixo Y (lado esquerdo) - RPM
ax1.set_xlabel(titulo_tempo)
ax1.set_ylabel('Velocidade (RPM)', color='tab:blue')
ax1.plot(tempo, rpm_medio, label=titulo_rpm_medio, color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_ylim(1920, 2100)
ax1.set_yticks(range(1920, 2101, 30))  # Definir marcações de 60 em 60 RPM

# Configuração do segundo eixo Y (lado direito) - Bits
ax2 = ax1.twinx()
ax2.set_ylabel('D (u.a)', color='tab:orange')
ax2.plot(tempo, entrada, label=titulo_entrada, color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')
ax2.set_ylim(0, 300)

# Ajustar o eixo x para variar de 8 a 9 segundos
ax1.set_xlim(7, 7.05)
ax1.set_xticks([x/100 for x in range(700, 706, 1)])  # Marcação de 0,2 em 0,2 segundos

# Título e legenda
plt.title('Resposta em Frequência - 1000Hz')
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
