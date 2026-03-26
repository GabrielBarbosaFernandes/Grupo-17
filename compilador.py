# PREENCHA ESTAS LINHAS ANTES DE ENTREGAR
# Integrantes:
# Nome 1 - github
# Nome 2 - github
# Nome 3 - github
# Nome 4 - github
# Grupo no Canvas: NOME_DO_GRUPO

import sys

# Tipos de token
TOKEN_NUMBER = "NUMBER"
TOKEN_OPERATOR = "OPERATOR"
TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_KEYWORD = "KEYWORD"
TOKEN_ERROR = "ERROR"


# Lê operadores simples: + - * ^ %
def estadoOperador(linha, pos, tokens):
    tokens.append((TOKEN_OPERATOR, linha[pos]))
    return pos + 1


# Lê / ou //
def estadoDivisao(linha, pos, tokens):
    pos = pos + 1

    if pos < len(linha) and linha[pos] == "/":
        tokens.append((TOKEN_OPERATOR, "//"))
        return pos + 1

    tokens.append((TOKEN_OPERATOR, "/"))
    return pos


# Lê números
# Aceita 10, 3.14, 2.0
# Rejeita 3,45 e 3.14.5
def estadoNumero(linha, pos, tokens):
    numero = ""
    temPonto = False

    while pos < len(linha):
        c = linha[pos]

        if c >= "0" and c <= "9":
            numero = numero + c
            pos = pos + 1

        elif c == ".":
            if temPonto:
                numero = numero + c
                pos = pos + 1

                while pos < len(linha):
                    c = linha[pos]
                    if c == " " or c == "\t" or c == "(" or c == ")":
                        break
                    numero = numero + c
                    pos = pos + 1

                tokens.append((TOKEN_ERROR, numero))
                return pos

            temPonto = True
            numero = numero + c
            pos = pos + 1

        elif c == ",":
            numero = numero + c
            pos = pos + 1

            while pos < len(linha):
                c = linha[pos]
                if c == " " or c == "\t" or c == "(" or c == ")":
                    break
                numero = numero + c
                pos = pos + 1

            tokens.append((TOKEN_ERROR, numero))
            return pos

        else:
            break

    if numero == ".":
        tokens.append((TOKEN_ERROR, numero))
        return pos

    if len(numero) > 0 and numero[len(numero) - 1] == ".":
        tokens.append((TOKEN_ERROR, numero))
        return pos

    tokens.append((TOKEN_NUMBER, numero))
    return pos


# Lê palavras em maiúsculas
# Exemplo: RES, MEM, VAR, X
def estadoPalavraChave(linha, pos, tokens):
    palavra = ""

    while pos < len(linha):
        c = linha[pos]

        if c >= "A" and c <= "Z":
            palavra = palavra + c
            pos = pos + 1
        else:
            break

    if pos < len(linha):
        c = linha[pos]

        if (c >= "a" and c <= "z") or (c >= "0" and c <= "9"):
            while pos < len(linha):
                c = linha[pos]
                if c == " " or c == "\t" or c == "(" or c == ")":
                    break
                palavra = palavra + c
                pos = pos + 1

            tokens.append((TOKEN_ERROR, palavra))
            return pos

    tokens.append((TOKEN_KEYWORD, palavra))
    return pos


# Estado inicial do AFD
# Decide para qual estado deve ir
def estadoInicial(linha, pos, tokens):
    while pos < len(linha):
        c = linha[pos]

        if c == " " or c == "\t" or c == "\n" or c == "\r":
            pos = pos + 1

        elif c == "(":
            tokens.append((TOKEN_LPAREN, "("))
            pos = pos + 1

        elif c == ")":
            tokens.append((TOKEN_RPAREN, ")"))
            pos = pos + 1

        elif c == "+" or c == "-" or c == "*" or c == "^" or c == "%":
            pos = estadoOperador(linha, pos, tokens)

        elif c == "/":
            pos = estadoDivisao(linha, pos, tokens)

        elif c >= "0" and c <= "9":
            pos = estadoNumero(linha, pos, tokens)

        elif c >= "A" and c <= "Z":
            pos = estadoPalavraChave(linha, pos, tokens)

        else:
            erro = c
            pos = pos + 1

            while pos < len(linha):
                c = linha[pos]
                if c == " " or c == "\t" or c == "(" or c == ")":
                    break
                erro = erro + c
                pos = pos + 1

            tokens.append((TOKEN_ERROR, erro))

    return pos


