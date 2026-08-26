from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler

import time

import sys
import os

import re

import platform 


# TODO - replace nmap data structures with nmap.py module
import nmap



subnetMask_Table = (
    (  '/30'  ,  '255.255.255.252'  ),
    (  '/29'  ,  '255.255.255.248'  ),
    (  '/28'  ,  '255.255.255.240'  ),
    (  '/27'  ,  '255.255.255.224'  ),
    (  '/26'  ,  '255.255.255.192'  ),
    (  '/25'  ,  '255.255.255.128'  ),
    (  '/24'  ,  '255.255.255.0'  ),
    (  '/23'  ,  '255.255.254.0'  ),
    (  '/22'  ,  '255.255.252.0'  ),
    (  '/21'  ,  '255.255.248.0'  ),
    (  '/20'  ,  '255.255.240.0'  ),
    (  '/19'  ,  '255.255.224.0'  ),
    (  '/18'  ,  '255.255.192.0'  ),
    (  '/17'  ,  '255.255.128.0'  ),
    (  '/16'  ,  '255.255.0.0'  ),
)


# when set to auto detect, it gets the ANSI version of the output-string
def ANSI_escapeSequence(text):
    print("Original Text: ",text)
    reaesc = re.compile(r'\x1b[^m]*m')
    new_text = reaesc.sub('', text)
    return new_text

# NOTES
'''
    PROCEDURE
    auto detect router
    connect to it via SSH
    get device info


    todo
    make a function for full scan and another for spec. amount



    INSTALLATION REQUIREMENT <MAC>
    # have python 3
    # pip3 install netmiko
    # install xcode 
    # install brew
    # install ip calc
    # install nmap

    INSTALLATION REQUIREMENT <LINUX>
    # have python 3
    # pip3 install netmiko
    # apt update
    # apt upgrade
    # apt-get install ip calc
    # apt-get install nmap

    INSTALLATION REQUIREMENT <WINDOWS>
    # have python 3
    # pip3 install netmiko
    # Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    # choco install nmap


    ONCE DONE, REPLACE NOTES WITH INSTALLATION GUIDE





    provide a list of everything that is old/getting old / almost old ... etc 
    let them know to work towards a plan to get them out of the EOL range

'''





# ROUTER AUTOMATION COMMAND (under construction)
'''
    commands for cisco
    - sysinfo 

    grab
    serial number
    model number

    run eol list check
'''
def netmikoCommands(username , password , device ):
    routerInfo = {
        'ip' : device['ip'] ,
        'device_type' : 'autodetect' , #firmware
        'username' : username ,
        'password' : password
    }
    connection = ConnectHandler( **routerInfo  )
    SSH = connection.send_command( "ls"  )
    # SSH = connection.send_command( "sysinfo"  )
    
    output = ANSI_escapeSequence(SSH)
    print(output)

    connection.disconnect()




# FETCH ALL_DEVICE_STATS

# Windows (returns all ips)
def find_OpenPORTS_WINDOWS():
    myCmd = os.popen('ipconfig').readlines()

    curWIFI_ip = ''
    cur_SUBNETMASK = ''
    wifiPassed = False
    for x in myCmd:
        if x.startswith('Wireless LAN adapter Wi-Fi'):
            wifiPassed = True
        if wifiPassed == True:
            if x.startswith('   IPv4'):
                curWIFI_ip = x
            elif x.startswith('   Subnet Mask'):
                cur_SUBNETMASK = x
                break

    
    for x in curWIFI_ip.split():
        if x.startswith('1'):
            curWIFI_ip = x


    for x in cur_SUBNETMASK.split():
        if x.startswith('2'):
            cur_SUBNETMASK = x

    maskRange = ''
    for x in subnetMask_Table:
        if cur_SUBNETMASK == x[1]:
            maskRange = x[0]

    ip_split = curWIFI_ip.split('.')
    ip_range = ''
    for x in range(0,len(ip_split)-1 , 1):
        ip_range = ip_range + ip_split[x] + '.'
    
    ip_range = ip_range + '0' + maskRange

    print("Scanning network...\n\n")
    myCmd = os.popen('nmap {} --open'.format(ip_range)).readlines()

    all_device_stats = []
    name = ''
    tcp_ports = []
    mac_addrs = ''
    not_shown = ''
    macPass = False


    for x in myCmd:
        # goes through sys output and MAC addr pass point will "blink True" for a moment.
        if x.startswith('Nmap scan report'):
            name = x[21:]
        elif x.startswith('Not shown:'):
            not_shown = x[11:]
        elif 'open' in x:
            tcp_ports.append(x)
        elif x.startswith('MAC Address:'):
            mac_addrs = x[13:]
            macPass = True

        if macPass ==  True:
            nameSplit = name.split()
            if len(nameSplit) > 1:
                name = nameSplit[0]
                ip = nameSplit[1].strip('(' )
                ip = ip.strip(')' )
            else:
                name = 'none'
                ip = nameSplit[0]

            macSplit = mac_addrs.split('(')
            mac_addrs = macSplit[0]

            type_ = macSplit[1][:-2]

            stat = {
                'Device_name' : name,
                'Device_type' : type_,
                'ip' : ip,
                'tcp_ports' : set(tcp_ports),
                'mac_addrs' : mac_addrs,
                'not_shown' : not_shown,
            }
            tcp_ports = []
            all_device_stats.append(stat)
            macPass = False


    for device in all_device_stats:

        device['not_shown'] = device['not_shown'].split()[0]

        cleanTCPs = []
        for replace in  device['tcp_ports']:
            portOnly = replace.split()[0]
            cleanTCPs.append(portOnly)

        device['tcp_ports'] = cleanTCPs

    return all_device_stats

