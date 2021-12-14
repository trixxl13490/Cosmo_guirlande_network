import paramiko
import argparse
import socket
import time


#All args here: args.guirlande_number, args.num_pixel, args.server_tcp_ip, args.tcp_port, args.buffer_size
#Get Server (this computer) IP address
h_name = socket.gethostname()
IP_addres = socket.gethostbyname(h_name)

#Create SSH connection with paramiko
ssh1 = paramiko.SSHClient()
ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh1.connect(hostname='192.168.0.5', username='pi', password='vbcgxb270694', timeout=2, port=22)

# kill GUI if running
ssh_stdin1, ssh_stdout1, ssh_stderr1 = ssh1.exec_command("sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill -9")

# Start GUI again on rpi
channel1 = ssh1.invoke_shell()
stdin1 = channel1.makefile('wb')
stdout1 = channel1.makefile('rb')

stdin1.write('''
  export XAUTHORITY=/home/pi/.Xauthority
  DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 2 30 192.168.0.20 50002 1024'
  ''')

print(stdout1.read())
#----------------------------------------------------------------------------------------------------------------------
ssh2 = paramiko.SSHClient()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect(hostname='192.168.0.26', username='pi', password='vbcgxb270694', timeout=2, port=22)


# kill GUI if running
ssh_stdin2, ssh_stdout2, ssh_stderr2 = ssh2.exec_command("sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill -9")

# Start GUI again on rpi
channel2 = ssh2.invoke_shell()
stdin2 = channel2.makefile('wb')
stdout2 = channel2.makefile('rb')

stdin2.write('''
  export XAUTHORITY=/home/pi/.Xauthority
  DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 30 192.168.0.20 50001 1024'
  ''')
print(stdout2.read())
#----------------------------------------------------------------------------------------------------------------------

'''
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


channel = ssh.invoke_shell()
stdin = channel.makefile('wb')
stdout= channel.makefile('rb')

cmd1 = 'export XAUTHORITY=/home/pi/.Xauthority'
cmd2 = 'DISPLAY=:0  /usr/bin/lxterm -e "sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py ' + str(args.guirlande_number) + ' ' + str(args.num_pixel) + ' ' + str(IP_addres) + ' ' + str(args.tcp_port) + ' ' + str(args.buffer_size) + '"'
'''
#cmd = str("'''") + "\n" + cmd1 + "\n" + cmd2 + "\n"  + str("'''")
'''
print("cmd: ", cmd)
print("cmd1: ", cmd1)
print("cmd2: ", cmd2)
stdin.write(cmd)
'''

#if __name__ == '__main__':
