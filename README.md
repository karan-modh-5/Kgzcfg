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

## Quickstart

### Prerequisites

- **Python 3.x** is required.
- The `csv` module (included with Python standard library).

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
Permission Denied: Ensure you have write permissions for the CSV file.
Incorrect Inputs: Double-check that all inputs are correctly formatted.
