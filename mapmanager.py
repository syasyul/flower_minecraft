import pickle
class Mapmanager():
    def __init__(self):
        self.model='block'
        self.texture='block.png'
        self.colors=[(0.165, 0.549, 0.78, 1),(0.729, 0.365, 0.027, 1),(0.729, 0.365, 0.027, 1),(0.729, 0.365, 0.027, 1),(0.447, 0.78, 0.153, 1),(0.349, 0.651, 0.086, 1),(0.349, 0.651, 0.086, 1),(0.447, 0.78, 0.153, 1),(0.447, 0.78, 0.153, 1),(0.349, 0.651, 0.086, 1),(0.855, 0.275, 0.941, 1),(0.855, 0.275, 0.941, 1),(0.855, 0.275, 0.941, 1),(0.941, 0.275, 0.784, 1),(0.941, 0.275, 0.784, 1),(0.941, 0.275, 0.784, 1),(0.941, 0.275, 0.784, 1),(0.941, 0.275, 0.784, 1)]
        self.startNew()
    def startNew(self):
        self.land=render.attachNewNode("Land")
    def getColor(self,z):
        if z<len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors)-1]
    def addBlock(self,position):
        self.block=loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.color=self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.setTag("at",str(position))
        self.block.reparentTo(self.land)
    def clear(self):
        self.land.removeNode()
        self.startNew()
    def loadLand(self,filename):
        self.clear()
        with open(filename) as file:
            y=0
            for line in file:
                x=0
                line=line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        self.addBlock((x,y,z0))
                    x+=1
                y+=1
        return x,y
    def findBlocks(self,pos): #tambahakan
        return self.land.findAllMatches("=at="+str(pos))
    def isEmpty(self,pos): #tambahakan
        blocks=self.findBlocks(pos)
        return not blocks
    def findHighestEmpty(self,pos): #tambahakan
        x,y,z=pos
        z=1
        while not self.isEmpty((x,y,z)):
            z+=1
        return (x,y,z)
    def buildBlock(self,pos): #tambahakan
        x,y,z=pos
        new=self.findHighestEmpty(pos)
        if new[2]<=z+1:
            self.addBlock(new)
    def delBlock(self,position): #tambahakan
        blocks=self.findBlocks(position)
        for block in blocks:
            block.removeNode()
    def delBlockFrom(self,position): #tambahakan
        x,y,z=self.findHighestEmpty(position)
        pos=x,y,z-1
        for block in self.findBlocks(pos):
            block.removeNode()
    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x,y,z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)
    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            lenght = pickle.load(fin)
            for i in range(lenght):
                pos = pickle.load(fin)
                self.addBlock(pos)