minickt
=======

Analyzer and simulator of logic circuit

---

### Environments

You have to install `Python2` (python2.7.6 is the version in development).<br />
And you do not need to install minickt, it's just a script.

If you want to use the complete functions of minickt, you should install python packages: `matplotlib` and `networkx`.

---

### Run minickt

```sh
$ python minickt.py 
```

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

#### Get circuit infomation

Command `get` can get the specified property of circuit.

```
[ miniCkt ] >> get gate_num
```

try `?get` to know the properies that can be acquired by `get`.

#### Show graph

`show_ckt` or `show -c`  will show a circuit graph by taking each logic gate as a node.

`show_ratio` or `show -r` will show a pie chart of gates ratio.

---

### Circuit Simulation





