"""
DOCUMENTATION
    Creates a simple, balanced subnet for integer input

PROCEDURE
    enter original ip addr
    enter how many networks you want to make
    create pandas df of sunny chart
"""


import pandas as pd

from pprint import pprint
import time




subnet_model = {
    "1" : {"hosts": 256 , "subnet_mask":"/24"},
    "2" : {"hosts": 128 , "subnet_mask":"/25"},
    "4" : {"hosts": 64 , "subnet_mask":"/26"},
    "8" : {"hosts": 32 , "subnet_mask":"/27"},
    "16" : {"hosts": 16 , "subnet_mask":"/28"},
    "32" : {"hosts": 8 , "subnet_mask":"/29"},
    "64" : {"hosts": 4 , "subnet_mask":"/30"},
    "128" : {"hosts": 2 , "subnet_mask":"/31"},
    "256" : {"hosts": 1 , "subnet_mask":"/32"}
}
subnet_list = list(subnet_model.keys())
subnet_list = [ int(subnet_list[net]) for net in range(0,len(subnet_list),1) ] 






# fetch user input
print("""
Please enter original network ip  

    ex: 192.168.4.0/24
    """)
original_ip = input("> ").strip()
amount_of_networks = input("\nPlease enter amount of sub-networks\n> ")



# user input validation
ip_groups = original_ip.split(".")
if len(ip_groups) < 3 or len(ip_groups) > 4 :
    print("ERROR: Please enter valid original ip address.")
    exit()
if len(ip_groups[-1]) < 1:
    print("ERROR: Please enter valid original ip address.")
    exit()

try:
    amount_of_networks = int(amount_of_networks)
except:
    print("ERROR: Please enter valid amount of subnets.")
    exit()
if amount_of_networks < 1:
    print("ERROR: Please enter valid amount of subnets.")
    exit()



# reformat user input for subnetting procedure
original_ip = ""
for i in range(0 , 3 , 1):
    original_ip += f"{ip_groups[i]}."


# calculate subnet
selected_subnet = None
for net in subnet_list:
    if amount_of_networks <= net:
        selected_subnet = net
        break
if not selected_subnet: #validation
    print("ERROR: Please enter valid amount of subnets.")
    exit()




# create subnet information
subnet_output = {}
index_counter = 0
usable_hosts = subnet_model[str(selected_subnet)]['hosts']
for net in range( 0  , 256 , usable_hosts  ):
    network_id = original_ip + str(net)
    broadcast_id = original_ip + str( net + (usable_hosts-1) )
    host_id_range = f"{original_ip}{net+1} - {original_ip}{net+(usable_hosts-2)}  "


    subnet_output[index_counter] = {
        "network_id" : network_id,
        "subnet_mask" : subnet_model[str(selected_subnet)]['subnet_mask'],
        "host_id_range" : host_id_range,
        "usable_hosts" : usable_hosts,
        "broadcast_id" : broadcast_id,
    }
    index_counter += 1





# debug output
for x in range(0 ,selected_subnet ,1 ):
    pprint(subnet_output[x])
    print()
    # time.sleep(1.2)
print( f"\nAMOUNT OF SUBNETS: {len(subnet_output)}"  )