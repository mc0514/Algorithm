import argparse
import string
import math
from random import shuffle
from random import randint
from random import random

alpha = 0.92
L = 100
T_max = 280


class TSP:
    """A class to solve the problem"""
    def __init__(self, filename, outname):
        # construct
        self.N, self.distances = TSP.cal_dist_between(filename)
        self.state = self.gen_first_state()
        self.temp = T_max
        self.k = 0
        # calculate the cost of the first state
        self.cost = 0
        for i in range(1,self.N+1):
            self.cost += self.distance(self.state[i%self.N], self.state[(i-1)])
        self.write_out = open(outname,'w')
        self.solve()
        self.write_out.close()

    def solve(self):
        """solve the problem"""
        while True:
            this_state = self.state[:]
            for never_used in range(L*self.N):
                u = randint(0, self.N-3)
                v = randint(u+3, self.N)
                cost_delta = self.cost_delta(u, v)
                if cost_delta > 0:
                    if random() > math.exp(-cost_delta/self.temp):
                        # not accept
                        continue
                # else: change state
                self.cost += cost_delta
                self.state[u+1: v] = self.state[u+1:v][::-1]
            self.temp *= alpha
            self.print_state()
            if this_state == self.state:
                # if there's no change, break
                break

    def cost_delta(self, u, v):
        v %= self.N
        return self.distance(self.state[v - 1], self.state[u]) + self.distance(self.state[v], self.state[u+1]) - \
               self.distance(self.state[u+1],self.state[u]) - self.distance(self.state[v],self.state[v-1])

    def gen_first_state(self):
        tmp = [i for i in range(1, self.N)]
        shuffle(tmp)
        return [0] + tmp

    def distance(self, i, j):
        if i < j:
            return self.distance(j,i)
        return self.distances[i % self.N][j % self.N]

    def print_state(self):
        for i in range(self.N):
            self.write_out.write(string.ascii_uppercase[self.state[i]]+' ')
        self.write_out.write(str(self.cost)+'\n')


    @staticmethod
    def cal_dist_between(filename):       
        file = open(filename, 'r')
        #N = int(file.readline())
        arrayLines=file.readlines()
        N=int(len(arrayLines))
        #print N
        position=[]
        
        #index=1
        for line in arrayLines:
            dataset=[]*2
            print line
            each = line.split('\t')
            #print each[0]
            dataset.append(float(each[0]))
            dataset.append(float(each[1]))
            #print dataset
            position.append(dataset)
            #print index
            #index+=1
        #print position
        distances = [[] for i in range(N)]                    
        for i in range(N):
            for j in range(i):
                distances[i].append(math.sqrt((position[i][0] - position[j][0]) ** 2 + (position[i][1] - position[j][1]) ** 2))
        file.close()
        print distances
        return N, distances   

if __name__ == '__main__':
    # args
    #parser = argparse.ArgumentParser("Read in and out put")
    #parser.add_argument('data_dir')
    #parser.add_argument('out_dir')
    # solve the problem
    #tsp = TSP(parser.parse_args().data_dir,parser.parse_args().out_dir)
    tsp = TSP('data.txt','out.txt')
    
