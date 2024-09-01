import csv
import argparse
import sys
import re
import ipaddress
import os
import shutil
import math

version = "1.6"

# undefined start point
file_path = ""
mac_addresses = ""
model = ""
ucm_ip = ""
start_ip = ""
subnet_mask = ""
gateway_ip = ""
dns_ip = ""
start_account = ""
ip_mode = ""
        
def is_numeric(input_str):
    return re.match(r"^\d{2,}$", input_str) is not None

def is_valid_ip(ip):
    # Regular expression pattern for valid IPv4 addresses
    ip_pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                            r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                            r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                            r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    return bool(ip_pattern.match(ip))  # Return True if valid, False otherwise

def is_valid_subnet_mask(subnet_mask):
    try:
        # Parse the subnet mask
        subnet = ipaddress.IPv4Network(f"0.0.0.0/{subnet_mask}", strict=False)
        return not subnet.with_prefixlen.endswith('/0')
    except ValueError:
        return False

def is_in_list(input_value, my_list):
    """
    Checks if `input_value` is in `my_list`.

    Args:
        input_value: The value to search for.
        my_list: The list to search in.

    Returns:
        bool: True if `input_value` is in `my_list`, otherwise False.
    """
    return input_value in my_list

supported_model_list = ["GHP610", "GHP610W", "GHP611", "GHP611W", "GHP620", "GHP620W", "GHP621", "GHP621W", "GHP630", "GHP630W", "GHP631", "GHP631W", "GRP2601", "GRP2601P", "GRP2601W", "GRP2602", "GRP2602G", "GRP2602P", "GRP2602W", "GRP2603", "GRP2603P", "GRP2604", "GRP2604P", "GRP2612", "GRP2612G", "GRP2612P", "GRP2612W", "GRP2613", "GRP2614", "GRP2615", "GRP2616", "GRP2624", "GRP2634", "GRP2636", "GRP2650", "GRP2670", "GSC3505", "GSC3506", "GSC3510", "GSC3516", "GSC3570", "GSC3574", "GSC3575", "GSC3610", "GSC3615", "GSC3620", "GXP1100", "GXP1105", "GXP1600C", "GXP1610C", "GXP1610P", "GXP1615", "GXP1628B", "GXP1760", "GXP1760W", "GXP1780", "GXP1782", "GXP2130", "GXP2135", "GXP2136", "GXP2140", "GXP2160", "GXP2170", "GXV3240", "GXV3275", "GXV3350", "GXV3370", "GXV3380", "GXV3450", "GXV3470", "GXV3480", "GXV3500", "WP800", "WP810", "WP816", "WP820", "WP822", "WP825", "WP826", "WP856",]
    
parser = argparse.ArgumentParser(description="karan's grandstream zero configuration file generator")
parser.add_argument("-v", action="store_true", help="Print version info")
parser.add_argument("-m", help="IP Phone Model")
parser.add_argument("-u", help="UCM IP Address")
parser.add_argument("-s", help="Starting IP Address")
parser.add_argument("-n", help="Subnet Mask")
parser.add_argument("-g", help="Gateway IP Address")
parser.add_argument("-a", help="Starting Account")
parser.add_argument("-d", help="DNS IP Address")
parser.add_argument("-i", type=int, help="IP Phones mode")

args = parser.parse_args()

if args.v:
    print("\nkgzcfg version: {}".format(version))
    sys.exit(0)

if args.m:
    check = args.m.upper()
    if is_in_list(check, supported_model_list):
        print(check)
        model = args.m

if args.u:
    if is_valid_ip(args.u):
        ucm_ip = args.u

if args.s:
    if is_valid_ip(args.s):
        start_ip = args.s

if args.n:
    try:
        if int(args.n) <= 32:
            print("Invalid IP address. Please enter a valid Subnet Mask.")
    except:
        if is_valid_subnet_mask(args.u):
            subnet_mask = args.n

if args.g:
    if is_valid_ip(args.g):
        gateway_ip = args.g

if args.a:
    if is_numeric(args.a):
        start_account = int(args.a)

