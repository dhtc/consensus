# Hello, there! I went out of creativity and this script is going to be named just as "consensus".
# This simple and small script uses some third-party software to produce a consensus sequence based on the ones
# you submit on FASTA format as input. You can apply it to DNA, RNA or proteins (one type per run, of course).
# I am not going to describe details of the process here since the documentation of these software are acessible.

# To execute just use: python3 consensus.py <InputFastaFile> <OutputFile>
# If you want to set the number of threads to be used: python3 consensus.py <InputFastaFile> <OutputFile> <NumberOfThreads>

# This code can and will be improved for better usability and robustness.
# There are not many comments since the code is very simple and one can have an idea of what is going on by reading
# the messages printed to the console

import sys
import subprocess
from os import remove
from os import popen
from os import devnull


# Checks if some packages are already installed (through APT). If not, it tries to install.
# In case where installation is not successful, stops the execution
# TODO: Use the APT wrapper here
def Install():
    print("=====")
    print("#Checking if you have the packages needed")
    isClustaloInstalled = popen("dpkg -l | grep -c clustalo").read()[0]
    isHmmerInstalled = popen("dpkg -l | grep -c hmmer").read()[0]
    if isClustaloInstalled != "1" or isHmmerInstalled != "1":
        print("#Installing packages")
        # Ok... I admit the crime. I try to supress the warnings generated by calling APT on the next lines.
        # But... Trust me :). There should be no harm. Should not... 
        FNULL = open(devnull, 'w')
        subprocess.Popen("sudo apt install clustalo > /dev/null", shell = True, stderr = FNULL).wait()
        subprocess.Popen("sudo apt install hmmer > /dev/null", shell = True, stderr = FNULL).wait()
    isClustaloInstalled = popen("dpkg -l | grep -c clustalo").read()[0]
    isHmmerInstalled = popen("dpkg -l | grep -c hmmer").read()[0]
    if isClustaloInstalled != "1" or isHmmerInstalled != "1":
        print("-For some reason, was not possible to install the packages needed")
        print("-Check if both your internet connection and APT are working properly")
        print("=====")
        sys.exit(1)


Install()
print("#Parsing command line arguments")
# TODO: Use getopt here
input = sys.argv[1]
output = sys.argv[2]
if len(sys.argv) < 4:
    threads = "1"
else:
    threads = sys.argv[3]
print("#Generating global alignment")
subprocess.Popen("clustalo -i " + input + " -o ClustaloOut_Raw --outfmt=selex --threads=" + threads + " --force  > /dev/null", shell = True).wait()
print("#Removing comments from selex file")
writeFile = open("ClustaloOut", "w+")
with open("ClustaloOut_Raw") as readFile:
    for line in readFile:
        if line[0] != "#":
            writeFile.write(line)
writeFile.close()
remove("ClustaloOut_Raw")
print("#Generating profile HMM")
subprocess.Popen("hmmbuild -n File:" + input + " --cpu " + threads + " HMMFile ClustaloOut > /dev/null", shell = True).wait()
remove("ClustaloOut")
print("#Extracting consensus sequence from profile HMM")
subprocess.Popen("hmmemit -c -o " + output + " HMMFile > /dev/null", shell = True).wait()
remove("HMMFile")
print("#Done! Check the output file")
print("=====")
