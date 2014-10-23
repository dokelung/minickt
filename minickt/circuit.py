import copy
import matplotlib.pyplot as plt
import networkx as nx
from gate import *

class CircuitConstructer(object):

    def __init__(self,circuit,ckt_info):

        self.circuit = circuit

        # followings are the must-give info
        self.circuit.circuit_name = ckt_info['ckt_name']
        self.outputs = ckt_info['output']
        self.inputs = ckt_info['input']
        self.wires = ckt_info['wire']
        self.ands = ckt_info['and']
        self.ors = ckt_info['or']
        self.xors = ckt_info['xor']
        self.nors = ckt_info['nor']
        self.nands = ckt_info['nand']
        self.xnors = ckt_info['xnor']
        self.bufs = ckt_info['buf']
        self.nots = ckt_info['not']
        self.const0 = ckt_info['const0']
        self.const1 = ckt_info['const1']

    # main parse function
    def construct(self):
        self.createGates()
        self.connectGates()
        self.relatePO2RealGate()

    # sub parse function
    def createGates(self):
        
        for name in self.inputs:
            gate = PIGate(len(self.circuit.gates))
            gate.setName(name)
            self.circuit.addGate(gate)

        for name in self.outputs:
            gate = POGate(len(self.circuit.gates))
            gate.setName(name)
            self.circuit.addGate(gate)

        self.circuit.po_end_index = len(self.circuit.gates)
            
        for name in self.ands:
            gate = AndGate(len(self.circuit.gates))
            gate.setName(name)
            self.circuit.addGate(gate)
            
        for name in self.ors:
            gate = OrGate(len(self.circuit.gates))
            gate.setName(name)
            self.circuit.addGate(gate)
            
        for name in self.xors:
            gate = XorGate(len(self.circuit.gates))
            gate.setName(name)
            self.circuit.addGate(gate)
            
        for name in self.nors:
            gate = NorGate(len(self.circuit.gates))
            gate.setName(name)
            self.circuit.addGate(gate)
            
        for name in self.nands:
            gate = NandGate(len(self.circuit.gates))
            gate.setName(name)
            self.circuit.addGate(gate)

        for name in self.xnors:
            gate = XnorGate(len(self.circuit.gates))
            gate.setName(name)
            self.circuit.addGate(gate)
        
        for name in self.bufs:
            gate = BufGate(len(self.circuit.gates))
            gate.setName(name)
            self.circuit.addGate(gate)
            
        for name in self.nots:
            gate = NotGate(len(self.circuit.gates))
            gate.setName(name)
            self.circuit.addGate(gate)

        if self.const0:
            gate = ConstZeroGate(len(self.circuit.gates))
            gate.setName('const_zero')
            self.circuit.addGate(gate)

        if self.const1:
            gate = ConstOneGate(len(self.circuit.gates))
            gate.setName('const_one')
            self.circuit.addGate(gate)

    def connectGates(self):
        for name in self.ands:
            gate = self.circuit.getGateFromName(name)
            for fanin_name in self.ands[name]:
                fanin_gate = self.circuit.getGateFromName(fanin_name)
                gate.addFanIn(fanin_gate)
                fanin_gate.addFanOut(gate)
        for name in self.ors:
            gate = self.circuit.getGateFromName(name)
            for fanin_name in self.ors[name]:
                fanin_gate = self.circuit.getGateFromName(fanin_name)
                gate.addFanIn(fanin_gate)
                fanin_gate.addFanOut(gate)
        for name in self.xors:
            gate = self.circuit.getGateFromName(name)
            for fanin_name in self.xors[name]:
                fanin_gate = self.circuit.getGateFromName(fanin_name)
                gate.addFanIn(fanin_gate)
                fanin_gate.addFanOut(gate)
        for name in self.nors:
            gate = self.circuit.getGateFromName(name)
            for fanin_name in self.nors[name]:
                fanin_gate = self.circuit.getGateFromName(fanin_name)
                gate.addFanIn(fanin_gate)
                fanin_gate.addFanOut(gate)
        for name in self.nands:
            gate = self.circuit.getGateFromName(name)
            for fanin_name in self.nands[name]:
                fanin_gate = self.circuit.getGateFromName(fanin_name)
                gate.addFanIn(fanin_gate)
                fanin_gate.addFanOut(gate)
        for name in self.xnors:
            gate = self.circuit.getGateFromName(name)
            for fanin_name in self.xnors[name]:
                fanin_gate = self.circuit.getGateFromName(fanin_name)
                gate.addFanIn(fanin_gate)
                fanin_gate.addFanOut(gate)
        for name in self.bufs:
            gate = self.circuit.getGateFromName(name)
            for fanin_name in self.bufs[name]:
                fanin_gate = self.circuit.getGateFromName(fanin_name)
                gate.addFanIn(fanin_gate)
                fanin_gate.addFanOut(gate)
        for name in self.nots:
            gate = self.circuit.getGateFromName(name)
            for fanin_name in self.nots[name]:
                fanin_gate = self.circuit.getGateFromName(fanin_name)
                gate.addFanIn(fanin_gate)
                fanin_gate.addFanOut(gate)

    def relatePO2RealGate(self):

        for po_gate in self.circuit.getPOGates():
            po_id = po_gate.getId()
            for gate in self.circuit.gates[self.circuit.po_end_index:]:
                if gate.getName()==po_gate.getName():
                    gate.setTypeStr('PO-'+gate.getTypeStr())
                    self.circuit.gates[po_id] = gate
                    self.circuit.gates[po_id].relateToPo()


