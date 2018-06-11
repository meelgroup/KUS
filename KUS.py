import argparse
import pickle
import random
import time

import numpy as np
import pydot


class Node():
    def __init__(self,label=None,children=[],decision=None):
        self.label = label
        self.children = children
        self.models = 1
        self.decisionat = decision

class Sampler():
    '''Main class which defines parsing, graph drawing, counting and sampling functions'''
    def __init__(self):
        self.totalvariables = None
        self.treenodes = []
        self.useList = False
        self.graph = None
        self.samples = None
        self.drawnnodes = {}
    
    def drawtree(self,root):
        '''Recursively draws tree for the d-DNNF'''
        rootnode = pydot.Node(str(root.label)+" "+str(root.models))
        self.graph.add_node(rootnode)
        self.drawnnodes[root.label] = rootnode
        for ch in root.children:
            if ch.label not in self.drawnnodes:
                node = self.drawtree(ch)
                self.graph.add_edge(pydot.Edge(rootnode,node))
            else:
                self.graph.add_edge(pydot.Edge(rootnode,self.drawnnodes[ch.label]))
        return rootnode

    def parse(self,inputnnffile):
        '''Parses the d-DNNF tree to a tree like object'''
        with open(inputnnffile) as f:
            treetext = f.readlines()
        nodelen = 0
        for node in treetext:
            node = node.split()
            if node[0] == 'c':
                continue
            elif node[0] == 'nnf':
                self.totalvariables = int(node[3])
            elif node[0] == 'L':
                self.treenodes.append(Node(label=int(node[1])))
                nodelen+=1
            elif node[0] == 'A':
                if node[1] == '0':
                    self.treenodes.append(Node(label='T ' + str(nodelen)))
                else:
                    andnode = Node(label='A '+ str(nodelen))
                    andnode.children = list(map(lambda x: self.treenodes[int(x)],node[2:]))
                    self.treenodes.append(andnode)
                nodelen+=1
            elif node[0] == 'O':
                if node[2] == '0':
                    self.treenodes.append(Node(label='F '+ str(nodelen)))
                else:
                    ornode = Node(label='O '+ str(nodelen),decision = int(node[1]))
                    ornode.children = list(map(lambda x: self.treenodes[int(x)],node[3:]))
                    self.treenodes.append(ornode)
                nodelen+=1

    def counting(self,root):
        '''Computes Model Counts'''
        if(str(root.label)[0] == 'A'):
            root.models = 1
            finalbitvec = set()
            for ch in root.children:
                finalbitvec.update(self.counting(ch)) 
                root.models = root.models * ch.models    
            return finalbitvec
        elif(str(root.label)[0] == 'O'):
            bitvecs = []
            bitvecs.append(self.counting(root.children[0]))
            bitvecs.append(self.counting(root.children[1]))
            # set difference to find out uncommon variables
            bitvec2_1 = bitvecs[1] - bitvecs[0]
            bitvec1_2 = bitvecs[0] - bitvecs[1]
            if (not root.children[0].models):
                model1 = 0
            else:
                # accomodating cylinders from uncommon variables in model counts
                model1 = root.children[0].models * (2 ** len(bitvec2_1))
            if (not root.children[1].models):
                model2 = 0
            else:
                model2 = root.children[1].models * (2 ** len(bitvec1_2))
            root.models = model1 + model2
            root.children[0].models = model1
            root.children[1].models = model2
            return bitvecs[0].union(bitvec2_1)
        else:
            bitvec = set()
            try:
                int(root.label)
                bitvec.add(abs(root.label))
                root.models = 1
            except:
                if (str(root.label)[0] == 'F'):
                    root.models = 0
                elif (str(root.label)[0] == 'T'):                    
                    root.models = 1
            return bitvec 

    def getsamples(self,root,indices):
        '''Generates Uniform Independent Samples'''
        if(not indices.shape[0]):
            return
        if(str(root.label)[0] == 'O'):
            z0 = root.children[0].models
            z1 = root.children[1].models
            p = (1.0*z0)/(z0+z1)
            tosses = np.random.binomial(1, p, indices.shape[0])
            self.getsamples(root.children[0],np.array(indices[np.where(tosses==1)[0]]))
            self.getsamples(root.children[1],np.array(indices[np.where(tosses==0)[0]]))
        elif(str(root.label)[0] == 'A'):
            for ch in root.children:
                self.getsamples(ch,indices)
        else:
            try:
                int(root.label)
                for index in indices:
                    if (self.useList):
                        self.samples[index][abs(root.label)-1] = root.label
                    else:
                        self.samples[index] += str(root.label)+' '
            except:
                pass

