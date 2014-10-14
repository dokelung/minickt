from sop import *
import copy
import itertools

class Gate(object):
    
    def __init__(self,id):
        super(Gate, self).__init__()
        self.id = id
        self.fanins = []
        self.fanouts = []
        self.flag = False
        self.ispo = False
        self.value = None
        self.probability = None
        self.depth = None
        self.path_num = None
        self.SOP = None
        self.structure_equal_gates = []
        return self

    def __str__(self):
        return '{0}:{1}'.format(self.type_str,self.getName())

    def __repr__(self):
        return '{0}:{1}'.format(self.type_str,self.getName())

    def getDepth(self):
        if not self.depth==None:
            return self.depth
        else:
            self.depth = max([fanin.getDepth() for fanin in self.fanins])+1
            return self.depth

    def getPathNum(self):
        if not self.path_num==None:
            return self.path_num
        else:
            self.path_num = sum([fanin.getPathNum() for fanin in self.fanins])
            return self.path_num

    def getId(self,increase=False):
        if increase:
            return self.id+1
        return self.id

    def getName(self):
        return self.name

    def getFanOuts(self):
        return self.fanouts

    def getFanOutNum(self):
        return len(self.fanouts)

    def getFanIns(self):
        return self.fanins

    def getFanInNum(self):
        return len(self.fanins)

    def getFanOut(self,index):
        return self.fanouts[index]

    def getFanIn(self,index):
        return self.fanins[index]

    def getTypeStr(self):
        return self.type_str

    def getValue(self):
        return self.value

    def setValue(self,value):
        self.value = value

    def deduceValue(self,value):
        if not self.value == None and not self.value==value:
            return False
        else:
            self.value = value
            return True

    def setName(self,name):
        self.name = name
        return self.id

    def addFanOut(self,gate):
        self.fanouts.append(gate)
        return len(self.fanouts)-1

    def addFanIn(self,gate):
        self.fanins.append(gate)
        return len(self.fanins)-1

    def addStructureEqualGate(self,gate):
        self.structure_equal_gates.append(gate)

    def getStructureEqualGates(self):
        return self.structure_equal_gates

    def upFlag(self):
        self.flag = True

    def downFlag(self):
        self.flag = False

    def isFlagUp(self):
        return self.flag

    def getTypeStr(self):
        return self.type_str

    def setTypeStr(self,type_str):
        self.type_str = type_str

    def getCopy(self,id):
        gate = copy.copy(self)
        gate.id = id
        gate.fanins = []
        gate.fanouts = []
        return gate

    def relateToPo(self):
        self.ispo = True

    def isPoGate(self):
        return self.ispo

    def getFanOutTypes(self):
        return set([type(fanout) for fanout in self.getFanOuts()])

    def reset(self):
        self.value = None

    def canReason(self):
        if not self.value==None:
            try:
                if self.value==(self.ctrl_value ^ self.phase):
                    return True
            except TypeError:
                pass
            finally:
                assigned_fi = [fi for fi in self.fanins if not fi.value==None]
                if len(assigned_fi)==self.getFanInNum()-1 and all([not fi.value==self.ctrl_value for fi in assigned_fi]):
                    return True
        return False

    def canPropagate(self):
        if all([not fi.value==None for fi in self.fanins]):
            return True
        elif any([fi.value==self.ctrl_value for fi in self.fanins if not fi.value==None]):
            return True 
        else:
            return False

    def reason(self):
        print 'hello'
        try:
            if self.value==(self.ctrl_value^self.phase):
                for fi in self.fanins:
                    #print '------- deduce',fi
                    if not fi.deduceValue(not self.ctrl_value):
                        return False
                return True
        except TypeError:
            one_num = 0
            is_odd = not one_num%2==0
            for fi in self.fanins:
                if fi.value==True:
                    one_num += 1
            for fi in self.fanins:
                if fi.value==None:
                    if self.value==True:
                        #print '------ deduce', fi
                        if not fi.deduceValue(self.phase^is_odd):
                            return False
                    else:
                        #print '------ deduce', fi
                        if not fi.deduceValue(not self.phase^is_odd):
                            return False
            return True
        finally:
            for fi in self.fanins:
                if fi.value==None:
                    #print '------ deduce', fi
                    if not fi.deduceValue(self.ctrl_value):
                        return False
            return True

    def getEncodeConstraint(self):
        added_clas = []
        constraint_type = {'and-not':0,'and-or':0,'and-nor':0,'and-and':0,'or-not':0}
        if self.getFanOutNum() > 1:
            for fanout in self.getFanOuts():
                if isinstance(fanout,AndGate):
                    #print self.getFanOuts()
                    for fanout2 in self.getFanOuts():
                        if isinstance(fanout2,NotGate):
                            continue
                            constraint_type['and-not'] += 1
                            added_clas.append([-fanout.getId(True),-fanout2.getId(True)])
                            added_clas.append([-fanout2.getId(True),-fanout.getId(True)])
                        if isinstance(fanout2,OrGate):
                            constraint_type['and-or'] += 1
                            added_clas.append([-fanout.getId(True),fanout2.getId(True)])
                            added_clas.append([fanout2.getId(True),-fanout.getId(True)])
                        if isinstance(fanout2,NorGate):
                            constraint_type['and-nor'] += 1
                            added_clas.append([-fanout.getId(True),-fanout2.getId(True)])
                            added_clas.append([-fanout2.getId(True),-fanout.getId(True)])
                        if isinstance(fanout2,AndGate):
                            continue
                            constraint_type['and-and'] += 1
                            cla = []
                            for fi in fanout2.getFanIns():
                                if fi==self:
                                    cla.append(-fanout.getId(True))
                                else:
                                    cla.append(-fi.getId(True))
                            cla.append(fanout2.getId(True))
                            added_clas.append(cla)
                        

                        #if isinstance(fanout2,XorGate):
                        #    print 'add and-xor constraint'

                if isinstance(fanout,OrGate):
                    for fanout2 in self.getFanOuts():
                        if isinstance(fanout2,NotGate):
                            constraint_type['or-not'] += 1
                            added_clas.append([fanout.getId(True),fanout2.getId(True)])
                            added_clas.append([fanout2.getId(True),fanout.getId(True)])

        else:
            #print self,'has single fanout'
            pass
        return added_clas, constraint_type
        
