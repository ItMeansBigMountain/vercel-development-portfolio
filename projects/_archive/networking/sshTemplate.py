from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler

from socket import *


# automatically get your current ip address
computer_Name = gethostname() 
wired_IP_addr = gethostbyname( gethostname() )
WIFI_ip = gethostbyname( getfqdn() )

print(computer_Name)
print( 'Wired IP Address:' , wired_IP_addr)
print( 'WIFI IP Address:' , WIFI_ip)




# connecting to router
connection = ConnectHandler(ip='192.168.1.1' , port=22, device_type='cisco_ios' , username='' , password=''  )
# connection = ConnectHandler(ip = '' , device_type = 'autodetect' , username = '' , password = ''  )


# # send command and recv output
SSH_command = connection.send_command("ls")
print(SSH_command)




connection.disconnect()