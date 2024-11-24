import csv
import argparse
import sys
import re
import ipaddress
import os
import shutil
import math
import time

version = "1.0.7.2" # Version of the script

# Variables for storing input parameters
export_zero_config_csv_file_path = ""
mac_addresses = []
model = ""
ucm_ip = ""
start_ip = ""
subnet_mask = ""
gateway_ip = ""
dns_ip = ""
start_account = ""
ip_mode = ""
loading_time = 0.01 # Time delay for the loading effect

# Function to check if input is numeric
def is_numeric(input_str):
    return re.match(r"^\d{2,}$", input_str) is not None

# Function to validate if the input is a valid IP address
def is_valid_ip(ip):
    ip_pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                            r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                            r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                            r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$") # Regular expression for IPv4
    return bool(ip_pattern.match(ip))  # Return True if valid, False otherwise

# Function to validate subnet mask input
def is_valid_subnet_mask(subnet_mask):
    try:
        subnet = ipaddress.IPv4Network(f"0.0.0.0/{subnet_mask}", strict=False)  # Parse subnet mask
        return not subnet.with_prefixlen.endswith('/0')  # Ensure the subnet is valid
    except ValueError:
        return False

# Regular expression to match valid MAC addresses (with or without colons or dashes)
mac_pattern = re.compile(r'([0-9A-Fa-f]{2}[:\-]?[0-9A-Fa-f]{2}[:\-]?[0-9A-Fa-f]{2}[:\-]?[0-9A-Fa-f]{2}[:\-]?[0-9A-Fa-f]{2}[:\-]?[0-9A-Fa-f]{2})')

# Function to check if a MAC address is valid
def is_valid_mac(mac):
    # Remove any separators (colons or dashes)
    cleaned_mac = mac.replace(":", "").replace("-", "").upper()
    # Check if the MAC address has exactly 12 hexadecimal characters and isn't a repeating sequence
    if len(cleaned_mac) == 12 and re.match(r'^[0-9A-F]{12}$', cleaned_mac):
        if len(set(cleaned_mac)) > 1:  # Rejects all same-character addresses like '111111111111'
            return True
    return False

# Function to process the MAC addresses found in the file or input
def mac_processing(found_macs):
    valid_macs = []
    invalid_macs = []

    for mac in found_macs:
        formatted_mac = mac.replace(":", "").replace("-", "").upper()
        if is_valid_mac(formatted_mac):
            valid_macs.append(formatted_mac)
        else:
            invalid_macs.append(mac)

    return valid_macs, invalid_macs

# Function to prompt the user for MAC addresses if no file is found or valid MACs are present
def get_user_mac_input():
    while True:
        user_input = input("Enter the MAC addresses (comma-separated) > ").split(',')
        valid_macs, invalid_macs = mac_processing(user_input)
        
        if valid_macs:
            return valid_macs, invalid_macs
        else:
            print("No valid MAC addresses found. Please try again.")

# Check if a given value exists in a list
def is_in_list(input_value, my_list):
    return input_value in my_list

# List of supported phone models
supported_model_list = ["GHP610", "GHP610W", "GHP611", "GHP611W", "GHP620", "GHP620W", "GHP621", "GHP621W", "GHP630", "GHP630W", "GHP631", "GHP631W", "GRP2601", "GRP2601P", "GRP2601W", "GRP2602", "GRP2602G", "GRP2602P", "GRP2602W", "GRP2603", "GRP2603P", "GRP2604", "GRP2604P", "GRP2612", "GRP2612G", "GRP2612P", "GRP2612W", "GRP2613", "GRP2614", "GRP2615", "GRP2616", "GRP2624", "GRP2634", "GRP2636", "GRP2650", "GRP2670", "GSC3505", "GSC3506", "GSC3510", "GSC3516", "GSC3570", "GSC3574", "GSC3575", "GSC3610", "GSC3615", "GSC3620", "GXP1100", "GXP1105", "GXP1600C", "GXP1610C", "GXP1610P", "GXP1615", "GXP1628B", "GXP1760", "GXP1760W", "GXP1780", "GXP1782", "GXP2130", "GXP2135", "GXP2136", "GXP2140", "GXP2160", "GXP2170", "GXV3240", "GXV3275", "GXV3350", "GXV3370", "GXV3380", "GXV3450", "GXV3470", "GXV3480", "GXV3500", "WP800", "WP810", "WP816", "WP820", "WP822", "WP825", "WP826", "WP856",]

# Argument parser setup for command-line inputs
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

# Parse the command-line arguments
args = parser.parse_args()

# Handle version argument
if args.v:
    print("\nkgzcfg version: {}".format(version))
    sys.exit(0)

# Model input validation
if args.m:
    check = args.m.upper()
    if is_in_list(check, supported_model_list):
        model = args.m.upper()

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
        if is_valid_subnet_mask(args.n):
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
    if args.i in (1, 2):
        ip_mode = args.i

