
# Autor: Dassaev Pereira

lista_vazia = []
hosts_global = []
mascara_global = []

# Funcao para converter de Decimal para Binario:
def converter_Decimal(num):
    # Lista que ira armazenar o resto da divisao do numero ate que a divisao chegue a 0 ou 1:
    num_bits = []
    while num >= 1:
        # Capturando o resto da divisao do numero informado e adicionando a lista, assegurando que retorne somente dados do tipo inteiro (0 ou 1):
        sobra = num % 2
        num_bits.append(int(sobra))
        # Convertendo o numero para o resultado da divisao do mesmo por 2 ate que o loop termine:
        num = num / 2
        # Criando segundo loop que, caso incompleto, ira completar com os bits "0" o octeto da representacao binaria para formar 1 byte (necessario para o VLSM):
    while len(num_bits) < 8:
        num_bits.append(0)
    # Verificando se o numero nao e maior que 255; se for, mostre o erro e feche o programa para nao exibir representacoes erradas:
    if len(num_bits) > 8:
        return("Erro: O numero nao pode ser maior que 255.")
        exit()
    # Convertendo a lista para uma string para trabalhar nas representacoes:
    num_bits = ''.join(map(str, num_bits))
    # Posicionando os bits ao contrario para a representacao binaria correta:
    num_bits = num_bits[::-1]
    # Eis o numero em binario, em formato de 1 byte:
    return(num_bits)



# Funcao para converter de Binario para Decimal:
def converter_Binario(num):
    # Assegurando que o dado que vamos trabalhar seja uma string e convertendo o mesmo para lista:
    numero = list(str(num))
    # Checando cada item da lista para assegurar que foi recebido um numero binario, caso contrario, mostre o erro e feche:
    for bit in numero:
        if bit != "0" and bit != "1":
            return("Erro: o valor recebido nao e binario")
            exit()
        # Caso esteja tudo certo, continue:
        else:
            pass
    # Invertendo os bits para fazer as operacoes matematicas de forma ordenada:
    numero = numero[::-1]
    # Criando a lista que vai armazenar a sequencia da base 2:
    sequencia = []
    # Declarando uma variavel para contagem da execucao:
    contador = 0
    # Declarando a variavel que vai iniciar a sequencia da base 2, que comeca com 1:
    n1 = 1
    # Iniciando o loop do processo, que vai adicionando os valores da sequencia na lista ate que a quantidade de vezes se encaixe ao numero de bits recebido:
    while contador < len(numero):
        sequencia.append(n1)
        # Incrementando a variavel para a contagem:
        contador += 1
        # Multiplicando o valor da variavel a ela mesma para gerar os valores da base 2:
        n1 += n1
    # Criando uma terceira lista que vai armazenar os resultados da multiplicacao dos bits do numero recebido com os valores da sequencia, de acordo com suas posicoes em ambas as listas:
    bits_ativos = []
    for (unidade_binaria, unidade_decimal) in zip(numero, sequencia):
        bits_ativos.append(int(unidade_binaria) * unidade_decimal)
    # Guardando o resultado da soma de todos os valores da nova lista, e eis o valor em decimal:
    resultado = sum(bits_ativos)
    return(resultado)

# Criei uma funcao exclusiva para checar os dados de entrada da funcao calculo_Endereco() e barrar de antemao os possiveis erros:
def filtro_de_dados(ip_masc, v_f):
    # Assegurando que o endereco contenha os caracteres "." e "/" :
    if not "." in list(ip_masc) or not "/" in list(ip_masc):
        print("Erro: representacao mal formada")
        exit()
    # Criando uma lista de 1 a 9 e adicionando os mesmos na lista validos:
    numeros = range(10)
    validos = []
    for n in numeros:
        validos.append(str(n))
    # Adicionando tambem os caracteres "." e "/" na lista validos
    validos.append(".")
    validos.append("/")
    # Agora vamos verificar se cada caractere recebido e permitido:
    for caractere in list(ip_masc):
        if caractere not in validos:
            print("Erro: entrada de dados invalidos no endereco")
            exit()
        else:
            pass
    # Aqui vamos fazer uma regra para permitir apenas os valores 0 e 1 que definirao nossa escolha para calcular respectivamente o endereco de rede e o endereco de broadcast
    if v_f != 0 and v_f != 1:
        print("Erro: entrada invalida para definicao de rede ou broadcast")
        exit()
    else:
        pass

