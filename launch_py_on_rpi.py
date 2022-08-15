import paramiko
import argparse
import socket
import time

#To be tested
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
parser.add_argument('rpi_IP', metavar='rpi_IP', type=str, help='rpi_IP')
parser.add_argument('guirlande_number', metavar='guirlande_number', type=int, help='Cosmo Guirlande NUmber')
parser.add_argument('num_pixel', metavar='num_pixel', type=int, help='Number of pixel')
parser.add_argument('server_tcp_ip', metavar='server_tcp_ip', type=str, help='Server IP')
parser.add_argument('tcp_port', metavar='tcp_port', type=int, help='Tcp Port')
parser.add_argument('buffer_size', metavar='buffer_size', type=int, help='Buffer Size')
args = parser.parse_args()

#Create SSH connection with paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=str(args.rpi_IP), username='pi', password='vbcgxb270694', timeout=2, port=22)

# kill GUI if running
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill -9")


channel = ssh.invoke_shell()
stdin = channel.makefile('wb')
stdout= channel.makefile('rb')

cmd1 = 'export XAUTHORITY=/home/pi/.Xauthority'
cmd2 = 'DISPLAY=:0  /usr/bin/lxterm -e "sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py ' + str(args.guirlande_number) + ' ' + str(args.num_pixel) + ' ' + str(args.rpi_IP) + ' ' + str(args.tcp_port) + ' ' + str(args.buffer_size) + '"'

cmd = str("'''") + "\n" + cmd1 + "\n" + cmd2 + "\n"  + str("'''")
cmd = cmd1 + "\n" + cmd2 + "\n"
cmd = cmd1 + "\n" + cmd2
cmd_bis = cmd1 + "\n" + cmd2

print("args.rpi_IP : ", args.rpi_IP)

print("cmd: \n", cmd)
print('\n')

print("cmd1: \n", cmd1)
print('\n')

print("cmd2: \n", cmd2)
print('\n')

print("cmd bis: \n", cmd_bis)
print('\n')


'''#launch on RPI
stdin.write(cmd)
time.sleep(0.2)

stdin.write(cmd1)
time.sleep(0.2)

stdin.write(cmd2)
time.sleep(0.2)

stdin.write(cmd_bis)
time.sleep(0.2)'''

stdin.write('''
    export XAUTHORITY=/home/pi/.Xauthority
    DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 4 144 192.168.0.20 50004 1024 RGBW'
    ''')