#encoding:utf-8


import random

import re
import sys

class T:
    def __init__(self,gameid):
        self.gameid = gameid
        self.moves = []
        self.move = Move()

    def turn(self, player):
        self.moves.append(player.replay(self.moves, self))

class Move:
    def __init__(self):

        self.pre = ['pp','dp','dd','pd']
        self.pre = readsgf(175853)
        print str(self.pre[:10])+"#################"
        self.pos = ''


def readsgf(gameid):
    with open("/var/www/html/static/sgf/%s.sgf" %gameid) as f:
        ss = f.read()
    moves = re.findall("[W|B]\[..\]", ss)
    return [m[2:4] for m in moves]

def writesgf(T):
    with open("/var/www/html/static/sgf/101.sgf",'w') as f:
        f.write(','.join(T.moves))
#------------------------------------------------------------

class Player:
    def __init__(self,color):
        self.name = 'K'
        self.color = color

    def replay(self, moves,T):
        return self.color + '[%s]' %ML_response(T, moves, self.color)


def ML_response(T, moves, color):

    move = T.move
    if  ask(moves, 'continue') == True:
        dot(moves, move)
    else:

        move.pos = 'tt'
    gen_comment(T, moves)

    return move.pos



def gen_comment(T, moves):

    return 'pass'


def ask (moves, request):

    if request ==     'continue':
        return len(moves) < 100


def next(moves, move, method):

    if method == 'random':
        POSES = 'abcdefghijklmnopqrs'

        i = random.randint(0,18)
        j = random.randint(0,18)
        pos = '%s%s' % (POSES[i],POSES[j])

    elif method == 'predefine':
        
        pos = move.pre[len(moves)]
    else:
        pos = 'pp'

    move.pos = pos

    return pos in moves


def dot(moves,move):
    if len(moves) < 24:
       if next(moves,move, 'predefine'):
           while  next(moves, move, 'random'):
               pass
    else:
       while next(moves, move, "random"):
           pass




Ten = T(20)
p,q = Player('B'), Player('W')
for i in range(50):
    Ten.turn(p)
    Ten.turn(q)
writesgf(Ten)


ret = Ten ,p,q






