import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.0.26', username='pi', password='vbcgxb270694', timeout=2, port=22)
# kill
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
    "sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill -9")
# Start GUI again on rpi
channel1 = ssh.invoke_shell()
stdin = channel1.makefile('wb')
stdout = channel1.makefile('rb')
stdin.write('''
  export XAUTHORITY=/home/pi/.Xauthority
  DISPLAY=:0  /usr/bin/lxterm -e ' sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 2 30 192.168.0.20 50002 1024'
  ''')
print(stdout.read())
