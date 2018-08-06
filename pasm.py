#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser
from terminaltables import SingleTable
from termcolor import colored
import sys
import subprocess
import linecache
import commands
import readline 

config_parser = SafeConfigParser()
config_parser.read(__file__.replace('pasm.py', '')+'config.ini')


syntax = config_parser.get('assembler', 'syntax')
arch = config_parser.get('assembler', 'arch')
bits = config_parser.get('assembler', 'bits')
os = config_parser.get('assembler', 'os')
mode = config_parser.get('assembler', 'starting_mode')
endian_prompt = config_parser.get('assembler', 'endian')
#config_parser.set('assembler', 'syntax', res.SYNTAX)

class color:
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
        BLINK = '\033[5m'
        DIM = '\033[2m'
        HIDDEN = '\033[8m'
        MAGENTA = '\033[95m'
        LIGHT_MAGENTA = '\033[95m'

def bold(msg):
    return "{}{}{}".format(color().BOLD,msg,color().END)

def red(msg):
    return "{}{}{}".format(color().RED,msg,color().END)

def blue(msg):
    return "{}{}{}".format(color().BLUE,msg,color().END)

def green(msg):
    return "{}{}{}".format(color().GREEN,msg,color().END)

def cyan(msg):
    return "{}{}{}".format(color().CYAN,msg,color().END)

def magenta(msg):
    return "{}{}{}".format(color().MAGENTA,msg,color().END)

def underline(msg):
    return "{}{}{}".format(color().BOLD,msg,color().END)

def print_error(msg):
        p = '%s %s' % (colored('[X]', 'red'), msg)
        print p

def print_good(msg):
        p = '%s %s' % (colored('[+]', 'green'), msg)
        print p

def print_underline(msg):
        p = color().UNDERLINE+msg+color().END
        print p

def print_wrn(msg):
        p = '%s %s' % (colored('[WARNING]', 'yellow'), msg)
        print p

def print_info(msg):
        info = '[INFO]%s' % msg
        print info

def print_star(msg, color='magenta'):
        p = '%s%s' %(colored('*', color), msg)
        print p

def print_exception():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

__version__ = "1.0"
sun = "{}{}o{}{}{}O{}".format(color.BLINK, color.RED, color.END, color.BLINK, color.YELLOW, color.END)


print "\n *******      **      ******** ****     ****"
print "/**////**    ****    **////// /**/**   **/**"
print "/**   /**   **//**  /**       /**//** ** /**"
print "/*******   **  //** /*********/** //***  /**"
print "/**////   **********////////**/**  //*   /**"
print "/**      /**//////**       /**/**   /    /**"
print "/**      /**     /** ******** /**        /**"
print "//       //      // ////////  //         // \n"
print "{} PASM assembler ver. {}".format(red("<.>"), __version__)
print "{} Created by: TheSecondSun {} (thescndsun@gmail.com)".format(red("<.>"), sun)
print "\n"

class Rasm2:
    def __init__(self):
        pass
        
    def raw_asm(self, instr):
        if endian_prompt == 'little':
            self.endian = ''
        else:
            self.endian = '-e'
        op = commands.getoutput(('rasm2 -s {} -a {} -b {} -k {} {} "{}"'.format(syntax, arch, bits, os, self.endian, instr)))
        return binascii.unhexlify(op)

    def asm(self, instr):
        if endian_prompt == 'little':
            self.endian = ''
        else:
            self.endian = '-e'
        op = commands.getoutput(('rasm2 -s {} -a {} -b {} -k {} {} "{}"'.format(syntax, arch, bits, os, self.endian, instr)))
        return op

    def disasm(self, opcodes):
        if endian_prompt == 'little':
            self.endian = ''
        else:
            self.endian = '-e'
        instr = commands.getoutput(('rasm2 -s {} -a {} -b {} -k {} -D {} {}'.format(syntax, arch, bits, os, self.endian, opcodes)))
        return instr

    def raw_disasm(self, opcodes):
        if endian_prompt == 'little':
            self.endian = ''
        else:
            self.endian = '-e'
        instr = commands.getoutput(('rasm2 -s {} -a {} -b {} -k {} -d {} {}'.format(syntax, arch, bits, os, self.endian, opcodes)))
        return instr

Rasm2 = Rasm2()

cmds = ["help", "os", "syntax", "arch", 
        "bits", "asm", "disasm", "c", 
        "exit", "endian"]

