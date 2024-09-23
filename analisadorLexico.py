import re

token_especificacao = [
    ('PALAVRA_RESERVADA', r'\b(programa|variaveis|constantes|registro|tipo|'
                          r'funcao|retorno|vazio|principal|se|entao|senao|enquanto|'
                          r'para|ate|leia|escreva|inteiro|real|logico|caractere|cadeia|verdadeiro|falso)\b'),
    ('IDENTIFICADOR', r'[a-zA-Z_]\w*'),
    ('NUMERO', r'\d+(\.\d+)?'),
    ('OPERADOR', r'\+|\-|\*|\/|==|!=|>|>=|<|<=|&&|\|\||=|\+\+|\-\-'),
    ('DELIMITADOR', r'[;,\(\)\{\}\[\]]'),
    ('CADEIA_CONSTANTE', r'"[^"]*"'),
    ('CARACTERE_CONSTANTE', r"'[^']'"),
    ('COMENTARIO_LINHA', r'//.*'),
    ('COMENTARIO_BLOCO', r'/\*.*?\*/'),
    ('ESPACO', r'[ \t\n]+'),  # Espaços em branco e quebras de linha
    ('ERRO', r'.'),  # Captura qualquer caractere desconhecido
]

token_re = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_especificacao)

def tokenize(codigo, linha_atual):
    for iguais in re.finditer(token_re, codigo):
        tipo_token = iguais.lastgroup
        valor_token = iguais.group(tipo_token)
        
        # Ignora espaço em branco
        if tipo_token == 'ESPACO':
            continue
        
        
        yield tipo_token, valor_token, linha_atual
        
def analisar_arquivo(entrada, token_saida, erros_saida):
    with open(entrada, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
        
    tokens = []
    erros = []
    linha_atual = 1
    
    for linha in linhas:
        for tipo_token,valor_token, linha_num in tokenize(linha, linha_atual):
            if tipo_token == 'ERRO':
                erros.append(f"Erro léxico: '{valor_token}' na linha {linha_num}\n")
            else:
                tokens.append(f"{tipo_token}: '{valor_token}' (Linha {linha_num})\n")
        linha_atual += 1
        
    with open(token_saida, 'w', encoding='utf-8') as file:
        file.writelines(tokens)
        
    with open(erros_saida, 'w', encoding='utf-8') as file:
        if erros:
            file.writelines(erros)
        else:
            file.write("Análise Léxica concluída com sucesso!\n")
            
def processa_arquivos(identificador):
    entrada =  f'entrada{identificador}.prog'
    tokens_saida = f'tokens{identificador}.lex'
    erros_saida = f'erros{identificador}.lex'    
    
    analisar_arquivo(entrada, tokens_saida, erros_saida)
        
processa_arquivos(1)