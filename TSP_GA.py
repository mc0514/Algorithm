
import argparse
import string
import math
import operator
from random import *
from bisect import *
from time import clock


number_of_states = 1000  # must be even number
p_c = 1  # JIAOPEIGAILV,no use for now
p_m = 0.4
times = 100000
M = 10**7
to_stop = 100

# seed(0)

class TSP:
    def __init__(self, filename, outname):
        self.count = number_of_states
        """A class to solve the problem"""
        # construct
        self.N, self.distances = TSP.cal_dist_between(filename)
        self.states = self.generate_states()
        self.optimize_state = []
        self.optimize_cost = float('inf')
        self.costs = [0] * number_of_states
        self.adapts = [0] * number_of_states
        self.result_cost = float('inf')
        self.result_state = []
        for i in range(5):
            # print('haha')
            seed(clock())
            self.genetic()
            if self.result_cost > self.optimize_cost:
                self.result_cost = self.optimize_cost
                self.result_state = self.optimize_state
            self.optimize_cost = float('inf')
            self.states = self.generate_states()
        self.write_out = open(outname, 'w')
        self.print_state()
        self.write_out.close()


    def generate_states(self):
        """Genereate the first states"""
        states = []
        for _ in range(number_of_states):
            tmp = [x for x in range(self.N)]
            shuffle(tmp)
            states.append(tmp)
        #print states
        return states

    def adapt_value(self, cost, opti_cost):
        """Calculate adapt value, by using non-linear boost method"""
        return 1/(cost - opti_cost + 0.15)

    def genetic(self):
        """Main solving function"""
        opt_costs = [i for i in range(to_stop)]
        for t in range(times):
            # calculate cost and adapt
            # calculate cost and adapt
            for i in range(number_of_states):
                self.costs[i] = self.cost(self.states[i])
            idx, tmp_cost = min(enumerate(self.costs), key=operator.itemgetter(1))
            if tmp_cost < self.optimize_cost:
                self.optimize_cost = tmp_cost
                self.optimize_state = self.states[idx]
            for i in range(number_of_states):
                self.adapts[i] = self.adapt_value(self.costs[i], self.optimize_cost)
                if i > 0:
                    self.adapts[i] += self.adapts[i-1]

            if opt_costs[t % to_stop] == self.optimize_cost:
                break
            opt_costs[t % to_stop] = self.optimize_cost

            # binary search
            new_state = []
            for i in range(number_of_states):
                new_state.append(self.states[bisect_left(self.adapts, uniform(0, self.adapts[-1]))])
            to_be_mating = []
            self.states = []
            # mate
            for state in new_state:
                to_be_mating.append(state)
                if len(to_be_mating) == 2:
                    self.mating(to_be_mating)
                    to_be_mating = []
            # if t%(to_stop // 2 ) == 0:
            #     self.variation(0.8)
            # else:
            self.variation()
            # if t % 50 == 0:
            #     self.print_state_screen(self.optimize_state, self.optimize_cost)
            #     print(self.count)
            # self.count = number_of_states

    def mating(self, fathers):
        """ JIYUWEIZHIDEJIAOPEI"""
        son1 = fathers[1][:]
        son2 = fathers[0][:]
        if not fathers[1].__eq__(fathers[0]):
            self.count -= 2
            # posis = [2, 3, 5, 7, 9]
            posis = set(sample(range(self.N), self.N//2))
            f1_rest = {fathers[0][i] for i in range(self.N) if i not in posis}
            f2_rest = {fathers[1][i] for i in range(self.N) if i not in posis}
            f1 = [x for x in fathers[0] if x in f2_rest][::-1]
            f2 = [x for x in fathers[1] if x in f1_rest][::-1]
            son1 = fathers[1][:]
            son2 = fathers[0][:]
            for j in range(self.N):
                if j not in posis:
                    son1[j] = f1.pop()
                    son2[j] = f2.pop()
        self.states.append(son1)
        self.states.append(son2)

    def variation(self, p = p_m):
        """JIYUCIXUDEBIANYI"""
        for i in range(number_of_states):
            if random() < p:
                posis = sample(range(self.N), self.N//2)
                tmp = self.states[i][posis[0]]
                self.states[i][posis[0]] = self.states[i][posis[1]]
                self.states[i][posis[1]] = tmp

    def cost(self, state):
        """calculate the cost of a state"""
        cost = 0
        for i in range(1, self.N+1):
            cost += self.distance(state[i % self.N], state[(i-1)])
        return cost

    def distance(self, i, j):
        """generate num_of_states of first state"""
        if i < j:
            return self.distance(j, i)
        return self.distances[i % self.N][j % self.N]

    def print_state(self):
        for i in range(self.N):
            self.write_out.write(string.ascii_uppercase[self.result_state[i]]+' ')

    def print_state_screen(self,state, cost ):
        for i in range(self.N):
            print(string.ascii_uppercase[state[i]])
            #print(string.ascii_uppercase[state[i]], end = ' ')
        print(cost)
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
    #tsp = TSP(parser.parse_args().data_dir, parser.parse_args().out_dir)
    tsp=TSP('data.txt','out.txt')
    tsp.print_state_screen(tsp.result_state, tsp.result_cost)
