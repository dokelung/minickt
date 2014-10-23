from circuitManager import *
from equivalentCheck import *
from tempfile import NamedTemporaryFile
import os
import subprocess
import sys
import cmd
import time

class OriShell(cmd.Cmd,object):
    intro = \
"""
================================
           miniCkt

     * author: dokelung
     # use "?" or "cmd"         
================================
"""
    prompt = '[ miniCkt ] >> '

    def __init__(self):
        super(Shell, self).__init__()
        self.cktmgr = CircuitManager()

    def do_read(self,arg):
        """
        read circuit file by specified parser and construct a circuit
        SYNOPSIS: read <circuit file> by <parser>
        DESCRIPTION:
            1.  each parser is a python module located in directory "cktParser"
                and it must have a global function "getCktInfo(file_name)"
                which return a circuit infomation dictionary
                to know the details of this dictionary,
                user can reference to "primitive.py" in "cktParser"
                note that file_name is any kind of circuit file, e.g. verilog
            2.  also, "cktParser" is a python package
            3.  command "ls_parser" can list all avalible parsers
        """
        args = self.parseArg(arg)
        try:
            file_name = args[0]
            assert args[1]=='by'
            parser= args[2]

            exec 'from cktParser import {0}'.format(parser)
            exec 'ckt_info = {0}.getCktInfo("{1}")'.format(parser,file_name)

            print 'read {0} ...'.format(file_name)
            ckt = Circuit()
            ckt.constructCkt(ckt_info)
            self.cktmgr.addCkt(ckt)
            self.cktmgr.transToCkt(len(self.cktmgr.getCkts())-1)
            print 'success:', 'circuit "{0}" is in circuit manager now'.format(ckt)
        except:
            print 'error: reading failed'

    def do_write(self,arg):
        """
        write current circuit out to a verilog of primitive-gate type
        SYNOPSIS: write <file name> by <writer>
        DESCRIPTION:
            1.  if user want to modify the module's name, please use cmd "chname"
                to change the name of circuit(module) first
                note that the name with '()' may result in error!
            2.  each writer is a python module located in directory "cktWriter"
                and it must have a global function "writeOutCkt(ckt,file_name)"
                for writing out circuit
                user can reference to "primitive.py" in "cktWriter"
                note that file_name is any kind of circuit file, e.g. verilog
            2.  also, "cktWriter" is a python package
            3.  command "ls_writer" can list all avalible writers
        """
        #try:
        args = self.parseArg(arg)
        ckt = self.cktmgr.getCurrentCkt()

        file_name = args[0]
        assert args[1]=='by'
        writer = args[2]

        exec 'from cktWriter import {0}'.format(writer)
        exec '{0}.writeOutCkt(ckt,"{1}")'.format(writer,file_name)

        print 'success:', 'circuit "{0}" has been writen out'.format(ckt)

        #except:
        #    print 'error: cannot write out circuit'

    def do_cmd(self,arg):
        """
        list all cmds and their brief descriptions
        """
        try:
            print '=================================='
            print '  command list'
            print '=================================='
            commands = [name for name in dir(self) if name[0:3]=='do_']
            for command in commands:
                doc = eval('self.'+command+'.__doc__')
                if not doc==None:
                    doc = doc.strip()
                    doc = doc.split('\n')
                    print '{cmd:12}: {state}'.format(cmd=command[3:], state=doc[0])
        except:
            print 'error: cannot list commands'

    def do_ls(self,arg):
        """
        list items
        SYNOPSIS: ls <option>
        OPTION:
            -c = (cmd)list_ckt: list circuits in the circuit manager
            -p = (cmd)ls_parser: list avalible parsers
            -w = (cmd)ls_writer: list avalible writers
        """
        try:
            args = self.parseArg(arg)
            if args[0] == 'c':
                self.excCmd('ls_ckt')
            elif args[0] == 'p':
                self.excCmd('ls_parser')
            elif args[0] == 'w':
                self.excCmd('ls_writer')
            else:
                print 'error: no this option'
        except:
            print 'error: cannot list, use "?ls" to check the usage'

    def do_ls_parser(self,arg):
        """
        list all avalible parsers in package(directory) cktParser
        """
        try:
            files = os.listdir('cktParser')
            files = [file for file in files if '.py' in file and '__init__' not in file and '.pyc' not in file]
            files = [file.split('.')[0] for file in files]
            print 'there are {0} parsers in cktParser'.format(len(files))
            for index, file in enumerate(files):
                print '[{0}]'.format(index), file
        except:
            print 'error: cannot list parsers'

    def do_ls_writer(self,arg):
        """
        list all avalible writers in package(directory) cktWriter
        """
        try:
            files = os.listdir('cktWriter')
            files = [file for file in files if '.py' in file and '__init__' not in file and '.pyc' not in file]
            files = [file.split('.')[0] for file in files]
            print 'there are {0} parsers in cktWriter'.format(len(files))
            for index, file in enumerate(files):
                print '[{0}]'.format(index), file
        except:
            print 'error: cannot list writers'

    def do_sec(self,arg):
        """
        check structural equivalence
        SYNOPSIS: sec <[ckt id.]gate name> <[ckt id.]gate name>
        DESCRIPTION:
            1. if just give gate name, miniCkt take it as a gate in current ckt
            2. user can use "ls -c" or "ls_ckt" to get "ckt id"
        EXAMPLE:
            ex1. [ miniCkt ] >> sec 0.out 2.out
                 ---> sec for two circuit
            ex2. [ miniCkt ] >> sec n4 n5
                 ---> sec for two gate cones
        """
        try:
            args = self.parseArg(arg)
            if '.' in args[0]:
                ckt1_id, gate_name1 = args[0].split('.')
                ckt1_id = int(ckt1_id)
            else:
                ckt1_id = self.cktmgr.getToken()
                gate_name1 = args[0]

            if '.' in args[1]:
                ckt2_id, gate_name2 = args[1].split('.')
                ckt2_id = int(ckt2_id)
            else:
                ckt2_id = self.cktmgr.getToken()
                gate_name2 = args[1]

            ckt1 = self.cktmgr.getCkt(ckt1_id)
            ckt2 = self.cktmgr.getCkt(ckt2_id)
            gate1 = ckt1.getGateFromName(gate_name1)
            gate2 = ckt2.getGateFromName(gate_name2)

            if checkStructuralEquivalence(gate1,gate2):
                print 'structural eq'
            else:
                print 'structural uneq'
        except:
            print 'error: checking error'

    def do_fec(self,arg):
        """
        check functional equivalence
        SYNOPSIS: sec <ckt id> <ckt id>
        DESCRIPTION:
            1.  fec checks functional equivalence with miter
                and now just supports "single output" curcuit.
                So make sure two things:
                    1. The specified ckts should be single output ckt.
                    2. Their inputs can be mapped.
                       (It means the corresponding inputs should have same name.)
            2.  If the miter's satisfiability is SAT, these two ckts are not 
                functional equivalence, otherwise the are functional equivalence.
            3.  It use lingeling SAT solver and TST encoding to solve
                miter's circuit SAT.
            4.  user can use "ls -c" or "ls_ckt" to get "ckt id"
        """
        try:
            args = self.parseArg(arg)
            ckt1_id = int(args[0])
            ckt2_id = int(args[1])
            ckt1 = self.cktmgr.getCkt(ckt1_id)
            ckt2 = self.cktmgr.getCkt(ckt2_id)

            for g in ckt1.getGatesOnce(): 
                if g not in ckt1.getPIGates():
                    g.nameTranslate('_m1')
            for g in ckt2.getGatesOnce(): 
                if g not in ckt2.getPIGates():
                    g.nameTranslate('_m2')

            from cktWriter import primitive
            primitive.writeOutCkt(ckt1,'c1')
            primitive.writeOutCkt(ckt2,'c2')

            inputs = []
            outputs = []
            wires = []
            gates = []

            for file_name in ['c1','c2']:
                with open(file_name,'r') as reader:
                    for line in reader:
                        line = line.strip()
                        if line[0:2]=='//':
                            continue
                        else:
                            items = line.split()
                            keyword = items[0]
                            if keyword in ['module','endmodule']:
                                continue
                            if keyword == 'input':
                                inputs.append(items[1].strip(';'))
                            elif keyword == 'output':
                                outputs.append(items[1].strip(';'))
                            elif keyword == 'wire':
                                wires.append(items[1].strip(';'))
                            else:
                                gates.append(line)

            inputs = set(inputs)

            io_name = ['out'] + list(inputs)

            with open('miter','w') as writer:
                print >>writer,'//benchmark writen by minickt'
                print >>writer,'module {0} ({1});'.format('miter',','.join(io_name))
                for i in inputs:
                    print >>writer,'input {0};'.format(i)
                print >>writer, 'output out;'
                for w in wires+outputs:
                    print >>writer,'wire {0};'.format(w)
                for g in gates:
                    print >>writer, g
                print >>writer,'xor (out,{0},{1});'.format(outputs[0],outputs[1])
                print >>writer,'endmodule'

            os.system('rm c1')
            os.system('rm c2')

            self.excCmd('read miter by primitive')
            self.excCmd('chname miter')
            self.excCmd('!rm miter')
            self.excCmd('sat by lingeling -f with TST')

        except:
            print 'error: checking error'

    def do_reset(self,arg):
        """
        reset the value of all gates
        """
        try:
            ckt = self.cktmgr.getCurrentCkt()
            ckt.resetAllGates()
        except:
            print 'error: cannot reset'

    def do_reason(self,arg):
        """
        reason the ckt under current assignment
        DESCRIPTION:
            1. user can use cmd "set" to assign gate value
            2. use cna use cmd "reset" to reset all gate values
            3. also, cmd "sg" with option "-v" can check the
               result of reasoning
        """
        try:
            ckt = self.cktmgr.getCurrentCkt()
            t1 = time.time()
            if ckt.reason():
                print 'reason success'
            else:
                print 'conflict'
            t2 = time.time()
            print '* reason time: {time} sec'.format(time=t2-t1)
        except:
            print 'error: cannot reason'

    def do_sat_reason(self,arg):
        """
        use sat solving for totally reasoning
        SYNOPSIS: sat_reason <gate types/gate names> <value>
        GATE_TYPE:
            pi, po, and, or, buf, not, nand, nor, xor, xnor, all
        VALUE:
            logical one  -> "1" or "t"
            logical zero -> "0" or "f"
        DESCRIPTION:
            use tseitin transformation to encode
            use lingeling and its default setting to solve
        """
        try:
            self.excCmd('encode by PTST to tempf')
            self.excCmd('reset')
            self.excCmd('set {0}'.format(arg))
            ckt = self.cktmgr.getCurrentCkt()
            with open('tempf','a') as f:
                for gate in ckt.getGates()[ckt.po_end_index:]+ckt.getPIGates():
                    if not gate.getValue()==None:
                        if gate.getValue()==True:
                            print >>f,gate.getId(True),
                            print >>f,'0'
                        elif gate.getValue()==False:
                            print >>f,-gate.getId(True),
                            print >>f,'0'
            os.system('./bin/lingeling -f tempf')
            os.system('rm tempf')
        except:
            print 'error: cannot do sat reasoning'

    def do_encode(self,arg):
        """
        encode circuit to a cnf file
        SYNOPSIS: encode by <method> to <file>
        METHOD:
            PTST:   pure tseitin transformation(no assign output) 
            TST:    tseitin transformation
            NTST:   new tseitin transformation(includes additional constraints)
            TST-F:  TST but assign output=False
            NTST-F: NTST but assign output=False
            RTST:   TST with reasoning
        DESCRIPTION:
            this cmd does not generate header of cnf file
        """
        try:
            ckt = self.cktmgr.getCurrentCkt()
            args = self.parseArg(arg)
            assert args[0]=='by'
            assert args[2]=='to'

            file_name = args.pop()
            
            #print 'id-table'
            #for gate in ckt.getGatesInTopologicalOrder():
            #    print gate,gate.getId(True)
            #with open('test1.tb','w') as writer:
            #    for gate in ckt.getGates():
            #        print >>writer, gate.getId(), gate

            constraint_type = {}

            t1 = time.time()
            if args[1]=='PTST':
                ckt.encTseitin(file_name,option='pure')
            elif args[1]=='TST' or args[1]=='TST-F':
                if args[1]=='TST':
                    ckt.encTseitin(file_name)
                elif args[1]=='TST-F':
                    ckt.encTseitin(file_name,option='unsat')
            elif args[1]=='NTST' or args[1]=='NTST-F':
                if args[1]=='NTST':
                    ckt.encTseitin(file_name)
                elif args[1]=='NTST-F':
                    ckt.encTseitin(file_name,option='unsat')
                with open(file_name,'a') as writer:
                    for gate in ckt.getPIGates()+ckt.getGates()[ckt.po_end_index:]:
                        added_clas, types = gate.getEncodeConstraint()
                        for type in types:
                            if constraint_type.has_key(type):
                                constraint_type[type] += types[type]
                            else:
                                constraint_type[type] = types[type]
                        for cla in added_clas:
                            for lit in cla:
                                print >>writer,lit,
                            print >>writer,'0'
            elif args[1]=='RTST':
                ckt.encReason(file_name)
            t2 = time.time()
            print '--------<other constraint>--------'
            for type in constraint_type:
                print 'add {0} constraint X {1}'.format(type,constraint_type[type])
            print '----------------------------------'
            print '\n* encode time: {time} sec \n'.format(time=t2-t1)
        except:
            print 'error: cannot encode'

    def do_sat(self,arg):
        """
        solve circuit sat by specified sat solver
        SYNOPSIS: sat by <sat solver & option> with <encoding method>
        DESCRIPTION:
            1. the excutable file of sat solver must be compiled
               and placed in the directory "bin"
            2. if user want to specify the solving setting, the setting must
               be given in "sat solver & option" with 
               example:
                    sat by lingeling -f with tseitin
            3. user can add new solver by modifying the function "do_sat"
               in "core/cmdManager"
            4. the supported encoding method can reference to cmd "encode"
               use "?encode" to know the details
        """
        try:
            args = arg.partition('by')[2]
            solver_setting, _ ,encoding_method = args.partition('with')
            solver_setting = solver_setting.strip()
            encoding_method = encoding_method.strip()
            with NamedTemporaryFile('w+t') as f:
                self.excCmd('encode by {method} to {fname}'.format(method=encoding_method,fname=f.name))
                os.system('./bin/{sat} {fname}'.format(sat=solver_setting,fname=f.name))

            #self.excCmd('encode')
        except:
            print 'error: cannot solve'

    def do_ls_ckt(self,arg):
        """
        list all (current) circuits in the circuit manager
        """
        try:
            print 'there are {0} circuits now'.format(len(self.cktmgr.getCkts()))
            for index, ckt in enumerate(self.cktmgr.getCkts()):
                if index==self.cktmgr.getToken():
                    print '[{0}]'.format(index), ckt, '<--- current'
                else:
                    print '[{0}]'.format(index), ckt
        except:
            print 'error: cannot list circuits'

    def do_eval(self,arg):
        """
        evaluate each gate in circuit
        """
        try:
            ckt = self.cktmgr.getCurrentCkt()
            t1 = time.time()
            ckt.evaluateCkt()
            t2 = time.time()
            print '* eval time: {time} sec'.format(time=t2-t1)
        except:
            print 'error: cannot evaluate'

    def do_cc(self,arg):
        """
        change current circuit to i-th circuit of circuit manager
        SYNOPSIS: cc <i>
        """
        try:
            self.cktmgr.transToCkt(int(arg))
        except:
            print 'error: no this circuit'

    def do_rm(self,arg):
        """
        remove circuit of circuit manager
        SYNOPSIS: rm [i]
        DESCRIPTION:
            if option "i" is given, remove i-th circuit of circuit manager
            otherwise, remove the current circuit
        """
        try:
            if not arg:
                self.cktmgr.rmCktByIndex(self.cktmgr.getToken())
            else:
                self.cktmgr.rmCktByIndex(int(arg))
        except:
            print 'error: cannot remove this circuit'

    def do_chname(self,arg):
        """
        change name of current circuit (set a new name for it)
        SYNOPSIS: chname <new name>
        """
        try:
            self.cktmgr.changeCktName(arg.strip())
        except:
            print 'error: cannnot change circuit name'

    def do_loadsc(self,arg):
        """
        load a script file and excute the commands in it
        SYNOPSIS: loadsc <script file> 
        """
        with open(arg,'r') as reader:
            for line in reader:
                line = line.strip()
                print '-------------------------'
                print 'EXC({0})'.format(line)
                print '-------------------------'
                self.excCmd(line)

    def do_shell(self,arg):
        """
        excute the command as in shell
        SYNOPSIS: shell <command>
        DESCRIPTION:
            user can simply use symbol ! to run cmd in shell
        EXAMPLE:
            to list file names of current directory in long format
            [ miniCkt ] >> shell ls -l
            [ miniCkt ] >> ! ls -l
        """
        os.system(arg)

    def do_show(self,arg):
        """
        show graph of circuit
        SYNOPSIS: show <option>
        OPTION:
            -c = (cmd)show_ckt: show a circuit graph
            -r = (cmd)show_ratio: show a pie chart of gates ratio
        """
        try:
            args = self.parseArg(arg)
            if args[0] == 'c':
                self.excCmd('show_ckt')
            elif args[0] == 'r':
                self.excCmd('show_ratio')
            else:
                print 'error: no this option'
        except:
            print 'error: cannot show, use "?show" to check the usage'

    def do_show_ckt(self,arg):
        """
        show the circuit graph
        """
        try:
            self.cktmgr.getCurrentCkt().showCircuitGraph()
        except:
            print 'error: cannot show the graph'

    def do_show_ratio(self,arg):
        """
        show the pie chart for listing gates ratio
        """
        try:
            self.cktmgr.getCurrentCkt().showGatesRatio()
        except:
            print 'error: cannot show the ratio of gates'

    def do_get(self,arg):
        """
        get the properties of circuit
        SYNOPSIS: get <circuit property> [>,>>log file]
        DESCRIPTION:
            user can output the infomation to specified file by notations
            ">"(write to log file) or ">>"(append to log file)
        CIRCUIT PROPERTY:
            ckt_name:       show the current circuit name
            avg_fanout_num: show the average number of fanout
            max_fanout_num: show the max number of fanout
            var_fanout_num: show the variance of number of fanout
            avg_fanin_num:  show the average number of fanin
            max_fanin_num:  show the max number of fanin
            var_fanin_num:  show the variance of number of fanin
            gate_num:       list the gate numbers and ratio
            path_num:       list the path numbers of circuit
            depth:          show the depths of all PO gates
            probability:    list the probabilities of all PO gates
                            also the cone gates whose probability=1 or =0
            consistency:    show the consistent rate
                            consistent => all fanouts' phases are the same
                            consistency = #consistent gate/#gate
            sop:            show the sum of product expression of POs 
        """
        try:
            ckt = self.cktmgr.getCurrentCkt()
            args = self.parseArg(arg)
            outplace = sys.stdout
            file_open = False
            if '>' in args[-1] or '>>' in args[-1]:
                try:
                    out_info = args[-1]
                    if '>>' in out_info:
                        file_name = out_info.rpartition('>')[2]
                        outplace = open(file_name,'a')
                    elif '>' in out_info:
                        file_name = out_info.rpartition('>')[2]
                        outplace = open(file_name,'w')
                    file_open = True
                except:
                    print 'error: please use "?get" to see the usage'
                    return False
                args = args[:-1]
            if 'probability' in args:
                for po in ckt.getPOGates():
                    print >>outplace,'{0} ==> probability={1}'.format(po,po.getProbability())
                    print '------------------------------------'
                    ckt.traverseCone(po)
                    for gate in ckt.getGates():
                        if gate.isFlagUp():
                            prob = gate.getProbability()
                            if prob <= 0:
                                print >>outplace,'{0} ==> probability={1}'.format(gate,prob)
                            elif prob >= 1:
                                print >>outplace,prob,'{0} ==> probability={1}'.format(gate,prob)
            if 'avg_fanout_num' in args:
                print >>outplace,'average #fanout = {0}'.format(ckt.getAvgFanOutNum())
            if 'max_fanout_num' in args:
                print >>outplace,'max #fanout = {0}'.format(ckt.getMaxFanOutNum())
            if 'var_fanout_num' in args:
                print >>outplace,'variance of #fanout = {0}'.format(ckt.getFanOutNumVariance())
            if 'avg_fanin_num' in args:
                print >>outplace,'average #fanin = {0}'.format(ckt.getAvgFanInNum())
            if 'max_fanin_num' in args:
                print >>outplace,'max #fanin = {0}'.format(ckt.getMaxFanInNum())
            if 'var_fanin_num' in args:
                print >>outplace,'variance of #fanin = {0}'.format(ckt.getFanInNumVariance())
            if 'depth' in args:
                for po in ckt.getPOGates():
                    print >>outplace,'{0} ==> depth={1}'.format(po,po.getDepth())
            if 'path_num' in args:
                for po in ckt.getPOGates():
                    print >>outplace,'{0} ==> path_num={1}'.format(po,po.getPathNum())
            if 'ckt_name' in args:
                print >>outplace,'circuit name = {0}'.format(ckt)
            if 'gate_num' in args:
                gate_count = ckt.getGateCount()
                labels = ['PI', 'AND', 'OR', 'XOR', 'XNOR', 'NAND', 'NOR', 'NOT', 'BUF', 'Const0', 'Const1']
                sizes = []
                sizes.append(ckt.getPiNum())
                sizes.append(ckt.getAndNum())
                sizes.append(ckt.getOrNum())
                sizes.append(ckt.getXorNum())
                sizes.append(ckt.getXnorNum())
                sizes.append(ckt.getNandNum())
                sizes.append(ckt.getNorNum())
                sizes.append(ckt.getNotNum())
                sizes.append(ckt.getBufNum())
                sizes.append(ckt.getConstZeroNum())
                sizes.append(ckt.getConstOneNum())
                print >>outplace,'total gate count = {0}'.format(gate_count)
                print '------------------------------------'
                for index, label in enumerate(labels):
                    print >>outplace,'#{0} = {1}({2})'.format(label,sizes[index],float(sizes[index])/float(gate_count))
            if 'consistency' in args:
                print >>outplace,'consistent rate = {0}'.format(ckt.getPhaseConsistentRate())
            if 'sop' in args:
                for po in ckt.getPOGates():
                    print >>outplace,'{0} ==> sop =\n{1}'.format(po,po.getSOP())
            if file_open:
                outplace.close()
        except:
            print 'error: cannot get'
            if file_open:
                outplace.close()

    def do_set(self,arg):
        """
        set value of gate in circuit
        SYNOPSIS: set <gate types/gate names> <value>
        GATE_TYPE:
            pi, po, and, or, buf, not, nand, nor, xor, xnor, all
        VALUE:
            logical one  -> "1" or "t"
            logical zero -> "0" or "f"
        DESCRIPTION:
            user can use script file to set
            just write set commands in script file
            and excute command loadsc script
        EXAMPLE:
            1. set directlly
                [ miniCkt ] >> set pi n01 n02 t
            2. set by script file
                [ miniCkt ] >> loadsc setting_script
                ---------------------------
                contents of setting_script
                ---------------------------
                set pi t
                set n01 n02 t
                --------------------------- 
            note that n01, n02 are the name of gates
        """
        try:
            ckt = self.cktmgr.getCurrentCkt()
            args = self.parseArg(arg)
            value = args.pop()
            if value=='1' or value=='t':
                value = True
            elif value=='0' or value=='f':
                value = False
            args = [arg.strip(',') for arg in args ]
            gates = self.collectGates(ckt,args)
            for gate in gates:
                gate.setValue(value)
        except:
            print 'error: cannot set'
        
    def do_sg(self,arg):
        """
        see the gates of current circuit
        SYNOPSIS: sg <gate types/gate names> [option] [k]
        GATE_TYPE:
            pi, po, and, or, buf, not, nand, nor, xor, xnor, const0, const1, all
        OPTION:
            -v: also see the value of gates
            -i: also see the fanins
            -o: also see the fanouts
        DESCRIPTION:
            1. k is an integer that indicates how many gates listed in a line
               default value: k=5, note that if user use option "-i" or "-o",
               k will be set 1(k=1) automatically
            2. user also can use gate type "all" to see all gates in circuit
        EXAMPLE:
            [ miniCkt ] >> sg n01 n02 and or -iov 3
            note that n01, n02 are the gate names
        """
        try:
            ckt = self.cktmgr.getCurrentCkt()
            #args = self.parseArg(arg)
            args = arg.strip().split()

            k = 5

            try:
                k = int(args[-1])
                args.pop()
            except:
                pass

            option = ''
            #if not args[-1] in ['pi', 'po', 'and', 'or', 'buf', 'not', 'nand', 'nor', 'xor', 'xnor', 'const0', 'const1', 'all']:
            #    option = args[-1]
            #    if 'i' in option or 'o' in option:
            #        k=1
            if args[-1][0]=='-':
                option = args.pop()

            args = [arg.strip(',') for arg in args]
            gates = self.collectGates(ckt,args)

            if 'i' in option or 'o' in option:
                k=1

            for index, gate in enumerate(gates):
                if 'v' in option:
                    print '{0}={1}'.format(gate,gate.getValue()),
                else:
                    print gate,

                if 'i' in option:
                    print '\n    -fanin-> {0}'.format(gate.getFanIns()),
                if 'o' in option:
                    print '\n    -fanout-> {0}'.format(gate.getFanOuts()),
                if index%k==k-1:
                    print '' 
            if not len(gates)%k==0:
                print ''         
        except:
            print 'error: cannot see the gates'

    def do_gen_cone_ckt(self,arg):
        """
        genearate a independent circuit by getting cone of specifed gates
        SYNOPSIS: gen_cone_ckt <gate name> [cone ckt name]
        DESCRIPTION:
            it is a combinational command
            gen_cone_ckt <gate name> [cone ckt name]:
                1. cone <gate name> [cone ckt name]
                2. write by primitive
                3. rm
                4. read by primitive
        """
        try:
            with NamedTemporaryFile('w+t') as f:
                self.excCmd('cone {args}'.format(args=arg))
                self.excCmd('write {fname} by primitive'.format(fname=f.name))
                self.excCmd('rm')
                self.excCmd('read {fname} by primitive'.format(fname=f.name))
        except:
            print 'error: cannot generate cone ckt'

    def do_cone(self,arg):
        """
        generate a sub-circuit by getting cone of specified gate
        SYNOPSIS: cone <gate name> [cone ckt name]
        DESCRIPTION:
            this cmd will generate a cone circuit by given name of gate
            also, this circuit will be added to circuit manager as a new circuit
            its name can be specified by "cone ckt name"
            if user wants to let cone circuit be an independent circuit, please
            write it out and read it again
            or can use combinational cmd "gen_cone_ckt" in convenience
        """
        try:
            ckt_name = 'coneckt'
            args = self.parseArg(arg)
            if len(args)==2:
                gate_name = args[0]
                ckt_name = args[1]
            else:
                gate_name = args[0]
            ckt = self.cktmgr.getCurrentCkt()
            cone = ckt.getConeCircuit(ckt.getGateFromName(gate_name))
            cone.setName(ckt_name)
            self.cktmgr.addCkt(cone)
            self.cktmgr.transToCkt(len(self.cktmgr.getCkts())-1)
            print 'success: generate cone of {0}'.format(cone.getGateFromName(gate_name))
        except:
            print 'error: cannot generate cone circuit'

    def do_exit(self,arg):
        """
        terminate this tool
        """
        exit()

    def excCmd(self,cmd):
        l = self.precmd(cmd)
        r = self.onecmd(l)
        r = self.postcmd(r,l)

    def parseArg(self,arg):
        args = arg.strip().split()
        args = [arg.strip('-') for arg in args]
        return args

    def collectGates(self,ckt,args):

        gates = []

        if 'pi' in args:
            gates.extend(ckt.getPIGates())
        if 'po' in args:
            gates.extend(ckt.getPOGates())
        if 'and' in args:
            gates.extend(ckt.getAndGates())
        if 'or' in args:
            gates.extend(ckt.getOrGates())
        if 'buf' in args:
            gates.extend(ckt.getBufGates())
        if 'not' in args:
            gates.extend(ckt.getNotGates())
        if 'nand' in args:
            gates.extend(ckt.getNandGates())
        if 'nor' in args:
            gates.extend(ckt.getNorGates())
        if 'xor' in args:
            gates.extend(ckt.getXorGates())
        if 'xnor' in args:
            gates.extend(ckt.getXnorGates())
        if 'const0' in args:
            gates.extend(ckt.getConstZeroGates())
        if 'const1' in args:
            gates.extend(ckt.getConstOneGates())
        if 'all' in args:
            gates.extend(ckt.getGates())

        for gate_name in args:
            try:
                gates.append(ckt.getGateFromName(gate_name))
            except:
                pass

        return list(set(gates))

