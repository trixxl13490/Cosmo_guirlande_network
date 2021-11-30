sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill - 9
sudo python3 gui_rpi.py 2 30 192.168.0.20 50002 1024