import time
import csv   
import hashtable 
import trie
import re
from mergeSort import mergeSort
from tabulate import tabulate
from functools import reduce

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

#--------------------------------------------
# Main
#--------------------------------------------
#Leitura dos arquivos

filePlayers = csv.DictReader(open('players.csv'))
fileRating = csv.DictReader(open('rating.csv'))
fileTags = csv.DictReader(open('tags.csv'))

# Inicializacao das estruturas de dados
hashTablePlayers = hashtable.HashPlayer()
hashTableUsers = hashtable.HashUser()
triePlayers = trie.TrieTree()
trieTags = trie.TrieTags()

#Insercao dos dados nos hashTables e contagem do tempo
inicio = time.time()
for player in filePlayers: # Itera pelo arquivo csv lido utilizando a lib csv
   hashTablePlayers.insere(int(player['sofifa_id']), player['short_name'], player['long_name'], player['player_positions'], player['nationality'], player['club_name'], player['league_name'])
   triePlayers.insertName(player['long_name'], player['sofifa_id'])
stopclock = time.time()
tempojogadores = stopclock - inicio
print("Tempo para criar HashPlayers e triePlayers: ",tempojogadores)

# Insercao das ratings nas hashtables

inicio = time.time()
for rating in fileRating:
    hashTableUsers.insere(int(rating['user_id']),int(rating['sofifa_id']),float(rating['rating']))
    hashTablePlayers.insereAvaliacao(int(rating['sofifa_id']),float(rating['rating'])) 
stopclock = time.time()
tempoUsers = stopclock - inicio 
print("Terminou file de ratings: ", tempoUsers)
hashTablePlayers.setMedia()


inicio = time.time()
for tags in fileTags:
     trieTags.insertTag(int(tags['user_id']), tags['sofifa_id'], tags['tag'])
stopclock = time.time()
tempoTag = stopclock - inicio
print("Terminou file de tags: ",tempoTag)


def headerTabulate(numSearch):
    if numSearch == 1:
        return ["sofifa_id", "short_name", "long_name", "player_positions", "rating", "count"]
    elif numSearch == 2:
        return ["sofifa_id", "short_name", "long_name", "global_rating", "count", "rating"]
    elif numSearch == 3:
        return ["sofifa_id", "short_name", "long_name", "player_positions", "nationality", "club_name", "league_name","rating","count"]
    elif numSearch == 4:
        return ["sofifa_id", "short_name", "long_name", "player_positions", "nationality", "club_name", "league_name","rating","count"]

#
def listOfLists(list,searchNumber):
    listOfLists = []
    if(searchNumber == 1):
        mergeAux = mergeSort(list, MEDIA_INDEX)
        sortedList = mergeAux.sort()
            
        for players in sortedList:
            player = hashTablePlayers.busca(int(players.attributes[0]))
            playerList = [player.attributes[0], player.attributes[1], player.attributes[2], player.attributes[3], player.attributes[9], player.attributes[8]]
            
            listOfLists.append(playerList)
        return listOfLists
    
    elif(searchNumber == 2):
        mergeAux = mergeSort(list, MEDIA_INDEX)
        sortedList = mergeAux.sort()
        mergeAux2 = mergeSort(sortedList, NOTAUSERATUAL_INDEX)
        sortedList2 = mergeAux2.sort()
        
        for players in sortedList2:
            player = hashTablePlayers.busca(int(players.attributes[0]))
            playerList = [player.attributes[0], player.attributes[1], player.attributes[2], player.attributes[9], player.attributes[8], player.attributes[10]]
            
            listOfLists.append(playerList)
            
        return listOfLists
    
    elif(searchNumber == 3):
        mergeAux = mergeSort(list, MEDIA_INDEX)
        sortedList = mergeAux.sort()
        for players in sortedList:
            player = hashTablePlayers.busca(int(players.attributes[0]))
            if(player.attributes[CONTADOR_INDEX] >= 1000):
                playerList = [player.attributes[0], player.attributes[1], player.attributes[2], player.attributes[3], player.attributes[4], player.attributes[5], player.attributes[6], player.attributes[9], player.attributes[8]]
                listOfLists.append(playerList)
        return listOfLists

    elif(searchNumber == 4):
        mergeAux = mergeSort(list, MEDIA_INDEX)
        sortedList = mergeAux.sort()
        for players in sortedList:
            player = hashTablePlayers.busca(int(players.attributes[0]))
            playerList = [player.attributes[0], player.attributes[1], player.attributes[2], player.attributes[3], player.attributes[4], player.attributes[5], player.attributes[6], player.attributes[9], player.attributes[8]]
            listOfLists.append(playerList)
        return listOfLists

