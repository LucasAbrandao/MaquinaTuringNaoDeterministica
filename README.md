# Maquina Turing Nao Deterministica

## Lucas Andrade Brandao e Gustavo Assis

Simulador de Máquina de Turing Não-Determinística

Este projeto implementa uma simulação de uma Máquina de Turing (MT) não-determinística em Python. O objetivo é permitir que a máquina simule a execução sobre uma palavra de entrada e verifique se essa palavra pertence à linguagem descrita pela máquina.

FUNCIONALIDADES
- Definição da MT: A máquina é definida através de um arquivo JSON que especifica seus estados, alfabeto, transições, estado inicial, e estados finais.
- Execução da MT: A partir de uma palavra de entrada, o simulador percorre a fita da máquina de acordo com as transições especificadas, decidindo se a palavra pertence à linguagem da MT.
- Suporte a Fitas Infinitas: A fita é considerada virtualmente infinita à direita, com um símbolo de espaço vazio (_) sendo adicionado conforme necessário.

ESTRUTURA DO PROJETO
- MaquinaTuring.py: Implementa a lógica da Máquina de Turing, incluindo a leitura da palavra de entrada, aplicação das transições e determinação se a palavra é aceita ou não.
- Arquivos JSON: Contêm a definição das Máquinas de Turing a serem simuladas. Exemplos:
  - mt1.json
  - mt2.json
  - mt3.json
  - mt4.json

COMO FUNCIONA
1. Definição da Máquina de Turing (JSON):
   - A máquina é especificada em um arquivo JSON contendo:
     - Conjunto de estados.
     - Alfabeto de entrada.
     - Alfabeto da fita.
     - Estado inicial.
     - Estado(s) final(is).
     - Transições (definidas como uma lista de tuplas que descrevem o estado atual, símbolo lido, próximo estado, símbolo a ser escrito e a direção do cabeçote).

2. Execução:
   - A simulação é iniciada através de uma linha de comando, onde se passa o arquivo JSON da máquina e a palavra de entrada.
   - O simulador lê a fita e aplica as transições definidas na máquina, percorrendo os estados até que uma decisão seja tomada: a palavra é aceita (Sim) ou rejeitada (Não).

COMO COMPILAR E USAR

Pré-requisitos:
- Python 3.x
- Nenhuma biblioteca externa é necessária além das bibliotecas padrão (collections, queue, sys, json).

Compilação:
- Este projeto é implementado em Python, então não requer compilação. Basta garantir que o Python 3.x esteja instalado no sistema.

Execução:
1. Abra um terminal.
2. Navegue até o diretório onde o código está salvo.
3. Execute o comando a seguir para testar uma máquina de Turing específica com uma palavra de entrada:

```bash
   python3 maquinaTuring.py [MT.json] [Palavra]
```
   Onde:
   - [MT.json] é o caminho para o arquivo JSON que define a máquina de Turing.
   - [Palavra] é a palavra de entrada que será verificada pela máquina.

Exemplo de Uso:
python3 MaquinaTuring.py mt1.json 000000

Saída esperada:
Sim

python3 maquinaTuring.py mt1.json 111111

Saída esperada:
Não

OBSERVAÇÕES:

- Caso seja passado na entrada uma palavra com simbolo fora do alfabeto informado no .json da maquina de turing, a resposta pode ser Sim ou Nao dependendo do estado momentaneo da maquina. Portanto, utilize somente palavras dentro do alfabeto para teste.
