import socket # importando socket
import sys # importando sys para receber por parametros
import hashlib # importando hashlib

params = sys.argv[1:] # definindo variável igual aos parâmetros

if(len(sys.argv) > 1):
    # Criando HELP da aplicação
    if(params[0] == "--help" or params[0] == "-h"):
        print("Execucao do servidor: python3 <nomeArquivo.py> <porta> <nomeArquivoSaida>")
        print("--------------- Ex: python3 serverUDP.py 12000 saida.txt ---------------")
    
    else:
        serverPort = int(params[0]) # definindo variável para o parâmetro da porta
        
        nameArqSave = params[1] # definindo variável para o parâmetro que recebe nome do arquivo para salvar
        
        arqSave = open(nameArqSave, 'w') # sinaliza para escrever no aquivo para salvar dados e definir na variavel

        socketServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # inicializando socket UDP
        
        socketServer.bind(('', serverPort)) # recebendo conecção do socket

        hash = hashlib.md5()

        print('Servidor ligado...')

        while 1:
            message, clientAddress = socketServer.recvfrom(2048) # recebendo mensagens do cliente

            # se receber mensagem de confirmação do cliente que os dados foram enviados
            if(message == b'ok'):
                print("Dados recebidos.")
                arqSave.close() # fechando arquivo
            else:

                msgSend = message.decode('utf-8').split(' ',2) # Divide a string nos dois primeiros espaços
                nSeq = msgSend[0] # Recebe o numero de sequencia provinda do transmissor
                hashcod = msgSend[1]# Recebe o codigo de verificação do transmissor
                cargaUtil = msgSend[2]# Recebe a carga util provinda do transmissor    

                hash.update(nSeq.encode())
                nHash = hash.hexdigest() # Transforma em hash md5

                if(nSeq): # Verifica se possui numero de sequencia

                    if(nHash == hashcod): # Verifica se o numero de sequencia e o codigo de verifcação condizem com o esperado
              
                        arqSave.writelines(cargaUtil) # Escreve a mensagem contida no frame no arquivo de saída
                        socketServer.sendto(str.encode('ACK'),clientAddress)#envia para o transmissor que tudo foi verificado e está OK          
                    
                    else: 
                      
                        socketServer.sendto(str.encode('NACK'),clientAddress) #Envia para o transmissor que houve um NACK

                else:

                  socketServer.sendto(str.encode('NACK'),clientAddress) #Envia para o transmissor que houve um NACK

socketServer.close()