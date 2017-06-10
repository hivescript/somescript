import os, re, igraph, networkx
import pandas as pd

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
            


#--------- networkx version -----------

# halfgraph : networkx MultiGraph An undirected graph class that can store multiedges.
# series : time series of current stone's position
# step : get position tuple use step number of this node in series

# add a tuple as node in an undirected graph and edges 

def add(halfgraph, series, step):
    

    tok  = series[step]
    halfgraph.add_node(tok)
    
    for t in get_neighbor(tok):
        if t in halfgraph.node:
            halfgraph.add_edge(tok, t)

def get_neighbor(tok):
    xx, yy = tok
    return [(xx+1,yy),(xx-1,yy),(xx,yy+1),(xx,yy-1)]    
    


class GSeries:
    
    def __init__(self, GClass = networkx.MultiGraph):
        
        # maybe this is in Ring
        # game
        #
        
        self.seq
        self.G = GClass()

        self.i = 0
        
    def __iter__(self):
        return self
        
    def next(self):
        if self.i >= len(self.seq):
            raise StopIteration
        else:
            add (self.G, self.seq,self.i)
            self.i += 1

    def __getter__(self,name):
        if name == 'game' and False:
            return getattr(self.ring, name)
        return getattr(self, name)
        


class Ring:
    # let sigma^4 == 1, then put a time series in 4 thread
    # 

    allgame = init()

    def __init__(self, gameid):

        self.game = Ring.allgame[gameid]

        self.W, self.B = GSeries(), GSeries()
        self.W.ring = self.B.ring = self
        def fff(game,color):
            return [(ord(i[2]) ,ord(i[3])) for i in game if i.startswith(color)]
        self.W.seq = self.W.gw = fff(self.game,"W")
        self.B.seq = self.B.gb = fff(self.game,"B")

        self.dict = {0:self.B,1:self.W}
        self.step = 0


        # dataframe , each row relate to a  move and the context at the moment
        # stepnum : int step number of a stone
        # j1, j2, j3, j4 : when a stone linked or join with another block ,set j =1
        #                  if another block's color is opposite set j=-1 ,
        #                  j1, j2, j3 ,j4 refer to   four diffrent direction
        #irrational : when a join produce a block shape strange( based on statistic of a set of games) its irrational ,a machine learnig target
        #impossible : when a join make a block has only one branch ,set impossible -1
        #             when after a join with impossible -2, its possible to get impossible -1 with a  single move
        #

        #alpha : count of independent block
        #top, bottom  : inside alpha, top with most branch, bottom with least branch
        #tokhead, tokend : see self.tokendf
        self.df = pd.DataFrame(columns = ["stepnum", "j1", "j2", "j3", "j4","brach","irration", "impossible","alpha", "top", "bottom"])
        #self.recentdf , stack (5) step in a row
        #self.tokendf,  stack steps which match a 'regular expression'
                                                                            
                                                                            
    def __iter__(this):
        return this
    def next(this):
        if  this.step >= len(self.game):
            raise StopIteration
        else:
            c = this.step % 2
            this.dict[c].next()
            this.step += 1

                              
#---------------       analysis  graph's properties use pandas dataframe      ----------------------------


R = Ring(177777)
for n in R:
    print len(R.W.G.node)

