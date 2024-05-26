import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Coeficientes do numerador e denominador da função de transferência
num_FTMA = [1.095e29, 2.088e31]
den_FTMA = [1.961e28, 5.736e29, 1.981e30]

# Criando a função de transferência
ftma = signal.TransferFunction(num_FTMA, den_FTMA)

# Definindo a faixa de frequências de interesse (em Hz)
frequencies_hz = np.logspace(-2, 4, num=1000)

# Convertendo as frequências para rad/s
frequencies_rad_per_sec = 2 * np.pi * frequencies_hz

# Calculando o diagrama de Bode para a faixa de frequências especificada
w, mag, phase = signal.bode(ftma, frequencies_rad_per_sec)

# Convertendo frequências de rad/s para Hz para os gráficos
frequencies_hz = w / (2 * np.pi)

# Frequências específicas para análise
target_frequencies_hz = [0.1, 1, 10, 100, 1000]
target_frequencies_rad_per_sec = [2 * np.pi * f for f in target_frequencies_hz]

# Interpolando os valores de magnitude e fase para as frequências específicas
target_magnitudes = np.interp(target_frequencies_rad_per_sec, w, mag)
target_phases = np.interp(target_frequencies_rad_per_sec, w, phase)

# Salvando os valores em um arquivo de texto
with open('bode_points.txt', 'w') as file:
    file.write('Frequência (Hz)\tMagnitude (dB)\tFase (graus)\n')
    for f, m, p in zip(target_frequencies_hz, target_magnitudes, target_phases):
        file.write(f'{f}\t{m}\t{p}\n')

# Plotando o diagrama de Bode
plt.figure()
plt.semilogx(frequencies_hz, mag)
plt.title('Diagrama de Bode - Módulo')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude (dB)')
plt.xlim(1e-2, 1e4)
plt.ylim(-100, 40)
plt.yticks(np.arange(-100, 41, 20))
plt.grid(which='both', linestyle='-', linewidth=0.5)
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth=0.5)

plt.figure()
plt.semilogx(frequencies_hz, phase)
plt.title('Diagrama de Bode - Fase')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Fase (graus)')
plt.xlim(1e-2, 1e4)
plt.grid(which='both', linestyle='-', linewidth=0.5)
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth=0.5)

plt.show()