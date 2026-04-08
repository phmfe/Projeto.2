import random
import datetime

def menu():
    nome_arq = 'log.txt'

    while True:
        print('\nMENU')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - Gerar e analisar logs')
        print('4 - Sair')

        opc = input('Digite a opção desejada: ')

        if opc == '1':
            qtd = int(input('Quantidade de logs: '))
            gerarArquivo(nome_arq, qtd)

        elif opc == '2':
            analisarLogs(nome_arq)

        elif opc == '3':
            qtd = int(input('Quantidade de logs: '))
            gerarArquivo(nome_arq, qtd)
            analisarLogs(nome_arq)

        elif opc == '4':
            print('Até mais!')
            break

        else:
            print('Opção inválida!')


def gerarArquivo(nome_arq, qtd):
    with open(nome_arq, 'w') as arq:
        for i in range(qtd):
            arq.write(montarLog(i) + '\n')
    print('Logs gerados com sucesso!')


def montarLog(i):
    data = gerarData(i)
    ip = gerarIp(i)
    recurso = gerarRecurso(i)
    metodo = gerarMetodo(i)
    status = gerarStatus(i)
    tempo = gerarTempo(i)
    agente = gerarAgente(i)
    tamanho = gerarTamanho(i)
    protocolo = gerarProtocolo(i)

    return f'[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - {tamanho} - {protocolo} - {agente} - /home'


def gerarData(i):
    base = datetime.datetime.now()
    delta = datetime.timedelta(seconds=i * random.randint(5, 20))
    return (base + delta).strftime('%d/%m/%Y %H:%M:%S')


def gerarIp(i):
    if 20 <= i <= 50:
        return '203.120.45.7'
    return '192.168.1.' + str(random.randint(1, 10))


def gerarRecurso(i):
    if i % 6 == 0:
        return '/admin'
    elif i % 4 == 0:
        return '/login'
    else:
        return '/home'


def gerarMetodo(i):
    if i % 2 == 0:
        return 'GET'
    return 'POST'


def gerarStatus(i):
    if i % 9 == 0:
        return '500'
    elif i % 4 == 0:
        return '403'
    elif i % 5 == 0:
        return '404'
    else:
        return '200'


def gerarTempo(i):
    return random.randint(150, 950)


def gerarAgente(i):
    if i % 6 == 0:
        return 'Bot'
    return 'Chrome'


def gerarTamanho(i):
    return str(random.randint(300, 1200)) + 'B'


def gerarProtocolo(i):
    if i % 2 == 0:
        return 'HTTP/1.1'
    return 'HTTP/2'


def extrairStatus(linha):
    cont = 0
    valor = ''
    i = 0

    while i < len(linha):
        if linha[i] == '-':
            cont += 1
            i += 2
            if cont == 2:
                while linha[i] != ' ':
                    valor += linha[i]
                    i += 1
                return valor
        i += 1
    return valor


def extrairTempo(linha):
    cont = 0
    valor = ''
    i = 0

    while i < len(linha):
        if linha[i] == '-':
            cont += 1
            i += 2
            if cont == 4:
                while linha[i] != 'm':
                    valor += linha[i]
                    i += 1
                return int(valor)
        i += 1
    return 0


def extrairIP(linha):
    texto = ''
    i = 0

    while linha[i] != ']':
        i += 1
    i += 2

    while linha[i] != ' ':
        texto += linha[i]
        i += 1

    return texto


def extrairRecurso(linha):
    cont = 0
    texto = ''
    i = 0

    while i < len(linha):
        if linha[i] == '-':
            cont += 1
            i += 2
            if cont == 3:
                while linha[i] != ' ':
                    texto += linha[i]
                    i += 1
                return texto
        i += 1
    return texto


def tipoTempo(t):
    if t < 200:
        return 'rapido'
    elif t < 800:
        return 'normal'
    else:
        return 'lento'


def analisarLogs(nome_arq):
    arq = open(nome_arq, 'r')

    total = 0
    ok = 0
    erros = 0
    s403 = 0
    s404 = 0
    s500 = 0

    soma = 0
    maior = 0
    menor = 99999

    r = 0
    n = 0
    l = 0

    seq500 = 0
    falha = 0

    anterior = 0
    subida = 0
    degrada = 0

    ip_ant = ''
    cont_ip = 0
    bots = 0
    ultimo_bot = ''

    brute = 0
    seq_login = 0
    ultimo_brute = ''

    admin_erro = 0

    home = 0
    login = 0
    admin = 0

    ip1 = ''
    c1 = 0
    ip2 = ''
    c2 = 0

    for linha in arq:
        total += 1

        st = extrairStatus(linha)
        tp = extrairTempo(linha)
        ip = extrairIP(linha)
        rec = extrairRecurso(linha)

        soma += tp

        if tp > maior:
            maior = tp
        if tp < menor:
            menor = tp

        t = tipoTempo(tp)

        if t == 'rapido':
            r += 1
        elif t == 'normal':
            n += 1
        else:
            l += 1

        if st == '200':
            ok += 1
        else:
            erros += 1

        if st == '403':
            s403 += 1
        elif st == '404':
            s404 += 1
        elif st == '500':
            s500 += 1

        if st == '500':
            seq500 += 1
        else:
            seq500 = 0

        if seq500 == 3:
            falha += 1

        if tp > anterior:
            subida += 1
        else:
            subida = 0

        if subida == 3:
            degrada += 1

        anterior = tp

        if ip == ip_ant:
            cont_ip += 1
        else:
            cont_ip = 1

        if cont_ip == 5:
            bots += 1
            ultimo_bot = ip

        ip_ant = ip

        if rec == '/login' and st == '403':
            seq_login += 1
        else:
            seq_login = 0

        if seq_login == 3:
            brute += 1
            ultimo_brute = ip

        if rec == '/admin' and st != '200':
            admin_erro += 1

        if rec == '/home':
            home += 1
        elif rec == '/login':
            login += 1
        elif rec == '/admin':
            admin += 1

        if ip == ip1 or ip1 == '':
            ip1 = ip
            c1 += 1
        else:
            ip2 = ip
            c2 += 1

    arq.close()

    if home >= login and home >= admin:
        mais_rec = '/home'
    elif login >= admin:
        mais_rec = '/login'
    else:
        mais_rec = '/admin'

    if c1 >= c2:
        ip_mais = ip1
    else:
        ip_mais = ip2

    media = soma / total
    disp = (ok / total) * 100
    taxa = (erros / total) * 100

    if falha > 0 or disp < 70:
        estado = 'CRITICO'
    elif disp < 85:
        estado = 'INSTAVEL'
    elif disp < 95:
        estado = 'ATENCAO'
    else:
        estado = 'SAUDAVEL'

    print('\nRELATORIO FINAL')
    print('Total:', total)
    print('Sucessos:', ok)
    print('Erros:', erros)
    print('500:', s500)
    print('403:', s403)
    print('404:', s404)

    print('Disponibilidade:', disp)
    print('Taxa erro:', taxa)

    print('Media:', media)
    print('Maior:', maior)
    print('Menor:', menor)

    print('Rapidos:', r)
    print('Normais:', n)
    print('Lentos:', l)

    print('Recurso mais acessado:', mais_rec)
    print('IP mais ativo:', ip_mais)

    print('Forca bruta:', brute)
    print('Ultimo IP brute:', ultimo_brute)

    print('Admin indevido:', admin_erro)

    print('Falhas criticas:', falha)
    print('Degradacao:', degrada)

    print('Bots:', bots)
    print('Ultimo bot:', ultimo_bot)

    print('Estado:', estado)


menu()