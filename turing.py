import json
import sys
from collections import deque

def load_turing_machine(json_file):
    """Carrega a especificação da Máquina de Turing a partir de um arquivo JSON."""
    with open(json_file, 'r') as file:
        tm = json.load(file)
    return tm['mt']

def simulate_turing_machine(tm, word):
    """Simula a execução de uma Máquina de Turing não-determinística."""
    # Extrai os elementos da definição da MT
    states = set(tm[0])  # Conjunto de estados
    input_alphabet = set(tm[1])  # Alfabeto de entrada
    tape_alphabet = set(tm[2])  # Alfabeto da fita
    start_marker = tm[3]  # Símbolo de início de fita
    blank_symbol = tm[4]  # Símbolo de células vazias
    transitions = tm[5]  # Função de transição
    initial_state = tm[6]  # Estado inicial
    final_states = set(tm[7])  # Conjunto de estados finais

    # Converte as transições para um formato mais fácil de usar
    transition_dict = {}
    for transition in transitions:
        (current_state, read_symbol, new_state, write_symbol, direction) = transition
        if (current_state, read_symbol) not in transition_dict:
            transition_dict[(current_state, read_symbol)] = []
        transition_dict[(current_state, read_symbol)].append((new_state, write_symbol, direction))

    # Fita inicial e estado inicial
    tape = list(word)
    tape_position = 0
    current_states = [(initial_state, tape, tape_position)]

    # Execução da máquina
    step = 0
    while current_states:
        step += 1
        print(f"Passo {step}: Estados atuais: {current_states}")

        new_states = []

        for state, tape, tape_position in current_states:
            if state in final_states:
                print(f"Estado final {state} alcançado. Palavra aceita.")
                return "Sim"
            
            current_symbol = tape[tape_position] if tape_position < len(tape) else blank_symbol

            print(f"  Estado: {state}, Símbolo lido: '{current_symbol}', Posição na fita: {tape_position}")

            if (state, current_symbol) in transition_dict:
                for new_state, write_symbol, direction in transition_dict[(state, current_symbol)]:
                    new_tape = list(tape)
                    if tape_position < len(new_tape):
                        new_tape[tape_position] = write_symbol
                    else:
                        new_tape.append(write_symbol)
                    
                    new_tape_position = tape_position + (1 if direction == '>' else -1)

                    if new_tape_position < 0:
                        new_tape.insert(0, blank_symbol)
                        new_tape_position = 0

                    print(f"    Nova transição: ({state}, {current_symbol}) -> ({new_state}, {write_symbol}, {direction}), Nova fita: {new_tape}, Nova posição: {new_tape_position}")
                    
                    new_states.append((new_state, new_tape, new_tape_position))
            else:
                print(f"  Sem transições disponíveis para estado '{state}' com símbolo '{current_symbol}'.")

        if not new_states:
            print("  Nenhum novo estado foi gerado. Máquina de Turing está em loop ou parou.")
        
        current_states = new_states

    print("Nenhum estado final alcançado. Palavra rejeitada.")
    return "Não"

def main():
    if len(sys.argv) != 3:
        print("Usar: python3 turing.py [MT] [Palavra]")
        sys.exit(1)

    json_file = sys.argv[1]
    word = sys.argv[2]

    tm = load_turing_machine(json_file)
    result = simulate_turing_machine(tm, word)
    print(result)

if __name__ == "__main__":
    main()
