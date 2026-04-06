import random
import datetime


def menui():
    nome_arq = 'log.txt'
    while True:
        print('MENU\n')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - Gerar e Analisar logs')
        print('4 - SAIR')
        opc = int(input('Escolha uma opção: '))
        if opc == 1:
            try:
                qtd = int(input('Quantidade de logs (registros):'))
                gerarArquivo(nome_arq, qtd)
            except:
                print('Entrada invalidada.')
        elif opc == 2:
            analisarLogs(nome_arq)
        elif opc == 3:
            try:
                qtd = int(input('Quantidade de logs (registros):'))
                gerarArquivo(nome_arq, qtd)
                analisarLogs(nome_arq)
            except:
                print('Entrada invalidada.')
        elif opc == 4:
            print('Até mais')
            break
        else:
            print('Opção Invalida')



def gerarArquivo(nome_arq, qtd):
    with open(nome_arq, 'w', encoding='UTF-8') as arq:
        for i in range(qtd):
            arq.write(montarLog(i) + '\n')
    print('log gerado')

def montarLog(i):
    data = gerarData(i)
    ip = gerarIp(i)
    recurso = gerarRecurso(i)
    metodo = gerarMetodo(i)
    status = gerarStatus(i)
    tempo = gerarTempo(i)
    agente = gerarAgente(i)
    prootocolo = gerarProtocolo(i)
    tamanho = gerarTamnho(i)

    return f'[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - {tamanho} - {prootocolo} - {agente} -/home'

def gerarData(i):
    base = datetime.datetime.now()
    delta = datetime.timedelta(seconds=i * random.randint(5, 20))
    return (base + delta).strftime('%d/%m/%Y %H:%M:%S')

def gerarIp(i):
    r = random.randint(1, 6)
    if i >= 20 and i <= 50:
        return '203.120.45.7'
    if r == 1:
        return '192.168.12.1'
    elif r == 2:
        return '192.168.12.3'
    elif r == 3:
        return '192.100.12.3'
    elif r == 4:
        return '192.168.162.3'
    elif r == 5:
        return '192.168.23.3'
    elif r == 6:
        return '192.168.0.3'

def gerarRecurso(i):
    r = random.randint(1, 8)
    if i >= 20 and i <= 50:
        return '/login'
    if r == 1:
        return '/home'
    elif r == 2:
        return '/login'
    elif r == 3:
        return '/admin'
    elif r == 4:
        return '/produtos'
    elif r == 5:
        return '/backup'
    elif r == 6:
        return '/config'
    elif r == 7:
        return '/private'
    elif r == 8:
        return '/contato'

def gerarMetodo(i):
    r = random.randint(1, 3)
    if r == 1:
        return 'GET'
    elif r == 2:
        return 'POST'
    elif r == 3:
        return 'PUT'

def gerarStatus(i):
    r = random.randint(1, 6)
    if i >= 20 and i <= 50:
        return 403
    if r == 1:
        return 200
    elif r == 2:
        return 200
    elif r == 3:
        return 200
    elif r == 4:
        return 404
    elif r == 5:
        return 403
    elif r == 6:
        return 500

def gerarTempo(i):
    return random.randint(50, 3000)

def gerarAgente(i):
    r = random.randint(1, 4)
    if i >= 20 and i <= 50:
        return 'python-requests/2.28'
    if r == 1:
        return 'Mozilla/5.0'
    elif r == 2:
        return 'Chrome/110.0'
    elif r == 3:
        return 'curl/7.68'
    elif r == 4:
        return 'python-requests/2.28'

def gerarProtocolo(i):
    r = random.randint(1, 2)
    if r == 1:
        return 'HTTP/1.1'
    elif r == 2:
        return 'HTTP/2.0'

def gerarTamnho(i):
    return str(random.randint(200, 9000)) + 'B'


def extrairIp(linha):
  
    inicio = 0
   
    while linha[inicio] != ']':
        inicio += 1
    inicio += 2  

    ip = ''
    i = inicio
    while linha[i] != ' ':
        ip += linha[i]
        i += 1
    return ip