# Linux (returns all ips)
def find_OpenPORTS_LINUX():
    myCmd = os.popen('ifconfig | grep broadcast').read()
    myCmd = set(myCmd.split(' '))

    # GRAB WIFI IP
    curWIFI_ip = ''
    for x in myCmd:
        if x.startswith('1'):
            curWIFI_ip = x
            break
    
    # GRAB SUBNETMASK
    myCmd = os.popen('ipcalc {}'.format(curWIFI_ip)).read()
    myCmd = myCmd.split()
    data = ''
    for x in range(len(myCmd)):
        if myCmd[x].startswith('Network'):
            data = myCmd[x+1]
            

    print(f"\nYour ip address is {curWIFI_ip}")
    print(f"Your subnet mask is {data}")
    print("\nScanning network...\n\n")
    myCmd = os.popen('nmap {} --open'.format(data)).readlines()


    all_device_stats = []
    name = ''
    tcp_ports = []
    mac_addrs = ''
    not_shown = ''
    macPass = False
    for x in myCmd:
        # goes through sys output and MAC addr pass point will "blink True" for a moment.
        if x.startswith('Nmap scan report'):
            name = x[21:]
        elif x.startswith('Not shown:'):
            not_shown = x[11:]
        elif 'open' in x:
            tcp_ports.append(x)
        elif x.startswith('MAC Address:'):
            mac_addrs = x[13:]
            macPass = True

        if macPass ==  True:

            nameSplit = name.split()
            name = nameSplit[0]
            ip = nameSplit[1]

            macSplit = mac_addrs.split('(')
            mac_addrs = macSplit[0]
            type_ = macSplit[1][:-2]


            stat = {
                'Device_name' : name,
                'Device_type' : type_,
                'ip' : ip,
                'tcp_ports' : set(tcp_ports),
                'mac_addrs' : mac_addrs,
                'not_shown' : not_shown,
            }
            tcp_ports = []
            all_device_stats.append(stat)
            macPass = False


    for device in all_device_stats:

        device['not_shown'] = device['not_shown'].split()[0]

        cleanTCPs = []
        for replace in  device['tcp_ports']:
            portOnly = replace.split()[0]
            cleanTCPs.append(portOnly)

        device['tcp_ports'] = cleanTCPs

        # clean check of all items
        # for key , value in device.items():
        #     print(key)
        #     print(value)
        #     print()
        # print('---------------------------')
        # print()
        # print()

    return all_device_stats

# MAC (testing)
def find_OpenPORTS_MAC():
    myCmd = os.popen('ifconfig | grep broadcast').read()
    myCmd = set(myCmd.split(' '))

    curWIFI_ip = ''
    for x in myCmd:
        if x.startswith('1'):
            curWIFI_ip = x
            break

    myCmd = os.popen('ipcalc {}'.format(curWIFI_ip)).read()
    myCmd = myCmd.split()

    data = ''
    for x in range(len(myCmd)):
        if myCmd[x].startswith('Network'):
            data = myCmd[x+1]

    print("Scanning network...\n\n")
    myCmd = os.popen('nmap {} --open'.format(data)).readlines()


    all_device_stats = []
    name = ''
    tcp_ports = []
    mac_addrs = ''
    not_shown = ''
    macPass = False
    for x in myCmd:
        # goes through sys output and MAC addr pass point will "blink True" for a moment.
        if x.startswith('Nmap scan report'):
            name = x[21:]
        elif x.startswith('Not shown:'):
            not_shown = x[11:]
        elif 'open' in x:
            tcp_ports.append(x)
        elif x.startswith('MAC Address:'):
            mac_addrs = x[13:]
            macPass = True

        if macPass ==  True:

            nameSplit = name.split()
            name = nameSplit[0]
            ip = nameSplit[1]

            macSplit = mac_addrs.split('(')
            mac_addrs = macSplit[0]
            type_ = macSplit[1][:-2]


            stat = {
                'Device_name' : name,
                'Device_type' : type_,
                'ip' : ip,
                'tcp_ports' : set(tcp_ports),
                'mac_addrs' : mac_addrs,
                'not_shown' : not_shown,
            }
            tcp_ports = []
            all_device_stats.append(stat)
            macPass = False


    for device in all_device_stats:

        device['not_shown'] = device['not_shown'].split()[0]

        cleanTCPs = []
        for replace in  device['tcp_ports']:
            portOnly = replace.split()[0]
            cleanTCPs.append(portOnly)

        device['tcp_ports'] = cleanTCPs

        # clean check of all items
        # for key , value in device.items():
        #     print(key)
        #     print(value)
        #     print()
        # print('---------------------------')
        # print()
        # print()



    return all_device_stats