def random_assignment(totalVars, solution, useList):
    '''Takes total number of variables and a partial assignment
    to return a complete assignment'''
    literals = set()
    if useList:
        solutionstr = ''
        for literal in solution:
            if literal:
                literals.add(abs(int(literal)))
        for i in range(1,totalVars+1):
            if i not in literals:
                solutionstr += str(((random.randint(0,1)*2)-1)*i)+" "
            else:
                solutionstr += str(int(solution[i-1]))+" "
    else:
        solutionstr = solution
        for x in solution.split():
            literals.add(abs(int(x)))
        for i in range(1,totalVars+1):
            if i not in literals:
                solutionstr += str(((random.randint(0,1)*2)-1)*i)+" "
    return solutionstr

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputfile", type=str, default="samples.txt", help="output file for samples", dest='outputfile')
    parser.add_argument("--drawtree", type=int, default = 0, help="draw nnf tree", dest='draw')
    parser.add_argument("--samples", type=int, default = 10, help="number of samples", dest='samples')
    parser.add_argument("--useList", type=int, default = 0, help="use list for storing samples internally instead of strings", dest="useList")
    parser.add_argument("--randAssign", type=int, default = 1, help="randomly assign unassigned variables in a model with partial assignments", dest="randAssign")
    parser.add_argument("--savePickle", type=str, default=None, help="specify name to save Pickle of count annotated dDNNF for incremental sampling", dest="savePickle")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dDNNF', type=str, help="specify dDNNF file", dest="dDNNF")
    group.add_argument('--countPickle', type=str, help="specify Pickle of count annotated dDNNF", dest="countPickle")
    args = parser.parse_args()
    draw = args.draw
    totalsamples = args.samples
    useListInt = args.useList
    randAssignInt = args.randAssign
    dDNNF = False
    countPickle = False
    if args.dDNNF:
        dDNNF = args.dDNNF
    else:
        countPickle = args.countPickle
    savePickle = args.savePickle
    useList = False
    if (useListInt == 1):
        useList = True
    randAssign = False
    if (randAssignInt == 1):
        randAssign = True
    sampler = Sampler()
    sampler.useList = useList
    if dDNNF:
        start = time.time()
        sampler.parse(dDNNF)
        print("The time taken to parse the nnf text:", time.time() - start)
        start = time.time()
        bitvec = sampler.counting(sampler.treenodes[-1])
        sampler.treenodes[-1].models = sampler.treenodes[-1].models * (2**(sampler.totalvariables - len(bitvec)))
        print("The time taken for Model Counting:", time.time()-start)
        timepickle = time.time()
        if savePickle:
            fp = open(savePickle, "wb")
            pickle.dump((sampler.totalvariables,sampler.treenodes), fp)
            fp.close()
            print("Time taken to save the count annotated dDNNF pickle:", time.time() - timepickle)
    else:
        timepickle = time.time()
        fp = open(countPickle, "rb")
        (sampler.totalvariables,sampler.treenodes) = pickle.load(fp)
        fp.close()
        print("The time taken to read the pickle:", time.time() - timepickle)
        if savePickle:
            fp = open(savePickle, "wb")
            pickle.dump((sampler.totalvariables,sampler.treenodes), fp)
            fp.close()
            print("Time taken to save the count annotated dDNNF pickle:", time.time() - timepickle)

    print("Model Count:",sampler.treenodes[-1].models)
    if draw:
        sampler.graph = pydot.Dot(graph_type='digraph')
        sampler.drawtree(sampler.treenodes[-1])
        sampler.graph.write_png('d-DNNFgraph.png')
    if (useList):
        sampler.samples = np.zeros((totalsamples,sampler.totalvariables))
    else:
        sampler.samples = []
        for i in range(totalsamples):
            sampler.samples.append('')
    start = time.time()
    sampler.getsamples(sampler.treenodes[-1],np.arange(0,totalsamples))
    print("The time taken by sampling:", time.time()-start)
    if randAssign:
        sampler.samples = list(map(lambda x: random_assignment(sampler.totalvariables, x, sampler.useList), sampler.samples))
    f = open(args.outputfile,"w+")
    for i in range(totalsamples):
        f.write(str(i+1) + ", " + sampler.samples[i] + "\n")
    f.close()
    print("Samples saved to", args.outputfile)

if __name__== "__main__":
    main()