class AndGate(Gate):

    def __init__(self,id):
        super(AndGate, self).__init__(id)
        self.type_str = 'AND'
        self.ctrl_value = False
        self.phase = True

    def getProbability(self):
        if not self.probability==None:
            return self.probability
        one_probability = 1
        for fanin in self.fanins:
            one_probability *= fanin.getProbability()
        self.probability = one_probability
        return self.probability

    def eval(self):
        if any([fanin.getValue()==False for fanin in self.fanins]):
            self.value = False
            return self.value
        if any([fanin.getValue()==None for fanin in self.fanins]):
            self.value = None
            return self.value
        self.value = True
        return self.value

    def getSOP(self):
        if not self.SOP==None:
            return self.SOP
        sop = self.fanins[0].getSOP()
        for fanin in self.fanins[1:]:
            sop *= fanin.getSOP()
        self.SOP = sop.clear()
        print self.SOP
        return self.SOP

    def encTseitin(self):
        left_cla = []
        left_cla.append(self.getId(True))
        right_clas = []
        for fanin in self.getFanIns():
            left_cla.append(-fanin.getId(True))
            right_clas.append([-self.getId(True),fanin.getId(True)])
        right_clas.append(left_cla)
        return right_clas

class OrGate(Gate):

    def __init__(self,id):
        super(OrGate, self).__init__(id)
        self.type_str = 'OR'
        self.ctrl_value = True
        self.phase = True

    def getProbability(self):
        if not self.probability==None:
            return self.probability
        zero_probability = 1
        for fanin in self.fanins:
            zero_probability *= (1-fanin.getProbability())
        self.probability = 1 - zero_probability
        return self.probability

    def eval(self):
        if any([fanin.getValue()==True for fanin in self.fanins]):
            self.value = True
            return self.value
        if any([fanin.getValue()==None for fanin in self.fanins]):
            self.value = None
            return self.value
        self.value = False
        return self.value

    def getSOP(self):
        if not self.SOP==None:
            return self.SOP
        sop = self.fanins[0].getSOP()
        for fanin in self.fanins[1:]:
            sop += fanin.getSOP()
        self.SOP = sop.clear()
        print self.SOP
        return self.SOP

    def encTseitin(self):
        right_cla = []
        right_cla.append(-self.getId(True))
        left_clas = []
        for fanin in self.getFanIns():
            right_cla.append(fanin.getId(True))
            left_clas.append([self.getId(True),-fanin.getId(True)])
        left_clas.append(right_cla)
        return left_clas

