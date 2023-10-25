#import paramiko
import json
import socket
import time
import threading
import subprocess
from getmac import get_mac_address as gma
#import paramiko
import os
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

class Thread_start_display_MAC(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    self.mac = str(mac)

  def run(self):
      try:
        #subprocess.Popen(args = "sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill -9", shell=True)
        print("supposed to kill former term")

      except socket.timeout:
          print("ss1 timeout")

      except:
          print("no active guirlande python term")

      finally:
        print("mac = ", self.mac)
        try:

          """ssh = paramiko.SSHClient()
          ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

          ssh.connect(hostname=self.ip, username='pi', password='vbcgxb270694', timeout=5, port=22)

          # Start GUI again on rpi
          channel = ssh.invoke_shell()
          stdin = channel.makefile('wb')
          stdout = channel.makefile('rb')"""
          #----------------------------------------------case 1 : config RGBW 144 LEDs
          if self.mac == "74:da:38:f6:dd:ef":
              
              """ssh.exec_command('''
                export XAUTHORITY=/home/pi/.Xauthority
                DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
              ''')"""
              print("guirlande 1")
              os.system("DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'")
              list_files = subprocess.run(["DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'"])
              print("The exit code was: %d" % list_files.returncode)
              subprocess.Popen(args='''
                export XAUTHORITY=/home/pi/.Xauthority
                DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
                ''', shell=True)
          #----------------------------------------------case 2 : config RGBW 144 LEDs
          elif self.mac == "b8:27:eb:04:77:43":
              
              """ssh.exec_command('''
                export XAUTHORITY=/home/pi/.Xauthority
                DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 42 192.168.0.20 50001 1024 RGB'
              ''')"""
              print("guirlande 2")
              list_files = subprocess.run(["DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'"])
              print("The exit code was: %d" % list_files.returncode)

              os.system("DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'")

              subprocess.Popen(args='''
                export XAUTHORITY=/home/pi/.Xauthority
                DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 42 192.168.0.20 50001 1024 RGB'
                ''', shell=True)
          #----------------------------------------------case 3 : config RGBW 144 LEDs
          elif self.mac == "b8:27:eb:5d:3d:de":
              
              """ssh.exec_command('''
                export XAUTHORITY=/home/pi/.Xauthority
                DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
            ''')"""
              print("guirlande 3")
              list_files = subprocess.run(["DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'"])
              print("The exit code was: %d" % list_files.returncode)

              os.system("DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'")

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
              print("guirlande 4")

              list_files = subprocess.run(["DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'"])
              print("The exit code was: %d" % list_files.returncode)

              os.system("DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'")

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
              print("guirlande 5")

              list_files = subprocess.run(["DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'"])
              print("The exit code was: %d" % list_files.returncode)

              subprocess.Popen(args='''
                export XAUTHORITY=/home/pi/.Xauthority
                DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
                ''', shell=True)
              
              os.system("DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'")

          #----------------------------------------------case 6 : config RGBW 144 LEDs
          elif self.mac == "b8:27:eb:c2:e9:2b":
              
              """ssh.exec_command('''
                export XAUTHORITY=/home/pi/.Xauthority
                DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 35 192.168.0.20 50001 1024 RGB'
            ''')"""
              print("guirlande 6")

              list_files = subprocess.run(["DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'"])
              print("The exit code was: %d" % list_files.returncode)

              os.system("DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'")


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
              print("guirlande 7")

              list_files = subprocess.run(["DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'"])
              print("The exit code was: %d" % list_files.returncode)

              os.system("DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'")

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
              print("guirlande 8")

              list_files = subprocess.run(["DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'"])
              print("The exit code was: %d" % list_files.returncode)
              
              os.system("DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'")

              subprocess.Popen(args='''
                export XAUTHORITY=/home/pi/.Xauthority
                DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
                ''', shell=True)
          #----------------------------------------------case 9 : config RGBW 144 LEDnot known
          else:
            print("no matching MAC, basic config 144 RGBW")
          #----------------------------------------------
          print("ssh passed MAC: ", self.mac)
          """print("ssh passed IP: ", self.ip)
          
          print('stdout.read()' , repr(stdout.read()))
          stdout.close()
          stdin.close()"""

        except socket.timeout:
          print("ss1 timeout")

if __name__ == "__main__":
    # Process arguments
    mac = gma()
    print("no args")
    newThread = Thread_start_display_MAC()
    newThread.start()