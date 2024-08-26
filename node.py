SOFIFAID_INDEX = 0
APELIDO_INDEX = 1
NOME_INDEX = 2
POSICAO_INDEX = 3
NACIONALIDADE_INDEX = 4
CLUBE_INDEX = 5
LIGA_INDEX = 6
AVALIACAO_INDEX = 7
CONTADOR_INDEX = 8
MEDIA_INDEX = 9
NOTAUSERATUAL_INDEX = 10

# Hash table que guarda nodos sobre jogadores (parecida com o lab 4)
class NodoJogador:
    #Constants for attribute index
    
    def __init__(self, sofifaID, apelido, nome, posicao, nacionalidade, clube, liga):
        self.attributes = [sofifaID, apelido, nome, posicao, nacionalidade, clube, liga, 0, 0, 0, 0]
    
    def addAvaliacao(self,avaliacao):
        self.attributes[AVALIACAO_INDEX] += avaliacao # soma avaliacao
        self.attributes[CONTADOR_INDEX] += 1 # incrementa contador
    
    def setMedia(self):
        if self.attributes[CONTADOR_INDEX] != 0: # se tiver avaliacoes
            #print("player",self.attributes[SOFIFAID_INDEX],"has a score of",self.attributes[AVALIACAO_INDEX], "and a count of",self.attributes[CONTADOR_INDEX])
            self.attributes[MEDIA_INDEX] = self.attributes[AVALIACAO_INDEX]/self.attributes[CONTADOR_INDEX] # media
            #print("player",self.attributes[SOFIFAID_INDEX],"has a media of",self.attributes[MEDIA_INDEX])
        else:
            self.attributes[MEDIA_INDEX] = 0.0 # se nao tiver avaliacoes media = 0

# Estrutura de dados que guarda tags de jogadores. tag é o id para hash e o nome do jogador é o dado satelite
class TagJogador:
    def __init__(self, userID, sofifaID, tag):
        self.userID = userID
        self.sofifaID = sofifaID
        self.tag = tag

# Estrutura da dados que guarda opinioes dos usuarios
class NodoUser:
    def __init__(self, userID, fifaID, nota):
        self.userID = userID
        self.fifaID = fifaID
        self.nota = nota     

# Arvore Trie, guarda os nomes dos jogadores
class TrieNode:
    def __init__(self):
        self.children = [None] * 128 # 128 caracteres do ascii
        self.fifaID = None

# Arvore Trie que guarda tags dos jogadores
class TrieNodeTag:
    def __init__(self):
        self.children = [None] * 128 # 128 caracteres do ascii
        self.fifaID = []
        self.userID = []