minickt
=======

Analyzer and simulator of logic circuit

### Environments

You have to install `Python2` (python2.7.6 is the version in development).
And you do not need to install minickt, it's just a script.

### Run minickt

```sh
$ python minickt.py 
```

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

### A quick start

Here I will give you a quick start of doing circuit analyzing.

#### Read a logic circuit

Command "read" can read a logic circuit with specified parser.

```
[ miniCkt ] >> read mycircuit.v by primitive
read mycircuit.v ...
success: circuit "top(mycircuit.v) is in circuit manager now
```

Commmand "ls -p" or "ls_parser" can list all avalible parsers.
You can write parser by yourself to fit the circuit format.

Now we can use cmd "ls -c" or "ls_ckt" to list all circuits in circuit manager of minickt.

```
[ miniCkt ] >> ls -c
there are 1 circuits now
[0] top(mycircuit.v) <--- current
```

It means that minickt can hold several circuits not just single one!


