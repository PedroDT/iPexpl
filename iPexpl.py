#!/bin/env Python

'''
***********************************************************
*          Code to save your Apple files easly            *
***********************************************************
___________________________________________________________
|                                                         |
|You can configurate your preferences                     |
|in code, that's all commented.                           |
|-                                                        |
|it's desgined for Linux machines                         |
|Preference directory "/usr/local/bin"                    |
|to prevents erros install the necessary packges          |
|run "sudo apt-get install libimobiledevice-utils"        |
|and "sudo apt-get install ifuse" in terminal             |
|you can also run                                         |
|"alias iPexpl='python3 /usr/local/bin/iPexpl/iPexpl.py'" |
|and you will only need type "iPexpl" in terminal         |  
|to save your files.                                      |
|-                                                        |
|Created by: Doria, Pedro.                                |
|version: v1.0                                            |
|date: 10/09/2021                                         |
|_________________________________________________________|
'''

#Imports

import subprocess
import os
import time

#Variables

temp_dir = "~/temp" # Temporary Directory
save_path = "~/saveapplefiles" # Location to save Apple files
copy_dir = "/DCIM" # Device directory to be copied
trs_tm = 5 # Time to Retry Pairing
home_dir = '/home/doria/'
#Functions

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    GREEN = '\033[32m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BGBLACK='\033[40m'
    BGRED='\033[41m'
    BGGREEN='\033[42m'
    BGORANGE='\033[43m'
    BGBLUE='\033[44m'
    BGPURPLE='\033[45m'
    BGCYAN='\033[46m'
    BGLIGHTGREY='\033[47m'

def time_to_transfer(pth):

    data_size = subprocess.Popen(['du', '-sh', f'{home_dir}{pth[2:]}'], stdout=subprocess.PIPE)
    new_dt = data_size.communicate()
    nw_dt = str(new_dt[0])
    
    if "G" in nw_dt:
        spl_str = nw_dt.split("G")
        spl_str = str(spl_str[0])
        print(spl_str[2:], " Gigabytes")
        transfer_time = float(spl_str[2:]) * 40
    elif "M" in nw_dt:
        spl_str = nw_dt.split("M")
        spl_str = str(spl_str[0])
        print(spl_str[2:], " Megabytes")
        transfer_time = 40
    elif "K" in nw_dt:
        spl_str = nw_dt.split("K")
        spl_str = str(spl_str[0])
        print(spl_str[2:], " Kilobytes")
        transfer_time = 10
    else:
        transfer_time = 30

    print_func(f"Time to Transfer the files: {transfer_time} seconds", 'Success', '*')
    return transfer_time

def print_func(prt_str, tp_pr, sep_chr=' ', tr_time='20'):
    
    ad_siz = len(prt_str)

    if tp_pr == "Success":
        print(f"{bcolors.BOLD}{bcolors.BGORANGE}" + sep_chr * ad_siz + 
            f"{bcolors.ENDC}" + f"\n{bcolors.OKBLUE}{prt_str}{bcolors.ENDC}\n" +
            f"{bcolors.BGORANGE}" + sep_chr * ad_siz + f"{bcolors.ENDC}")
    
    if tp_pr == "Fail":
        print(f"{bcolors.BOLD}{bcolors.OKBLUE}" + sep_chr * ad_siz + 
                f"{bcolors.FAIL}\n{prt_str}\n" + 
                f"{bcolors.OKBLUE}" + sep_chr * ad_siz + f"{bcolors.ENDC}")    
    
    if tp_pr == "Alert":
        print("\n")
        for _ in range(round(tr_time / 2)):
            print(f"{bcolors.WARNING}#{prt_str} \\  {bcolors.ENDC} {round(tr_time)} seconds left ", end='\r')
            time.sleep(0.5)
            print(f"{bcolors.WARNING}#{prt_str} - {bcolors.ENDC} {round(tr_time)} seconds left ", end='\r')
            time.sleep(0.5)
            tr_time -= 1
            print(f"{bcolors.WARNING}#{prt_str} / {bcolors.ENDC} {round(tr_time)} seconds left ", end='\r')
            time.sleep(0.5)
            print(f"{bcolors.WARNING}#{prt_str} | {bcolors.ENDC} {round(tr_time)} seconds left ", end='\r')
            time.sleep(0.5)
            tr_time -= 1
        print("\n")

def test_device(): # This Function tests if an Apple device is plugged on USB
    
    usb = subprocess.Popen(["lsusb"], stdout=subprocess.PIPE)
    res = usb.communicate()
    result = str(res[0])
    
    if "Apple," in result: # Checks if have an Apple device plugged
        print("Plugged")
        return True
    else:
        return False

def verify_validate(): # Tests if have permission, and try get it
    
    while True:
        validate = subprocess.Popen(["idevicepair", "validate"], stdout = subprocess.PIPE)
        conf = validate.communicate()
        confg = str(conf[0])
        
        if "SUCCESS:" in confg:
            print("WE HAVE PERMISSION")
            break
        else:
            print("Trying to get Permission")
            subprocess.run(["idevicepair", "pair"])
            time.sleep(trs_tm)
    return True

def copy_files(tmp_dir, cp_dir, sv_path): # Fuction to copy files to your system
    
    os.system(f"mkdir {tmp_dir}") # Create a Temporary directory
    os.system(f"mkdir {sv_path}") # Create the saving directory
    print_func("Directories Created", "Sucess")
    os.system(f"ifuse {tmp_dir}") # Mount the apple device on the Temporary directory
    os.system(f"cp -r {tmp_dir}{cp_dir} {sv_path}") # Copy the specified files to save directory    
    trasnf_tm = 3 #time_to_transfer(tmp_dir + cp_dir)
    print_func("WAIT... COPING FILES", "Alert", tr_time=trasnf_tm)
    os.system(f"fusermount -u {tmp_dir}") # Umount the apple device
    os.system(f"rmdir {tmp_dir}") # Delete the Temporary directory
    print_func("Files Copied", "Success", "*")

#Program

if __name__ == '__main__':

    is_plugged = test_device()

    if is_plugged:
        is_val = verify_validate()
    else:
        is_val = False
        print_func("Apple Device Not Plugged", "Fail", "H")
    if is_val:        
        copy_files(temp_dir, copy_dir, save_path)