if args.d:
    if is_valid_ip(args.d):
        dns_ip = args.d

if args.i:
    if args.i in ("1" ,"2"):
        ip_mode = args.i

# Get the path to the current script file
script_directory = os.path.dirname(__file__)

# Specify the file name (e.g., "data.json")
file_name = "kgzcfg_export_zc_devices.csv"

# Construct the full path to the file
file_path = os.path.join(script_directory, file_name)

def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    terminal_width, _ = shutil.get_terminal_size()

    # Calculate the number of '#' characters based on the completion percentage
    bar_width = int((terminal_width - 10) * (percent / 100))
    bar = '#' * bar_width + '-' * (terminal_width - 10 - bar_width)

    # Display the progress bar
    print(f"\r|{bar}| {percent:.2f}%", end="\r")

# Generate a list of numbers, each multiplied by 5
numbers = [x * 5 for x in range(2000, 2100)]
results = []

logo = (r"""
88                                           ad88
88                                          d8"
88                                          88
88   ,d8  ,adPPYb,d8 888888888  ,adPPYba, MM88MMM ,adPPYb,d8
88 ,a8"  a8"    `Y88      a8P" a8"     ""   88   a8"    `Y88
8888[    8b       88   ,d8P'   8b           88   8b       88
88`"Yba, "8a,   ,d88 ,d8"      "8a,   ,aa   88   "8a,   ,d88
88   `Y8a `"YbbdP"Y8 888888888  `"Ybbd8"'   88    `"YbbdP"Y8
          aa,    ,88                              aa,    ,88
           "Y8bbdP"                                "Y8bbdP"
""")
print()  # Print a newline after completion
    
try:
    # Try to open the file for reading
    with open(file_path, "r") as file:
        # Process the data as needed
        print(f"Found existing '{file_name}' in the same folder as the script.")
except FileNotFoundError:
    # If the file doesn't exist, create it
    with open(file_path, "w") as file:
        # Initialize the file content (if required)
        print(f"Created '{file_name}' in the same folder as the script.")

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

def create_dhcp_config(mac, account, model, ucm_ip):
    return {
        "device_start": [
            "======== Device Start ========",
            "mac,model,ip,file_url,version,vendor,url_parameter,config_name,account_secret,state,ad_state,port,hot_desking,last_access",
            f"{mac},{model},0.0.0.0,https://{ucm_ip}:8089/zccgi/,1.0.5.58,Grandstream,,,,8,0,5060,no,2024-07-27 16:08:27",
            "",
        ],
        "basic_settings": [
            "######## Basic Settings ########",
            "mac,element,element_number,entity_name,value",
            f"{mac},Account,1,AccountChoice,{account}",
            "",
        ]
    }
    
def create_static_config(mac, ip, account, model, dns_ip, subnet_mask, gateway_ip, ucm_ip):
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
            f"{mac},IPAddressMode,1,SubnetMask_1,{subnet_mask.split('.')[0]}",
            f"{mac},IPAddressMode,1,SubnetMask_2,{subnet_mask.split('.')[1]}",
            f"{mac},IPAddressMode,1,SubnetMask_3,{subnet_mask.split('.')[2]}",
            f"{mac},IPAddressMode,1,SubnetMask_4,{subnet_mask.split('.')[3]}",
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

