import os, re, igraph

def init ():
    allgame = {}


    file_path = "/var/www/html/static/sgf"
    for f in os.listdir(file_path):
        with open(file_path+'/'+f) as fp:
            ss = fp.read()
            moves = re.findall("[W|B]\[..\]", ss)
            allgame[int(f[:-4])] = moves
    print '--------------------------'
    return allgame




#-------- igraph version -----------

# note tuple cant be vertex
def add(gr, gb,i):
    x,y = gb[i]
    v = chr(x)+chr(y)
    gr.add_vertex(v)
    for m in [(x,y+1), (x,y-1), (x-1,y),(x-1,y)]:
        if m in gb[:i]:
            u  = chr(m[0])+chr(m[1])
            gr.add_edge(v,u)
            

class Giter:
    
    allgame = init()
    def __init__(self):
        
        self.game = Giter.allgame[177777]
        self.gb = [(ord(i[2]) ,ord(i[3])) for i in self.game if i.startswith('B')]
        self.G = igraph.Graph()
        self.i = 0
        
    def __iter__(self):
        return self
        
    def next(self):
        if self.i >= len(self.gb):
            raise StopIteration
        else:
            add (self.G, self.gb,self.i)
            self.i += 1

#--------- networkx version -----------
        


#---------------       analysis  graph's properties use pandas dataframe      ----------------------------



G = Giter()
Giter.next = next

def edges_vetice():
  for g in G:
      if G.i % 10 == 0:
            print '-------------------'
            for v in G.G.vs:
                print v
            for e in G.G.es:
                print e.tuple
            
def charactor():
    for g in G:
        #print G.G.omega()
        print G.G.alpha()

def blink():
    pass


