//First line defines the start state with syntax 'S_{start state}'
S 0
//Second line defines the input tape with syntax 'T_{tape}'
T AAA AAA A AAAA
//Third line defines the start position with syntax 'P_{start position}'
P 0
//Starts the main program body
START
//Defines a submachine
SUB add:
        //Defines a submachine start state
	S 0
	//Command syntax defined below
	0 A >> 0;
	0 B >> 0;
	0 _ A 1;
	//Submachine has no state 1, moves out of machine
ENDSUB
SUB foo:
	S 0
	0 A C 0;
	0 C >> 1;
	1 A B 2;
ENDSUB
//Syntax for calling a submachine is '{state} call {machine name} {go to state}'
0 call add 1;
1 call foo 2;
//Syntax for defining a command is '{state} {tape reading} {do} {go to state}'
2 A ! 3;
2 B ! 3;
3 ! >> 0;
//Ends program
END 