# Faz a análise léxica da expressão
# Aqui ainda é uma validação mais léxica do que sintática
def parseExpressao(linha, tokens):
    estadoInicial(linha.strip(), 0, tokens)

    i = 0
    while i < len(tokens):
        if tokens[i][0] == TOKEN_ERROR:
            print("ERRO LEXICO:", tokens[i][1])
            return False
        i = i + 1

    if len(tokens) == 0:
        print("ERRO: expressao vazia")
        return False

    abre = 0
    fecha = 0
    i = 0

    while i < len(tokens):
        if tokens[i][0] == TOKEN_LPAREN:
            abre = abre + 1
        elif tokens[i][0] == TOKEN_RPAREN:
            fecha = fecha + 1
        i = i + 1

    if abre != fecha:
        print("ERRO: parenteses desbalanceados")
        return False

    if tokens[0][0] != TOKEN_LPAREN or tokens[len(tokens) - 1][0] != TOKEN_RPAREN:
        print("ERRO: expressao deve comecar com ( e terminar com )")
        return False

    return True


# Lê o arquivo texto linha por linha
def lerArquivo(nomeArquivo, linhas):
    try:
        arquivo = open(nomeArquivo, "r", encoding="utf-8")

        for linha in arquivo:
            linha = linha.strip()
            if linha != "":
                linhas.append(linha)

        arquivo.close()
        return True

    except FileNotFoundError:
        print("Erro: arquivo nao encontrado.")
        return False

    except Exception as e:
        print("Erro ao abrir arquivo:", e)
        return False


# Salva os tokens da última execução
def salvarTokens(tokens_por_linha, nomeArquivoSaida):
    try:
        arquivo = open(nomeArquivoSaida, "w", encoding="utf-8")

        i = 0
        while i < len(tokens_por_linha):
            arquivo.write("Expressao " + str(i + 1) + ":\n")

            j = 0
            while j < len(tokens_por_linha[i]):
                tipo = tokens_por_linha[i][j][0]
                valor = tokens_por_linha[i][j][1]
                arquivo.write("  " + tipo + ": " + valor + "\n")
                j = j + 1

            arquivo.write("\n")
            i = i + 1

        arquivo.close()
        return True

    except Exception as e:
        print("Erro ao salvar tokens:", e)
        return False


# Mantida só para preservar o nome pedido no trabalho
# O fluxo principal não usa Python para calcular o resultado final
def executarExpressao(tokens, resultados, memoria):
    return None


# Mantida só para preservar o nome pedido no trabalho
def exibirResultados(resultados):
    print("Os resultados devem ser verificados no arquivo saida.s e no CPUlator.")


# Verifica se uma string é inteiro positivo
def ehInteiro(texto):
    if texto == "":
        return False

    i = 0
    while i < len(texto):
        c = texto[i]
        if c < "0" or c > "9":
            return False
        i = i + 1

    return True


# Coleta nomes de memória usados no arquivo
# Exemplo: MEM, VAR, X
def coletarMemorias(tokens_por_linha):
    memorias = []
    i = 0

    while i < len(tokens_por_linha):
        j = 0
        while j < len(tokens_por_linha[i]):
            tipo = tokens_por_linha[i][j][0]
            valor = tokens_por_linha[i][j][1]

            if tipo == TOKEN_KEYWORD and valor != "RES":
                if valor not in memorias:
                    memorias.append(valor)

            j = j + 1
        i = i + 1

    return memorias


# Escolhe um registrador temporário
# Vai de r4 até r9 e depois volta
def proximoRegistrador(controle):
    reg = "r" + str(controle[0])
    controle[0] = controle[0] + 1

    if controle[0] > 9:
        controle[0] = 4

    return reg