# SSH INTO ALL DEVICES FOUND
def filterSSH(all_device_stats , credentials):
    # go through all devices
    # look through all tcp connections per device
    # attempt to connect using device ip & port    # send netmiko command...
    '''
    stat = {
        'Device_name' : name,
        'Device_type' : type_,
        'ip' : ip,
        'tcp_ports' : set(tcp_ports),
        'mac_addrs' : mac_addrs,
        'not_shown' : not_shown,
    }

    '''

    failed = 0
    failed_devices = []

    username = credentials[0]
    password = credentials[1]

    for device in all_device_stats:
        if failed > 3 :
            print("\nLooks like these credentials may need to be re-authenticated...")
            pprint.pprint(device)
            username , password  = credential_storage()

        # netmiko command
        try:
            # print(device['Device_name'])
            # print(device['Device_type'])
            # print(device['ip'])
            # print(device['tcp_ports'])
            # print(device['mac_addrs'])
            # print(device['not_shown'])

            # print()
            # print()
            netmikoCommands(username , password , device)


        except Exception as e:
            failed_devices.append(device)
            failed += 1
            print(e)

        '''

        store all failed attempts in an array
        display all failed devices 
        reiterate that array asking for re-auth

        re run log in attempt 
        '''






# installation functions

# have python 3
# pip3 install netmiko
# Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
# choco install nmap
def install_windows():
    pass


# have python 3
# pip3 install netmiko
# apt update
# apt upgrade
# apt-get install ip calc
# apt-get install nmap
def install_linux():

    os.popen('apt update')
    print('System updated...')

    os.popen('apt upgrade')
    print('System upgraded...')
    
    os.popen('apt-get nmap')
    os.popen('apt-get ipcalc')
    print('Nmap & ipcalc installed...\n')


# install xcode 
# install brew
# install ip calc
# install nmap
def install_mac():

    myCMD = os.popen('xcode-select -–p ').read()

    print('Checking Xcode...')
    if 'Developer' in myCMD.split('/'):
        print("You have Xcode")
    else:
        print('Installing Xcode...')
        os.popen('xcode-select –-install') 
        time.sleep(10)
    
    os.popen('curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install')
    print('Verified brew... installing Nmap')
    time.sleep(10)

    os.popen('brew install nmap ') 
    time.sleep(10)
    os.popen('brew install ipcalc ') 
    time.sleep(10)
    print('!!!! DONE !!!!')







# helper functions
def credential_storage():
    username = input("Please provide valid username: ")
    password = input("Please provide valid password: ")
    return  username , password  



def main():
    print("Router Automation")
    
    plt = platform.system()
    if plt == "Windows":
        print("Your system is Windows")
        options = "1"
    elif plt == "Linux":
        print("Your system is Linux")
        options = "2"
    elif plt == "Darwin":
        print("Your system is MacOS")
        options = "3"
    else:
        print("Unidentified system")
        exit()

    time.sleep(2)

    # windows
    if options == '1':
        # installation validation
        # install = input("Do you have Nmap installed? ( y / N / not sure ): ")
        # if install.lower().startswith('n'):
        #     install_windows()
        # else:
        #     print('Proceeding With No Installation')
        
        credentials = credential_storage()
        filterSSH(find_OpenPORTS_WINDOWS() , credentials)

    # linux
    elif options == '2':
        # installation validation
        # install = input("Do you have Nmap installed? ( y / N / not sure ): ")
        # if install.lower().startswith('n'):
        #     install_linux()
        # else:
        #     print('Proceeding With No Installation')

        credentials = credential_storage()
        filterSSH(find_OpenPORTS_LINUX() , credentials)

    # mac
    elif options == '3':
        # installation validation
        # install = input("Do you have Nmap installed? ( y / N / not sure ): ")
        # if install.lower().startswith('n'):
        #     install_mac()
        # else:
        #     print('Proceeding With No Installation')

        credentials = credential_storage()
        filterSSH(find_OpenPORTS_MAC() , credentials)


    else:
        print("Inavalid option\n\n")




# main()

from pprint import pprint
pprint( find_OpenPORTS_LINUX()   )