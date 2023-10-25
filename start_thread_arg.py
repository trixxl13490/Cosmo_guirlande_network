import paramiko
import json
import socket
import time
import threading
import argparse
import subprocess

'''
You need first to setup Pi with:
74:da:38:f6:dd:ef - 144 RGBW
b8:27:eb:04:77:43 - 42  RGB  (string)
b8:27:eb:5d:3d:de - 144 RGBW
b8:27:eb:a4:fd:a8 - 30  RGBW
b8:27:eb:bf:ac:3a - 144 RGBW
b8:27:eb:c2:e9:2b - 35  RGB  (stick)
b8:27:eb:d0:01:ff - 50  RGBW (stick)
b8:27:eb:ed:90:54 - 144 RGBW

'''

#All args here: args.guirlande_number, args.num_pixel, args.server_tcp_ip, args.tcp_port, args.buffer_size
#Get Server (this computer) IP address
h_name = socket.gethostname()
IP_addres = socket.gethostbyname(h_name)

conf_file = open('IP_configuration.json')
strip_configuration = json.load(conf_file)

  
class Thread_start_display_remote_ssh(threading.Thread):

  def __init__(self, message,  mac):
    threading.Thread.__init__(self)
    self.message = message
    #self.ip = ip
    self.mac = mac

  def run(self):
      try:
        """ssh1 = paramiko.SSHClient()
        ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh1.connect(hostname=self.ip, username='pi', password='vbcgxb270694', timeout=5, port=22)

        #time.sleep(2)

        # kill GUI if running
        ssh_stdin, ssh_stdout, ssh_stderr = ssh1.exec_command("sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill -9")
        #time.sleep(1)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip, username='pi', password='vbcgxb270694', timeout=5, port=22)

        # Start GUI again on rpi
        channel = ssh1.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb')"""

                    subprocess.Popen(args = "sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill -9", shell=True))

        #----------------------------------------------case 1 : config RGBW 144 LEDs
        if self.mac == "74:da:38:f6:dd:ef":
            """ssh.exec_command('''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 42 192.168.0.20 50001 1024 RGB'
              ''')"""
            
            subprocess.Popen(args='''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 42 192.168.0.20 50001 1024 RGB'
              ''', shell=True)
        #----------------------------------------------case 2 : config RGBW 144 LEDs
        elif self.mac == "b8:27:eb:04:77:43":
            """ssh.exec_command('''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
              ''')"""
            
            ssh.exec_command('''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
              ''', shell=True)
        #----------------------------------------------case 3 : config RGBW 144 LEDs
        elif self.mac == "b8:27:eb:5d:3d:de":
            """ssh.exec_command('''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
              ''')"""
            
            subprocess.Popen(args='''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
              ''', shell=True)
        #----------------------------------------------case 4 : config RGBW 144 LEDs
        elif self.mac == "b8:27:eb:a4:fd:a8":
            """ssh.exec_command('''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 30 192.168.0.20 50001 1024 RGBW'
              ''')"""  
                  
            subprocess.Popen(args='''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 30 192.168.0.20 50001 1024 RGBW'
              ''', shell=True)
        #----------------------------------------------case 5 : config RGBW 144 LEDs
        elif self.mac == "b8:27:eb:bf:ac:3a":
            """ssh.exec_command('''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
              ''')"""
            
            subprocess.Popen(args='''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
              ''', shell=True)
        #----------------------------------------------case 6 : config RGBW 144 LEDs
        elif self.mac == "b8:27:eb:c2:e9:2b":
            """ssh.exec_command('''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 35 192.168.0.20 50001 1024 RGB'
              ''')   """  
           
            subprocess.Popen(args='''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 35 192.168.0.20 50001 1024 RGB'
              ''', shell=True)
        #----------------------------------------------case 7 : config RGBW 144 LEDs
        elif self.mac == "b8:27:eb:d0:01:ff":
            """ssh.exec_command('''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 50 192.168.0.20 50001 1024 RGBW'
              ''')"""
            
            subprocess.Popen(args='''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 50 192.168.0.20 50001 1024 RGBW'
              ''', shell=True)
        #----------------------------------------------case 8 : config RGBW 144 LEDs
        elif self.mac == "b8:27:eb:ed:90:54":
            """ssh.exec_command('''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
              ''')"""
            
            subprocess.Popen(args='''
              export XAUTHORITY=/home/pi/.Xauthority
              DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
              ''', shell=True)
        else:
           print("no matching MAC, basic config 144 RGBW")
        #----------------------------------------------
        print("ssh passed : ", self.ip)
        """print('stdout.read()' , repr(stdout.read()))
        stdout.close()
        stdin.close()"""

      except socket.timeout:
          print("ss1 timeout")
      #except:
      #  time.sleep(1)

if __name__ == "__main__":
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('mac_address', metavar='mac_address', type=int, help='mac_address')
    args = parser.parse_args()
  