def extrairCampos(linha):
   

    campos = ''  
    pedaco = ''
    i = 0
    while i < len(linha):
        
        if linha[i] == ' ' and i + 2 < len(linha) and linha[i+1] == '-' and linha[i+2] == ' ':
            campos += pedaco + '|'
            pedaco = ''
            i += 3  
        else:
            pedaco += linha[i]
            i += 1

    
    campos += pedaco

    return campos

def pegarCampo(campos_str, numero):
  
    count = 0
    campo = ''
    i = 0
    while i < len(campos_str):
        if campos_str[i] == '|':
            if count == numero:
                return campo
            count += 1
            campo = ''
        else:
            campo += campos_str[i]
        i += 1
   
    if count == numero:
        return campo
    return ''

def extrairData(campos_str):
    
    c = pegarCampo(campos_str, 0)
 
    data = ''
    for ch in c:
        if ch != '[' and ch != ']':
            data += ch
    return data.strip()

def extrairTempo(campos_str):
 
    c = pegarCampo(campos_str, 5).strip()
    numero = ''
    for ch in c:
        if ch != 'm' and ch != 's':
            numero += ch
    try:
        return int(numero)
    except:
        return 0

def extrairStatus(campos_str):
    c = pegarCampo(campos_str, 3).strip()
    try:
        return int(c)
    except:
        return 0

def extrairRecurso(campos_str):
    return pegarCampo(campos_str, 4).strip()

def extrairAgente(campos_str):
    return pegarCampo(campos_str, 8).strip()



def adicionarOuContar(registro, chave, contador):

    encontrou = False
    resultado = ''
    i = 0
    itens = ''
    pedaco = ''

    pos = 0
    while pos < len(registro):
        if registro[pos] == '|':
            itens += pedaco + '\n'
            pedaco = ''
        else:
            pedaco += registro[pos]
        pos += 1
    if pedaco != '':
        itens += pedaco + '\n'

    
    linhas = ''
    temp = ''
    for ch in itens:
        if ch == '\n':
            linhas += temp + '§'
            temp = ''
        else:
            temp += ch

    pares = ''
    idx = 0
    chave_atual = ''
    valor_atual = ''
    vez = 0  

    partes = ''
    p = ''
    for ch in linhas:
        if ch == '§':
            partes += p + '\n'
            p = ''
        else:
            p += ch

    
    par_chave = ''
    par_valor = ''
    linha_num = 0
    resultado_final = ''
    linhas_arr = ''
    l = ''
    for ch in partes:
        if ch == '\n':
            if linha_num % 2 == 0:
                par_chave = l
            else:
                par_valor = l
                
                if par_chave == chave:
                    novo_val = int(par_valor) + contador
                    resultado_final += par_chave + '|' + str(novo_val) + '|'
                    encontrou = True
                elif par_chave != '':
                    resultado_final += par_chave + '|' + par_valor + '|'
            linha_num += 1
            l = ''
        else:
            l += ch

    if not encontrou:
        resultado_final += chave + '|' + str(contador) + '|'

    return resultado_final

def pegarContagem(registro, chave):
 
    modo = 'chave'
    chave_atual = ''
    i = 0
    while i < len(registro):
        if registro[i] == '|':
            if modo == 'chave':
                if chave_atual == chave:
                    
                    i += 1
                    valor = ''
                    while i < len(registro) and registro[i] != '|':
                        valor += registro[i]
                        i += 1
                    try:
                        return int(valor)
                    except:
                        return 0
                modo = 'valor'
                chave_atual = ''
            else:
                modo = 'chave'
                chave_atual = ''
            i += 1
        else:
            if modo == 'chave':
                chave_atual += registro[i]
            i += 1
    return 0

def pegarMaiorChave(registro):
    
    maior_chave = ''
    maior_val = -1
    chave_atual = ''
    valor_atual = ''
    modo = 'chave'
    i = 0
    while i < len(registro):
        if registro[i] == '|':
            if modo == 'chave':
                modo = 'valor'
                valor_atual = ''
            else:
                try:
                    v = int(valor_atual)
                    if v > maior_val:
                        maior_val = v
                        maior_chave = chave_atual
                except:
                    pass
                modo = 'chave'
                chave_atual = ''
                valor_atual = ''
            i += 1
        else:
            if modo == 'chave':
                chave_atual += registro[i]
            else:
                valor_atual += registro[i]
            i += 1
    return maior_chave


