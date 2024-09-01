# Grandstream Zero Configuration File Generator

This script is designed to generate zero configuration files for Grandstream IP phones. It supports a wide range of models and provides the ability to configure both DHCP and static IP addresses.

## Version

Current version: **1.0.6**

## Description

The script generates configuration files for Grandstream IP phones based on various parameters provided by the user, including MAC addresses, IP address settings, phone models, and other network configurations.

## Features

- Supports multiple Grandstream IP phone models.
- Configures IP phones with either DHCP or static IP addresses.
- Automatically validates IP addresses, subnet masks, and other inputs.
- Creates or appends configuration files in CSV format.

## Usage

To use this script, you need Python 3.x installed on your system.

### Command Line Arguments

- `-v` : Print version info.
- `-m` : IP Phone Model.
- `-u` : UCM IP Address.
- `-s` : Starting IP Address.
- `-n` : Subnet Mask.
- `-g` : Gateway IP Address.
- `-a` : Starting Account number.
- `-d` : DNS IP Address.
- `-i` : IP Phone network mode (1 for DHCP, 2 for Static).

### Examples

To run the script with arguments:

    python kgzcfg.py -m GRP2601P -u 192.168.1.1 -s 192.168.1.100 -n 255.255.255.0 -g 192.168.1.1 -a 1000 -d 8.8.8.8 -i 2

To display the version:

```sh
python kgzcfg.py -v
```

### Interactive Mode

If no arguments are provided, the script will prompt the user to input the necessary values interactively.

## Supported Models

The script supports the following Grandstream IP phone models:

- GHP610, GHP610W, GHP611, GHP611W, GHP620, GHP620W, GHP621, GHP621W, GHP630, GHP630W, GHP631, GHP631W, GRP2601, GRP2601P, GRP2601W, GRP2602, GRP2602G, GRP2602P, GRP2602W, GRP2603, GRP2603P, GRP2604, GRP2604P, GRP2612, GRP2612G, GRP2612P, GRP2612W, GRP2613, GRP2614, GRP2615, GRP2616, GRP2624, GRP2634, GRP2636, GRP2650, GRP2670, GSC3505, GSC3506, GSC3510, GSC3516, GSC3570, GSC3574, GSC3575, GSC3610, GSC3615, GSC3620, GXP1100, GXP1105, GXP1600C, GXP1610C, GXP1610P, GXP1615, GXP1628B, GXP1760, GXP1760W, GXP1780, GXP1782, GXP2130, GXP2135, GXP2136, GXP2140, GXP2160, GXP2170, GXV3240, GXV3275, GXV3350, GXV3370, GXV3380, GXV3450, GXV3470, GXV3480, GXV3500, WP800, WP810, WP816, WP820, WP822, WP825, WP826, WP856.

## Output

The script will generate or update a file named `kgzcfg_export_zc_devices.csv` in the same directory as the script. This file contains the configuration settings for the specified IP phones.

### Example Output

```
|###############################-----------------| 60.00%
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
```

## Error Handling

The script will display appropriate error messages if any input is invalid, such as:

- "Invalid IP address. Please enter a valid IPv4 address."
- "Invalid Subnet Mask. Please enter a valid Subnet Mask."

## Dependencies

- Python Standard Libraries: `csv`, `argparse`, `sys`, `re`, `ipaddress`, `os`, `shutil`, `math`.

## Quickstart

### Prerequisites

- **Python 3.x** is required.
- The `csv`, `argparse`, `sys`, `re`, `ipaddress`, `os`, `shutil`, `math` module (included with Python standard library).

### Installation

1. **Clone the Repository or Download the Script:**

   ```bash
   git clone https://github.com/karan-modh-5/kgzcfg.git
   cd kgzcfg
2. Run the Script:
   ```bash
    python kgzcfg.py

## Usage
### 1. Follow the Prompts:

When you run the script, you will be prompted to enter the following details:

-  CSV file path: Path to the existing CSV file to which configurations will be appended.
-  MAC addresses: Comma-separated list of MAC addresses.
-  Model, UCM IP address, DNS, Subnet Mask, Gateway IP: Configuration details for each phone.
-  Starting IP address: The base IP address to begin assigning.
-  Starting account number: The base account number to begin assigning.

### 2. Example Input:

    Enter the path to the CSV file: /path/to/your/file.csv
    Enter the MAC addresses (comma separated): C074AD73443,C074ADC34566,EC74D745677F
    Enter the Model: GRP2601P
    UCM IP address: 192.168.43.160
    Enter the IP Phone starting IP address: 192.168.1.10
    Enter the Subnetmask default (255.255.255.0): 
    Enter the Gateway IP address default (192.168.1.1): 
    Enter the DNS IP address default (8.8.8.8): 
    Enter the starting account number: 300

### 3. Output:

The script will append new configurations to the specified CSV file and display assigned IPs and account numbers:

    Assigned IPs and Accounts:
    MAC Address: C074AD778923 - IP: 192.168.1.10 - Account: 300
    MAC Address: C074ADC89745 - IP: 192.168.1.11 - Account: 301
    MAC Address: EC74D7840392 - IP: 192.168.1.12 - Account: 302

## Troubleshooting
- Permission Denied: Ensure you have write permissions for the CSV file.
- Incorrect Inputs: Double-check that all inputs are correctly formatted.



