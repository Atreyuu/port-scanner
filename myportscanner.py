import socket
import psutil


def validate_IPv4_address (given_ip_address):
    parts = given_ip_address.split('.')

    if len(parts) != 4:
        return False

    for x in range(4):
        if int(parts[x]) > 255 or int(parts[x]) < 0:
            return False
        if x == 3:
            return True


def validate_port_format (ports):
    parts = ports.split('-')

    if len(parts) != 2:
        print("You passed wrong port format, here is an example: 11-6535")
        return False

    try:
        if int(parts[0]) > int(parts[1]):
            print("You should pass lower port number first")
            return False
    except:
        print("You probaby passed some chars as port number, because I could not convert it to int type properly :c")

    for x in range(2):
        if int(parts[x]) < 1 or int(parts[x]) > 65535:
            print("You should pass port numbers from range 1-65535")
            return False
    return True


def get_own_IPv4_address ():
    data = psutil.net_if_addrs()
    inters = list(data.keys())
    my_ips = []
    for x in range(1,len(data)):
        if validate_IPv4_address(data[inters[x]][0][1]):
            my_ips.append(data[inters[x]][0][1])
    return my_ips


def scan_ports(given_IP):
    print("Currently scanning:", given_IP)
    print("Do you want to scan all ports (type all) or specific range (give me that range in format xxxx-xxxx)?")
    ans = input()
    if ans == 'all':
        try:
            for x in range(1,65535):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                if not s.connect_ex((given_IP, x)):
                    print("Port", x, "is open")
        except:
            print("Something went wrong")          
    else:
        if validate_port_format(ans):
            ports = ans.split('-')
            try:
                for x in range(int(ports[0]),int(ports[1])):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(1)
                    if not s.connect_ex((given_IP, x)):
                        print("Port", x)
            except:
                print("Something went wrong")


print("Walcome in my own port scanner!")
owned_IPs = get_own_IPv4_address()
print("Found IP addresses: ")
for x in range(len(owned_IPs)):
    print("Press", x+1, "if you want to scan", owned_IPs[x], "address")
chosen_ip = input()
try:
    if int(chosen_ip) in range(len(owned_IPs)+1):
        scan_ports(owned_IPs[int(chosen_ip)-1])
        pass
    else:
        print("Wrong choice (you should pass me number from range 1-"+ str(len(owned_IPs)) + ")")
except:
    print("Wrong choice (you should pass me NUMBER from range 1-"+ str(len(owned_IPs)) + ")")
