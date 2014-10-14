# gate-level parser

def isComment(line):
    if line[0:2]=='//':
        return True
    else:
        return False

def readStatement(reader):
    statement = ''
    while True:
        line = reader.readline()
        if not line:
            return False
        line = line.strip()
        if not line:
            continue
        if isComment(line):
            continue
        if line[-1] == ';' or line=='endmodule':
            return (statement+' '+line).strip()
        else:
            statement += ' '+line

def getCktInfo(file_name):

    ckt_info = {}

    const0 = False
    const1 = False
    verilog_module = ['module','endmodule']
    verilog_pin = {'input':[],'output':[],'wire':[]}
    verilog_gate = {'and':{},'or':{},'xor':{},'nor':{},'nand':{},'xnor':{},'buf':{},'not':{},'zero':{},'one':{}}

    with open(file_name,'r') as reader:
        while True:
            statement = readStatement(reader)
            if not statement:
                break
            tokens = statement.strip(';').split()
            tokens = tokens if len(tokens)>1 or tokens[0]=='endmodule' else statement.strip(';').split('(')
            keyword = tokens.pop(0)
            tokens = ' '.join(tokens)

            keyword = keyword.strip('1234567890')
            if keyword == 'inv':
                keyword = 'not'
            #print keyword,

            if keyword=='module':
                circuit_name = '{0}({1})'.format(tokens.split()[0],file_name)

            elif keyword in verilog_pin:
                tokens = tokens.split()
                pin_names = [token.strip(',') for token in tokens]
                #print pin_names
                verilog_pin[keyword].extend(pin_names)

            elif keyword in verilog_gate:
            	tokens = tokens.partition('(')[2]
            	tokens = tokens.split(',')
            	tokens = [token.strip(' .') for token in tokens]

            	fanins = []

            	for token in tokens:
            		gate_pin_name = token.partition('(')[0]
            		pin_name = token.partition('(')[2]
            		if gate_pin_name=='O':
            			output = pin_name.strip(')')
            		else:
            			fanins.append(pin_name.strip(')'))

                #print output, fanins

                #gate_pins = tokens[1].strip('()').split(',')
                #gate_pins = [pin.strip() for pin in gate_pins]
                #output = gate_pins[0]
                #fanins = gate_pins[1:]
                fanins = ['const_zero' if fanin=="1'b0" else fanin for fanin in fanins]
                fanins = ['const_one' if fanin=="1'b1" else fanin for fanin in fanins]

                #print fanins

                if 'const_zero' in fanins: const0 = True
                if 'const_one' in fanins: const1 = True

                if keyword=='zero':
                    verilog_gate['buf'][output] = ['const_zero']
                    const0 = True
                    continue
                if keyword=='one':
                    verilog_gate['buf'][output] = ['const_one']
                    const1 = True
                    continue

                verilog_gate[keyword][output] = fanins 
            elif keyword in verilog_module:
                pass
            else:
                print 'wrong,wrong,wrong!'

    ckt_info['ckt_name'] = circuit_name
    ckt_info['output'] = verilog_pin['output']
    ckt_info['input'] = verilog_pin['input']
    ckt_info['wire'] = verilog_pin['wire']
    ckt_info['and'] = verilog_gate['and']
    ckt_info['or'] = verilog_gate['or']
    ckt_info['xor'] = verilog_gate['xor']
    ckt_info['nor'] = verilog_gate['nor']
    ckt_info['nand'] = verilog_gate['nand']
    ckt_info['xnor'] = verilog_gate['xnor']
    ckt_info['buf'] = verilog_gate['buf']
    ckt_info['not'] = verilog_gate['not']
    ckt_info['const0'] = const0
    ckt_info['const1'] = const1

    return ckt_info