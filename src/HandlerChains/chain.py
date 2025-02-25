import random, time, re
from collections import defaultdict
from unidecode import unidecode

class MarkovChain():
    def __init__(self, n=2):  # O valor de n pode ser ajustado para bi-grama (2) ou maior
        self.n = n  # ordem dos n-gramas
        self.states = set()  # Conjunto de estados (tuplas de n palavras)
        self.transitions = defaultdict(lambda: defaultdict(int))  # Transições de estados
        self.probabilities = defaultdict(lambda: defaultdict(int))  # Probabilidades das transições
    
    def getTransitions(self, words: list) -> None:
        if len(words) < self.n:
            raise ValueError(f"At least {self.n} words are required to fit the Markov chain model.")
        for i in range(len(words) - self.n):
            current_state = tuple(words[i:i+self.n])  # O estado agora é uma tupla de n palavras
            next_state = words[i + self.n]
            self.transitions[current_state][next_state] += 1

    def generateProbabilities(self) -> None:
        for state, transitions in self.transitions.items():
            total_transitions = sum(transitions.values())
            for next_state, count in transitions.items():
                self.probabilities[state][next_state] = count / total_transitions

    def fit(self, text: str = None) -> None:
        if text is None:
            raise ValueError("Text data is required to fit the Markov chain model.")
        
        # Remove números usando regex
        text = re.sub(r'\d+', '', text)  # Remove todos os números
        
        text = text.replace(",", "").replace(".", "")  # Remove pontuação
        words = text.lower().split()  # Divide o texto em palavras e coloca tudo em minúsculo
        
        self.states.update(set(tuple(words[i:i+self.n]) for i in range(len(words)-self.n)))  # Atualiza estados com tuplas
        self.getTransitions(words)
        self.generateProbabilities()

    def selectNextState(self, current_state: tuple) -> str:
        if current_state not in self.probabilities:
            raise ValueError(f"Invalid current state: {current_state}")
        
        probabilities = self.probabilities[current_state]
        next_state = random.choices(
            list(probabilities.keys()),  # estados possíveis
            weights=probabilities.values(),  # probabilidades associadas
            k=1  # apenas um valor
        )[0]
        return next_state
        
    def generate(self, begin: str, delay: float = 0.2) -> str:
        if begin not in self.states:
            raise ValueError(f"Invalid starting state: {begin}")
        
        state = begin  # Agora é uma tupla, não mais uma lista
        output = [state]  # Começamos com a palavra inicial
        history = list(state)  # Histórico das palavras já geradas
        while len(history) < 1000:  # gerar até 100 palavras
            # Utiliza todo o histórico gerado até agora
            next_state = self.selectNextState(tuple(history[-self.n:]))  # Usa o histórico completo
            output.append(next_state)
            history.append(next_state)  # Atualiza o histórico
            time.sleep(delay)  # Adiciona um atraso entre as palavras geradas
            print(next_state, end=" ", flush=True)
        
        return " ".join(output)

    def __str__(self) -> str:
        # Organizando os estados e transições para visualização
        output = []
        for state, transitions in self.transitions.items():
            transition_str = ', '.join([f"{next_state}: {count}" for next_state, count in transitions.items()])
            output.append(f"{state} -> [{transition_str}]")
        
        # Unindo todas as representações das transições para formar a string final
        return "\n".join(output)


# Exemplo de uso:
with open("../../docs/test.txt", "r", encoding='utf-8') as text_file:
    text = text_file.read()

chain = MarkovChain(n=2)  # Usando bi-gramas (ordem 2)
chain.fit(text)

# Agora, o input é para a palavra inicial
entrada = input("Digite uma palavra para iniciar a geração:\n\n")

# Aqui, escolhemos a próxima palavra com base na primeira palavra do usuário
valid_next_words = [word for word in chain.transitions if word[0] == entrada.lower()]
selected_word_pair = random.choice(valid_next_words)
chain.generate(selected_word_pair, delay=0.2)
