"""
    Turing Machine Package Handler
    Author: Max Miller
    Purpose: To allow for packages and code organization in large TM processes
"""
import os
import fnmatch

IMPORT_STATEMENT = "#import "
PACKAGE_EXTENSION = ".tmpk"


def find_local_packages(local_file):
	current_directory_path = os.path.dirname(os.path.realpath(local_file))
	if current_directory_path != '' or current_directory_path is not None:
		matches = []
		for root, dirnames, filenames in os.walk(current_directory_path):
		    for filename in fnmatch.filter(filenames, '*{}'.format(PACKAGE_EXTENSION)):
		        matches.append(os.path.join(root, filename))
		print(matches)
	else:
		return


def read_package_file(local_file):
	f = file(local_file, 'rb')

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

def main():
	find_local_packages(__file__)

if __name__ == "__main__":
	main()