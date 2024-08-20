import pandas as pd
import time 

# Hash table que guarda nodos sobre jogadores (parecida com o lab 4)
class NodoJogador:
    def __init__(self, sofifaID, apelido, nome, posicao, nacionalidade, clube, liga):
        self.sofifaID = sofifaID
        self.apelido = apelido #nome curto
        self.nome = nome #nome longo
        self.posicao = posicao
        self.nacionalidade = nacionalidade
        self.clube = clube
        self.liga = liga
        self.sumAvaliacao = 0.0
        self.counter = 0
    
    def addAvaliacao(self,avaliacao):
        self.sumAvaliacao += avaliacao
        self.counter += 1
        
class HashTable:
    def __init__(self):
        self.size = 7993 # tamanho teste, da pra mudar dps
        self.table = [None] * self.size
    
    def calculaHash(self,sofifaID):
        return sofifaID % self.size
    
    def insere(self,sofifaID,apelido,nome,posicao,nacionalidade,clube,liga):
        index = self.calculaHash(sofifaID)
        if self.table[index] == None:
            self.table[index] = [NodoJogador(sofifaID,apelido,nome,posicao,nacionalidade,clube,liga)]
        else:
            self.table[index].append(NodoJogador(sofifaID,apelido,nome,posicao,nacionalidade,clube,liga))

    def busca(self,sofifaid):
        index = self.calculaHash(sofifaid)
        if self.table[index] == None:
            return None
        else:
            for nodo in self.table[index]:
                if nodo.id == sofifaid:
                    return nodo
            return None
    
    def printaHash(self):
        for i in range(10):
            if self.table[i] != None:
                print(self.table[i][0].apelido)

# Arvore Trie, guarda os nomes dos jogadores
class TrieNode:
    def __init__(self):
        self.children = [None] * 128 # 128 caracteres do ascii
        self.fifaID = None

class TrieTree:
    def __init__(self):
        self.root = TrieNode()

    def insertName(self, name, fifaID):
        nodoAtual = self.root

        for char in name:
            index = ord(char) - ord('a')
            if nodoAtual.children[index] is None:
                novoNodo = TrieNode()
                nodoAtual.children[index] = novoNodo
            nodoAtual = nodoAtual.children[index]

        nodoAtual.fifaID = fifaID

    def searchName(self, prefix):
        nodoAtual = self.root
        for char in prefix:
            index = ord(char) - ord('a')
            if nodoAtual.children[index] is None:
                return None
            nodoAtual = nodoAtual.children[index]
        return nodoAtual.fifaID


    # Funcao que retorna uma lista de fifaIDs de jogadores que tem o prefixo dado
    def listOfNames(self, prefix):
        def aux(node, listID): # funcao auxiliar para percorrer a arvore 
            if node.fifaID is not None:
                listID.append(node.fifaID)
            for child in node.children:
                if child is not None:
                    aux(child, listID)
    
        nodoAtual = self.searchPrefix(prefix)  # chama funcao searchPrefix para achar nodo com prefixo
        if nodoAtual is None:
            return []
        listID = []
        aux(nodoAtual, listID)
        return listID    

    def searchPrefix(self, prefix):
        nodoAtual = self.root
        for char in prefix:
            index = ord(char) - ord('a')
            if nodoAtual.children[index] is None:
                return False
            nodoAtual = nodoAtual.children[index]
        return nodoAtual

# Estrutura da dados que guarda opinioes dos usuarios
class NodoUser:
    def __init__(self, userID, fifaID, nota):
        self.userID = userID
        self.fifaID = fifaID
        self.nota = nota
        self.next = None      
    
class HashUser:
    def __init__(self):
        self.size = 1000019 # tamanho teste 
        self.table = [None] * self.size
    
    def calculaHash(self,userID):
        return userID % self.size 
    
    def insere(self,userID,fifaID,nota):
        index = self.calculaHash(userID)
        new_node = NodoUser(userID, fifaID, nota)
        new_node.next = self.table[index]
        self.table[index] = new_node
    
    def pegaAvaliacao(self,userID):
        index = self.calculaHash(userID)
        if self.table == None:
            return None
        else:
            avaliacoes = [] # cria lista de avaliacoes
            for user in self.table[index]:
                if user.userID == userID:
                    avaliacoes.append(user)    # adiciona nodo na lista de todas avaliacoes do usuario
            return avaliacoes
     
    def printaHash(self):
        for i in range(10):
            if self.table[i] != None:
                print(self.table[i][0].userID)    
                print(self.table[i][0].nota)

# Estrutura de dados que guarda tags de jogadores. tag é o id para hash e o nome do jogador é o dado satelite
class TagJogador:
    def __init__(self, userID, sofifaID, tag):
        self.userID = userID
        self.sofifaID = sofifaID
        self.tag = tag
        
class HashTags:
    def __init__(self):
        self.size = 49999
        self.table = [None] * self.size

    def CalculaHash(self, tag):
        return sum(ord(char) for char in str(tag)) % self.size # soma unicode da string e usa como key da hash

    def insere(self,userID,sofifaID,tag):
        index = self.CalculaHash(tag)
        if self.table[index] is None:
            self.table[index] = [TagJogador(userID,sofifaID,tag)]
        else:
            self.table[index].append(TagJogador(userID,sofifaID,tag))

#--------------------------------------------
# Main
#--------------------------------------------
#Leitura dos arquivos
filePlayers = pd.read_csv('players.csv')
fileRating = pd.read_csv('rating.csv')
fileTags = pd.read_csv('tags.csv')
# Inicializacao das estruturas de dados
hashTablePlayers = HashTable()
hashTableUsers = HashUser()
triePlayers = TrieTree()
hashTags = HashTags()

# Insercao dos dados nos hashTables e contagem do tempo
inicio = time.time()
for i in range(len(filePlayers)):
    hashTablePlayers.insere(filePlayers['sofifa_id'][i],filePlayers['short_name'][i],filePlayers['long_name'][i],filePlayers['player_positions'][i],filePlayers['nationality'][i],filePlayers['club_name'][i],filePlayers['league_name'][i])
    triePlayers.insertName(filePlayers['long_name'][i],filePlayers['sofifa_id'][i])
stopclock = time.time()
tempojogadores = stopclock - inicio
print("Tempo para criar HashPlayers e triePlayers: ",tempojogadores)


inicio = time.time()
for i in range(len(fileRating)):
    hashTableUsers.insere(fileRating['user_id'][i],fileRating['sofifa_id'][i],fileRating['rating'][i]) 
stopclock = time.time()
tempoUsers = stopclock - inicio 
print("Terminou file de ratings: ", tempoUsers)

inicio = time.time()
for i in range(len(fileTags)):
    hashTags.insere(fileTags['user_id'][i], fileTags['sofifa_id'][i], fileTags['tag'][i])
stopclock = time.time()
tempoTag = stopclock - inicio
print("Terminou file de tags: ",tempoTag)