# Gera Assembly recursivamente para subexpressões
# Exemplo: ((3 4 *) (2 1 +) -)
def gerarSubexpressao(tokens, inicio, fim, arquivo, controle):
    if inicio > fim:
        return None

    # Caso base: número isolado
    if inicio == fim:
        if tokens[inicio][0] == TOKEN_NUMBER:
            reg = proximoRegistrador(controle)
            arquivo.write("    ldr " + reg + ", =" + tokens[inicio][1] + "\n")
            return reg

        # Caso base: leitura de memória
        if tokens[inicio][0] == TOKEN_KEYWORD and tokens[inicio][1] != "RES":
            regBase = proximoRegistrador(controle)
            regValor = proximoRegistrador(controle)
            arquivo.write("    ldr " + regBase + ", =" + tokens[inicio][1] + "\n")
            arquivo.write("    ldr " + regValor + ", [" + regBase + "]\n")
            return regValor

        return None

    # Caso de expressão entre parênteses
    if tokens[inicio][0] == TOKEN_LPAREN and tokens[fim][0] == TOKEN_RPAREN:
        posOperador = -1
        nivel = 0

        # Procura o operador principal da subexpressão
        i = fim - 1
        while i > inicio:
            if tokens[i][0] == TOKEN_RPAREN:
                nivel = nivel + 1
            elif tokens[i][0] == TOKEN_LPAREN:
                nivel = nivel - 1
            elif nivel == 0 and tokens[i][0] == TOKEN_OPERATOR:
                posOperador = i
                break
            i = i - 1

        # Caso especial: (MEM)
        if posOperador == -1:
            if inicio + 2 == fim and tokens[inicio + 1][0] == TOKEN_KEYWORD and tokens[inicio + 1][1] != "RES":
                regBase = proximoRegistrador(controle)
                regValor = proximoRegistrador(controle)
                arquivo.write("    ldr " + regBase + ", =" + tokens[inicio + 1][1] + "\n")
                arquivo.write("    ldr " + regValor + ", [" + regBase + "]\n")
                return regValor
            return None

        # Descobre onde termina o operando da esquerda
        corte = -1
        nivel = 0
        i = inicio + 1

        while i < posOperador:
            if tokens[i][0] == TOKEN_LPAREN:
                nivel = nivel + 1
            elif tokens[i][0] == TOKEN_RPAREN:
                nivel = nivel - 1

            if nivel == 0:
                corte = i
                break

            i = i + 1

        if corte == -1:
            return None

        # Gera os dois lados
        regEsq = gerarSubexpressao(tokens, inicio + 1, corte, arquivo, controle)
        regDir = gerarSubexpressao(tokens, corte + 1, posOperador - 1, arquivo, controle)

        if regEsq is None or regDir is None:
            return None

        regSaida = proximoRegistrador(controle)
        operador = tokens[posOperador][1]

        # Operações inteiras
        if operador == "+":
            arquivo.write("    add " + regSaida + ", " + regEsq + ", " + regDir + "\n")
        elif operador == "-":
            arquivo.write("    sub " + regSaida + ", " + regEsq + ", " + regDir + "\n")
        elif operador == "*":
            arquivo.write("    mul " + regSaida + ", " + regEsq + ", " + regDir + "\n")
        elif operador == "/" or operador == "//":
            # Aqui / e // estão indo para divisão inteira
            arquivo.write("    mov r0, " + regEsq + "\n")
            arquivo.write("    mov r1, " + regDir + "\n")
            arquivo.write("    bl rot_div\n")
            arquivo.write("    mov " + regSaida + ", r2\n")
        elif operador == "%":
            arquivo.write("    mov r0, " + regEsq + "\n")
            arquivo.write("    mov r1, " + regDir + "\n")
            arquivo.write("    bl rot_mod\n")
            arquivo.write("    mov " + regSaida + ", r2\n")
        elif operador == "^":
            arquivo.write("    mov r0, " + regEsq + "\n")
            arquivo.write("    mov r1, " + regDir + "\n")
            arquivo.write("    bl rot_pow\n")
            arquivo.write("    mov " + regSaida + ", r2\n")
        else:
            return None

        return regSaida

    return None

