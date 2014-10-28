minickt
=======

Analyzer and simulator of logic circuit (Version-0.8)

* [Environments](#environments)
 * [Python](#python)
 * [SAT solver](#sat-solver)
* [How to get minickt](#how-to-get-minickt)
* [Run minickt](#run-minickt)
* [List commmands and get help](#list-commands-and-get-help)
* [Circuit I/O](#circuit-io)
  * [Read a logic circuit](#read-a-logic-circuit)
  * [Rename](#rename)
  * [Write out a circuit](#write-out-a-circuit)
* [Circuit Analysis](#circuit-analysis)
  * [Get circuit information](#get-circuit-information)
  * [Show graph](#show-graph)
* [Circuit Simulation](#circuit-simulation)
  * [List gates and their information](#list-gates-and-their-information)
  * [Set gate value](#set-gate-value)
  * [Simulation](#simulation)
* [Circuit Reasoning](#circuit-reasoning)
* [Circuit Manager] (#circuit-manager)
  * [Circuit switching](#circuit-switching)
  * [Remove circuit](#remove-circuit)
  * [Get cone circuit](#get-cone-circuit)
* [Equivalence checking](#equivalence-checking)
  * [Structural equivalence checking](#structural-equivalence-checking)
    * [SEC for two circuits](#sec-for-two-circuits)
    * [SEC for cones of current circuit](#sec-for-cones-of-current-circuit)
  * [Functional equivalence checking](#functional-equivalence-checking)
* [Circuit SAT](#circuit-sat)
* [Shell commands](#shell-commands)
* [minickt script](#minickt-script)
 * [simple_io.sc with sample.v](#simple_iosc-with-samplev)
 * [simulation.sc with sample2.v](#simulationsc-with-sample2v)

===

### Environments

#### Python

You have to install `Python2` (python2.7.6 is the version in development).
* [Python](https://www.python.org/)

You should install following python packages: 
* [matplotlib](http://matplotlib.org/)
* [networkx](https://networkx.github.io/)

#### SAT solver

Some commands of minickt is based on external SAT solver, and lingeling is default.<br />
You can get it from [lingeling](http://fmv.jku.at/lingeling/) and compiled to fit your os version.<br >
(The one in directory `bin` is possible not fit your OS.)

Other SAT solvers are also avalible, just put the excution file to directory `bin`. 

Here are some suggested solvers:

* [ MiniSAT ](http://minisat.se/)
* [ glucose ](http://www.labri.fr/perso/lsimon/glucose/)

---

### How to get minickt

Just download from github tarball:
* [download minickt](https://github.com/dokelung/minickt/tarball/v0.7.1)

User also can install minickt from pip:

```sh
$ pip install minickt
```

If there is new version, use upgrade:

```sh
$ pip install minickt --upgrade
```

Here is the pypi page of minickt:

* [Pypi page of minickt](https://pypi.python.org/pypi/minickt/)

Note that if you install minickt from pip, you will not get the scripts and benches here.

---

### Run minickt

If you do not install the packages and script, just `cd` to the top directory:

```sh
$ ./minic
```

If you have already installed it, you should do configuring first:

```sh
$ minic configure
```

you will find that a directory named `minickt` including 3 sub-directories with nothing: `bin`, `bench` and `script`.

* Remember to put your lingeling solver to dir `bin`.
* The needed benchmarks and scripts can be downloaded here.

Then you just excute it anywhere:

```sh
$ minic
```

and you can run any avalible command by entering it after the prompt `[ miniCkt ] >> `:

```
[ miniCkt ] >> exit
```

Command `exit` will terminate minickt.

---

### List commands and get help

Use "?" to list all avalible commands in minickt.

```
[ miniCkt ] >> ?

Documented commands (type help <topic>):
========================================
cc       encode        help       ls_writer  sat         shell     
chname   eval          loadsc     read       sat_reason  show      
cmd      exit          ls         reason     sec         show_ckt  
collect  gen_cone_ckt  ls_ckt     reset      set         show_ratio
cone     get           ls_parser  rm         sg          write
```

or use "cmd" to get the short description of all commands

```
[ miniCkt ] >> cmd
```

If you want to know the details of a specified cmd, use `help<cmd>` or `?<cmd>`:

```
[ miniCkt ] >> ?shell
[ miniCkt ] >> help shell
```

---

### Circuit I/O

Let me introduce you the commands of circuit IO.

#### Read a logic circuit

Command `read` can read a logic circuit with specified parser.

```
[ miniCkt ] >> read mycircuit.v by primitive
read mycircuit.v ...
success: circuit "top(mycircuit.v) is in circuit manager now
```

Commmand `ls -p` or `ls_parser` can list all avalible parsers.<br />
You can write parser by yourself to fit the circuit format.

#### Rename

The default name of a circuit is `top(CIRCUIT_FILE_NAME)`.<br />
You can use `chname` to rename it.

```
[ minickt ] >> chname ckt1
```

Now we can use cmd `ls -c` or `ls_ckt` to list all circuits in circuit manager of minickt.

```
[ miniCkt ] >> ls -c
there are 1 circuits now
[0] ckt1 <--- current
```

It means that minickt can hold several circuits not just single one! <br />
I will talk about this later.

#### Write out a circuit

use `write` to write out the circuit.

```
[ miniCkt ] >> write ckt1.v by primitive
```

The format of `write` is similar to `read`.<br />
Commmand `ls -w` or `ls_writer` can list all avalible writers.<br />
You can write your own writer, too.

---

### Circuit Analysis

Here are some methods of doing analyzing

#### Get circuit information

Command `get` can get the specified property of circuit.

```
[ miniCkt ] >> get gate_num
```

try `?get` to know the properies that can be acquired by `get`.

#### Show graph

`show_ckt` or `show -c`  will show a circuit graph by taking each logic gate as a node.<br />
`show_ratio` or `show -r` will show a pie chart of gates ratio.

---

### Circuit Simulation

This part will introduct the method to set the gate values and doing simulation.

#### List gates and their information

`sg` can list a gate or a gate set in current circuit.<br />
For example, if you want to see all of the gates in circuit:

```
[ miniCkt ] >> sg all
...
AND:n28 OR:n1017 OR:n230 XOR:n1101 
```

Note that the gate format is "GATE_TYPE:GATE_NAME".<br />
If the gate is PO gate, the GATE_TYPE will be composed with PO and its type, like "PO-XOR".

Or you want to see the PI gate:

```
[ miniCkt ] >> sg pi
```

Or you just want to see the PO gate named po_0:

```
[ miniCkt] >> sg po_0
```

Even you can mix them:

```
[ miniCkt ] >> sg pi, po_0
```

We could add some additional options to see more information.

```
[ miniCkt ] >> sg pi -ivo
```

`-i` will list the fanins of each gate.<br />
`-o` will list the fanouts of each gate.<br />
`-v` will list the values of each gates.


#### Set gate value

You can assign value to a "gate" or a "gate set".<br />
For example, we want to assign one(True) to all PI gates:

```
[ miniCkt ] >> set pi 1
```

If you want to reset all gates(it means you want to let all gates value be unknown):

```
[ miniCkt ] >> reset
```

#### Simulation

After setting the gate values of circuit, we can do simulation with cmd `eval` which means evaluate:

```
[ miniCkt ] >> eval
```

We commonly use `sg -v` to check the evalation results.

---

### Circuit Reasoning

minickt also supports circuit reasoning. <br />
There are two ways to do that: cmd `reason` and `sat_reason`.

After doing assignments to some gates , we can use `reason` to deduce other gates' values:

```
[ miniCkt ] >> reset
[ miniCkt ] >> set po 1
[ miniCkt ] >> reason
```

If some conflict occur, reasoning will fail.<br />
Note that this command just deduces the values which can be implied directly, it does not do any guess.

If you want to do a complete reasoning, use `sat_reason`:

```
[ miniCkt ] >> sat_reason po_0 1
```

User should be ware of the differences between `read` and `sat_reason`.<br />
`sat_reason` does not depend on the current assignments, it depends on gates and their values specified with command.

Also, this command use an external SAT solver which is located in directory `bin` with name `lingeling`.<br />
You should check the name and the version fo SAT solver are avalible, otherwise it will result in fail.

---

### Circuit Manager

You could add several circuits to minickt because it can hold multiple circuits.(I think it's really cool!)

#### Circuit switching

Assume we have two circuits in circuit manager(the current arrow points the "current circuit"):

```
[ miniCkt ] >> ls -c
there are 2 circuits now
[0] ckt1 <--- current
[1] ckt2
```

Current circuit is the circuit which can be controled directly by commands.

User can use `cc` to switch to the circuit we want to control and do something.

```
[ miniCkt ] >> cc 1
[ miniCkt ] >> ls -c
there are 2 circuits now
[0] ckt1
[1] ckt2 <--- current
```

#### Remove circuit

`rm` can remove the current circuit(if no option) or remove the i-th circuit.

```
[ miniCkt ] >> rm
[ miniCkt ] >> rm 0
```

#### Get cone circuit

You can specify a gate to get its `cone` circuit.

```
[ miniCkt ] >> cone po_0
```

It generates a new circuit with default name "coneckt"(it can be specified).

But sometimes we want an independent cone circuit(the specified gate should be taken as a PO gate), we can do by:

```
[ miniCkt ] >> cone po_0
[ miniCkt ] >> write ckt1.v by primitive
[ miniCkt ] >> rm
[ miniCkt ] >> read ckt1.v by primitive
```

or use a combinational command `gen_cone_ckt` which is equal to the commands above.

```
[ miniCkt ] >> gen_cone_ckt po_0
```

---

### Equivalence checking

#### Structural equivalence checking

There are two ways to check the equivalence of two single-outpu circuits.<br />
Command `sec` helps us doing these.

##### SEC for two circuits

If you want to do SEC for two circuits in circuit manager of minickt, you have to use `CKT_ID` to specify circuits:

```
[ miniCkt ] ls -c
there are 1 circuits now
[0] ckt1 <--- current
[1] ckt2
[ miniCkt ] sg po
[ miniCkt ] >> sec 0.out 1.out
```

It will compare ckt1's cone(its root is gate "out") and ckt2's cone(its root is gate "out").

##### SEC for cones of current circuit

If you want to do SEC for two cones of urrent circuit, just give the names of cone roots:

```
[ minickt ] >> sec gate1 gate2
```

#### Functional equivalence checking

We use miter to do FEC in minickt and now just supports "single output ckt".

So make sure two things:

1. The specified ckts should be single output ckt.
2. Their inputs can be mapped.(It means the corresponding inputs should have same name.)

You can use `fec` to check functional equivalence of two circuits in circuit manager:

```
[ miniCkt ] >> ls -c
there are 2 circuits now
[0] ckt1 <--- current
[1] ckt2
[ miniCkt ] >> fec 0 1
```

Above operation will check the functional equivalence of ckt1 and ckt2.

We use SAT solver(default by lingeling solver and TST encoding) to get the satisfiability of miter.<br >
If the result is SAT: it means they are not FEC.<br >
If the result is UNSAT: it means they are FEC.


Also, the miter of them will be created:

```
[ miniCkt ] >> ls -c
there are 3 circuits now
[0] c1
[1] c2
[2] miter <--- current
```

---

### Circuit SAT

To know the circuit satisfiability, minickt supports circuit encoding and circuit sat solving.

`encode` can be use to encode a circuit to a CNF file:

```
[ miniCkt ] >> encode by PTST to ckt1.cnf
```

`PTST` means "pure tseitin transformation" that is we do not assign value to PO.<br />
If you want to have an traditional circuit sat instance, use method `TST`:

```
[ miniCkt ] >> encode by TST to ckt1.cnf
```

If you want to solve circuit SAT in minisat, you could use cmd `sat`:

```
[ miniCkt ] >> sat by lingeling with PTST
```

You should specify the sat solver(and its options) and encoding method.

---

### Shell commands

Use `!` or cmd `shell` to run a shell command.

```
[ miniCkt ] >> !ls
[ miniCkt ] >> shell ls
```

---

### minickt script

minickt allows user to write scripts and execute them.

Just put wanted commands in a scirpt file then use cmd `loadsc` to load script:

```
[ miniCkt ] >> loadsc ./script/simulation.sc
```

or you can run the script in your os shell with `script` option:

```sh
$ minic script ./script/simulation.sc
```

There are several sample circuits and scripts in the directory `bench` and `script` respectively.
Now I will show you some of them.

#### simple_io.sc with sample.v

```
read ./bench/sample.v by primitive
chname sample
write ./bench/sample_copy.v by primitive
exit
```

This script(`simple_io.sc`) will read `sample.v` by primitive parser.
Then change its name to "sample".
Note that if you want to safely write out the circuit with default primitive writer, you should always use `chname` for guaranteeing there is no "()" in module name.
In the end, write out the circuit with name "sample_copy.v" and exit minickt shell.

#### simulation.sc with sample2.v

```
read ./bench/sample2.v by primitive
sg all -v
set a b c 1
set d 0
eval
sg out -v
exit
```

First, we read `sample2.v` by using primitive parser.
`sg all -v` let us know all names of gates with their values.
Then we set PI a,b,c and d with value 1,1,1,0 respectively.
`eval` does the simulaiton and we sg again for checking the value of PO "out".

---






