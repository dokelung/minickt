from minickt.gate import *

def writeOutCkt(ckt,file_name):
    inputs = []
    outputs = []
    wires = []
    gates = ckt.getPIGates()
    gates.extend(ckt.getGates()[ckt.po_end_index:])
    for gate in gates:
        if isinstance(gate,ConstZeroGate) or isinstance(gate,ConstOneGate):
            continue
        if gate.getFanInNum()==0:
            inputs.append(gate)
        elif gate.getFanOutNum()==0:
            outputs.append(gate)
        else:
            wires.append(gate)

    with open(file_name,'w') as writer:
        print >>writer,'//benchmark writen by minickt'
        io_name = outputs + inputs
        io_name = [gate.getName() for gate in io_name]
        ckt.circuit_name = ckt.circuit_name.partition('(')[0]
        print >>writer,'module {0} ({1});'.format(ckt.circuit_name,','.join(io_name))
        for o in outputs:
            print >>writer,'output {0};'.format(o.getName())
        for i in inputs:
            print >>writer,'input {0};'.format(i.getName())
        for w in wires:
            print >>writer,'wire {0};'.format(w.getName())
        for gate in ckt.getGates()[ckt.po_end_index:]:
            if isinstance(gate,ConstZeroGate) or isinstance(gate,ConstOneGate):
                continue
            gate_type = gate.getTypeStr()
            if '-' in gate_type:
                gate_type = gate_type.partition('-')[2]
            gate_type = gate_type.lower()
            gate_name = gate.getName()
            fanins = gate.getFanIns()
            gate_pins = []
            for fanin in fanins:
                if isinstance(fanin,ConstZeroGate):
                    gate_pins.append("1'b0")
                elif isinstance(fanin,ConstOneGate):
                    gate_pins.append("1'b1")
                else:
                    gate_pins.append(fanin.getName())
            print >>writer,'{0} ({1});'.format(gate_type,','.join([gate_name]+gate_pins))
        print >>writer,'endmodule'