import subprocess
import sys

# ping ip 
p = {} # ip -> process
ips = []
ip = "192.168.1.45"

for n in range(1, 255): # start ping processes
    ip = "192.168.1.%d" % n
    #ignore output
    p[ip] = subprocess.Popen(['ping', '-w5', '-c3', ip],stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    #With output
    '''p[ip] = subprocess.Popen(['ping', '-w5', '-c3', ip])
    out, err = p[ip].communicate()'''

# arp list 
p = subprocess.Popen(['arp', '-a'], stderr=subprocess.PIPE,stdout=subprocess.PIPE)

out, err = p.communicate()

#parse and store output:
for line in out.splitlines():
    print(line)
    if 'b8-27-eb-d0-01-ff' in str(line):
        ips.append(line)
    elif 'b8-27-eb-c2-e9-2b' in str(line):
        ips.append(line)
    '''if 'b8-27-eb-d0-01-ff' in str(line):
        ips.append(line)
    if 'b8-27-eb-d0-01-ff' in str(line):
        ips.append(line)
    if 'b8-27-eb-d0-01-ff' in str(line):
        ips.append(line)
    if 'b8-27-eb-d0-01-ff' in str(line):
        ips.append(line)
    if 'b8-27-eb-d0-01-ff' in str(line):
        ips.append(line)
    if 'b8-27-eb-d0-01-ff' in str(line):
        ips.append(line)
    if 'b8-27-eb-d0-01-ff' in str(line):
        ips.append(line)'''

print(ips)