class XorGate(Gate):

    def __init__(self,id):
        super(XorGate, self).__init__(id)
        self.type_str = 'XOR'
        self.ctrl_value = None
        self.phase = True

    def getProbability(self):
        if not self.probability==None:
            return self.probability
        probability = 0
        for one_num in range(self.getFanInNum()+1):
            if not (one_num % 2 == 0):
                combs = itertools.combinations(range(self.getFanInNum()),one_num)
                for comb in combs:
                    sub_probability = 1
                    for index, fanin in enumerate(self.fanins):
                        if index in comb:
                            sub_probability *= fanin.getProbability()
                        else:
                            sub_probability *= 1-fanin.getProbability()
                    probability += sub_probability
        self.probability = probability
        return self.probability

    def eval(self):
        if any([fanin.getValue()==None for fanin in self.fanins]):
            self.value = None
            return self.value
        else:
            self.value = self.fanins[0].getValue()
            for fanin in self.fanins[1:]:
                self.value = not (self.value==fanin.getValue())
            return self.value

    def getSOP(self):
        if not self.SOP==None:
            return self.SOP
        sop = self.fanins[0].getSOP()
        for fanin in self.fanins[1:]:
            sop = (~sop)*(fanin.getSOP())+(sop)*(~fanin.getSOP())
        self.SOP = sop.clear()
        print self.SOP
        return self.SOP

    def encTseitin(self):
        clas = []
        for one_num in range(self.getFanInNum()+1):
            #if not (one_num % 2 == 0):
            combs = itertools.combinations(range(self.getFanInNum()),one_num)
            for comb in combs:
                cla = []
                for index, fanin in enumerate(self.fanins):
                    if index in comb:
                        cla.append(fanin.getId(True))
                    else:
                        cla.append(-fanin.getId(True))
                if one_num % 2 == 0:
                    cla.append(-self.getId(True))
                else:
                    cla.append(self.getId(True))
                clas.append(cla)
        return clas
            
class BufGate(Gate):

    def __init__(self,id):
        super(BufGate, self).__init__(id)
        self.type_str = 'BUF'
        self.ctrl_value = None
        self.phase = True

    def getProbability(self):
        if not self.probability==None:
            return self.probability
        self.probability = self.fanins[0].getProbability()
        return self.probability

    def eval(self):
        self.value = self.fanins[0].getValue()
        return self.value

    def getSOP(self):
        if not self.SOP==None:
            return self.SOP
        self.SOP = self.fanins[0].getSOP()
        print self.SOP
        return self.SOP

    def encTseitin(self):
        cla1 = [-self.getId(True),self.getFanIn(0).getId(True)] 
        cla2 = [self.getId(True),-self.getFanIn(0).getId(True)]
        return [cla1,cla2]

class NotGate(Gate):

    def __init__(self,id):
        super(NotGate, self).__init__(id)
        self.type_str = 'NOT'
        self.ctrl_value = None
        self.phase = False

    def getProbability(self):
        if not self.probability==None:
            return self.probability
        self.probability = 1 - self.fanins[0].getProbability()
        return self.probability

    def eval(self):
        self.value = not self.fanins[0].getValue()
        return self.value

    def getSOP(self):
        if not self.SOP==None:
            return self.SOP
        self.SOP = ~self.fanins[0].getSOP()
        self.SOP = self.SOP.clear()
        print self.SOP
        return self.SOP

    def encTseitin(self):
        cla1 = [self.getId(True),self.getFanIn(0).getId(True)]
        cla2 = [-self.getId(True),-self.getFanIn(0).getId(True)]
        return [cla1,cla2]

class NorGate(Gate):

    def __init__(self,id):
        super(NorGate, self).__init__(id)
        self.type_str = 'NOR'
        self.ctrl_value = True
        self.phase = False

    def getProbability(self):
        if not self.probability==None:
            return self.probability
        probability = 1
        for fanin in self.fanins:
            probability *= (1-fanin.getProbability())
        self.probability = probability
        return self.probability

    def eval(self):
        if any([fanin.getValue()==True for fanin in self.fanins]):
            self.value = False
            return self.value
        if any([fanin.getValue()==None for fanin in self.fanins]):
            self.value = None
            return self.value
        self.value = True
        return self.value

    def getSOP(self):
        if not self.SOP==None:
            return self.SOP
        sop = self.fanins[0].getSOP()
        for fanin in self.fanins[1:]:
            sop += fanin.getSOP()
        self.SOP = ~sop
        self.SOP = self.SOP.clear()
        print self.SOP
        return self.SOP

    def encTseitin(self):
        left_cla = []
        left_cla.append(self.getId(True))
        right_clas = []
        for fanin in self.getFanIns():
            left_cla.append(fanin.getId(True))
            right_clas.append([-self.getId(True),-fanin.getId(True)])
        right_clas.append(left_cla)
        return right_clas