def main():
    global syntax
    global arch
    global bits
    global os
    global mode
    global endian_prompt
    cmd_loop = True
    while cmd_loop:
        try:
            input = raw_input("{}:[{}][{}][{}][{}][{}]\n-➤ ".format(bold(underline(mode)), 
                cyan(arch), red(bits), blue(os), green(endian_prompt),magenta(syntax)))
        except KeyboardInterrupt:
            print "\n"
            print_info("Exiting...")
            exit()
        cmd = input.split()[0]
        args = input.split()[1::]
        if cmd not in cmds:
            if mode == "asm":
                line_to_asm = "{} {}".format(cmd, ' '.join(args))
                out = Rasm2.asm(line_to_asm)
                if "invalid" in out:
                    print_error("Unable to assemble '{}': invalid mnemonic".format(line_to_asm))
                elif "Warning" in out:
                    print_wrn(' '.join(out.split()[1:-1]))
                    print '\n'
                else:
                    nulls = out.count("00")
                    def nsplit(s, n):
                        return [s[k:k+n] for k in xrange(0, len(s), n)]
                    print_good("Length: {} bytes".format(bold(len(out)/2)))
                    if nulls != 0:
                        print_error("Found {} nullbytes".format(red(bold(nulls))))
                    print "Raw bytes:   {}".format(out.replace('00', red(bold("00"))))
                    print "Hex escaped: \\x{}".format('\\x'.join(nsplit(out,2)).replace('00', red(bold("00"))))
                    print '\n'
            elif mode == "disasm":
                opcodes = "{} {}".format(cmd, ''.join(args))
                line_to_disasm = opcodes.replace('\\x', '').replace('0x', '').replace(',', '')
                out = Rasm2.disasm(line_to_disasm)
                if "invalid" in out:
                    print_error("Unable to disassemble '{}': invalid instruction".format(line_to_disasm))
                elif "Warning" in out:
                    print_wrn(out.replace("Warning:", ''))
                    print "\n"
                else:
                    print_good("Disassembly of '{}':".format(opcodes))
                    print out
                    print "\n"
        elif cmd == "asm":
            if "-h" in args:
                    print "\nUSAGE: asm [-h]"
                    print "DESCRIPTION: Change mode to assembly\n"
            else:
                mode = "asm"
                print_good("Changed mode to asm\n") 

        elif cmd == "disasm":
            if "-h" in args:
                    print "\nUSAGE: disasm [-h]"
                    print "DESCRIPTION: Change mode to disassembly\n"
            else:
                mode = "disasm"
                print_good("Changed mode to disasm\n")
        elif cmd == "os":
            try:
                oses = ["linux", "windows", "osx"]
                new_os = args[0]
                if "-h" in args:
                    print "\nUSAGE: os [-h] {linux|windows|osx}"
                    print "DESCRIPTION: Specify OS to set\n"
                else:
                    if new_os not in oses:
                        print_error("No such OS")
                    else:
                        os = new_os
                        print_good("Changed OS to {}\n".format(os))
            except:
                print_error("Specify OS")
        elif cmd == "bits":
            try:
                bts = ["16", "32", "64"]
                new_bits = args[0]
                if "-h" in args:
                    print "\nUSAGE: bits [-h] {16|32|64}"
                    print "DESCRIPTION: Specify number of bits\n"
                else:
                    if new_bits not in bts:
                        print_error("Wrong bits number")
                    else:
                        bits = new_bits
                        print_good("Changed bits to {}\n".format(bits))
            except:
                print_error("Specify the number of bits")
        elif cmd == "syntax":
            try:
                syntaxes = ["intel", "att"]
                new_syntax = args[0]
                if "-h" in args:
                    print "\nUSAGE: syntax [-h] {intel|att}"
                    print "DESCRIPTION: Specify the syntax\n"
                else:
                    if new_syntax not in syntaxes:
                        print_error("Wrong syntax")
                    else:
                        syntax = new_syntax
                        print_good("Changed syntax to {}\n".format(syntax))
            except:
                print_error("Specify the syntax")
        elif cmd == "arch":
            try:
                new_arch = args[0]
                if "-h" in args:
                    print "\nUSAGE: arch [-h] ARCHITECTURE"
                    print "DESCRIPTION: Set the architecture. To list available architectures, type 'arch ?'\n"
                else:
                    if new_arch == "?":
                        print '\nMODE  BITS       NAME        LICENSE DESCRIPTION'
                        print '====  ====       ====        ======= ==========='
                        print commands.getoutput("rasm2 -L")
                    else:
                        if new_arch not in commands.getoutput("rasm2 -L"):
                            print_error("No such architecture\n")
                        else:
                            arch = new_arch
                            print_good("Changed arch to {}\n".format(arch))
            except:
                print_error("Specify the arch")
        elif cmd == "endian":
            try:
                endians = ['big', 'little']
                new_endian = args[0]
                if "-h" in args:
                    print "\nUSAGE: endian [-h] {big|little} }"
                    print "DESCRIPTION: Set the endianess\n"
                else:
                    if new_endian not in endians:
                        print_error("No such endian\n")
                    else:
                        endian_prompt = new_endian
                        print_good("Changed endian to {}\n".format(endian_prompt))
            except:
                print_error("Specify the endianess")
        elif cmd == "c":
            if "-h" in args:
                print "\nUSAGE: c [-h]"
                print "DESCRIPTION: Clear the screen\n"
            else:
                subprocess.call("clear")
        elif cmd == "exit":
            if "-h" in args:
                print "\nUSAGE: exit [-h]"
                print "DESCRIPTION: Exit the program\n"
            else:
                cmd_loop = False
                print_info("Exiting...")
        elif cmd == "help":
            if "-h" in args:
                print "\nUSAGE: help [-h]"
                print "DESCRIPTION: Show help message\n"
            else:
                table_data = [["--COMMAND--", "--DESCRIPTION--"]]
                table_data.append(['help', "Show this help message"])
                table_data.append(['os', "Change OS"])
                table_data.append(['syntax', "Change syntax"])
                table_data.append(['asm', "Change mode to assembly"])
                table_data.append(['disasm', "Change mode to disassembly"])
                table_data.append(['bits', "Change number of bits"])
                table_data.append(['arch', "Change the architecture"])
                table_data.append(['endian', "Change the endianess"])
                table_data.append(['c', "Clear screen"])
                table_data.append(['exit', "Exit PASM"])
                table_instance = SingleTable(table_data) 
                table_instance.inner_heading_row_border = True
                table_instance.justify_columns = {0: 'left', 1: 'left', 2: 'left'}
                print table_instance.table
                print '\n'

if __name__ == "__main__":
    try:
        main()
    except:
        print_exception()
        


