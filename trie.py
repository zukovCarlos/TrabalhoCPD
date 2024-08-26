import node

class TrieTree:
    def __init__(self):
        self.root = node.TrieNode()

    def insertName(self, name, fifaID):
        nodoAtual = self.root

        for char in name:
            index = ord(char.lower()) - ord('a')
            if nodoAtual.children[index] is None:
                nodoAtual.children[index] = node.TrieNode()
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
    
        nodoAtual = self.searchPrefix(prefix.lower())  # chama funcao searchPrefix para achar nodo com prefixo
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
                return None
            nodoAtual = nodoAtual.children[index]
        return nodoAtual
    
class TrieTags:
    def __init__(self):
        self.root = node.TrieNodeTag()
    
    def insertTag(self,userID,fifaID,tag):
        currentNode = self.root
        for char in tag:
            index = ord(char.lower()) - ord('a')
            if currentNode.children[index] is None:
                currentNode.children[index] = node.TrieNodeTag()
            currentNode = currentNode.children[index]

        if currentNode.fifaID is not None:      # caso a tag ja tenha sido inserida, precisamos preservar os IDs anteriormente inseridos
            currentNode.fifaID.append(fifaID)
            currentNode.userID.append(userID)
        else:                                   # caso a tag seja nova na Trie
            currentNode.fifaID = fifaID
            currentNode.userID = userID
    
    def searchForTag(self,tag):
        currentNode = self.root
        listOfFifaID = []
        for char in tag:
            index = ord(char.lower()) - ord('a')
            if currentNode.children[index] is None:
                return None
            currentNode = currentNode.children[index]
        return currentNode.fifaID  # retorna a lista de fifaIDs que possuem a tag procurada

        # while currentNode is not None:
        #     if currentNode.fifaID is not None:
        #         listOfFifaID.append(currentNode.fifaID)
        #     currentNode = currentNode.next
        # return listOfFifaID