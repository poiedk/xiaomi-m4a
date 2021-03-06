import os
import sys
import telnetlib
import subprocess
import ftplib

router_ip_address = "192.168.31.1"
router_ip_address = input("Router IP address [press enter for using the default {}]: ".format(router_ip_address)) or router_ip_address

for path,dirs,files in os.walk('firmwares'):
	c=len(files)
	if c <= 0:
		print ("OS firmware not found")
		sys.exit(1)
	i=1
	while i <= len(files):
		print("(%d) %s" % (i, files[i-1]))
		i += 1
print()
try:
	i = int(input("Select OS firmware: "))
except:
	print ("Input error")
	sys.exit(1)

if i <= 0 or i > c:
	print ("Input not found")
	sys.exit(1)

file1=open(os.path.join(path,files[i-1]), 'rb')

try:
	file2=open('data/flashos.sh', 'rb')
except:
	print ("flash script not found")
	sys.exit(1)

try:
	ftp=ftplib.FTP(router_ip_address)
except:
	print ("ftp server not found")
	sys.exit(1)

print ("Uploading OS upgrade ...")
ftp.storbinary('STOR /tmp/sysupgrade.bin', file1)
ftp.storbinary('STOR /tmp/flashos.sh', file2)
file1.close()
file2.close()
ftp.quit()
print ("Upload done")

tn = telnetlib.Telnet(router_ip_address)
tn.read_until(b"login:")
tn.write(b"root\n")
tn.read_until(b"root@XiaoQiang:~#")
tn.write(b"nohup sh /tmp/flashos.sh >/dev/null 2>&1 &\n")
tn.read_until(b"root@XiaoQiang:~#",10)
print ("Router has just started rewriting the OS firmware.")
print ("Do not switch off the router.")
print ("Router will automatically reboot.")
print ("The current window can be closed.")