# Verifica se um texto é um número real válido
# Ex.: 3.5, 10.0, 2.25
def ehNumeroRealValido(texto):
    if texto == "":
        return False

    pontos = 0
    i = 0

    while i < len(texto):
        c = texto[i]

        if c >= "0" and c <= "9":
            pass
        elif c == ".":
            pontos = pontos + 1
            if pontos > 1:
                return False
        else:
            return False

        i = i + 1

    if texto == ".":
        return False

    if texto[0] == "." or texto[len(texto) - 1] == ".":
        return False

    return True


# Decide se a expressão precisa ir para o caminho float
# Aqui eu tratei o caso simples:
# (A B +), (A B -), (A B *), (A B /)
# quando houver ponto em algum número, ou quando o operador for /
def precisaPontoFlutuante(tokens):
    if len(tokens) != 5:
        return False

    if tokens[0][0] != TOKEN_LPAREN or tokens[4][0] != TOKEN_RPAREN:
        return False

    if tokens[1][0] != TOKEN_NUMBER or tokens[2][0] != TOKEN_NUMBER or tokens[3][0] != TOKEN_OPERATOR:
        return False

    valor1 = tokens[1][1]
    valor2 = tokens[2][1]
    operador = tokens[3][1]

    if not ehNumeroRealValido(valor1) or not ehNumeroRealValido(valor2):
        return False

    if operador == "/":
        return True

    if "." in valor1 or "." in valor2:
        if operador == "+" or operador == "-" or operador == "*":
            return True

    return False


# Cria um nome de label para cada constante float
# Ex.: 3.5 -> CONSTF_3_5
def rotuloConstanteFloat(valor):
    nome = valor.replace("-", "NEG_")
    nome = nome.replace(".", "_")
    return "CONSTF_" + nome


# Junta todas as constantes float usadas no arquivo
def coletarConstantesFloat(tokens_por_linha):
    constantes = []
    i = 0

    while i < len(tokens_por_linha):
        tokens = tokens_por_linha[i]

        if precisaPontoFlutuante(tokens):
            valor1 = tokens[1][1]
            valor2 = tokens[2][1]

            if valor1 not in constantes:
                constantes.append(valor1)

            if valor2 not in constantes:
                constantes.append(valor2)

        i = i + 1

    return constantes


# Escreve uma expressão float simples em Assembly
# Ex.: (3.5 2.0 +), (8.0 2.0 /)
def escreverExpressaoFloatSimples(arquivo, tokens, numeroExpressao):
    valor1 = tokens[1][1]
    valor2 = tokens[2][1]
    operador = tokens[3][1]

    rot1 = rotuloConstanteFloat(valor1)
    rot2 = rotuloConstanteFloat(valor2)

    arquivo.write("    @ Expressao " + str(numeroExpressao) + " -> FLOAT\n")
    arquivo.write("    ldr r0, =" + rot1 + "\n")
    arquivo.write("    vldr d0, [r0]\n")
    arquivo.write("    ldr r1, =" + rot2 + "\n")
    arquivo.write("    vldr d1, [r1]\n")

    if operador == "+":
        arquivo.write("    vadd.f64 d2, d0, d1\n")
    elif operador == "-":
        arquivo.write("    vsub.f64 d2, d0, d1\n")
    elif operador == "*":
        arquivo.write("    vmul.f64 d2, d0, d1\n")
    elif operador == "/":
        arquivo.write("    vdiv.f64 d2, d0, d1\n")
    else:
        arquivo.write("    @ operador float ainda nao implementado\n")
        arquivo.write("\n")
        return False

    arquivo.write("    ldr r2, =RESULTADOF_" + str(numeroExpressao) + "\n")
    arquivo.write("    vstr d2, [r2]\n")
    arquivo.write("\n")
    return True

