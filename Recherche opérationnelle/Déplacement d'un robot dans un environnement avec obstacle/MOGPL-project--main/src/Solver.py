class Solver:
    def __init__(self):
        self.directionDict = {
            'nord':0,
            'ouest':1,
            'sud':2,
            'est':3
        }

    def bfsSolver(self,graph): # bfs algo in a not-weighted directed graph gives shortest path ->
                               # O(V + E) = O(length*width)
        currX = graph.currX
        currY = graph.currY
        currOrientation = graph.currOrientation
        idx = (currX, currY, currOrientation)
        queue = [idx]
        visited = []
        bestPath = dict()
        finalOrientation = None
        
        if(currX, currY) in graph.blockedList:
            print("Position de départ non valide")
            return None

        while len(queue) > 0:
            node = queue.pop(0)
            if (node[0],node[1]) in graph.blockedList:
                raise Exception("Error: graph was incorrectly generated or parsed!")
            if (node[0], node[1]) == (graph.endx , graph.endy):
                finalOrientation = node[2]
                break
            if node in visited:
                continue
            visited.append(node)
            queue.extend(graph.Nodes[node].next)
            if node not in bestPath.keys():
                bestPath[node] = [node]
            for nd in graph.Nodes[node].next:
                id = (nd[0],nd[1],nd[2])
                if id not in bestPath.keys():
                    bestPath[id] = bestPath[node] + [nd]
        if(finalOrientation not in ['sud','nord','est','ouest']):
            print("Erreur, il n'y a pas de chemin possible")
            return None
        return bestPath[(graph.endx,graph.endy,finalOrientation)]

    def writeOutput(self, bestPath, filename="examples/sortie.txt"):
        if(bestPath == None):
            print("Aucun chemin trouvé")
            with open("examples/sortie.txt", "w") as f:
                f.write("-1")
                return "-1"
        outStr = f"{len(bestPath)-1} "
        for i in range(len(bestPath)):
            if i == len(bestPath) - 1:
                break
            currX, currY, currOrientation = bestPath[i]
            nextX, nextY, nextOrientation = bestPath[i+1]
            if currOrientation == nextOrientation:
                outStr += f'a{max(abs(currX - nextX),abs(currY - nextY))} '
            else: 
                if (self.directionDict[nextOrientation] - self.directionDict[currOrientation]) % 4 == 1:
                    outStr += "G "
                else:
                    outStr += "D "
        outStr = outStr.strip()
        if filename is not None: 
            with open(filename,"+w") as f:
                f.write(outStr)
                return outStr
        return outStr
        

    def checkCorrectness(self,init_pos,end_pos,init_dir,graph,ans): ## not tested yet
        ans = ans.split()
        n = int(ans[0])
        dir = self.directionDict[init_dir]
        currpos = init_pos
        for i in range(n):
            if ans[i] == "D":
                dir += 1
                dir = dir % 4
            elif ans[i] == "G":
                dir -= 1 
                dir = dir % 4
            else: ## ans[i] = ak
                k = int(ans[i][1])
                if dir == 0: # nord
                    if currpos[1] - k <= 0:
                        raise Exception("wrong value!")
                    for m in range(1,k+1):
                        if (currpos[0], currpos[1] - m) in graph.blockedList:
                            raise Exception("wrong value!")
                    currpos[1] -= k
                elif dir == 1: # ouest
                    if currpos[0] + k >= graph.width:
                        raise Exception("wrong value!")
                    for m in range(1,k+1):
                        if (currpos[0]+m, currpos[1]) in graph.blockedList:
                            raise Exception("wrong value!")
                    currpos[0] += k
                elif dir == 2: # sud
                    if currpos[1] + k >= graph.length:
                        raise Exception("wrong value!")
                    for m in range(1,k+1):
                        if (currpos[0], currpos[1] + m) in graph.blockedList:
                            raise Exception("wrong value!")
                    currpos[1] += k
                else: # est
                    if currpos[0] - k <= 0:
                        raise Exception("wrong value!")
                    for m in range(1,k+1):
                        if (currpos[0] - m, currpos[1]) in graph.blockedList:
                            raise Exception("wrong value!")
                    currpos[0] -= k

        if currpos != end_pos:
            raise Exception("wrong end_pos")
        else: 
            print("correctness verified!")