def classificarTempo(tempo):
    if tempo < 500:
        return 'rapido'
    elif tempo <= 1500:
        return 'normal'
    else:
        return 'lento'





def analisarLogs(nome_arq): 
    total = 0
    total_200 = 0
    total_403 = 0
    total_404 = 0
    total_500 = 0
    total_erros = 0
    soma_tempo = 0
    maior_tempo = 0
    menor_tempo = 999999
    tempo_rapido = 0
    tempo_normal = 0
    tempo_lento = 0

  
    reg_ip = ''
    reg_recurso = ''
    reg_ip_erros = ''

    
    cont_login_403 = 0
    alerta_forca_bruta = False

    
    cont_500_seguidos = 0
    alerta_falha_critica = False

    
    cont_degradacao = 0
    ultimo_tempo = -1
    alerta_degradacao = False

    
    cont_ip_seguido = 0
    ultimo_ip = ''
    alerta_bot_ip = False
    alerta_bot_agente = False

    
    alerta_admin = False

    
    alerta_rotas = ''

    try:
        arq = open(nome_arq, 'r', encoding='UTF-8')
    except:
        print('Arquivo não encontrado. Gere os logs primeiro.')
        return

    for linha in arq:
        linha = linha.strip()
        if linha == '':
            continue

        campos_str = extrairCampos(linha)

        ip = extrairIp(linha)
        status = extrairStatus(campos_str)
        tempo = extrairTempo(campos_str)
        recurso = extrairRecurso(campos_str)
        agente = extrairAgente(campos_str)

        total += 1
        soma_tempo += tempo

      
        if status == 200:
            total_200 += 1
        elif status == 403:
            total_403 += 1
            total_erros += 1
        elif status == 404:
            total_404 += 1
            total_erros += 1
        elif status == 500:
            total_500 += 1
            total_erros += 1

        
        if tempo > maior_tempo:
            maior_tempo = tempo
        if tempo < menor_tempo:
            menor_tempo = tempo

       
        cls = classificarTempo(tempo)
        if cls == 'rapido':
            tempo_rapido += 1
        elif cls == 'normal':
            tempo_normal += 1
        else:
            tempo_lento += 1

       
        reg_ip = adicionarOuContar(reg_ip, ip, 1)

       
        reg_recurso = adicionarOuContar(reg_recurso, recurso, 1)

    
        if status != 200:
            reg_ip_erros = adicionarOuContar(reg_ip_erros, ip, 1)


        if recurso == '/login' and status == 403:
            cont_login_403 += 1
            if cont_login_403 >= 3:
                alerta_forca_bruta = True
        else:
            cont_login_403 = 0

       
        if status == 500:
            cont_500_seguidos += 1
            if cont_500_seguidos >= 3:
                alerta_falha_critica = True
        else:
            cont_500_seguidos = 0

       
        if ultimo_tempo != -1:
            if tempo > ultimo_tempo:
                cont_degradacao += 1
                if cont_degradacao >= 3:
                    alerta_degradacao = True
            else:
                cont_degradacao = 0
        ultimo_tempo = tempo

       
        if ip == ultimo_ip:
            cont_ip_seguido += 1
            if cont_ip_seguido >= 5:
                alerta_bot_ip = True
        else:
            cont_ip_seguido = 1
            ultimo_ip = ip

      
        if 'bot' in agente or 'curl' in agente or 'python' in agente:
            alerta_bot_agente = True

      
        if recurso == '/admin':
            alerta_admin = True

    
        if recurso == '/backup' or recurso == '/config' or recurso == '/private' or recurso == '/admin':
            
            if recurso not in alerta_rotas:
                alerta_rotas += recurso + ' '

    arq.close()

 
    if total > 0:
        media_tempo = soma_tempo / total
        disponibilidade = (total_200 / total) * 100
    else:
        media_tempo = 0
        disponibilidade = 0

    ip_mais_ativo = pegarMaiorChave(reg_ip)
    recurso_mais_acessado = pegarMaiorChave(reg_recurso)
    ip_mais_erros = pegarMaiorChave(reg_ip_erros)

   
    imprimirRelatorio(
        total, total_200, total_403, total_404, total_500,
        total_erros, disponibilidade, media_tempo,
        maior_tempo, menor_tempo,
        tempo_rapido, tempo_normal, tempo_lento,
        ip_mais_ativo, recurso_mais_acessado, ip_mais_erros,
        alerta_forca_bruta, alerta_admin, alerta_degradacao,
        alerta_falha_critica, alerta_bot_ip, alerta_bot_agente,
        alerta_rotas)

    


