#!/usr/bin/env python3

import os, sys
import re
import subprocess

RB = '\033[48;2;58;49;58m'
RC = '\033[0m\033[38;2;58;49;58m\033[3m'
RD = '\033[0m\033[38;2;58;49;58m'
R = '\033[0m\033[38;2;58;49;58m\033[1m'
WB = '\033[48;2;255;255;255m\033[38;2;58;49;58m\033[1m'
G = '\033[0m\033[48;2;85;72;85m\033[38;2;225;214;225m'

version = "1.5.0"

class color:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CURSIVE = '\033[3m'
    END = '\033[0m'

C = color.END + color.BOLD

helper = os.path.dirname(os.path.realpath(__file__)) + "/phase1.sh"
helper2 = os.path.dirname(os.path.realpath(__file__)) + "/phase3.sh"

globalfail = False

os.system("clear")
'''
print("""
____, __
   + ;  
   .:,
     ’  
    .   
    + ; 
    ;.  
     ;  
     ;  
     ’  


  {0}┌─[{1}i{0}]─[{1}{3}{4}
  {0}└──╼ {2}checkdoor{1}-scan{4}
""".format(color.END+RB, G, WB, version, color.END))
'''

vaile = '''{}                      |
                      :   
                      |   
                      .   
                      .   
                      .   
____, __             .|   
   + ;               .|   
   .{}:,                       
     ’                      
    .              /      
    + ;           :,      
    ;.           /,       
   {}  ;          /;' ;    
     ;         /;{}|{}  : ^  
     ’      / {}:{}  ;.’  °   
          '/; \\           
         ./ '. \\      {}|{}
          '.  ’·    __\\,_
         {}   '.      {}\\{}`{};{}{} 
              \\      {}\\ {}
              .\\.     {}V{}   
                \\.               
                 .,.      
                   .'.    
                  ''.;:     
                    .|.   
                     | .  
                     .    
'''.format(color.END, color.BOLD, color.END, color.CURSIVE, color.END, color.CURSIVE, color.END, color.CURSIVE, color.END, color.BOLD, color.END, color.BOLD, color.CURSIVE, color.END, color.BOLD, color.END, color.BOLD, color.END, color.BOLD)

print(vaile)

#print("[i] Checkdoor v{} - scan".format(version))
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

print("{}Phase 2: {}$PATH hijacking{}".format(RC, color.END+RB, color.END))
response = subprocess.check_output(["which","sudo"])
path = response.decode("utf-8").strip()
if path != "/usr/bin/sudo":
    print("{}[!]{} Potentially maliciovs path detected!\n{}".format(RD, color.END, path))
    globalfail = True
else:
    print(RD+"[+]"+C+" Clean."+color.END)
    
#print("Phase 3: Owner&permissions")
#path = path.replace("sudo", "")


print("Done.")

if globalfail:
    sys.exit(1)
