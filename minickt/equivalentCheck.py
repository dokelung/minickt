from gate import *
from itertools import permutations

def checkStructuralEquivalence(gate1,gate2):
    if gate2 in gate1.getStructureEqualGates():
        return True
    elif isinstance(gate1,PIGate) and isinstance(gate2,PIGate):
        return True
    elif not type(gate1)==type(gate2) or not gate1.getFanInNum()==gate2.getFanInNum():
        #print gate1,gate2,'now'
        return False
    else:
        for index,p in enumerate(permutations(gate1.getFanIns())):
            #print '  @  try', index ,'permutation',p
            if all(checkStructuralEquivalence(fi,gate2.getFanIn(i)) for i, fi in enumerate(p)):
                gate1.addStructureEqualGate(gate2)
                gate2.addStructureEqualGate(gate1)
                return True
        #print gate1,gate2,'under'
        #print '---  ',gate1, gate1.getFanIns()
        #print '---  ',gate2, gate2.getFanIns()
        return False