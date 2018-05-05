"""
    Turing Machine Program Inerpreter
    Author: Max Miller
"""

"""
TURING MACHINE EXAMPLE:

//First line defines the start state with syntax 'S_{start state}'
S 0
//Second line defines the input tape with syntax 'T_{tape}'
T AAABAAA A AAAA
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
//Ends program
END 
"""

import sys

DEBUG = True
VERBOSE = False
FINITE = False # Set to true only if you want a finite tape turing machine

# Command structure
START = 'start'
SUB = 'sub '
SUB_END = 'endsub'
LINE = '{};'
SUB_LINE = '\t'
TAPE = 't '
STATE_LIST = 's ' # Always start state list with first state
POS = 'p '
END = 'end'
SUB_CALL = 'call ' # 2 call add 3 <-- if in state 2, call ADD, when done move to state 3
COMMANDS = {'>>': 1, '<<': -1}


def log(cat, item, line_count):
    return 'Line {}: {}: {}'.format(line_count, cat, item)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def main(file_name='test.tm'):

    f = file(file_name, 'rb')

    current_tape_position = 0
    current_tape = ''
    current_state = 0

    in_sub = False
    submachine_list = {}
    current_sub_name = ''
    current_machine = {}
    current_machine_list = {}
    current_state_list = []
    
    master_state_list = []
    master_command_dict = {}
    line_count = 1
    
    for current_line in f:
        if current_line.startswith('//'):
            continue
        line=current_line.lower()
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        
        if not in_sub:
            if line.startswith(STATE_LIST):
                line = line.replace(STATE_LIST, '')
                master_state_list = line.split(' ')
                current_state = int(master_state_list[0])
            elif line.startswith(TAPE):
                line = line.replace(TAPE, '')
                current_tape = line
                #print 'Tape Found'
            elif line.startswith(POS):
                line = line.replace(POS, '')
                current_tape_position = int(line)
            elif line.startswith(SUB):
                if master_state_list == '':
                    print log('Error', 'Submachine found before start state defined', line_count)
                    return
                if current_tape == '':
                    print log('Error', 'Submachine found before tape defined', line_count)
                    return
                #print 'Sub found'
                in_sub = True
                current_machine_list = {}
                current_machine = {}
                line = line.replace(':', '')
                current_sub_name = line.strip(SUB)
            elif is_number(line[0:line.find(' ')]):
                if master_state_list == '':
                    print log('Error', 'Command found before start state defined', line_count)
                    return
                if current_tape == '':
                    print log('Error', 'Command found before tape defined', line_count)
                    return
                #print 'Command found'
                if master_command_dict.get(int(line[0:line.find(' ')])) is not None:
                    #print 'Already Command'
                    if not line.endswith(';'):
                        print log('Error', 'Command does not end with a \';\': {}'.format(line), line_count)
                        return
                    line = line.replace(';', '')
                    split_line = line.split(' ')
                    if len(split_line) > 4:
                        print log('Error', 'Command has too many arguments: {}'.format(line), line_count)
                        return
                    if len(split_line) < 4:
                        print log('Error', 'Command has too few arguments: {}'.format(line), line_count)
                        return
                    master_command_dict[int(line[0:line.find(' ')])][split_line[1]] = split_line[2:len(split_line)]
                else:
                    if not line.endswith(';'):
                        print log('Error', 'Command does not end with a \';\': {}'.format(line), line_count)
                        return
                    line = line.replace(';', '')
                    split_line = line.split(' ')
                    if len(split_line) > 4:
                        print log('Error', 'Command has too many arguments: {}'.format(line), line_count)
                        return
                    if len(split_line) < 4:
                        print log('Error', 'Command has too few arguments: {}'.format(line), line_count)
                        return
                    master_command_dict.update({int(line[0:line.find(' ')]): {split_line[1]: split_line[2:len(split_line)]}})
                    
        else:
            if line.startswith('\t' + STATE_LIST):
                line = line.replace(STATE_LIST, '')
                line = line.replace('\t', '')
                current_state_list = line.split(' ')
                #print 'State list found'
            elif line.startswith('\t'):
                line = line.replace('\t', '')
                if is_number(line[0:line.find(' ')]):
                    if master_state_list == '':
                        print log('Error', 'Command found before start state defined', line_count)
                        return
                    if current_tape == '':
                        print log('Error', 'Command found before tape defined', line_count)
                        return
                    #print 'Command found'
                    if current_machine_list.get(int(line[0:line.find(' ')])) is not None:
                        #print 'Already sub'
                        if not line.endswith(';'):
                            print log('Error', 'Command does not end with a \';\': {}'.format(line), line_count)
                            return
                        line = line.replace(';', '')
                        split_line = line.split(' ')
                        if len(split_line) > 4:
                            print log('Error', 'Command has too many arguments; {}'.format(line), line_count)
                            return
                        if len(split_line) < 4:
                            print log('Error', 'Command has too few arguments; {}'.format(line), line_count)
                            return
                        current_machine_list[int(line[0:line.find(' ')])][split_line[1]] = split_line[2:len(split_line)]
                    else:
                        if not line.endswith(';'):
                            print log('Error', 'Command does not end with a \';\': {}'.format(line), line_count)
                            return
                        line = line.replace(';', '')
                        split_line = line.split(' ')
                        if len(split_line) > 4:
                            print log('Error', 'Command has too many arguments; {}'.format(line), line_count)
                            return
                        if len(split_line) < 4:
                            print log('Error', 'Command has too few arguments; {}'.format(line), line_count)
                            return
                        current_machine_list.update({int(line[0:line.find(' ')]): {split_line[1]: split_line[2:len(split_line)]}})
                        
            elif line.startswith(SUB_END):
                #print 'End sub'
                submachine_list.update({current_sub_name: {'commands': current_machine_list, 'state_list': current_state_list}})
                in_sub = False
        if DEBUG: print line
        line_count+=1
        
    if DEBUG:
        print '-------------------------'
        print master_command_dict
        print current_tape
        print master_state_list
        print submachine_list
        print current_tape
        print current_tape_position
        print '-------------------------'

    working_tape = current_tape
    working_tape = working_tape.replace(' ', '_')
    print 'Starting Tape:\t\t{}'.format(current_tape.replace(' ', '_'))

    while True:
        try:
            current_command = ''
            current_commands = master_command_dict[current_state]
            if VERBOSE:
                print '{}\n\tCurrent state: {}'.format('NEXT', current_state)
                position_tape = ' ' * len(working_tape)
                position_tape = position_tape[:current_tape_position] + '|' + position_tape[current_tape_position:]
                print '\n\t{}\n\t{}\n'.format(working_tape, position_tape)
            #print current_commands
            if current_commands.get('call') is not None:
                #print 'Sub Machine started'
                current_state = int(current_commands.get('call')[1])

                current_machine = submachine_list[current_commands.get('call')[0]]
                current_machine_state = int(current_machine['state_list'][0])
                current_machine_commands = current_machine['commands']
                if VERBOSE: print '-------------------------------\nSub Machine {} started\n-------------------------------'.format(current_commands.get('call')[0])
                sub_started = True
                while sub_started:
                    if VERBOSE:
                        print '{}\n\tCurrent submachine state: {}'.format('NEXT', current_machine_state)
                        position_tape = ' ' * len(working_tape)
                        position_tape = position_tape[:current_tape_position] + '|' + position_tape[current_tape_position:]
                        print '\n\t{}\n\t{}\n'.format(working_tape, position_tape)
                    tape_value = working_tape[current_tape_position]
                    if DEBUG: print 'WK: {}'.format(working_tape)
                    if DEBUG: print 'TP: {}'.format(tape_value)
                    if DEBUG: print 'MS: {}'.format(current_machine_state)
                    try:
                        current_command = current_machine_commands[current_machine_state][tape_value][0]
                        if VERBOSE: print '\tCurrent command: {}'.format(current_command)
                        if DEBUG: print 'SUB CC: {}'.format(current_command)
                        if not '>>' in current_command and not '<<' in current_command:
                            if not '_' in current_command:
                                working_tape = working_tape[0:current_tape_position] + current_command + working_tape[current_tape_position+1:]
                            else:
                                working_tape = working_tape[0:current_tape_position] + '_' + working_tape[current_tape_position+1:]
                                
                        else:
                            current_tape_position += COMMANDS[current_command]
                        current_machine_state = int(current_machine_commands[current_machine_state][tape_value][1])
                    except KeyError as e:
                        if DEBUG: print(e)
                        sub_started = False
                        if VERBOSE: print '-------------------------------\nEND SUB MACHINE\n-------------------------------'
            else:
                tape_value = working_tape[current_tape_position]
                if DEBUG: print "TAPE: {}".format(tape_value)
                current_command = current_commands[tape_value][0]
                if DEBUG: print 'CC: {}'.format(current_command)
                if VERBOSE: print '\tCurrent command: {}'.format(current_command)
                if not '>>' in current_command and not '<<' in current_command:
                    if current_command is not '_':
                        working_tape = working_tape[0:current_tape_position] + current_command + working_tape[current_tape_position+1:]
                    else:
                        working_tape = working_tape[0:current_tape_position] + '_' + working_tape[current_tape_position+1:]
                else:
                    current_tape_position += COMMANDS[current_command]
                current_state = int(current_commands[tape_value][1])
        except KeyError as e:
            if DEBUG: print(e)
            break
        except IndexError as e:
            if DEBUG: print(e)
            if DEBUG: print(current_tape_position)
            if current_tape_position <= 0:
                if DEBUG: print("Went Behind")
                working_tape = '_' + working_tape
            elif current_tape_position >= len(working_tape):
                if DEBUG: print("Went Ahead")
                working_tape += '_'

            if FINITE: break
        except KeyboardInterrupt:
            if DEBUG: print('Manual Interupt')
            break

    print 'End Tape:\t\t{}'.format(working_tape)
        

 
                                            
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(file_name=sys.argv[1])
    else:
        main()