# Function to get the configuration file paths
def get_config_file(project):
    kgzcfg = "kgzcfg"
    script_directory = os.getcwd()  # Get the current script directory
    folder_path = os.path.join(script_directory, kgzcfg, project)  # Set folder path based on project name
    
    # Create the directory if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

    # Set file paths for output files
    export_zero_config_csv_file_name = "kgzcfg_export_zc_devices.csv"
    mac_file_name = "mac.txt"
    deployment_file_name = "deployment-details.csv"
    account_file_name = "account.txt"

    export_zero_config_csv_file_path = os.path.join(folder_path, export_zero_config_csv_file_name)  # Full path for config file
    mac_file_path = os.path.join(script_directory, kgzcfg, mac_file_name)  # Path for MAC address file
    deployment_file_path = os.path.join(folder_path, deployment_file_name)  # Path for deployment file
    account_file_path = os.path.join(script_directory, kgzcfg, account_file_name)  # Path for MAC address file
    
    # Open files or create them if they don't exist
    try:
        with open(export_zero_config_csv_file_path, "r") as file:
            # Process the data as needed
            print(f"Found existing '{export_zero_config_csv_file_name}' in the '{project}' folder as the script.")
        with open(deployment_file_path, "r") as file:
            # Process the data as needed
            print(f"Found existing '{deployment_file_name}' in the '{project}' folder as the script.")    
    except FileNotFoundError:
        # If the file doesn't exist, create it
        with open(export_zero_config_csv_file_path, "w") as file:
            # Initialize the file content (if required)
            print(f"Created '{export_zero_config_csv_file_name}' in the '{project}' folder as the script.")
        with open(deployment_file_path, "w") as file:
            # Process the data as needed
            print(f"Created '{deployment_file_name}' in the '{project}' folder as the script.")                
    finally:
        return (export_zero_config_csv_file_path, mac_file_path, deployment_file_path, account_file_path)

# Function to display a progress bar
def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    terminal_width, _ = shutil.get_terminal_size()
    if terminal_width > 72:
        terminal_width = 72

    bar_width = int((terminal_width - 10) * (percent / 100))
    bar = '#' * bar_width + '-' * (terminal_width - 10 - bar_width)

    print(f"\r|{bar}| {percent:.2f}%", end="\r")

# ASCII logo used in the script
logo = [
    ".--------------------------------------------------------------.",
    "| 88                                           ad88            |",
    "| 88                                          d8\"              |",
    "| 88                                          88               |",
    "| 88   ,d8  ,adPPYb,d8 888888888  ,adPPYba, MM88MMM ,adPPYb,d8 |",
    "| 88 ,a8\"  a8\"    `Y88      a8P\" a8\"     \"\"   88   a8\"    `Y88 |",
    "| 8888[    8b       88   ,d8P'   8b           88   8b       88 |",
    "| 88`\"Yba, \"8a,   ,d88 ,d8\"      \"8a,   ,aa   88   \"8a,   ,d88 |",
    "| 88   `Y8a `\"YbbdP\"Y8 888888888  `\"Ybbd8\"'   88    `\"YbbdP\"Y8 |",
    "|           aa,    ,88                              aa,    ,88 |",
    "|            \"Y8bbdP\"                                \"Y8bbdP\"  |",
    "`--------------------------------------------------------------'"
]

# Function to display the loading logo
def slow_print_logo(logo, delay):
    for line in logo:
        print(line)
        time.sleep(delay)  # Add delay between each line

def logo_loading():
    slow_print_logo(logo, delay=loading_time+0.01)  # Adjust delay for slower/faster printing

# Function to clear the terminal screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for Windows ('cls') or Unix/Linux ('clear')

# Main function for running the loading effect
def loading():
    #clear()  # Clear the terminal screen
    logo_loading()  # Show the ASCII logo with a loading effect

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

