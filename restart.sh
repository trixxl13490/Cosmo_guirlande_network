sudo ps aux | grep gui_rpi.py | awk '{print $2}' | xargs sudo kill - 9
export XAUTHORITY=/home/pi/.Xauthority
DISPLAY=:0  /usr/bin/lxterm -e 'sudo python3 /home/pi/Cosmo_guirlande_network/start_thread_no_arg.py'
