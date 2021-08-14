# Setup and Networking
## One time setup with IPv4
**Ensure the sensor is powered off and disconnected at this point.**  
  The ```[eth name]``` is the nework interface you're connecting to. On older Linux systems, that's ```eth0``` or similar. In newer versions, its ```enp...``` or ```enx...``` when you look at the output of ```ifconfig```.
 ```
 ip addr flush dev [eth name]  
 ip addr show dev [eth name]
 ```
The output you see from show should look something like ```[eth name] ... state DOWN ....``` Its only important that you see ```DOWN``` and not ```UP```. Next, lets setup a static IP address for your machine so you can rely on this in the future. Ouster uses the 10.5.5.* range, and I don't see a compelling reason to argue with it.
```
sudo ip addr add 10.5.5.1/24 dev [eth name]
```
Now, lets setup the connection. At this point you may now plug in and ```power on your sensor```.
```
sudo ip link set [eth name] up
sudo addr show dev [eth name]
```
The output you see from show should look something like ```[eth name] ... state UP ....``` Its only important that you see ```UP``` now and not ```DOWN```. At this point, you've setup the networking needed for the one time setup.
## Connection with IPv4
We can setup the network connection to the sensor now with the proper settings. Note: This command could take up to 30 seconds to setup, be patient. If after a minute you see no results, then you probably have an issue. Start the instructions above over. Lets set up the network
```
sudo dnsmasq -C /dev/null -kd -F 10.5.5.50,10.5.5.100 -i [eth name] --bind-dynamic
```
Instantly you should see something similar to:
```
dnsmasq: started, version 2.75 cachesize 150
dnsmasq: compile time options: IPv6 GNU-getopt DBus i18n IDN DHCP DHCPv6 no-Lua TFTP conntrack ipset auth DNSSEC loop-detect inotify
dnsmasq-dhcp: DHCP, IP range 10.5.5.50 -- 10.5.5.100, lease time 1h
dnsmasq-dhcp: DHCP, sockets bound exclusively to interface enxa0cec8c012f8
dnsmasq: reading /etc/resolv.conf
dnsmasq: using nameserver 127.0.1.1#53
dnsmasq: read /etc/hosts - 10 addresses
```
You need to wait until you see something like:
```
dnsmasq-dhcp: DHCPDISCOVER(enxa0cec8c012f8) [HWaddr]
dnsmasq-dhcp: DHCPOFFER(enxa0cec8c012f8) [ping name] [HWaddr]
dnsmasq-dhcp: DHCPREQUEST(enxa0cec8c012f8) [ping name] [HWaddr]
```
Now you're ready for business. Lets see what IP address it's on (10.5.5.87). Lets ping it
```
ping [ping name]
```
and we're good to go!

# ROS Connection
## set parameters
Determine the parameters in the launch file
```
sensor_hostname = LaunchConfiguration('sensor_hostname', default="10.5.5.86")
lidar_mode = LaunchConfiguration('sensor_hostname', default="512x10")
udp_dest = LaunchConfiguration('udp_dest', default="10.5.5.2")
```
Now that we have a connection over the network, lets view some data. After building your colcon workspace with this package, source the install space. Run
```
ros2 launch ouster_ros ouster.launch.py
```