def main(mac_addresses, model, ucm_ip, start_ip, subnet_mask, gateway_ip, dns_ip, start_account, ip_mode):
    # Display a progress bar for the calculation of factorials
    progress_bar(0, len(numbers))
    for i, x in enumerate(numbers):
        results.append(math.factorial(x))
        progress_bar(i + 1, len(numbers))
    print(logo)
    if mac_addresses == "":
        mac_addresses = input("Enter the MAC addresses (comma separated) >").split(',')
        mac_addresses = [addr.upper() for addr in mac_addresses]
    if ucm_ip == "":
        while True:
            ucm_ip = input("Enter the UCM IP address >")
            if is_valid_ip(ucm_ip):
                if is_valid_subnet_mask(ucm_ip):
                    print("Entered value is Subnet Mask not IP Addresss")
                    continue
                else:
                    break
            else:
                print("Invalid IP address. Please enter a valid IPv4 address.")
    if model == "":
        while True:
            model = input("Enter the Model default (GRP2601P) >") or "GRP2601P"
            model = model.upper()
            print(model)
            if is_in_list(model, supported_model_list):
                break
    if start_account == "":
        while True:
            start_account = input("Enter the starting Account number >")
            if is_numeric(start_account):
                start_account = int(start_account)
                break
    if ip_mode == "":
        while True: 
            ip_mode = input("Enter IP Phone network mode (1. DHCP 2. Static) >")
            if ip_mode in ("1" ,"2"):
                break
    ip_mode = int(ip_mode)
    if ip_mode == 2:
        if start_ip == "":
            while True:
                start_ip = input("Enter the IP Phone starting IP address >")
                if is_valid_ip(start_ip):
                    if is_valid_subnet_mask(start_ip):
                        print("Entered value is Subnet Mask not IP Addresss")
                        continue
                    else:
                        break
                else:
                    print("Invalid IP address. Please enter a valid IPv4 address.")
        if subnet_mask == "":
            while True:
                print("Enter the Subnet Mask default (255.255.255.0) >", end="")
                subnet_mask = input() or "255.255.255.0"
                try:
                    if int(subnet_mask) <= 32:
                        print("Invalid IP address. Please enter a valid Subnet Mask.")
                        continue
                except:
                    if is_valid_subnet_mask(subnet_mask):
                        break
                    else:
                        print("Invalid IP address. Please enter a valid Subnet Mask.")
        default_gateway = start_ip.rsplit(".", 1)[0] + ".1"
        if gateway_ip == "":
            while True:
                print(f"Enter the Gateway IP address default ({default_gateway}) >", end="")
                gateway_ip = input() or default_gateway
                if is_valid_ip(gateway_ip):
                    if is_valid_subnet_mask(gateway_ip):
                        print("Entered value is Subnet Mask not IP Addresss")
                        continue
                    else:
                        break
                else:
                    print("Invalid IP address. Please enter a valid IPv4 address.")            
        if dns_ip == "":
            while True:                        
                dns_ip = input("Enter the DNS IP address default (8.8.8.8) >") or "8.8.8.8"
                if is_valid_ip(dns_ip):
                    if is_valid_subnet_mask(dns_ip):
                        print("Entered value is Subnet Mask not IP Addresss")
                        continue
                    else:
                        break
                else:
                    print("Invalid IP address. Please enter a valid IPv4 address.")            
            
        
    count = len(mac_addresses)
    if ip_mode == 2:
        ips = generate_ip_range(start_ip, count)
    accounts = generate_account_numbers(start_account, count)
    
    # Create config file with static ip address
    if ip_mode == 2:
        configs = [create_static_config(mac.strip(), ips[i], accounts[i], model, dns_ip, subnet_mask, gateway_ip, ucm_ip) for i, mac in enumerate(mac_addresses)]
    if ip_mode == 1:
        configs = [create_dhcp_config(mac.strip(), accounts[i], model, ucm_ip) for i, mac in enumerate(mac_addresses)]
    
    append_config_to_csv(file_path, configs)
    
    # Display assigned IP and account numbers
    if ip_mode == 1:
        print("\nAssigned MAC Address to Accounts:")
        for i, mac in enumerate(mac_addresses):
            print(f"MAC Address: {mac.strip()} - Account: {accounts[i]}")    
    if ip_mode == 2:
        print("\nAssigned IPs and Accounts:")
        for i, mac in enumerate(mac_addresses):
            print(f"MAC Address: {mac.strip()} - IP: {ips[i]} - Account: {accounts[i]}")

try: 
    if __name__ == "__main__":
        main(mac_addresses, model, ucm_ip, start_ip, subnet_mask, gateway_ip, dns_ip, start_account, ip_mode)
except:
    print("\nkgzcfg Stop Executing.")

finally:
    print("\n[kgzcfg_v{}]:".format(version))