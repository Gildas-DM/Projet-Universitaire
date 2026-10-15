import random

class Node:
    def __init__(self,x,y, orientation):
        self.x = x 
        self.y = y
        self.next = []
        self.orientation = orientation

class Graph:
    def __init__(self, initx, inity, endx, endy, width, length, initialOrientation, blockedList):
        if (initx < 0 or initx > width):
            raise Exception("GraphCreationError: invalid initx value!")
        if (inity < 0 or inity > length):
            raise Exception("GraphCreationError: invalid inity value!")
        if ((initx, inity) in blockedList):
            raise Exception("GraphCreationError: invalid initial position!")
        if (endx < 0 or endx > width):
            raise Exception("GraphCreationError: invalid endx value!")
        if (endy < 0 or endy > length):
            raise Exception("GraphCreationError: invalid endy value!")
        if ((endx, endy) in blockedList):
            raise Exception("GraphCreationError: invalid final position!")
        self.currX = initx
        self.currY = inity
        self.initx = initx
        self.inity = inity
        self.initialOrientation = initialOrientation
        self.currOrientation = initialOrientation
        self.endx  = endx
        self.endy  = endy
        self.width = width
        self.length = length
        self.blockedList = blockedList
        self.Nodes = dict()

    def __str__(self):
        out = f'{self.length} {self.width} \n'
        for j in range(self.length):
            for i in range(self.width):
                if (i,j) in self.blockedList and (i+1,j) in self.blockedList and (i,j+1) in self.blockedList and (i+1,j+1) in self.blockedList:
                    out += "1 "
                else:
                    out += "0 "
            out += '\n'
        out += f'{self.inity} {self.initx} {self.endy} {self.endx} {self.initialOrientation}\n'
        out += "0 0"
        return out
        
    def createGraph(self):
        for i in range(self.width + 1):
            for j in range(self.length +1):
                if (i,j) not in self.blockedList:
                    for dir in ['sud','nord','est','ouest']:
                        self.Nodes[(i,j,dir)] = Node(i,j,dir)
        for idx in list(self.Nodes.keys()):
            self.addNeighbors(idx)
    
    def addNeighbors(self,idx):
        x, y, dir = idx
        if dir == "nord":
            for k in range(1,4):
                if y - k >= 0 and (x, y-k) not in self.blockedList: 
                    self.Nodes[idx].next.append((x,y-k,dir))
                if (x,y-k) in self.blockedList:
                    break
            self.Nodes[idx].next.extend([(x,y,'est'), (x,y,'ouest')])
        if dir == "est":
            for k in range(1,4):
                if x + k <= self.width  and (x+k, y) not in self.blockedList:
                    self.Nodes[idx].next.append((x+k,y,dir))
                if (x+k,y) in self.blockedList:
                    break
            self.Nodes[idx].next.extend([(x,y,'nord'), (x,y,'sud')])
        if dir == "sud":
            for k in range(1,4):
                if y+k <= self.length and (x, y+k) not in self.blockedList:
                    self.Nodes[idx].next.append((x,y+k,dir))
                if (x,y+k) in self.blockedList:
                    break
            self.Nodes[idx].next.extend([(x,y,'ouest'), (x,y,'est')])
        if dir == "ouest":
            for k in range(1,4):
                if x - k >= 0 and (x-k, y) not in self.blockedList:
                    self.Nodes[idx].next.append((x-k,y,dir)) 
                if (x-k,y) in self.blockedList:
                    break
            self.Nodes[idx].next.extend([(x,y,'nord'), (x,y,'sud')])

def generateRandomGraph(width,length,nblocked,filename = None):
    blockedList = []
    initx, inity = None, None
    endx, endy = None, None
    for n in range(nblocked):
        x,y = None,None
        while (x,y) not in blockedList or (x+1,y) not in blockedList or (x,y+1) not in blockedList or (x+1,y+1) not in blockedList:
            x = random.randint(0,width-1)
            y = random.randint(0,length-1)
            if (x,y) not in blockedList or (x+1,y) not in blockedList or (x,y+1) not in blockedList or (x+1,y+1) not in blockedList:
                blockedList.extend([(x,y),(x+1,y), (x,y+1), (x+1, y+1)])
    blockedList = list(set(blockedList))
    initx, inity, endx, endy = None, None, None, None
    while (initx,inity) == (None,None) or (initx, inity) in blockedList:
        initx = random.randint(0,width-1)
        inity = random.randint(0,length-1)
    while (endx,endy) == (None,None) or (endx, endy) in blockedList or (endx, endy) == (initx, inity):
        endx = random.randint(0,width-1)
        endy = random.randint(0,length-1)
    initialOrientation = random.choice(['sud','nord','est','ouest'])
    g =  Graph(initx,inity,endx,endy,width,length,initialOrientation,blockedList)
    g.createGraph()
    return g
