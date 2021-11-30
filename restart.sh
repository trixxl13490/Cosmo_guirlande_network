sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill - 9
sudo python3 /home/pi/Cosmo_guirlande_network/gui_rpi.py 2 30 192.168.0.20 50002 1024