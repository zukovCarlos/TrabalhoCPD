
class mergeSort:
    def __init__(self, listOfNodes, indexOfSorting):
        self.listOfNodes = listOfNodes
        self.indexOfSorting = indexOfSorting

    def merge(self, arrayAux, low, mid, high):
        assert self.isSorted(low, mid)
        assert self.isSorted(mid+1, high)

        for k in range(low, high + 1):
            arrayAux[k] = self.listOfNodes[k]
            
        i = low
        j = mid + 1
        for k in range(low, high + 1):
            if i > mid:
                self.listOfNodes[k] = arrayAux[j]
                j += 1
            elif j > high:
                self.listOfNodes[k] = arrayAux[i]
                i += 1
            elif arrayAux[j].attributes[self.indexOfSorting] > arrayAux[i].attributes[self.indexOfSorting]:
                self.listOfNodes[k] = arrayAux[j]
                j += 1
            else:
                self.listOfNodes[k] = arrayAux[i]
                i += 1

        assert self.isSorted(low, high)

    def sortAux(self,arrayAux, low, high):
        if high <= low:
            return
        mid = low + (high - low) // 2
        self.sortAux( arrayAux, low, mid)
        self.sortAux( arrayAux, mid + 1, high)
        self.merge( arrayAux, low, mid, high)

    def sort(self):
        self.sortAux( [None] * len(self.listOfNodes), 0, len(self.listOfNodes) - 1)
        return self.listOfNodes

    # Funcao que verifica se o array esta ordenado
    def isSorted(self,low, high):
        for i in range(low + 1, high + 1):
            if self.listOfNodes[i].attributes[self.indexOfSorting] > self.listOfNodes[i - 1].attributes[self.indexOfSorting]:
                return False
        return True
     
    

    
