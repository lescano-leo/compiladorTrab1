import os

class AnalisadorLexico:
    """Analisador Lexico"""
    def __init__(self, fonte):
        self.__arquivo = fonte
        if not os.path.exists(self.__arquivo):
            print(f'Erro: Arquivo {self.__arquivo} não encontrado.')
            self.__fita = ''
        else:
            with open(self.__arquivo, 'r') as arquivo:
                self.__fita = arquivo.read()
        self.__cabeca = 0
        self.__caracter = ''
        self.__numero_linha = 1
        self.__tabela_de_simbolos = []
        self.__erros_lexicos = []
        self.__fim_linha = '\n'

    def __obter_caractere(self):
        if self.__cabeca < len(self.__fita):
            caractere = self.__fita[self.__cabeca]
            self.__cabeca += 1
            return caractere
        return ''

    def __atualizar_numero_linha(self):
        self.__numero_linha += 1

    def __q4_comentario(self):
        """Estado para comentários de linha e bloco."""
        proximo_caracter = self.__obter_caractere()
        
        if proximo_caracter == '/':
            # Comentário de linha
            comentario = '//'
            while True:
                self.__caracter = self.__obter_caractere()
                if self.__caracter == self.__fim_linha or self.__cabeca >= len(self.__fita):  # Para no fim da linha ou fim da fita
                    break
                comentario += self.__caracter
            self.__tabela_de_simbolos.append(('Comentário de Linha', comentario, self.__numero_linha))
        elif proximo_caracter == '*':
            # Comentário de bloco
            comentario = '/*'
            while True:
                self.__caracter = self.__obter_caractere()
                comentario += self.__caracter
                if self.__caracter == '*' and self.__obter_caractere() == '/':
                    comentario += '/'
                    break
                elif self.__caracter == self.__fim_linha:
                    self.__atualizar_numero_linha()  # Para o caso de um comentário de bloco que termina na linha
                elif self.__cabeca >= len(self.__fita):  # Se atingir o fim da fita
                    self.__erros_lexicos.append(f'Comentário de bloco não fechado na linha {self.__numero_linha}')
                    break
            self.__tabela_de_simbolos.append(('Comentário de Bloco', comentario, self.__numero_linha))
        
        # Reiniciar a análise para evitar capturar mais tokens após um comentário
        return  # Adicionei um return para encerrar a execução após um comentário

    def __q0(self):
        while self.__cabeca < len(self.__fita):
            self.__caracter = self.__obter_caractere()
            # Identificadores e palavras reservadas
            if self.__caracter.isalpha():
                self.__q1_identificador()
            # Números
            elif self.__caracter.isdigit():
                self.__q2_numero()
            # Operadores
            elif self.__caracter in ['+', '-', '*', '=', '<', '>', '/']:
                self.__q3_operador()
            # Delimitadores (parênteses, chaves, etc.)
            elif self.__caracter in [';', ',', '(', ')', '{', '}', '[', ']']:
                self.__tabela_de_simbolos.append(('Delimitador', self.__caracter, self.__numero_linha))
            # Comentários
            elif self.__caracter == '/':
                self.__q4_comentario()
                continue  # Reinicia o loop, sem continuar com a análise após o comentário
            # Strings
            elif self.__caracter == '"':
                self.__q5_string()
            # Espaços e quebras de linha
            elif self.__caracter.isspace():
                if self.__caracter == self.__fim_linha:
                    self.__atualizar_numero_linha()
            # Caractere inválido
            else:
                self.__erros_lexicos.append(f'Caractere inválido "{self.__caracter}" na linha {self.__numero_linha}.')

    def __q1_identificador(self):
        """Estado para identificadores e palavras reservadas."""
        identificador = self.__caracter
        while True:
            self.__caracter = self.__obter_caractere()
            if not self.__caracter.isalnum() and self.__caracter != '_':
                self.__cabeca -= 1  # Recuar a cabeça de leitura
                break
            identificador += self.__caracter
        if identificador in ['programa', 'inteiro', 'real', 'se', 'escreva', 'enquanto']:
            self.__tabela_de_simbolos.append(('Palavra Reservada', identificador, self.__numero_linha))
        else:
            self.__tabela_de_simbolos.append(('Identificador', identificador, self.__numero_linha))

    def __q2_numero(self):
        """Estado para números inteiros e reais."""
        numero = self.__caracter
        while True:
            self.__caracter = self.__obter_caractere()
            if not self.__caracter.isdigit():
                if self.__caracter == '.':
                    numero += self.__caracter
                    while True:
                        self.__caracter = self.__obter_caractere()
                        if not self.__caracter.isdigit():
                            self.__cabeca -= 1  # Recuar a cabeça de leitura
                            break
                        numero += self.__caracter
                    self.__tabela_de_simbolos.append(('Número Real', numero, self.__numero_linha))
                    return
                self.__cabeca -= 1  # Recuar a cabeça de leitura
                break
            numero += self.__caracter
        self.__tabela_de_simbolos.append(('Número Inteiro', numero, self.__numero_linha))

    def __q3_operador(self):
        """Estado para operadores."""
        operador = self.__caracter
        if operador in ['+', '-', '*', '=', '<', '>']:
            self.__tabela_de_simbolos.append(('Operador', operador, self.__numero_linha))
        elif operador == '/':
            proximo_caracter = self.__obter_caractere()
            if proximo_caracter == '/' or proximo_caracter == '*':
                self.__cabeca -= 1  # Recuar a cabeça de leitura para tratar como comentário
                self.__q4_comentario()
            else:
                self.__tabela_de_simbolos.append(('Operador', operador, self.__numero_linha))
                self.__cabeca -= 1  # Recuar a cabeça de leitura para tratar o próximo caractere

    def __q5_string(self):
        """Estado para strings."""
        string = self.__caracter
        while True:
            self.__caracter = self.__obter_caractere()
            string += self.__caracter
            if self.__caracter == '"':
                break
            elif self.__caracter == self.__fim_linha or self.__cabeca >= len(self.__fita):
                self.__erros_lexicos.append(f'String não fechada na linha {self.__numero_linha}')
                break
        self.__tabela_de_simbolos.append(('Cadeia de Caracteres', string, self.__numero_linha))

    def obter_tabela_tokens(self):
        self.__q0()
        return self.__tabela_de_simbolos, self.__erros_lexicos

    def gerar_arquivos_saida(self, nome_saida):
        """Gera os arquivos de saída tokensX.lex e errosX.lex."""
        with open(f'tokens{nome_saida}.lex', 'w') as tokens_saida:
            for token in self.__tabela_de_simbolos:
                tokens_saida.write(f'{token[0]}: {token[1]} (linha {token[2]})\n')
        
        if not self.__erros_lexicos:
            with open(f'erros{nome_saida}.lex', 'w') as erros_saida:
                erros_saida.write('Nenhum erro léxico encontrado.\n')
        else:
            with open(f'erros{nome_saida}.lex', 'w') as erros_saida:
                for erro in self.__erros_lexicos:
                    erros_saida.write(f'{erro}\n')

# Exemplo de uso
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso correto: python analisador_lexico.py <arquivo_de_entrada>")
    else:
        arquivo_entrada = sys.argv[1]
        nome_saida = arquivo_entrada.replace('entrada', '').replace('.prog', '')
        
        analisador = AnalisadorLexico(arquivo_entrada)
        analisador.obter_tabela_tokens()
        analisador.gerar_arquivos_saida(nome_saida)
        print(f'Arquivos de saída gerados com sucesso: tokens{nome_saida}.lex e erros{nome_saida}.lex')