# Funcao para pegar nossa mascara de sub-rede nos seus dois modos de exibicao:
def calcular_Mascara(mascara, v_f):
    # Assegurando valor inteiro:
    mascara = int(mascara)
    # Lista que vai armazenar os bits da mascara:
    bits_mascara = []
    # Contador que vai adicionar bits até 32 vezes (32 bits, O zero conta):
    contador = 0
    while contador < 32:
        # Icrementador da contagem
        contador += 1
        # Se passar o tamanho da mascara adicione 0 para completar os 32 bits, se não, adicione 1:
        if contador > mascara:
            bits_mascara.append(0)
        else:
            bits_mascara.append(1)
    # Lista que vamos adicionar apenas os bits zero da mascara, vamos usar daqui a pouco:
    bits_selecionados = []

    # Mas antes, vou extrair os dados da mascara no formato x.x.x.x
    # Criei essa condicao para que os bytes da mascara nao se dupliquem no final pelo fato de estar usando variavel global
    # Por isso aproveitei o valor booleano que criamos para definir rede ou broadcast; para pegar carona aqui nessa funcao e definir a condicao:
    if v_f == 0:
        # Lista para armazenar os bits:
        extrair_mascara = []
        # Incrementador:
        contador = 0
        # Colocando os pontos no endereco a cada 8 bits:
        for bit in bits_mascara:
            extrair_mascara.append(str(bit))
            contador += 1
            if contador == 8:
                extrair_mascara.append(".")
                contador = 0
            else:
                pass
        extrair_mascara = "".join(map(str, extrair_mascara))
        # Separando para coletar os bytes:
        extrair_mascara = extrair_mascara.split(".")
        # Tenho um bug aqui que nao quis focar: Existe um quinto item da lista (A parte direita quebrada pelo ultimo ponto), em branco. Resolvi da forma rapida; apenas removendo o mesmo:
        extrair_mascara.pop(4)
        # Armazenando na lista os bytes convertidos em decimal:
        for byte in extrair_mascara:
            faixa = converter_Binario(byte)
            mascara_global.append(faixa)
    # Voltando para os bits da mascara
    # Adicionando os bits zero na lista para multiplicar por 2 a soma de todos eles (por item, cada um valendo 1):
    for bit in bits_mascara:
        if bit == 0:
            bits_selecionados.append(bit)
        else:
            pass
    hosts = 2**len(bits_selecionados)
    # Eis nossa representacao da mascara na forma /*
    return(str(hosts))


# Funcao para calcular nosso endereco de Rede ou Broadcast:
def calculo_Endereco(ip_masc, v_f):
    # Visando a prevencao de erros, checando os dados:
    filtro_de_dados(ip_masc, v_f)
    # Separando o IP e mascara de sub-rede:
    ip_masc = ip_masc.split("/")
    ip = ip_masc[0]
    mascara = ip_masc[1]
    qtde_hosts = calcular_Mascara(mascara, v_f)
    # qtde_hosts = "1"
    hosts_global.append(qtde_hosts)
    # Criando primeira lista que vai armazenar cada byte do endereco IP separado por ponto:
    bytes_ip = list(ip.split("."))
    # Criando segunda lista que vai armazenar os bytes que serao convertidos em binario:
    bytes_binario = []
    # Convertendo cada byte da lista em binario e adicionando cada um na segunda lista:
    for byte in bytes_ip:
       byte_binario = converter_Decimal(int(byte))
       bytes_binario.append(byte_binario)
    bytes_binario = "".join(map(str, bytes_binario))
    # Definindo contador para checarmos o tamanho da mascara de sub-rede:
    contador = int(0)
    # Criando terceira lista para armazenar os bits da rede em binario:
    rede_binario = []
    # Definindo os bits e completando com 0 a partir do limite da mascara para extrairmos nosso endereco de rede:
    for bit in bytes_binario:
        contador += 1
        if contador > int(mascara):
            bit = v_f
        else:
            pass
        rede_binario.append(str(bit))
    # Criando quarta lista que armazenara os bytes do endereco IP, colocando um ponto(.) a cada 8 bits:
    bytes_binario = []
    contador = int(0)
    for bit in rede_binario:
        if contador == 8:
            # Zerando contador ao chegar no numero 8:
            contador = 0
            # Adicionando o ponto:
            bytes_binario.append(".")
        else:
            pass
        # Incrementando o contador:
        contador += 1
        # Adicionando os bits:
        bytes_binario.append(str(bit))
        # Convertendo tudo em string para fazer a separacao dos bytes:
    rede = ''.join(map(str, bytes_binario))
    # Separando os bytes atraves do ponto:
    rede_bytes = rede.split(".")
    # Zerando a variavel rede para reutiliza-la:
    rede = []
    # Convertendo os bytes em decimal e adicionando os mesmos na ultima lista:
    for byte_bin in rede_bytes:
        byte_dec = converter_Binario(byte_bin)
        rede.append(byte_dec)
    # Convertendo a lista em string para a representacao do endereco IP:
    rede = '.'.join(map(str, rede))
    # Eis nosso endereco de rede, ou broadcast:
    return(rede)




#def Resposta(representacao, hosts_global, mascara_global1):
representacao = input("Entre com a representacao de rede (Ex: 192.168.1.10/24) ou s para sair:")
if representacao == "s":
    exit()
else:
    pass
rede = calculo_Endereco(representacao, 0)
broadcast = calculo_Endereco(representacao, 1)
hosts = int(hosts_global[0])
hosts_disponiveis = hosts - 2
mascara_global.append(":")
mascara_global = ".".join(map(str, mascara_global))
mascara_global = mascara_global.split(":")
lista_resposta = []
lista_resposta.append("Endereco de Rede: {0}".format(rede))
lista_resposta.append("Endereco de Broadcast: {0}".format(broadcast))
lista_resposta.append("Tamanho da Rede: {0}".format(str(hosts)))
lista_resposta.append("Quantidade maxima de hosts: {0}".format(str(hosts_disponiveis)))
lista_resposta.append("Mascara de Sub-rede: {0}".format(mascara_global[0]))

print()
for resposta in lista_resposta:
    print(resposta)