def append_config_to_csv(export_zero_config_csv_file_path, configs):
    with open(export_zero_config_csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for config in configs:
            for section, rows in config.items():
                for row in rows:
                    writer.writerow(row.split(','))

def main(mac_addresses, model, ucm_ip, start_ip, subnet_mask, gateway_ip, dns_ip, start_account, ip_mode, loading_time):
    loading()
    total_steps = 100
    progress_bar(0, total_steps)
    
    # Simulate a task that takes time (e.g., reading files, processing data, etc.)
    for i in range(total_steps):
        time.sleep(loading_time)  # Simulating work (replace with real task)
        progress_bar(i + 1, total_steps)
    print()  # Print a newline after completion    
    print()  # Print a newline after completion    
    site = input("Enter Site Name > ")
    path = get_config_file(site)
    export_zero_config_csv_file_path, mac_file_path, deployment_file_path, account_file_path = path
    try:
        with open(mac_file_path, 'r') as file:
            from_file_mac_addresses = []
            for line in file:
                found_macs = mac_pattern.findall(line.strip())
                from_file_mac_addresses.extend(found_macs)
            print("MAC addresses successfully read from mac.txt")

            # Process the found MAC addresses
            valid_macs, invalid_macs = mac_processing(from_file_mac_addresses)

            if valid_macs:
                print("\nValid MAC addresses:")
                for mac in valid_macs:
                    print(mac)
                    mac_addresses.append(mac)

            if invalid_macs:
                print("\nInvalid MAC addresses:")
                for mac in invalid_macs:
                    print(mac)
            print()
            # If no valid MAC addresses found, ask the user for input
            if not valid_macs:
                print("No valid MAC addresses found in the file.")
                valid_macs, invalid_macs = get_user_mac_input()

                print("\nValid MAC addresses from input:")
                for mac in valid_macs:
                    print(mac)
                    mac_addresses.append(mac)

                if invalid_macs:
                    print("\nInvalid MAC addresses from input:")
                    for mac in invalid_macs:
                        print(mac)

    except FileNotFoundError:
        print(f"'{mac_file_path}' not found in the same folder as the script.")
        valid_macs, invalid_macs = get_user_mac_input()

        print("\nValid MAC addresses from input:")
        for mac in valid_macs:
            print(mac)
            mac_addresses.append(mac)

        if invalid_macs:
            print("\nInvalid MAC addresses from input:")
            for mac in invalid_macs:
                print(mac)

    if ucm_ip == "":
        while True:
            ucm_ip = input("Enter the UCM IP address > ")
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
            model = input("Enter the Model default (GRP2601P) > ") or "GRP2601P"
            model = model.upper()
            if is_in_list(model, supported_model_list):
                break
    accounts = []
    try:
        with open(account_file_path, 'r') as file:
            print("Accounts successfully read from account.txt")
            for line in file:
                if is_numeric(line.strip()):
                    accounts.append(line.strip())
    except:
        print(f"'{account_file_path}' not found in the same folder as the script.")
        if start_account == "":
            while True:
                start_account = input("Enter the starting Account number > ")
                if is_numeric(start_account):
                    start_account = int(start_account)
                    break
        count = len(mac_addresses)
        accounts = generate_account_numbers(start_account, count)
    print(accounts)
    print()
    if ip_mode == "":
        while True: 
            ip_mode = input("Enter IP Phone network mode (1. DHCP 2. Static) > ")
            if ip_mode in ("1" ,"2"):
                break
    ip_mode = int(ip_mode)
    if ip_mode == 2:
        if start_ip == "":
            while True:
                start_ip = input("Enter the IP Phone starting IP address > ")
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
                print("Enter the Subnet Mask default (255.255.255.0) > ", end="")
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
                print(f"Enter the Gateway IP address default ({default_gateway}) > ", end="")
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
                dns_ip = input("Enter the DNS IP address default (8.8.8.8) > ") or "8.8.8.8"
                if is_valid_ip(dns_ip):
                    if is_valid_subnet_mask(dns_ip):
                        print("Entered value is Subnet Mask not IP Addresss")
                        continue
                    else:
                        break
                else:
                    print("Invalid IP address. Please enter a valid IPv4 address.")            
            

    if ip_mode == 2:
        ips = generate_ip_range(start_ip, count)

    if not len(mac_addresses) == len(accounts):
        print(f"Found number of MAC address and Account Number does not match. Numebr of MAC Address Found: {len(mac_addresses)} Number of Accounts Found: {len(accounts)}")
        sys.exit(0)

    # Create config file with static ip address
    if ip_mode == 2:
        configs = [create_static_config(mac.strip(), ips[i], accounts[i], model, dns_ip, subnet_mask, gateway_ip, ucm_ip) for i, mac in enumerate(mac_addresses)]
    if ip_mode == 1:
        configs = [create_dhcp_config(mac.strip(), accounts[i], model, ucm_ip) for i, mac in enumerate(mac_addresses)]
    
    append_config_to_csv(export_zero_config_csv_file_path, configs)
    
    # Display assigned IP and account numbers
    if ip_mode == 1:
        print("\nAssigned MAC Address to Accounts:")
        for i, mac in enumerate(mac_addresses):
            print(f"MAC Address: {mac.strip()} - Account: {accounts[i]}")
            with open(deployment_file_path, mode='a') as file:
                file.write(f"MAC Address,{mac.strip()},Account,{accounts[i]}\n")
    if ip_mode == 2:
        print("\nAssigned IPs and Accounts:")
        for i, mac in enumerate(mac_addresses):
            print(f"MAC Address: {mac.strip()} - IP: {ips[i]} - Account: {accounts[i]}")
            with open(deployment_file_path, mode='a') as file:
                file.write(f"MAC Address,{mac.strip()},IP,{ips[i]},Account,{accounts[i]}\n")            

try:
    if __name__ == "__main__":
        main(mac_addresses, model, ucm_ip, start_ip, subnet_mask, gateway_ip, dns_ip, start_account, ip_mode, loading_time)
except:
    print("\nkgzcfg Stop Executing.")

finally:
    print("\n[kgzcfg_v{}]:".format(version))