class Circuit:

    def __init__(self):

        self.circuit_name = None
        self.gates = []

        self.name2id_dic = {}
        self.id2name_dic = {}
        self.po_end_index = None

        self.num_pi = 0
        self.num_po = 0
        self.num_and = 0
        self.num_or = 0
        self.num_xor = 0
        self.num_nor = 0
        self.num_nand = 0
        self.num_xnor = 0
        self.num_buf = 0
        self.num_not = 0
        self.num_const0 = 0
        self.num_const1 = 0

        self.topological_orderd_gates = None

    def __str__(self):
        return '{0}'.format(self.circuit_name)

    # input
    def constructCkt(self,ckt_info):
        ckt_constructer = CircuitConstructer(self,ckt_info)
        ckt_constructer.construct()
        self.computeGateNum()

    def computeGateNum(self):
        for index, gate in enumerate(self.gates):
            if index < self.po_end_index:
                if isinstance(gate,PIGate):
                    self.num_pi += 1
                else:
                    self.num_po += 1
            else:
                if isinstance(gate,AndGate):
                    self.num_and += 1
                elif isinstance(gate,OrGate):
                    self.num_or += 1
                elif isinstance(gate,XorGate):
                    self.num_xor += 1
                elif isinstance(gate,NorGate):
                    self.num_nor += 1
                elif isinstance(gate,NandGate):
                    self.num_nand += 1
                elif isinstance(gate,XnorGate):
                    self.num_xnor += 1
                elif isinstance(gate,BufGate):
                    self.num_buf += 1
                elif isinstance(gate,NotGate):
                    self.num_not += 1
                elif isinstance(gate,ConstZeroGate):
                    self.num_const0 += 1
                elif isinstance(gate,ConstOneGate):
                    self.num_const1 += 1

    # setter
    def setName(self,name):
        self.circuit_name = name

    def idTranslate(self,num):
        for gate in self.getGatesOnce():
            gate.idTranslate(num)

    def gateNamesTranslate(self,append_str):
        for gate in self.getGatesOnce():
            gate.nameTranslate(append_str)

    # getter(gate num)
    def getPiNum(self):
        return self.num_pi

    def getPoNum(self):
        return self.num_po

    def getAndNum(self):
        return self.num_and

    def getOrNum(self):
        return self.num_or

    def getXorNum(self):
        return self.num_xor

    def getNorNum(self):
        return self.num_nor

    def getNandNum(self):
        return self.num_nand

    def getXnorNum(self):
        return self.num_xnor

    def getBufNum(self):
        return self.num_buf

    def getNotNum(self):
        return self.num_not

    def getConstZeroNum(self):
        return self.num_const0

    def getConstOneNum(self):
        return self.num_const1

    def getGateCount(self):
        gate_count = 0
        for gate in self.gates[:self.po_end_index]:
            if isinstance(gate,PIGate):
                gate_count += 1
        gate_count += len(self.gates[self.po_end_index:])
        return gate_count

    # getter(circuit properties)
    def getAllPOProbability(self):
        return [PO.getProbability() for PO in self.getPOGates()]

    def getPOProbability(self,index):
        return self.getPOGates()[index].getProbability()

    def getPhaseConsistentRate(self):
        num_of_not_consistent = 0
        for gate in self.gates:
            for index, fanout in enumerate(gate.getFanOuts()):
                if index==0:
                    consistent = isinstance(fanout,NotGate)
                else:
                    if not consistent==isinstance(fanout,NotGate):
                        num_of_not_consistent += 1
                        break
        return float(num_of_not_consistent)/float(self.getGateCount()) 

    def getAvgFanOutNum(self):
        total_fanout_num = 0
        for gate in self.gates[:self.po_end_index]:
            if isinstance(gate,PIGate):
                total_fanout_num += gate.getFanOutNum()
        for gate in self.gates[self.po_end_index:]:
            total_fanout_num += gate.getFanOutNum()
        return float(total_fanout_num)/float(self.getGateCount())
    
    def getAvgFanInNum(self):
        total_fanin_num = 0
        for gate in self.gates[self.po_end_index:]:
            total_fanin_num += gate.getFanInNum()
        return float(total_fanin_num)/float(self.getGateCount())

    def getMaxFanOutNum(self):
        max_fanout_num = 0
        for gate in self.gates[:self.po_end_index]:
            if isinstance(gate,PIGate):
                if gate.getFanOutNum() > max_fanout_num:
                    max_fanout_num = gate.getFanOutNum()
        for gate in self.gates[self.po_end_index:]:
            if gate.getFanOutNum() > max_fanout_num:
                max_fanout_num = gate.getFanOutNum()
        return max_fanout_num

    def getMaxFanInNum(self):
        max_fanin_num = 0
        for gate in self.gates[:self.po_end_index]:
            if isinstance(gate,PIGate):
                if gate.getFanInNum() > max_fanin_num:
                    max_fanin_num = gate.getFanInNum()
        for gate in self.gates[self.po_end_index:]:
            if gate.getFanInNum() > max_fanin_num:
                max_fanin_num = gate.getFanInNum()
        return max_fanin_num

    def getFanOutNumVariance(self):
        avg_fanout_num = self.getAvgFanOutNum()
        gates = [gate for gate in self.gates[:self.po_end_index] if isinstance(gate,PIGate)]
        gates.extend(self.gates[self.po_end_index:])
        sigma_result = 0
        for gate in gates:
            sigma_result += (gate.getFanOutNum()-avg_fanout_num)**2
        return float(sigma_result)/float(self.getGateCount())

    def getFanInNumVariance(self):
        avg_fanin_num = self.getAvgFanInNum()
        gates = [gate for gate in self.gates[:self.po_end_index] if isinstance(gate,PIGate)]
        gates.extend(self.gates[self.po_end_index:])
        sigma_result = 0
        for gate in gates:
            sigma_result += (gate.getFanInNum()-avg_fanin_num)**2
        return float(sigma_result)/float(self.getGateCount())

    def getMaxFanInDepthDiff(self):
        max_fanin_depth_diff = 0
        for gate in self.gates[self.po_end_index:]:
            if isinstance(gate,ConstOneGate) or isinstance(gate,ConstZeroGate):
                continue
            max_fanin_depth = max([fanin.getDepth() for fanin in gate.getFanIns()])
            min_fanin_depth = min([fanin.getDepth() for fanin in gate.getFanIns()])
            depth_diff = max_fanin_depth - min_fanin_depth
            if depth_diff > max_fanin_depth_diff:
                max_fanin_depth_diff = depth_diff
        return max_fanin_depth_diff

    def getAvgFanInDepthDiff(self):
        total_fanin_depth_diff = 0
        for gate in self.gates[self.po_end_index:]:
            if isinstance(gate,ConstOneGate) or isinstance(gate,ConstZeroGate):
                continue
            max_fanin_depth = max([fanin.getDepth() for fanin in gate.getFanIns()])
            min_fanin_depth = min([fanin.getDepth() for fanin in gate.getFanIns()])
            depth_diff = max_fanin_depth - min_fanin_depth
            total_fanin_depth_diff += depth_diff
        return float(total_fanin_depth_diff)/float(self.getGateCount())

    # getter(gate/id)
    def getGates(self):
        return self.gates

    def getGatesOnce(self):
        return self.getPIGates() + self.gates[self.po_end_index:]

    def getPIGates(self):
        return [gate for gate in self.gates[:self.po_end_index] if isinstance(gate,PIGate)]

    def getAndGates(self):
        return [gate for gate in self.gates[self.po_end_index:] if isinstance(gate,AndGate)]

    def getOrGates(self):
        return [gate for gate in self.gates[self.po_end_index:] if isinstance(gate,OrGate)]

    def getXorGates(self):
        return [gate for gate in self.gates[self.po_end_index:] if isinstance(gate,XorGate)]

    def getNandGates(self):
        return [gate for gate in self.gates[self.po_end_index:] if isinstance(gate,NandGate)]

    def getNorGates(self):
        return [gate for gate in self.gates[self.po_end_index:] if isinstance(gate,NorGate)]

    def getXnorGates(self):
        return [gate for gate in self.gates[self.po_end_index:] if isinstance(gate,XnorGate)]

    def getBufGates(self):
        return [gate for gate in self.gates[self.po_end_index:] if isinstance(gate,BufGate)]

    def getNotGates(self):
        return [gate for gate in self.gates[self.po_end_index:] if isinstance(gate,NotGate)]

    def getConstZeroGates(self):
        return [gate for gate in self.gates[self.po_end_index:] if isinstance(gate,ConstZeroGate)]

    def getConstOneGates(self):
        return [gate for gate in self.gates[self.po_end_index:] if isinstance(gate,ConstOneGate)]

    def getIdFromName(self,name):
        return self.name2id_dic[name]

    def getGateFromId(self,id):
        return self.gates[id]

    def getGateFromName(self,name):
        return self.getGateFromId(self.name2id_dic[name])

    def getPOGates(self):
        po_gates = []
        for gate in self.gates[:self.po_end_index]:
            if gate.isPoGate():
                po_gates.append(gate)
        return po_gates

    def getGatesInTopologicalOrder(self,reverse=False):
        if self.topological_orderd_gates:
            return self.topological_orderd_gates
        else:
            self.downGateFlag()
            gates = []
            tmp_gates = self.gates[:self.getPiNum()]+self.getConstOneGates()[:]+self.getConstZeroGates()[:]
            #if self.getConstZeroNum==1:
            #    tmp_gates.append(self.gates[-2])
            #if self.getConstOneNum==1:
            #    tmp_gates.append(self.gates[-1])
            for gate in tmp_gates:
                gate.upFlag()
            while tmp_gates:
                gate = tmp_gates.pop(0)
                for fanout in gate.getFanOuts():
                    if fanout.isFlagUp():
                        continue
                    if all([fanin.isFlagUp() for fanin in fanout.getFanIns()]):
                        tmp_gates.append(fanout)
                        fanout.upFlag()
                gates.append(gate)
            self.topological_orderd_gates = gates if not reverse else gates.reverse()
            return self.topological_orderd_gates

    # construct
    def addGate(self,gate):
        self.gates.append(gate)
        self.registerGate(gate)

    def registerGate(self,gate):
        self.name2id_dic[gate.getName()] = gate.getId()
        self.id2name_dic[gate.getId()] = gate.getName()

    # evaluate
    def evaluateCkt(self):
        for gate in self.getGatesInTopologicalOrder():
            gate.eval()

    def setPIValueZero(self):
        for pi in self.gates[:self.po_end_index]:
            if isinstance(pi,PIGate):
                pi.setValue(False)

    def setPIValueOne(self):
        for pi in self.gates[:self.po_end_index]:
            if isinstance(pi,PIGate):
                pi.setValue(True)

    def resetAllGates(self):
        for gate in self.gates:
            gate.reset()

    # cone and subckt
    def getConeCircuit(self,gate):
        assert gate in self.gates
        ckt = Circuit()
        self.traverseCone(gate)
        oldid2newid_dic = {}
        newid2oldid_dic = {}

        for id, gate in enumerate(self.gates):
            if gate.isFlagUp():
                oldid2newid_dic[id] = len(ckt.gates)
                newid2oldid_dic[len(ckt.gates)] = id
                copy_gate = gate.getCopy(len(ckt.gates))
                copy_gate.setName(gate.getName())
                ckt.addGate(copy_gate)

        for gate in self.gates[self.po_end_index:]:
            if gate.isFlagUp():
                #print gate, 'setting fanin and fanout ...'
                #print '\t fanins:', gate.getFanIns()
                for fanin in gate.getFanIns():
                    #print '\t fanin:', fanin, 'check flag ...'
                    if fanin.isFlagUp():
                        #print '\t\t fanin:', fanin, 'is flag up !'
                        new_fanin = ckt.getGateFromId(oldid2newid_dic[fanin.getId()])
                        new_gate = ckt.getGateFromId(oldid2newid_dic[gate.getId()])
                        new_gate.addFanIn(new_fanin)
                        new_fanin.addFanOut(new_gate)
    
        ckt.po_end_index = self.po_end_index

        for gate in ckt.gates:
            if gate.isPoGate():
                #print gate, 'is a po gate, its id:', gate.getId(),'its old id:',newid2oldid_dic[gate.getId()], 'cp with:', self.po_end_index
                if newid2oldid_dic[gate.getId()] < self.po_end_index:
                    ckt.po_end_index = gate.getId()

        if ckt.po_end_index==self.po_end_index:
            for gate in ckt.gates:
                if isinstance(gate,PIGate):
                    ckt.po_end_index = gate.getId()

        ckt.po_end_index += 1

        #print 'po end index of cone:', ckt.po_end_index

        for po_gate in ckt.getPOGates():
            po_id = po_gate.getId()
            for gate in ckt.gates[ckt.po_end_index:]:
                if gate.getName()==po_gate.getName():
                    ckt.gates[po_id] = gate

        ckt.computeGateNum()
        
        return ckt

    def traverseCone(self,gate):
        assert gate in self.gates
        self.downGateFlag()
        
        gates = [gate]
        while(gates):
            gate = gates.pop()
            #print 'now go to', gate, 'remain num in gates', len(gates)
            if gate.isFlagUp():
                continue
            gate.upFlag()
            for fanin_gate in gate.getFanIns():
                gates.append(fanin_gate)

    def isConeClose(self,gate):
        assert gate in self.gates
        #print 'cone',gate
        self.traverseCone(gate)
        for g in self.getPIGates()+self.getGates()[self.po_end_index:]:
            if g.isFlagUp() and not g==gate:
                #print '...check', g
                for fo in g.getFanOuts():
                    #print '......',fo
                    if not fo.isFlagUp():
                        #print 'error------------'
                        #print g, 'has outer fanout', fo
                        return False
        return True

    def getAllCloseCone(self):
        gates = []
        for gate in self.gates[self.po_end_index:]:
            if self.isConeClose(gate):
                gates.append(gate)
        return gates

    def downGateFlag(self):
        for gate in self.gates:
            gate.downFlag()

    # encode
    def encTseitin(self,file_name,option='sat'):
        with open(file_name,'with') as writer:
            print >>writer,'c cnf written by miniCkt'
            for gate in self.getGates()[self.po_end_index:]:
                for cla in gate.encTseitin():
                    for lit in cla:
                        print >>writer,lit,
                    print >>writer,'0'
            if option=='sat':
                for gate in self.getPOGates():
                    print >>writer,gate.getId(True),
                    print >>writer,'0'
            elif option=='unsat':
                for gate in self.getPOGates():
                    print >> writer,-gate.getId(True),
                    print >>writer,'0'
            elif option=='pure':
                pass

    def encReason(self,file_name):
        self.encTseitin(file_name)
        with open(file_name,'a') as writer:
            for gate in self.getAndGates()+self.getNorGates():
                self.resetAllGates()
                gate.setValue(True)
                self.reason()
                for g in self.getGatesInTopologicalOrder():
                    if not g.getValue()==None and g not in gate.getFanIns() and g not in gate.getFanOuts():
                        if g.getValue()==True:
                            print >>writer, -gate.getId(True), g.getId(True), '0'
                        else:
                            print >>writer, -gate.getId(True), -g.getId(True), '0'
            for gate in self.getOrGates()+self.getNandGates():    
                self.resetAllGates()
                gate.setValue(False)
                self.reason()
                for g in self.getGatesInTopologicalOrder():
                    if not g.getValue()==None and g not in gate.getFanIns() and g not in gate.getFanOuts():
                        if g.getValue()==True:
                            print >>writer, gate.getId(True), g.getId(True), '0'
                        else:
                            print >>writer, gate.getId(True), -g.getId(True), '0'


    # reason
    def reason(self):
        todo_gates = []
        for gate in self.getPIGates()+self.gates[self.po_end_index:]:
            #if any([fi.getValue()==None for fi in gate.getFanIns()]) or gate.getValue()==None:
            todo_gates.append(gate)
        check_num = len(todo_gates)
        while True:
            todo_gate_index = []
            for index, gate in enumerate(todo_gates):
                if gate.canReason():
                    #print '--- reason',gate
                    if not gate.reason():
                        return False
                elif gate.canPropagate():
                    #print '--- eval',gate
                    ori_value = gate.getValue()
                    if not ori_value==None and not gate.eval()==ori_value:
                        return False
                    else:
                        gate.eval()
                else:
                    todo_gate_index.append(index)
            temp_gates = []
            for index, gate in enumerate(todo_gates):
                if index in todo_gate_index:
                    temp_gates.append(gate)
            todo_gates = temp_gates
            if len(todo_gates)==check_num:
                break
            else:
                check_num = len(todo_gates)
        return True

    # show
    def showCircuitGraph(self):
        G = nx.DiGraph()
        for gate in self.gates:
            for fanout in gate.getFanOuts():
                G.add_edge(gate,fanout)
        nx.draw(G, node_size=1000, node_color='white')
        plt.show()

    def showGatesRatio(self, ):
        labels = ['PI', 'AND', 'OR', 'XOR', 'XNOR', 'NAND', 'NOR', 'NOT', 'BUF', 'Const0', 'Const1']
        sizes = []
        sizes.append(self.getPiNum())
        sizes.append(self.getAndNum())
        sizes.append(self.getOrNum())
        sizes.append(self.getXorNum())
        sizes.append(self.getXnorNum())
        sizes.append(self.getNandNum())
        sizes.append(self.getNorNum())
        sizes.append(self.getNotNum())
        sizes.append(self.getBufNum())
        sizes.append(self.getConstZeroNum())
        sizes.append(self.getConstOneNum())
        for index, size in enumerate(sizes):
            labels[index] = labels[index] + '[' + str(size) +']'
        rm_index = []
        for index, size in enumerate(sizes):
            if size==0 or float(size)/float(self.getGateCount())<0.05:
                rm_index.append(index)
        labels = [labels[index] for index in range(len(sizes)) if index not in rm_index]
        sizes = [sizes[index] for index in range(len(sizes)) if index not in rm_index]
        explode = []
        for i in range(len(sizes)):
            if sizes[i]==max(sizes):
                explode.append(0.1)
            else:
                explode.append(0)

        plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        plt.show()

    # test
    def testtopo(self,gates):
        self.downGateFlag()
        for gate in gates:
            for fanin in gate.getFanIns():
                if not fanin.isFlagUp():
                    print 'wrong', gate, '=>', fanin, 'is not traversed' 
                    exit()
            gate.upFlag()

    def printFanOutTypes(self):
        for gate in self.gates:
            print gate.getFanOutTypes()