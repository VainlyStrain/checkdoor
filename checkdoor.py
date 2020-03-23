#!/usr/bin/env python3

# -------------------------------------
# checkdoor ~ VainlyStrain
# simple sudo backdoor hunter in Python
# -------------------------------------

import os, sys
import re
import subprocess

#some colors
RB = '\033[48;2;58;49;58m'
RC = '\033[0m\033[38;2;58;49;58m\033[3m'
RD = '\033[0m\033[38;2;58;49;58m'
R = '\033[0m\033[38;2;58;49;58m\033[1m'
WB = '\033[48;2;255;255;255m\033[38;2;58;49;58m\033[1m'
G = '\033[0m\033[48;2;85;72;85m\033[38;2;225;214;225m'

version = "1.5.1"

#more colors
class color:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CURSIVE = '\033[3m'
    END = '\033[0m'

C = color.END + color.BOLD

#helper script executed by subprocess
helper = os.path.dirname(os.path.realpath(__file__)) + "/phase1.sh"

#has anything suspicious been detected?
globalfail = False

#display stuff
os.system("clear")

vaile = '''{0}                      |
                      :   
                      |   
                      .   
                      .   
                      .   
____, __             .|   
   + ;               .|   
   .{1}:,                       
     ’                      
    .              /      
    + ;           :,      
    ;.           /,       
   {0}  ;          /;' ;    
     ;         /;{2}|{0}  : ^  
     ’      / {2}:{0}  ;.’  °   
          '/; \\           
         ./ '. \\      {2}|{0}
          '.  ’·    __\\,_
         {1}   '.      {0}\\{1}`{2};{0}{1} 
              \\      {0}\\ {1}
              .\\.     {0}V{1}   
                \\.               
                 .,.      
                   .'.    
                  ''.;:     
                    .|.   
                     | .  
                     .    
'''.format(color.END, color.BOLD, color.CURSIVE)

print(vaile)

'''
Phase 1: searches for aliases and functions in local bash files using regex
if you are not using bash, modify the phase1.sh script to your respective config files
'''
print("{}Phase 1: {}maliciovs aliases{}".format(RC, color.END+RB, color.END))

response = subprocess.check_output(["bash",helper])
response = response.decode("utf-8")
parsed = response.replace(" ","")
fail = False
if "sudo()" in parsed:
    print("{}[!]{} Potentially maliciovs alias detected\n".format(RD, color.END))
    alias = re.split("sudo\s*\(\)", response)[1].split("}")[0]
    lines = alias.split("\n")
    print("  {}sudo(){}".format(WB,color.END)+lines[0])
    for line in lines[1::]:
        if line is not "":
            line = line.replace("\'","'")
            print("  "+line)
    print("  }\n")
    fail = True
if "aliassudo" in parsed:
    print("{}[!]{} Potentially maliciovs alias detected\n".format(RD, color.END))
    for i in response.split("\n"):
        if "aliassudo" in i.replace(" ", ""):
            print(i)
    print()
    fail = True
    
if fail:
    globalfail = True
else:
    print(RD+"[+]"+C+" Clean."+color.END)


'''
Phase 2: checks if a malicious binary has been appended at the beginning of $PATH,
thus being executed instead of the real sude
uses the which command
'''
print("{}Phase 2: {}$PATH hijacking{}".format(RC, color.END+RB, color.END))
response = subprocess.check_output(["which","sudo"])
path = response.decode("utf-8").strip()
if path != "/usr/bin/sudo":
    print("{}[!]{} Potentially maliciovs path detected!\n{}".format(RD, color.END, path))
    globalfail = True
else:
    print(RD+"[+]"+C+" Clean."+color.END)
    

'''
Phase 3: checks if the binary's owner & group is root and if the permissions are
correct
'''
print("{}Phase 3: {}Owner&permissions{}".format(RC, color.END+RB, color.END))
response = subprocess.check_output(["ls","-l",path])
response = response.decode("utf-8")
parsed = re.split("\s+", response)
if parsed[0] != "---s--x--x." and parsed[2] != "root" and parsed[3] != "root":
    print("{}[!]{} File permissions and ownership do not match expectations.\n{}".format(RD, color.END, path))
    print(response)
    globalfail = True
else:
    print(RD+"[+]"+C+" Clean."+color.END)

print("Done.")

#exit with failure when backdoor found. useful for && concatenation
if globalfail:
    sys.exit(1)
