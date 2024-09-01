import csv
import argparse
import sys

version = "1.3"

# undefined
file_path = ""
mac_addresses = ""
model = ""
ucm_ip = ""
start_ip = ""
subnetmask = ""
gateway_ip = ""
dns_ip = ""
start_account = ""

parser = argparse.ArgumentParser(description="grandstream zero configuration file generator")
parser.add_argument("-v", action="store_true", help="Print version info")
parser.add_argument("-f", help="CSV File Path")
parser.add_argument("-m", help="IP Phone Model")
parser.add_argument("-u", help="UCM IP Address")
parser.add_argument("-s", help="Starting IP Address")
parser.add_argument("-n", help="SubnetMask")
parser.add_argument("-g", help="Gateway IP Address")
parser.add_argument("-a", type=int, help="Starting Account")
parser.add_argument("-d", help="DNS IP Address")

args = parser.parse_args()

if args.v:
    print("\ngzcfg version: {}".format(version))
    sys.exit(0)

if args.f:
    file_path = args.f

if args.m:
    model = args.m

if args.u:
    ucm_ip = args.u

if args.s:
    start_ip = args.s

if args.n:
    subnetmask = args.n

if args.g:
    gateway_ip = args.g

if args.a:
    start_account = args.a

if args.d:
    dns_ip = args.d

def generate_ip_range(start_ip, count):
    base_ip = start_ip.split('.')
    base_ip[-1] = str(int(base_ip[-1]) - 1)  # Decrement last octet by 1 to start correctly
    ips = []
    for i in range(count):
        base_ip[-1] = str(int(base_ip[-1]) + 1)  # Increment last octet
        ips.append('.'.join(base_ip))
    return ips

def generate_account_numbers(start_account, count):
    return [start_account + i for i in range(count)]

def create_config(mac, ip, account, model, dns_ip, subnetmask, gateway_ip, ucm_ip):
    return {
        "device_start": [
            "======== Device Start ========",
            "mac,model,ip,file_url,version,vendor,url_parameter,config_name,account_secret,state,ad_state,port,hot_desking,last_access",
            f"{mac},{model},{ip},https://{ucm_ip}:8089/zccgi/,1.0.5.58,Grandstream,,,,8,0,5060,no,2024-07-27 16:08:27",
            "",
        ],
        "basic_settings": [
            "######## Basic Settings ########",
            "mac,element,element_number,entity_name,value",
            f"{mac},Account,1,AccountChoice,{account}",
            "",
        ],
        "advanced_settings": [
            "******** Advanced Settings ********",
            "mac,field_name,element_number,entity_name,value",
            f"{mac},IPAddressMode,1,AddressMode,1",
            f"{mac},IPAddressMode,1,DNSAddressType,0",
            f"{mac},IPAddressMode,1,DNSServer1_1,{dns_ip.split('.')[0]}",
            f"{mac},IPAddressMode,1,DNSServer1_2,{dns_ip.split('.')[1]}",
            f"{mac},IPAddressMode,1,DNSServer1_3,{dns_ip.split('.')[2]}",
            f"{mac},IPAddressMode,1,DNSServer1_4,{dns_ip.split('.')[3]}",
            f"{mac},IPAddressMode,1,DNSServer2_1,{gateway_ip.split('.')[0]}",
            f"{mac},IPAddressMode,1,DNSServer2_2,{gateway_ip.split('.')[1]}",
            f"{mac},IPAddressMode,1,DNSServer2_3,{gateway_ip.split('.')[2]}",
            f"{mac},IPAddressMode,1,DNSServer2_4,{gateway_ip.split('.')[3]}",
            f"{mac},IPAddressMode,1,Gateway_1,{gateway_ip.split('.')[0]}",
            f"{mac},IPAddressMode,1,Gateway_2,{gateway_ip.split('.')[1]}",
            f"{mac},IPAddressMode,1,Gateway_3,{gateway_ip.split('.')[2]}",
            f"{mac},IPAddressMode,1,Gateway_4,{gateway_ip.split('.')[3]}",
            f"{mac},IPAddressMode,1,StaticIP_1,{ip.split('.')[0]}",
            f"{mac},IPAddressMode,1,StaticIP_2,{ip.split('.')[1]}",
            f"{mac},IPAddressMode,1,StaticIP_3,{ip.split('.')[2]}",
            f"{mac},IPAddressMode,1,StaticIP_4,{ip.split('.')[3]}",
            f"{mac},IPAddressMode,1,SubnetMask_1,{subnetmask.split('.')[0]}",
            f"{mac},IPAddressMode,1,SubnetMask_2,{subnetmask.split('.')[1]}",
            f"{mac},IPAddressMode,1,SubnetMask_3,{subnetmask.split('.')[2]}",
            f"{mac},IPAddressMode,1,SubnetMask_4,{subnetmask.split('.')[3]}",
            "",
        ]
    }

def append_config_to_csv(file_path, configs):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for config in configs:
            for section, rows in config.items():
                for row in rows:
                    writer.writerow(row.split(','))

def main(file_path, mac_addresses, model, ucm_ip, start_ip, subnetmask, gateway_ip, dns_ip, start_account):
    if file_path == "":
        file_path = input("Enter the path to the CSV file: ")
    if mac_addresses == "":
        mac_addresses = input("Enter the MAC addresses (comma separated): ").split(',')
    if model == "":
        model = input("Enter the Model: ")
    if ucm_ip == "":
        ucm_ip = input("Enter the UCM IP address: ")
    if start_ip == "":
        start_ip = input("Enter the IP Phone starting IP address: ")
    if subnetmask == "":
        print("Enter the Subnetmask default (255.255.255.0): ", end="")
        subnetmask = input() or "255.255.255.0"
    default_gateway = start_ip.rsplit(".", 1)[0] + ".1"
    if gateway_ip == "":
        print(f"Enter the Gateway IP address default ({default_gateway}): ", end="")
        gateway_ip = input() or default_gateway
    if dns_ip == "":
        dns_ip = input("Enter the DNS IP address default (8.8.8.8): ") or "8.8.8.8"
    if start_account == "":
        start_account = int(input("Enter the starting Account number: "))
    
    count = len(mac_addresses)
    ips = generate_ip_range(start_ip, count)
    accounts = generate_account_numbers(start_account, count)
    
    configs = [create_config(mac.strip(), ips[i], accounts[i], model, dns_ip, subnetmask, gateway_ip, ucm_ip) for i, mac in enumerate(mac_addresses)]
    
    append_config_to_csv(file_path, configs)
    
    # Display assigned IP and account numbers
    print("\nAssigned IPs and Accounts:")
    for i, mac in enumerate(mac_addresses):
        print(f"MAC Address: {mac.strip()} - IP: {ips[i]} - Account: {accounts[i]}")

try: 
    if __name__ == "__main__":
        main(file_path, mac_addresses, model, ucm_ip, start_ip, subnetmask, gateway_ip, dns_ip, start_account)
except:
    print("\ngzcfg Stop Executing.")

finally:
    print("\n[gzcfg_v{}]:".format(version))