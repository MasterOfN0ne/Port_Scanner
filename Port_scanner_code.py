# Import the libraries needed, sys, pyfiglet for the ASCII banner, and socket to connect to a port, as well as IPy.
import sys
import pyfiglet
import socket
from IPy import IP

# Print the ASCII banner.
ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

# Create a disclaimer to make sure that I don't get in trouble for a bad thing that a user might do. Exits the program
# if the user does not want to agree to the disclaimer/use the program.
warning = input("[+] DISCLAIMER: The user is responsible for any harm that comes from this application. Enter? (y/n): ")
if warning == 'y':
    print(' ')
else:
    sys.exit()

# Make a dictionary with common ports and their uses/functions to compare to the open_ports list below.
common_Ports_Dict = {
    20: "FTP",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    137: "NetBIOS",
    139: "NetBIOS",
    443: "HTTPS",
    445: "SMTB"
}

# Create an empty list for the open ports from your scans to later compare to the dictionary above.
open_ports = []


# Create a scan function to connect to a port, set how long it takes to connect to each port, and add open ports to the
# open_ports list. Also used to clean up code, so I can just call the function later.
def scan(ipinput, port):
    global s
    try:
        s = socket.socket()
        s.settimeout(0.1)
        s.connect((ipinput, port))
        b = s.recv(1024)
        print(f"[-] Port {port} is open on {ipinput} with banner: {b}")
        open_ports.append(port)
    except socket.error as e:
        # This if statement helps the code if connection is refused, also showing if the port was having an error
        # instead of refusing a connection.
        if "refused" in str(e):
            print(f"[-] Connection to port {port} refused.")
        else:
            print(f"Error scanning port {port}")
    finally:
        s.close()


# scan an IPv4 address with a custom port range, starting at 1.
def scan_By_IP_Custom():
    p1 = int(input('[+] Enter the beginning port: '))
    p2 = int(input('[+] Enter the end port: '))
    ipinput = input('[+] Enter the target IP: ')
    for port in range(p1, p2 + 1):
        scan(ipinput, port)
    print("[-] Scan Complete!")


# Scan an IPv4 address from port 1 until 1024
def scan_By_IP_Common():
    ipinput = input('[+] Enter the target IP: ')
    for port in range(1, 1024):
        scan(ipinput, port)
    print("[-] Scan Complete!")


# Scan a hostname from port 1 to 1024.
def scan_By_Hostname_Common():
    target = input("[+] Enter a website in format: 'www.website.com': ")
    ipinput = socket.gethostbyname(target)
    for ports in range(1, 1024):
        scan(ipinput, ports)
    print("[-] Scan complete!")


# Scan a hostname with a custom port range starting at 1.
def scan_By_Hostname_Custom():
    target = input("[+] Enter a website in format: 'www.website.com': ")
    ipinput = socket.gethostbyname(target)
    p1 = int(input('[+] Enter the beginning port: '))
    p2 = int(input('[+] Enter the end port: '))
    for port in range(p1, p2 + 1):
        scan(ipinput, port)
    print("[-] Scan complete!")


# Main loop, basic intro and scan type selections. Includes a loop so that when the user enters an invalid input,
# the program presents the user with the option to try again.
print('Welcome to port scanner V1!')
while True:
    scan_Choice = input(
        "[+] Please choose scan type: 1:Scan IP w/custom port range, 2:Scan hostname's common ports, 3:Scan hostname "
        "w/custom port range, 4:Scan IP's common ports: ")
    if scan_Choice in {'1', '2', '3', '4'}:
        break
    else:
        print("[-] That's not an option! Try again.")

# Below are the scan choice modes. Users can select from 1-4.
if scan_Choice == '1':
    scan_By_IP_Custom()

if scan_Choice == '2':
    scan_By_Hostname_Common()

if scan_Choice == '3':
    scan_By_Hostname_Custom()

if scan_Choice == '4':
    scan_By_IP_Common()

# This extra code at the end shows the user if the IP is encrypted or not (HTTPS, HTTP, etc.) as well as some
# extra port information.
more_info = input("[+] Would you like to know more about the open ports on the hostname/IP? (y/n): ")
if more_info == "y":
    for port in open_ports:
        if port in common_Ports_Dict:
            print(f"[-] Port {port} is open and commonly used for {common_Ports_Dict[port]}.")
        else:
            print(f"[-] Port {port} is open, but there is no information about its common use.")
else:
    print("Bye!")