def imprimirRelatorio(
    total, total_200, total_403, total_404, total_500,
    total_erros, disponibilidade, media_tempo,
    maior_tempo, menor_tempo,
    tempo_rapido, tempo_normal, tempo_lento,
    ip_mais_ativo, recurso_mais_acessado, ip_mais_erros,
    alerta_forca_bruta, alerta_admin, alerta_degradacao,
    alerta_falha_critica, alerta_bot_ip, alerta_bot_agente,
    alerta_rotas):
    print('\n')
    print('=' * 50)
    print(' RELATÓRIO DE ANÁLISE DE LOGS')
    print('=' * 50)

    print('\n--- MÉTRICAS GERAIS ---')
    print('Total de acessos:      ', total)
    print('Total de sucessos 200: ', total_200)
    print('Total de erros:        ', total_erros)
    print('Erros críticos 500:    ', total_500)
    print('Disponibilidade:       ', round(disponibilidade, 2), '%')

    print('\n--- TEMPO DE RESPOSTA ---')
    print('Tempo médio:  ', round(media_tempo, 2), 'ms')
    print('Maior tempo:  ', maior_tempo, 'ms')
    print('Menor tempo:  ', menor_tempo, 'ms')
    print('Rápidos (<500ms):      ', tempo_rapido)
    print('Normais (500-1500ms):  ', tempo_normal)
    print('Lentos (>1500ms):      ', tempo_lento)

    print('\n--- CONTAGEM POR STATUS ---')
    print('Status 200: ', total_200)
    print('Status 403: ', total_403)
    print('Status 404: ', total_404)
    print('Status 500: ', total_500)

    print('\n--- DESTAQUES ---')
    print('Recurso mais acessado: ', recurso_mais_acessado)
    print('IP mais ativo:         ', ip_mais_ativo)
    print('IP com mais erros:     ', ip_mais_erros)

    print('\n--- ALERTAS DE SEGURANÇA E PADRÕES ---')

    if alerta_forca_bruta:
        print('[ALERTA] Possivel ataque de forca bruta no /login (3+ tentativas 403 seguidas)')
    else:
        print('[OK] Nenhum padrao de forca bruta detectado')

    if alerta_admin:
        print('[ALERTA] Acesso indevido ao /admin detectado')
    else:
        print('[OK] Nenhum acesso ao /admin')

    if alerta_degradacao:
        print('[ALERTA] Degradacao de desempenho detectada (tempo subindo 3x seguidas)')
    else:
        print('[OK] Desempenho estavel')

    if alerta_falha_critica:
        print('[ALERTA] Falha critica: 3 erros 500 consecutivos detectados')
    else:
        print('[OK] Nenhuma falha critica consecutiva')

    if alerta_bot_ip:
        print('[ALERTA] Possivel bot: mesmo IP acessou 5 vezes seguidas')
    else:
        print('[OK] Nenhum IP repetido suspeito')

    if alerta_bot_agente:
        print('[ALERTA] User-agent suspeito detectado (curl, python-requests, bot)')
    else:
        print('[OK] User-agents parecem normais')

    if alerta_rotas != '':
        print('[ALERTA] Acesso a rotas sensiveis:', alerta_rotas)
    else:
        print('[OK] Nenhum acesso a rotas sensiveis')

    print('\n' + '=' * 50)
    print('           FIM DO RELATÓRIO')
    print('=' * 50 + '\n')


menui()