class Shell(OriShell):

    def __init__(self):
        super(OriShell, self).__init__()
        self.cktmgr = CircuitManager()

    def do_collect(self,arg):
        """
        collect circuit info and print
        SYNOPSIS: collect [>,>>log file]
        DESCRIPTION:
            log file is a cvs file
        """
        try:
            outplace = sys.stdout
            args = self.parseArg(arg)
            title = False
            file_open = False
            if not len(args)==0:
                if '>' in args[-1] or '>>' in args[-1]:
                    try:
                        out_info = args[-1]
                        if '>>' in out_info:
                            file_name = out_info.rpartition('>')[2]
                            outplace = open(file_name,'a')
                        elif '>' in out_info:
                            file_name = out_info.rpartition('>')[2]
                            outplace = open(file_name,'w')
                            title = True
                        file_open = True
                    except:
                        print 'error: please use "?collect" to see the usage'
                        return False

            ckt = self.cktmgr.getCurrentCkt()
            ckt_info = []
            ckt_info.append( ('pi_num',ckt.getPiNum()) )
            ckt_info.append( ('and_num',ckt.getAndNum()) )
            ckt_info.append( ('or_num', ckt.getOrNum()) )
            ckt_info.append( ('xor_num', ckt.getXorNum()) )
            ckt_info.append( ('nand_num', ckt.getNandNum()) )
            ckt_info.append( ('nor_num', ckt.getNorNum()) )
            ckt_info.append( ('xnor_num',ckt.getXnorNum()) )
            ckt_info.append( ('buf_num',ckt.getBufNum()) )
            ckt_info.append( ('not_num',ckt.getNotNum()) )

            for i in range(len(ckt_info)):
                ckt_info.append( (ckt_info[i][0]+'_rate',float(ckt_info[i][1])/float(ckt.getGateCount())) )
        
        
            ckt_info.append( ('gate_count',ckt.getGateCount()) )
            ckt_info.append( ('probability',ckt.getPOProbability(0)) )
            ckt_info.append( ('avg_fanout_num',ckt.getAvgFanOutNum()) )
            ckt_info.append( ('max_fanout_num',ckt.getMaxFanOutNum()) )
            ckt_info.append( ('fanout_num_variance',ckt.getFanOutNumVariance()) )
            ckt_info.append( ('avg_fanin_num',ckt.getAvgFanInNum()) )
            ckt_info.append( ('max_fanin_num',ckt.getMaxFanInNum()) )
            ckt_info.append( ('fanin_num_variance',ckt.getFanInNumVariance()) )
            ckt_info.append( ('depth',ckt.getPOGates()[0].getDepth()) )
            ckt_info.append( ('path_num',ckt.getPOGates()[0].getPathNum()) )
        
            ckt_info = [(info[0],str(info[1])) for info in ckt_info]
            ckt_info_name = [info[0] for info in ckt_info]
            ckt_info_property = [str(info[1]) for info in ckt_info]

            if title:
                print >>outplace, ','.join(ckt_info_name)
            print >>outplace,','.join(ckt_info_property)
        
            if file_open:
                outplace.close()

        except:
            print 'error: cannot collect ckt info'
            if file_open:
                outplace.close()
            return False