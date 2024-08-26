import node

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

class HashPlayer:
    def __init__(self):
        self.size = 7993 # tamanho teste, da pra mudar dps
        self.table = [None] * self.size
    
    def calculaHash(self,sofifaID):
        return sofifaID % self.size
    
    def insere(self,sofifaID,apelido,nome,posicao,nacionalidade,clube,liga):
        index = self.calculaHash(sofifaID)
        if self.table[index] == None:
            self.table[index] = [node.NodoJogador(sofifaID,apelido,nome,posicao,nacionalidade,clube,liga)]
        else:
            self.table[index].append(node.NodoJogador(sofifaID,apelido,nome,posicao,nacionalidade,clube,liga))

    def busca(self,sofifaid):
        index = self.calculaHash(sofifaid)
        if self.table[index] == None:
            return None
        else:
            for nodo in self.table[index]:
                if nodo.attributes[0] == sofifaid: # atributo 0 é o sofifaID
                    return nodo
            return None
    
    def printaHash(self):
        for i in range(10):
            if self.table[i] != None:
                print(self.table[i][0].apelido)
    
    def insereAvaliacao(self,sofifaID,avaliacao):
        index = self.calculaHash(sofifaID)
        if self.table[index] == None:
            return None
        else:
            for nodo in self.table[index]:
                if nodo.attributes[0] == sofifaID:
                    nodo.addAvaliacao(avaliacao)
                    return None
            return None
        
    def listOfPositions(self,position):
        listOfPlayers = []
        for index in self.table:
            if(index):
                for player in index:
                    if position in player.attributes[POSICAO_INDEX]:
                        listOfPlayers.append(player)
        return listOfPlayers
        
    def setMedia(self):
        for index in self.table:
            if index != None:
                for player in index:
                    player.setMedia()               

class HashUser:
    def __init__(self):
        self.size = 500019 # tamanho teste 
        self.table = [None] * self.size
    
    def calculaHash(self,userID):
        return userID % self.size 
    
    def insere(self,userID,fifaID,nota):
        index = self.calculaHash(userID)
        new_node = node.NodoUser(userID, fifaID, nota)
        if self.table[index] is None:
            self.table[index] = []
            self.table[index].append(new_node)
        else:
            self.table[index].append(new_node)
            
    
    def pegaAvaliacao(self,userID):
        index = self.calculaHash(userID)
        if self.table == None:
            return None
        else:
            avaliacoes = [] # cria lista de avaliacoes
            count = 0
            for user in self.table[index]:
                if user.userID == userID:
                    avaliacoes.append(user)    # adiciona nodo na lista de todas avaliacoes do usuario
                    count += 1
                    if count == 20:
                        break
            return avaliacoes
    
    def printaHash(self):
        for i in range(10):
            if self.table[i] != None:
                print(self.table[i][0].userID)    
                print(self.table[i][0].nota)
                
    def listOfRatings(self,userID):
        listOfRatings = []
        index = self.calculaHash(userID)
        if self.table[index] == None:
            return None
        else:
            for user in self.table[index]:
                if user.userID == userID:
                    listOfRatings.append(user)
            return listOfRatings