def searchOne(userInput):
    list = triePlayers.listOfNames(userInput)
    playerList = []
    if(list):
        for fifaID in list:
            player = hashTablePlayers.busca(int(fifaID))
            playerList.append(player)
        searchOneList = listOfLists(playerList, 1)
        print(tabulate(searchOneList, headers = headerTabulate(1), tablefmt = "grid", floatfmt=".6f"))
    else:
         print("Nenhum jogador encontrado")   
                               

def searchTwo(userInput):
    list = hashTableUsers.listOfRatings(userInput)
    ratingsList = []
    searchTwoListOnly20 = []
    if(list):
        for userRating in list:
            player = hashTablePlayers.busca(int(userRating.fifaID))
            player.attributes[NOTAUSERATUAL_INDEX] = userRating.nota # modifica a nota atual do jogador para guardar a nota do usuario que por ultimo avaliou ele
            ratingsList.append(player)
        searchTwoList = listOfLists(ratingsList, 2)
        for i in range(20):
            if(searchTwoList[i]):
                searchTwoListOnly20.append(searchTwoList[i])
        print(tabulate(searchTwoListOnly20, headers = headerTabulate(2), tablefmt = "grid", floatfmt=".6f"))
    else:
         print("Nenhuma avaliação encontrada")


def searchThree(topN, position):
    list = hashTablePlayers.listOfPositions(position)
    searchThreeListTopN = []
    if(list):
        searchThreeList = listOfLists(list, 3)
        aux = len(searchThreeList)
        if(aux < topN):
            topN = aux
        for i in range(topN):   
            searchThreeListTopN.append(searchThreeList[i])
        print(tabulate(searchThreeListTopN, headers = headerTabulate(3), tablefmt = "grid", floatfmt=".6f"))
    else:
        print ("Nenhum jogador com essa posição encontrado")


def searchFour(InputString):
    
    def findTags(InputString):
        pattern = r"'(.*?)'"
        tags = re.findall(pattern, InputString)
        return tags
    
    def findFifaIDs(InputString):
        tags = findTags(InputString)
        if tags is None:
            print("Nenhuma tag encontrada")
            return None
        
        listOfPlayers = []
        intersection = []
        for tag in tags:
            players = trieTags.searchForTag(tag)
            if players is None:
                print("Nenhum jogador encontrado com a tag ", tag)
                return None
            listOfPlayers.append(set(players))
        if listOfPlayers:
            intersection = list(reduce(set.intersection, listOfPlayers))
            return intersection
        else:
            return None
    
    listOfIDs = findFifaIDs(InputString)
    playersList = []
    
    if (listOfIDs):
        for playerID in listOfIDs:
            player = hashTablePlayers.busca(int(playerID))
            playersList.append(player)
        searchFourList = listOfLists(playersList,4)
        print(tabulate(searchFourList, headers = headerTabulate(4), tablefmt = "grid", floatfmt=".6f"))

endProgram = False
while not endProgram:  
    
    print("Escolha a opção de busca:")
    print("1 - Busca por nome (Busca todos os jogadores com o prefixo dado)")
    print("2 - Busca por usuário (Busca avaliações feita por um usuário específico)")
    print("3 - Busca por posição (Busca os top N jogadores com a posição dada)")
    print("4 - Busca por tags (Busca jogadores com as tags dadas)")
    print("5 - Sair")
    userChoice = None
    
    while userChoice is None:
        userChoice = input("")
    print("\n")
    if (userChoice == "1"):
        print ("Tecle 5 para retornar ao menu principal")
        userChoice = input("Digite player<prefix> para buscar jogadores com o prefixo <prefix>:")
        if userChoice == 5:
            continue
        substring = userChoice[6:] # pega a substring apos o player
        searchOne(substring)
    elif (userChoice == "2"):
        print("Tecle 5 para retornar ao menu principal")
        userChoice = input("Digite user<userID> para buscar as avaliações do usuário <userID>:")
        if userChoice == 5:
            continue
        else:
            substring = userChoice[4:]
            searchTwo(int(substring))
    elif(userChoice == "3"):
        print("Tecle 5 para retornar ao menu principal")
        userChoice = input("Digite top<N><position> para buscar os <topN> jogadores com a posição <position>:")
        if userChoice == 5:
            continue
        userChoice = userChoice[3:]
        for i, char in enumerate(userChoice):
            if not char.isdigit():
                break
        
        topN = int(userChoice[:i])
        position = userChoice[i:]
        
        searchThree(topN,position)
    elif(userChoice == "4"):
        print("Tecle 5 para retornar ao menu principal")
        userChoice = input("Digite tags<list of tags> para buscar jogadores com as tags <list of tags>, onde list of tags são tags entre aspas simples:")
        if userChoice == 5:
            continue
        substring = userChoice[3:]
        
        searchFour(substring)
        
    elif(userChoice == "5"):
        endProgram = True
    else:
        print("Opção inválida, tente novamente")
        
        