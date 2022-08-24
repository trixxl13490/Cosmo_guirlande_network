import paramiko
import json
import socket
import time


#All args here: args.guirlande_number, args.num_pixel, args.server_tcp_ip, args.tcp_port, args.buffer_size
#Get Server (this computer) IP address
h_name = socket.gethostname()
IP_addres = socket.gethostbyname(h_name)

#Load config files with IP, port & LED number
conf_file = open('IP_configuration.json')
strip_configuration = json.load(conf_file)

for elt in strip_configuration["guirlande"]:
#for i in range(len(strip_configuration['guirlande'])):
    try:
        #Create SSH connection with paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=elt["IP"], username='pi', password='vbcgxb270694', timeout=5, port=22)

        channel = ssh.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb')

        # kill GUI if running
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("cd /home/pi/Cosmo_guirlande_network/ && sudo git pull")

        stdout.close()
        stdin.close()

        #print(stdout1.read())
        print("ssh passed")
    except socket.timeout:
        print("socket.timeout, device must be offline : ", elt["IP"])

"""
#--------------------------------------------------------------------------------------------------------------------
try:
    #Create SSH connection with paramiko
    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(hostname='192.168.0.50', username='pi', password='vbcgxb270694', timeout=5, port=22)

    # kill GUI if running
    ssh_stdin1, ssh_stdout1, ssh_stderr1 = ssh1.exec_command("cd /home/pi/Cosmo_guirlande_network/ && sudo git pull")

    #print(stdout1.read())
    print("ss1 passed")

except socket.timeout:
    print("ss1 timeout")
#----------------------------------------------------------------------------------------------------------------------
try:
    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.connect(hostname='192.168.1.45', username='pi', password='vbcgxb270694', timeout=5, port=22)


    # kill GUI if running

    ssh_stdin2, ssh_stdout2, ssh_stderr2 = ssh2.exec_command("cd /home/pi/Cosmo_guirlande_network/ && sudo git pull")

    print("ss2 passed")

except socket.timeout:
    print("ss2 timeout")

#----------------------------------------------------------------------------------------------------------------------
try:
    ssh3 = paramiko.SSHClient()
    ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh3.connect(hostname='192.168.1.53', username='pi', password='vbcgxb270694', timeout=5, port=22)


    # kill GUI if running
    ssh_stdin3, ssh_stdout3, ssh_stderr3 = ssh3.exec_command("cd /home/pi/Cosmo_guirlande_network/ && sudo git pull")

    print("ss3 passed")
    time.sleep(2.5)

except socket.timeout:
    print("ss3 timeout")

#----------------------------------------------------------------------------------------------------------------------
try:
    ssh4 = paramiko.SSHClient()
    ssh4.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh4.connect(hostname='192.168.1.43', username='pi', password='vbcgxb270694', timeout=5, port=22)


    # kill GUI if running
    ssh_stdin3, ssh_stdout3, ssh_stderr3 = ssh4.exec_command("cd /home/pi/Cosmo_guirlande_network/ && sudo git pull")

    print("ss4 passed")
    time.sleep(2.5)

except socket.timeout:
    print("ss4 timeout")

#----------------------------------------------------------------------------------------------------------------------
try:
    ssh5 = paramiko.SSHClient()
    ssh5.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh5.connect(hostname='192.168.1.15', username='pi', password='vbcgxb270694', timeout=5, port=22)

    # kill GUI if running
    ssh_stdin5, ssh_stdout5, ssh_stderr5 =  ssh5.exec_command("cd /home/pi/Cosmo_guirlande_network/ && sudo git pull")

    print("ss5 passed")
    time.sleep(2.5)

except socket.timeout:
    print("ss5 timeout")
"""