# Gera o Assembly de uma expressão completa
def escreverExpressao(arquivo, tokens, numeroExpressao, tipos_resultado, tipos_memoria):
    # Primeiro tenta o caminho float simples
    # Isso fecha o caso de reais e divisão real /
    if precisaPontoFlutuante(tokens):
        if escreverExpressaoFloatSimples(arquivo, tokens, numeroExpressao):
            tipos_resultado.append("float")
            return
        else:
            tipos_resultado.append("erro")
            return

    # Caso: (N RES)
    if len(tokens) == 4:
        if tokens[0][0] == TOKEN_LPAREN and tokens[3][0] == TOKEN_RPAREN:
            if tokens[1][0] == TOKEN_NUMBER and tokens[2][0] == TOKEN_KEYWORD:
                valor = tokens[1][1]
                nome = tokens[2][1]

                if nome == "RES":
                    if ehInteiro(valor):
                        n = int(valor)
                        anterior = numeroExpressao - n

                        if n >= 1 and anterior >= 1:
                            # Se o resultado anterior for float, copia como float
                            if tipos_resultado[anterior - 1] == "float":
                                arquivo.write("    @ Expressao " + str(numeroExpressao) + " -> RES FLOAT\n")
                                arquivo.write("    ldr r0, =RESULTADOF_" + str(anterior) + "\n")
                                arquivo.write("    vldr d0, [r0]\n")
                                arquivo.write("    ldr r1, =RESULTADOF_" + str(numeroExpressao) + "\n")
                                arquivo.write("    vstr d0, [r1]\n")
                                arquivo.write("\n")
                                tipos_resultado.append("float")
                                return

                            # Se o anterior for inteiro, copia como inteiro
                            arquivo.write("    @ Expressao " + str(numeroExpressao) + " -> RES\n")
                            arquivo.write("    ldr r0, =RESULTADO_" + str(anterior) + "\n")
                            arquivo.write("    ldr r1, [r0]\n")
                            arquivo.write("    ldr r2, =RESULTADO_" + str(numeroExpressao) + "\n")
                            arquivo.write("    str r1, [r2]\n")
                            arquivo.write("\n")
                            tipos_resultado.append("int")
                            return

                # Caso: (V MEM)
                else:
                    # Se o valor for real, grava como double
                    if ehNumeroRealValido(valor) and "." in valor:
                        rot = rotuloConstanteFloat(valor)

                        arquivo.write("    @ Expressao " + str(numeroExpressao) + " -> MEMORIA FLOAT " + nome + "\n")
                        arquivo.write("    ldr r0, =" + rot + "\n")
                        arquivo.write("    vldr d0, [r0]\n")
                        arquivo.write("    ldr r1, =" + nome + "\n")
                        arquivo.write("    vstr d0, [r1]\n")
                        arquivo.write("    ldr r2, =RESULTADOF_" + str(numeroExpressao) + "\n")
                        arquivo.write("    vstr d0, [r2]\n")
                        arquivo.write("\n")

                        tipos_memoria[nome] = "float"
                        tipos_resultado.append("float")
                        return

                    # Se for inteiro, grava como inteiro
                    if ehInteiro(valor):
                        arquivo.write("    @ Expressao " + str(numeroExpressao) + " -> MEMORIA " + nome + "\n")
                        arquivo.write("    ldr r0, =" + valor + "\n")
                        arquivo.write("    ldr r1, =" + nome + "\n")
                        arquivo.write("    str r0, [r1]\n")
                        arquivo.write("    ldr r2, =RESULTADO_" + str(numeroExpressao) + "\n")
                        arquivo.write("    str r0, [r2]\n")
                        arquivo.write("\n")

                        tipos_memoria[nome] = "int"
                        tipos_resultado.append("int")
                        return

    # Caso: (MEM)
    if len(tokens) == 3:
        if tokens[0][0] == TOKEN_LPAREN and tokens[2][0] == TOKEN_RPAREN:
            if tokens[1][0] == TOKEN_KEYWORD:
                nome = tokens[1][1]

                if nome != "RES":
                    # Se a memória foi marcada como float, lê como float
                    if nome in tipos_memoria and tipos_memoria[nome] == "float":
                        arquivo.write("    @ Expressao " + str(numeroExpressao) + " -> LE MEMORIA FLOAT " + nome + "\n")
                        arquivo.write("    ldr r0, =" + nome + "\n")
                        arquivo.write("    vldr d0, [r0]\n")
                        arquivo.write("    ldr r1, =RESULTADOF_" + str(numeroExpressao) + "\n")
                        arquivo.write("    vstr d0, [r1]\n")
                        arquivo.write("\n")
                        tipos_resultado.append("float")
                        return

                    # Caso padrão: lê como inteiro
                    arquivo.write("    @ Expressao " + str(numeroExpressao) + " -> LE MEMORIA " + nome + "\n")
                    arquivo.write("    ldr r0, =" + nome + "\n")
                    arquivo.write("    ldr r1, [r0]\n")
                    arquivo.write("    ldr r2, =RESULTADO_" + str(numeroExpressao) + "\n")
                    arquivo.write("    str r1, [r2]\n")
                    arquivo.write("\n")
                    tipos_resultado.append("int")
                    return

    # Caso geral: expressão inteira
    arquivo.write("    @ Expressao " + str(numeroExpressao) + "\n")
    controle = [4]
    regFinal = gerarSubexpressao(tokens, 0, len(tokens) - 1, arquivo, controle)

    if regFinal is not None:
        arquivo.write("    ldr r10, =RESULTADO_" + str(numeroExpressao) + "\n")
        arquivo.write("    str " + regFinal + ", [r10]\n")
        arquivo.write("\n")
        tipos_resultado.append("int")
        return

    arquivo.write("    @ Expressao " + str(numeroExpressao) + " ainda nao implementada\n")
    arquivo.write("\n")
    tipos_resultado.append("erro")


