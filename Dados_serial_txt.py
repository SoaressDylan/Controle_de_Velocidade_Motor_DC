import serial
import os # Criar arquivos ou verificar a existencia dele()
import keyboard  # Importa a biblioteca keyboard( se usar o input ele trava direto)
from datetime import datetime # usar a biblioteca das horas para administrar os arquivos
import time


# o arduino emite a partir de UART então para decodificar precisa ser o UTF-8
# Configuração da comunicação serial
ser = serial.Serial('COM5', 115200)  # Substitua 'COMx' pela porta correta


# Função para criar um nome de arquivo 
def generate_filename():
    now = datetime.now()
    return os.path.join(os.path.dirname(__file__),f'dados_{now.strftime("%H-%M-%S")}.txt')

filename = generate_filename()


# Verifica se o arquivo já existe
if not os.path.exists(filename):
    # Se não existir, cria o arquivo vazio
    open(filename, 'w').close()

# Fim~

print("Arquivo está sendo salvo em:", os.path.abspath(filename))


# Abre o arquivo em modo de escrita
with open(filename, 'a') as file: 
    while True:
        try:
            # Lê os dados da porta serial

            ##erro ao ler alguns dados???
            data = ser.readline().strip().decode('utf-8')
        
            # Escreve os dados no arquivo
            file.write(data + '\n')
            print(data)  # Exibe os dados se desejar
        
            # Verifica se a tecla 'q' foi pressionada
            if keyboard.is_pressed('q'):
                break  # Sai do loop 'while' se 'q' for pressionado
            
            # Verifica se a tecla 'x' foi pressionada para reiniciar a leitura
            if keyboard.is_pressed('x'):
                ser.flushInput()  # Limpa o buffer de entrada da porta serial
                filename = generate_filename()
                file.close()
                file = open(filename,'w')
        except Exception as e:
            print("Erro ao ler dados da porta serial:", e)

        time.sleep(0.1)# atraso para permitir que mais dados se acumulem no buffer serial