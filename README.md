# Bubu ePrint

### Firewall
1. Modify your `/etc/config/firewall` to accept packets on on TCP port 9100
   ```
   #Allow attached network printer
   config 'rule'
    option 'src' 'lan'
    option 'proto' 'tcp'
    option 'dest_port' '9100'
    option 'target' 'ACCEPT'
   ```
2. Restart firewall => `/etc/init.d/firewall restart`
### Avahi

1. Create the file `/etc/avahi/services/printer.service`
   
   ```xml
    <?xml version="1.0" standalone='no'?><!--*-nxml-*-->
    <!DOCTYPE service-group SYSTEM "avahi-service.dtd">
    <service-group>
      <name replace-wildcards="yes">ePrint PDF</name>
      <service>
        <type>_pdl-datastream._tcp</type>
        <port>9100</port>
        <txt-record>qtotal=1</txt-record>
        <txt-record>note=room 2</txt-record>
        <txt-record>ty=PDF Printer</txt-record>
        <txt-record>product=(PDF Printer)</txt-record>
        <txt-record>usb_MFG=Generic</txt-record>
        <txt-record>usb_MDL=PDF Printer</txt-record>
      </service>
    </service-group>
   ```
2. If you share a subnet between wired and wireless and the zeroconf traffic only shows up on the wired side, you might need be missing a broadcast address (bcast):
   ```
    #part of /etc/config/network
    config 'interface' 'lan'
      option 'type' 'bridge'
      option 'ifname' 'eth0.0'
      option 'proto' 'static'
      option 'ipaddr' '192.168.1.3'
      option 'netmask' '255.255.255.0
      option 'bcast' '192.168.1.255'
   ```
3. Restart avahi => `/etc/init.d/avahi-daemon restart`
   
### AWS S3
1. Create a new butcket on aws s3 name is `e-print`. 
2. Create a folder which name is `bubu-coffe-shop`.

### NODE-RED

1. Install node-red on App-Manager.
2. Install npm
   ```
   opkg update
   opkg install node-npm
   ```
3. Install aws s3 flow
   ```
   cd /root/.node-red
   npm install node-red-node-aws
   ```
4. Restart node-red.
5. Import node-red flow `nodered-flow.json`. Don't foret AWS S3 configurations !!!