class NandGate(Gate):

    def __init__(self,id):
        super(NandGate, self).__init__(id)
        self.type_str = 'NAND'
        self.ctrl_value = False
        self.phase = False

    def getProbability(self):
        if not self.probability==None:
            return self.probability
        probability = 1
        for fanin in self.fanins:
            probability *= fanin.getProbability()
        self.probability = 1 - probability
        return self.probability

    def eval(self):
        if any([fanin.getValue()==False for fanin in self.fanins]):
            self.value = True
            return self.value
        if any([fanin.getValue()==None for fanin in self.fanins]):
            self.value = None
            return self.value
        self.value = False
        return self.value

    def getSOP(self):
        if not self.SOP==None:
            return self.SOP
        sop = self.fanins[0].getSOP()
        for fanin in self.fanins[1:]:
            sop *= fanin.getSOP()
        self.SOP = ~sop
        self.SOP = self.SOP.clear()
        print self.SOP
        return self.SOP

    def encTseitin(self):
        right_cla = []
        right_cla.append(-self.getId(True))
        left_clas = []
        for fanin in self.getFanIns():
            right_cla.append(-fanin.getId(True))
            left_clas.append([self.getId(True),fanin.getId(True)])
        left_clas.append(right_cla)
        return left_clas

class XnorGate(Gate):

    def __init__(self,id):
        super(XnorGate, self).__init__(id)
        self.type_str = 'XNOR'
        self.ctrl_value = None
        self.phase = False

    def getProbability(self):
        if not self.probability==None:
            return self.probability
        probability = 0
        for one_num in range(self.getFanInNum()+1):
            if not (one_num % 2 == 0):
                combs = itertools.combinations(range(self.getFanInNum()),one_num)
                for comb in combs:
                    sub_probability = 1
                    for index, fanin in enumerate(self.fanins):
                        if index in comb:
                            sub_probability *= fanin.getProbability()
                        else:
                            sub_probability *= 1-fanin.getProbability()
                    probability += sub_probability
        self.probability = 1-probability
        return self.probability

    def eval(self):
        if any([fanin.getValue()==None for fanin in self.fanins]):
            self.value = None
            return self.value
        else:
            self.value = self.fanins[0].getValue()
            for fanin in self.fanins[1:]:
                self.value = (self.value==fanin.getValue())
            return self.value

    def getSOP(self):
        if not self.SOP==None:
            return self.SOP
        sop = self.fanins[0].getSOP()
        for fanin in self.fanins[1:]:
            sop = (~sop)*(fanin.getSOP())+(sop)*(~fanin.getSOP())
        self.SOP  = ~sop
        self.SOP = self.SOP.clear()
        print self.SOP
        return self.SOP

    def encTseitin(self):
        clas = []
        for one_num in range(self.getFanInNum()+1):
            #if not (one_num % 2 == 0):
            combs = itertools.combinations(range(self.getFanInNum()),one_num)
            for comb in combs:
                cla = []
                for index, fanin in enumerate(self.fanins):
                    if index in comb:
                        cla.append(fanin.getId(True))
                    else:
                        cla.append(-fanin.getId(True))
                if one_num % 2 == 0:
                    cla.append(self.getId(True))
                else:
                    cla.append(-self.getId(True))
                clas.append(cla)
        return clas

class PIGate(Gate):

    def __init__(self,id):
        super(PIGate, self).__init__(id)
        self.type_str = 'PI'
        self.depth = 0
        self.path_num = 1
        self.ctrl_value = None
        self.phase = True

    def getProbability(self):
        return 0.5

    def eval(self):
        self.value = self.value
        return self.value

    def getSOP(self):
        return SOP([Product([self.getId(True)])])

class POGate(Gate):

    def __init__(self,id):
        super(POGate, self).__init__(id)
        self.type_str = 'PO'
        self.ispo = True

class ConstZeroGate(Gate):

    def __init__(self,id):
        super(ConstZeroGate, self).__init__(id)
        self.type_str = 'ConstZero'
        self.value = False
        self.depth = 0
        self.path_num = 1

    def getProbability(self):
        return 0.0

    def eval(self):
        self.value = False
        return self.value

    def getSOP(self):
        return SOP()

    def encTseitin(self):
        cla = [-self.getId(True)]
        return [cla]

class ConstOneGate(Gate):

    def __init__(self,id):
        super(ConstOneGate, self).__init__(id)
        self.type_str = 'ConstOne'
        self.value = True
        self.depth = 0
        self.path_num = 1

    def getProbability(self):
        return 1.0

    def eval(self):
        self.value = True
        return self.value

    def getSOP(self):
        return SOP([Product()])

    def encTseitin(self):
        cla = [self.getId(True)]
        return [cla]
