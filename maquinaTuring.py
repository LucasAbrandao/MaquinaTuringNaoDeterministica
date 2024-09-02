from collections import defaultdict
from queue import Queue
import sys
import json

# Classe para gerenciar a função de transição da Máquina de Turing
class FuncaoTransicao:
    transicoes = defaultdict(list)
    
    def __init__(self, transicoesList):
        # Inicializa as transições. transicoesList deve ser uma lista de listas contendo [estadoAtual, simbolo, proximoEstado, simboloParaEscrever, sentido]
        for x in transicoesList:
            # Adiciona uma transição
            self.transicoes[x[0] + x[1]].append([x[2], x[3], x[4]])

    def checarProximoEstado(self, estadoAtual, cabecoteFita):
        # Retorna a lista de transições possíveis para o estadoAtual e o símbolo no cabeçote da mt
        return self.transicoes[estadoAtual + cabecoteFita]

    def transitarProximoEstado(self, proxEstado, escreve, sentido, posicaoFita, fita):
        # Atualiza a fita e a posiçao do cabeçote
        fita = fita[:posicaoFita] + escreve + fita[posicaoFita + 1:]
        if sentido == '>':
            posicaoFita += 1
        else:
            posicaoFita -= 1
        return posicaoFita, proxEstado, fita


class Automato:
    def __init__(self, json):
        # Inicializa os parâmetros
        self.estadosMaquina = set(json['mt'][0])
        self.alfabetoMaquina = set(json['mt'][1])
        self.alfabetoFita = set(json['mt'][2])
        self.inicioFita = json['mt'][3]
        self.fitaVazia = json['mt'][4]
        self.funcTransicoes = FuncaoTransicao(json['mt'][5])
        self.estadoInicial = json['mt'][6]
        self.estadosFinais = set(json['mt'][7])
        self.estadoAtual = ""
        self.fita = ""
        self.cabecoteFita = 1

    def ler_fita(self, fita):
        # Inicializa a fita e o estado inicial
        self.fita = fita
        self.estadoAtual = self.estadoInicial
        self.fita = self.inicioFita + self.fita + self.fitaVazia
        # Fila de "caminhos"
        fila = Queue()  
        passagens = set()

        # Verifica se o símbolo inicial está sendo usado novamente na primeira posição
        if self.cabecoteFita > 0 and self.fita[self.cabecoteFita] == self.inicioFita:
            print("Não, simbolo inicial usado novamente")
            return
        
        # Inicializa a fila com as transições possíveis a partir do estado inicial
        for at in self.funcTransicoes.checarProximoEstado(self.estadoAtual, self.fita[self.cabecoteFita]):
            fila.put([at[0], at[1], at[2], self.cabecoteFita, self.fita])
        
        #enquanto houver caminho, vai indo
        while fila.qsize() > 0:
            elemento = fila.get()
            while elemento is None and fila.qsize() > 0:
                elemento = fila.get()
            if elemento is None and fila.qsize() == 0:
                break

            # Atualiza o estado, a fita e a posição do cabeçote
            self.cabecoteFita, self.estadoAtual, self.fita = self.funcTransicoes.transitarProximoEstado(elemento[0], elemento[1], elemento[2], elemento[3], elemento[4])

            #caso cabeçote retroceda o inicio da fita:
            if self.cabecoteFita < 0:
                print("Não, cabeçote retrocedeu o inicio da fita")
                return

            # Verifica se o símbolo inicial está sendo usado novamente:
            if self.cabecoteFita > 0 and self.fita[self.cabecoteFita] == self.inicioFita:
                print("Não, fita reutilza simbolo inicial")
                return
            
            # Adiciona novas transições
            for at in self.funcTransicoes.checarProximoEstado(self.estadoAtual, self.fita[self.cabecoteFita]):
                if at[0] + at[1] + at[2] + str(self.cabecoteFita) + self.fita not in passagens:
                    fila.put([at[0], at[1], at[2], self.cabecoteFita, self.fita])
                    passagens.add(at[0] + at[1] + at[2] + str(self.cabecoteFita) + self.fita)

            # Verifica se não há mais transições possíveis e se o estado final foi alcançado
            if len(self.funcTransicoes.checarProximoEstado(self.estadoAtual, self.fita[self.cabecoteFita])) == 0:
                if self.estadoAtual in self.estadosFinais:
                    break
            
        # Imprime "Sim" se o estado final foi alcançado, caso contrário "Não"
        if self.estadoAtual in self.estadosFinais:
            print("Sim")
        else:
            print("Não")

# main
if len(sys.argv) != 3:
    print("Usar: python3 mt.py [MT.json] [Palavra]")
    sys.exit(1)

readjson = sys.argv[1]
fita = sys.argv[2]

with open(readjson) as f:
    data = json.load(f)
    maquinaTuring = Automato(data)
    maquinaTuring.ler_fita(fita)

    