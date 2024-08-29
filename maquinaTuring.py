from collections import defaultdict
from queue import Queue
import sys
import json


#maquina de turing
class FuncaoTransicao:
    transicoes = defaultdict(list)
    def __init__(self,transicoesList):
        for x in transicoesList:
            self.transicoes[x[0]+x[1]].append([x[2],x[3],x[4]])

    def checarProximoEstado(self,estadoAtual,cabecoteFita):
        return self.transicoes[estadoAtual+cabecoteFita]

    def transitarProximoEstado(self,proxEstado,escreve,sentido,posicaoFita,fita):
        fita = fita[:posicaoFita] + escreve +fita[posicaoFita+1:]
        if(sentido == '>'):
            posicaoFita = posicaoFita + 1
        else:
            posicaoFita = posicaoFita - 1
        return posicaoFita,proxEstado,fita
        
class Automato:
    def __init__(self,json):
        self.estadosMaquina  = set(json['mt'][0])
        self.alfabetoMaquina = set(json['mt'][1])
        self.alfabetoFita    = set(json['mt'][2])
        self.inicioFita      = json['mt'][3]
        self.fitaVazia       = json['mt'][4]
        self.funcTransicoes  = FuncaoTransicao(json['mt'][5])
        self.estadoInicial   = json['mt'][6]
        self.estadosFinais   = set(json['mt'][7])
        self.estadoAtual     = ""
        self.fita            = ""
        self.cabecoteFita    = 1

    def ler_fita(self,fita):
        self.fita = fita
        self.estadoAtual = self.estadoInicial
        self.fita = self.inicioFita + self.fita +self.fitaVazia
        fila = Queue()  
        passagens = set()
        
        for at in self.funcTransicoes.checarProximoEstado(self.estadoAtual,self.fita[self.cabecoteFita]):
            fila.put([at[0],at[1],at[2],self.cabecoteFita,self.fita])
        while fila.qsize() >0:
            elemento = fila.get()
            while elemento == None and fila.qsize() > 0:
                elemento = fila.get()
            if elemento == None and  fila.qsize() == 0:
                break

            self.cabecoteFita,self.estadoAtual,self.fita = self.funcTransicoes.transitarProximoEstado(elemento[0],elemento[1],elemento[2],elemento[3],elemento[4])

            for at in self.funcTransicoes.checarProximoEstado(self.estadoAtual,self.fita[self.cabecoteFita]):
                if at[0]+at[1]+at[2]+str(self.cabecoteFita)+self.fita not in passagens: # checar se já nao é um estado passado
                    fila.put(fila.put([at[0],at[1],at[2],self.cabecoteFita,self.fita]))
                    passagens.add(at[0]+at[1]+at[2]+str(self.cabecoteFita)+self.fita)

            if(len(self.funcTransicoes.checarProximoEstado(self.estadoAtual,self.fita[self.cabecoteFita])) == 0 ):
                if(self.estadoAtual in self.estadosFinais):
                    break
            
        if self.estadoAtual in self.estadosFinais:
            print("Sim")
        else:
            print("Não")



# main 
if len(sys.argv) != 3:
    print("Usar: python3 mt.py [MT.json] [Palavra]")
    sys.exit(1)
readjson = sys.argv[1]
fita = ""
fita = sys.argv[2]

with open(readjson) as f:
    data = json.load(f)
    maquinaTuring = Automato(data)
    maquinaTuring.ler_fita(fita)

