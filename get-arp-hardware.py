import subprocess
import pandas as pd
import json
import paho.mqtt.client as mqtt
import subprocess
import paramiko

#get known Hardware
MAC_RPi =[
  "74:da:38:f6:dd:ef", # - 144 RGBW
  "b8:27:eb:04:77:43", # - 56  RGB  (string)
  "b8:27:eb:5d:3d:de", # - 144 RGBW
  "b8:27:eb:a4:fd:a8", # - 30  RGBW
  "b8:27:eb:bf:ac:3a", # - 144 RGBW
  "b8:27:eb:c2:e9:2b", # - 35  RGB  (stick)
  "b8:27:eb:d0:01:ff", # - 50  RGBW (stick ring)
  "b8:27:eb:ed:90:54", # - 144 RGBW
  "01:00:5e:00:00:fc"  #for testing
]
#get arp table
proc = subprocess.Popen(["arp", "-a"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
out_list = []
out_list = out.splitlines()

IP = []
MAC = []

for lines in out_list:
    try:
      #decode bytes to str
      lines = lines.decode()
      c1 = str(lines).split("b'")
      #remove '' empty char from list
      c1 = "".join(c1).split()
      #get useful information here
      c1[0] = c1[0].replace(" ", "")
      c1[1] = c1[1].replace(" ", "")
      c1[2] = c1[2].replace(" ", "")
      #sort IP & MAC and append it to a list
      c1[0] = c1[0].strip()
      c1[1] = c1[1].strip()

      print("c1[0)] IP",c1[0]) #IP
      print("c1[1)] MAC",c1[1]) #MAC
      #print("c1[2)]",c1[2].strip()) #Bail

      #Replace '-' by ':'
      IP_MAC_array = [c1[0],
                      c1[1].replace('-',':')      ]
      
      IP.append(c1[0])
      MAC.append(c1[1].replace('-',':')  )
    except UnicodeDecodeError:
      print("UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 9: invalid start byte")
    except IndexError:
      print("Index Error")
    except TypeError:
      print("Type Error")

print("IP_MAC_array : ", IP_MAC_array)


#Create df
IP_MAC_df = pd.DataFrame(columns=['IP', 'MAC'])
IP_MAC_df["MAC"] = MAC 
IP_MAC_df["IP"] = IP
#print("IP_MAC_df : ", IP_MAC_df.to_string())  

#find if hardwares match
for elt1 in MAC_RPi:
  for elt2 in IP_MAC_df['MAC']:
    if elt1 == elt2:
      print("match")
      #try to connect & configure
      mqtt_cli = mqtt.Client() 
      mqtt_cli.connect(elt2["IP"],1883,60)
      mqtt_cli.publish('test1', "cosmoguirlande,blackout")

      #launch command to start scipt
      ssh1 = paramiko.SSHClient()
      ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh1.connect(hostname=elt2["IP"], username='pi', password='vbcgxb270694', timeout=5, port=22)

      # kill GUI if running
      ssh_stdin, ssh_stdout, ssh_stderr = ssh1.exec_command("sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill -9")

      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

      ssh.connect(hostname=elt2["IP"], username='pi', password='vbcgxb270694', timeout=5, port=22)

      # Start GUI again on rpi
      channel = ssh.invoke_shell()
      stdin = channel.makefile('wb')
      stdout = channel.makefile('rb')

      ssh.exec_command("sudo python3 start_thread_arg.py " + elt2["MAC"]")
      print("sudo python3 start_thread_arg.py " + elt2["MAC"]")

      print("ssh passed : ", elt2["IP"])
      
      print('stdout.read()' , repr(stdout.read()))
      stdout.close()
      stdin.close()

      #add on file for other scipts

#check in config.json file for IPs

#try to connect



