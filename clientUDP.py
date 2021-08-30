import socket # importando socket
import sys # importando sys para receber por parametros
import hashlib # importando hashlib
import time

params = sys.argv[1:] # definindo variável igual aos parâmetros

print("\nInicializando socket...")
socketClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("\nSocket inicializado.")

if(len(sys.argv) > 1):
    # Criando HELP da aplicação
    if(params[0] == "--help" or params[0] == "-h"):
        print("Execucao do cliente: python3 <nomeArquivo.py> <entradaDadosArquivo> <tamanhoQuadros> <ip> <porta>")
        print("-------------------- Ex: python3 clientUDP.py enviar.txt 7 127.0.0.1 12000 --------------------")
    
    else:
        nameArqSend = params[0] # definindo variável para o primeiro parâmetro
        
        print("\nLendo arquivo...")
        arqSend = open(nameArqSend, 'r') # ler aquivo para enviar dados e definir na variavel
        print("\nArquivo lido.")
        
        tamQuadros = int(params[1]) # definindo variável para o parâmetro de tamanho de quadros
        
        serverName = params[2] # definindo variável para o parâmetro de ip
        
        serverPort = int(params[3]) # definindo variável para o parâmetro da porta

        hostAndress = (serverName, serverPort) # definindo endereço completo 

        hash = hashlib.md5() # encriptando
        
        socketClient.settimeout(1) # atraso

        nSeq = 1

        for linha in arqSend:
            i = 0
            while(i < len(linha) - 1):

                message = linha[i:(i+tamQuadros)] # particionando mensagerm para envio

                hash.update(str(nSeq).encode())
                hashcod = hash.hexdigest() # Transforma o codigo em hash

                msgSend  = str(nSeq) + ' ' + hashcod + ' ' + "{}".format(message)  # Junta o numero do frame com o sequencial e a mensagem


                if(socketClient.sendto(msgSend.encode(),(hostAndress))) : # faz o envio do conjunto
          
                    try :
                
                        request, clientAddress = socketClient.recvfrom(1024) # confirmação de envio
                      
                        if(request == b'ACK') :
                            print(request.decode('utf-8')) # ACK
                            print("Frame salvo!")
                                        
                        elif(request == b'NACK') :
                            print(request.decode('utf-8')) # NACK
                            print("Falha no frame: "+str(nSeq)) # frame deu erro
                            print("Renviando frame...")
                            nSeq = 1
                            i = 0
                        
                    except:
                        print("Err: Timeout") # excedeu o tempo e fecha e para de enviar os frames
                        break 
                
                print("Pacote enviado: ", message)
                i = (i + tamQuadros) # pula pelo tamnho do quadro | prox. quadro
          
                nSeq += 1 # vai pra a prox. sequencia

        message = str.encode("ok") # definindo mensagem de confirmação de dados enviados
        
        socketClient.sendto(message, hostAndress) # enviando mensagem de confirmação para o servidor

        print("\nAplicação finalizada.")
        arqSend.close() # fechando arquivo
        socketClient.close() # finalizando socket