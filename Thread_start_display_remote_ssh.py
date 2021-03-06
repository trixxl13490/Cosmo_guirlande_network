import paramiko
import argparse
import socket
import time
import threading

'''
You need first to setup Pi with:


'''

#All args here: args.guirlande_number, args.num_pixel, args.server_tcp_ip, args.tcp_port, args.buffer_size
#Get Server (this computer) IP address
h_name = socket.gethostname()
IP_addres = socket.gethostbyname(h_name)

class Thread_start_display_remote_ssh(threading.Thread):

  def __init__(self, message, ip):
    threading.Thread.__init__(self)
    self.message = message
    self.ip = ip


def run(self):
    #try:
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect(hostname=self.ip, username='pi', password='vbcgxb270694', timeout=5, port=22)


      # kill GUI if running
      ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill -9")

      # Start GUI again on rpi
      channel = ssh.invoke_shell()
      stdin = channel.makefile('wb')
      stdout = channel.makefile('rb')

      stdin.write(self.message)

    #except:
    #  time.sleep(1)

if __name__ == "__main__":
    ssh1 = Thread_start_display_remote_ssh("export XAUTHORITY=/home/pi/.Xauthority  DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 30 192.168.0.5 50001 1024'"
      ,"192.168.0.5")
    ssh2 = Thread_start_display_remote_ssh("export XAUTHORITY=/home/pi/.Xauthority  DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 2 30 192.168.0.26 50002 1024'"
      ,"192.168.0.26")
    ssh3 = Thread_start_display_remote_ssh("export XAUTHORITY=/home/pi/.Xauthority  DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 3 30 192.168.0.29 50003 1024'"
      ,"192.168.0.29")
