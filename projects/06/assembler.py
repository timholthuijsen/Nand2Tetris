import sys


"""Dictionaries containing binary translations"""
comp_dict = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }

dest_dict = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }

jump_dict = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }

symbols_dict = {
    "SP" : 0,
    "LCL" : 1,
    "ARG" : 2,
    "THIS" : 3,
    "THAT" : 4,
    "R0" : 0,
    "R1" : 1,
    "R2" : 2,
    "R3" : 3,
    "R4" : 4,
    "R5" : 5,
    "R6" : 6,
    "R7" : 7,
    "R8" : 8,
    "R9" : 9,
    "R10" : 10,
    "R11" : 11,
    "R12" : 12,
    "R13" : 13,
    "R14" : 14,
    "R15" : 15,
    "SCREEN" : 16384,
    "KBD" : 24576
    }

"""Gets the file to be used from the command line"""
asm_filename =str(sys.argv[1])


"""Reads the asm file"""
text = open(asm_filename).read()




        
"""Filters the text to only program  lines"""
def clean_lines(lines):
    new_lines = []
    for line in lines:
        split_line = line.split("//")
        clean_line = split_line[0].replace(' ','')
        if clean_line:
            new_lines.append(clean_line)
    return new_lines

"""Translates a line to binary"""
def translate(line):
    #filtering out labels
    if line.startswith("("):
        return None
    #A commands
    elif line.startswith("@"):
        translated_line = A_command(line)
    #C commands
    else:
        translated_line = C_command(line)
    return translated_line

"""Translates a C command to Hack"""      
def C_command(line):
    #Setting dest and jump to default
    dest = "000"
    jump = "000"
    #Jump
    split_line = line.split(";")
    if len(split_line) == 2:
        jump = parse_jump(split_line[1])
        
    #Dest
    split_line2 = split_line[0].split("=")
    if len(split_line2)==2:
        dest = parse_dest(split_line2[0])
    
    #comp
    comp = parse_comp(split_line2[-1])
    
    #Return the translated C_command
    return "111" + comp + dest + jump
        
"""Returns translated dest"""
def parse_dest(dest):
        return dest_dict[dest]

"""Returns translated comp"""
def parse_comp(comp):
        return comp_dict[comp]
    
"""Returns translated jump"""
def parse_jump(jump):
        return jump_dict[jump]


"""Parses label symbols and updates the symbol dict"""
def parse_labels(lines):
    count = 0
    for line in lines:
        if line.startswith('('):
            symbols_dict[line[1:-1]] = count
        else:
            count += 1
"""Translates an A command to Hack"""    
def A_command(line):
    symbol_adder = 16
    com = line[1:]
    if com.isnumeric():
        return "0" + bin(int(com))[2:].zfill(15)
    #in case of a new symbol
    elif not com in symbols_dict:
        symbols_dict[com] = symbol_adder
        symbol_adder = symbol_adder + 1
    return '0' + bin(int(symbols_dict[com]))[2:].zfill(15)
        
        
    


"""Takes asm text as an input and outputs binary code"""        
def parse(text):
        result = ""
        lines = text.splitlines()
        lines = clean_lines(lines)
        parse_labels(lines)
        
        for line in lines:
            hack_line = translate(line)
            if hack_line:
                result += hack_line + "\n"
        
        return result
        print(lines)
        
hack_text = parse(text)        
        
#Generates the hack filename
def make_hack_filename(asm_filename):
    return ''.join(asm_filename.split('.')[:-1]) + ".hack"

#Creates a hack file
hack_filename = make_hack_filename(asm_filename)
try:
   open(hack_filename, 'w').write(hack_text)
except OSError:
        raise
        
        
        
        
        
