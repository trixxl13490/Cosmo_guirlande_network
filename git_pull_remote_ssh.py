import paramiko
import argparse
import socket
import time

'''
You need first to setup Pi with:


'''

#All args here: args.guirlande_number, args.num_pixel, args.server_tcp_ip, args.tcp_port, args.buffer_size
#Get Server (this computer) IP address
h_name = socket.gethostname()
IP_addres = socket.gethostbyname(h_name)

#--------------------------------------------------------------------------------------------------------------------
try:
    #Create SSH connection with paramiko
    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(hostname='192.168.1.53', username='pi', password='vbcgxb270694', timeout=5, port=22)

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
    ssh2.connect(hostname='192.168.0.7', username='pi', password='vbcgxb270694', timeout=5, port=22)


    # kill GUI if running

    ssh_stdin2, ssh_stdout2, ssh_stderr2 = ssh2.exec_command("cd /home/pi/Cosmo_guirlande_network/ && sudo git pull")

    print("ss2 passed")

except socket.timeout:
    print("ss2 timeout")

#----------------------------------------------------------------------------------------------------------------------
try:
    ssh3 = paramiko.SSHClient()
    ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh3.connect(hostname='192.168.0.36', username='pi', password='vbcgxb270694', timeout=5, port=22)


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
    ssh4.connect(hostname='192.168.0.36', username='pi', password='vbcgxb270694', timeout=5, port=22)


    # kill GUI if running
    ssh_stdin3, ssh_stdout3, ssh_stderr3 = ssh4.exec_command("cd /home/pi/Cosmo_guirlande_network/ && sudo git pull")

    print("ss4 passed")
    time.sleep(2.5)

except socket.timeout:
    print("ss4 timeout")
