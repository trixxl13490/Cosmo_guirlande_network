import paramiko
import json
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

conf_file = open('IP_configuration.json')
strip_configuration = json.load(conf_file)

  
class Thread_start_display_remote_ssh(threading.Thread):

  def __init__(self, message, ip):
    threading.Thread.__init__(self)
    self.message = message
    self.ip = ip

  def run(self):
      try:
        ssh1 = paramiko.SSHClient()
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
        stdout = channel.makefile('rb')

        ssh.exec_command('''
          export XAUTHORITY=/home/pi/.Xauthority
          DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 1 144 192.168.0.20 50001 1024 RGBW'
          ''')
        
        print("ssh passed : ", self.ip)
        
        print('stdout.read()' , repr(stdout.read()))
        stdout.close()
        stdin.close()

      except socket.timeout:
          print("ss1 timeout")
      #except:
      #  time.sleep(1)

if __name__ == "__main__":
  i = 0
  ssh = []
  for elt in strip_configuration["guirlande"]:
    ssh.append(Thread_start_display_remote_ssh("message",elt["IP"]))
    ssh[i].start()
    i = i+1
  #last one don't start
  '''ssh[i-1] = Thread_start_display_remote_ssh("message",elt["IP"])
  ssh[i-1].start()'''
  