# Gera o arquivo Assembly final
def gerarAssembly(tokens_por_linha, nomeArquivoSaida):
    try:
        arquivo = open(nomeArquivoSaida, "w", encoding="utf-8")

        memorias = coletarMemorias(tokens_por_linha)
        constantes_float = coletarConstantesFloat(tokens_por_linha)

        # Aqui eu guardo o tipo de cada resultado gerado:
        # int, float ou erro
        tipos_resultado = []

        # Aqui eu guardo o tipo atual de cada memória nomeada
        tipos_memoria = {}

        # Seção de código
        arquivo.write(".text\n")
        arquivo.write(".global _start\n")
        arquivo.write("\n")
        arquivo.write("_start:\n")

        i = 0
        while i < len(tokens_por_linha):
            escreverExpressao(arquivo, tokens_por_linha[i], i + 1, tipos_resultado, tipos_memoria)
            i = i + 1

        # Laço final
        arquivo.write("fim:\n")
        arquivo.write("    b fim\n")
        arquivo.write("\n")

        # Sub-rotina de divisão inteira
        arquivo.write("@ ------------------------------\n")
        arquivo.write("@ divisao inteira\n")
        arquivo.write("@ entrada: r0 = dividendo, r1 = divisor\n")
        arquivo.write("@ saida:   r2 = quociente\n")
        arquivo.write("@ ------------------------------\n")
        arquivo.write("rot_div:\n")
        arquivo.write("    cmp r1, #0\n")
        arquivo.write("    beq rot_div_zero\n")
        arquivo.write("    mov r2, #0\n")
        arquivo.write("    mov r3, r0\n")
        arquivo.write("rot_div_loop:\n")
        arquivo.write("    cmp r3, r1\n")
        arquivo.write("    blt rot_div_fim\n")
        arquivo.write("    sub r3, r3, r1\n")
        arquivo.write("    add r2, r2, #1\n")
        arquivo.write("    b rot_div_loop\n")
        arquivo.write("rot_div_zero:\n")
        arquivo.write("    mov r2, #0\n")
        arquivo.write("rot_div_fim:\n")
        arquivo.write("    bx lr\n")
        arquivo.write("\n")

        # Sub-rotina de resto
        arquivo.write("@ ------------------------------\n")
        arquivo.write("@ resto da divisao\n")
        arquivo.write("@ entrada: r0 = dividendo, r1 = divisor\n")
        arquivo.write("@ saida:   r2 = resto\n")
        arquivo.write("@ ------------------------------\n")
        arquivo.write("rot_mod:\n")
        arquivo.write("    cmp r1, #0\n")
        arquivo.write("    beq rot_mod_zero\n")
        arquivo.write("    mov r2, r0\n")
        arquivo.write("rot_mod_loop:\n")
        arquivo.write("    cmp r2, r1\n")
        arquivo.write("    blt rot_mod_fim\n")
        arquivo.write("    sub r2, r2, r1\n")
        arquivo.write("    b rot_mod_loop\n")
        arquivo.write("rot_mod_zero:\n")
        arquivo.write("    mov r2, #0\n")
        arquivo.write("rot_mod_fim:\n")
        arquivo.write("    bx lr\n")
        arquivo.write("\n")

        # Sub-rotina de potência inteira
        arquivo.write("@ ------------------------------\n")
        arquivo.write("@ potencia inteira\n")
        arquivo.write("@ entrada: r0 = base, r1 = expoente\n")
        arquivo.write("@ saida:   r2 = resultado\n")
        arquivo.write("@ ------------------------------\n")
        arquivo.write("rot_pow:\n")
        arquivo.write("    cmp r1, #0\n")
        arquivo.write("    beq rot_pow_zero\n")
        arquivo.write("    mov r2, r0\n")
        arquivo.write("    sub r1, r1, #1\n")
        arquivo.write("rot_pow_loop:\n")
        arquivo.write("    cmp r1, #0\n")
        arquivo.write("    beq rot_pow_fim\n")
        arquivo.write("    mul r2, r2, r0\n")
        arquivo.write("    sub r1, r1, #1\n")
        arquivo.write("    b rot_pow_loop\n")
        arquivo.write("rot_pow_zero:\n")
        arquivo.write("    mov r2, #1\n")
        arquivo.write("rot_pow_fim:\n")
        arquivo.write("    bx lr\n")
        arquivo.write("\n")

        # Seção de dados
        arquivo.write(".data\n")

        # Memórias nomeadas: todas com 8 bytes
        # Isso ajuda a guardar tanto inteiro quanto double
        i = 0
        while i < len(memorias):
            arquivo.write(memorias[i] + ":\n")
            arquivo.write("    .double 0.0\n")
            i = i + 1

        # Resultados inteiros
        i = 0
        while i < len(tokens_por_linha):
            arquivo.write("RESULTADO_" + str(i + 1) + ":\n")
            arquivo.write("    .word 0\n")
            i = i + 1

        # Resultados float
        i = 0
        while i < len(tokens_por_linha):
            arquivo.write("RESULTADOF_" + str(i + 1) + ":\n")
            arquivo.write("    .double 0.0\n")
            i = i + 1

        # Constantes float
        i = 0
        while i < len(constantes_float):
            arquivo.write(rotuloConstanteFloat(constantes_float[i]) + ":\n")
            arquivo.write("    .double " + constantes_float[i] + "\n")
            i = i + 1

        arquivo.close()
        return True

    except Exception as e:
        print("Erro ao gerar Assembly:", e)
        return False


def main():
    if len(sys.argv) != 2:
        print("Uso: python compilador.py teste1.txt")
        return

    nomeArquivo = sys.argv[1]
    linhas = []

    if not lerArquivo(nomeArquivo, linhas):
        return

    tokens_por_linha = []
    erro_encontrado = False

    i = 0
    while i < len(linhas):
        tokens = []
        ok = parseExpressao(linhas[i], tokens)
        tokens_por_linha.append(tokens)

        if not ok:
            erro_encontrado = True

        i = i + 1

    if not salvarTokens(tokens_por_linha, "tokens.txt"):
        print("Nao foi possivel gerar tokens.txt")
        return

    if erro_encontrado:
        print("Foram encontrados erros lexicos no arquivo.")
        print("O Assembly nao sera gerado enquanto houver erro.")
        return

    if gerarAssembly(tokens_por_linha, "saida.s"):
        print("Arquivo tokens.txt gerado com sucesso.")
        print("Arquivo saida.s gerado com sucesso.")
    else:
        print("Nao foi possivel gerar saida.s")

if __name__ == "__main__":
    main()