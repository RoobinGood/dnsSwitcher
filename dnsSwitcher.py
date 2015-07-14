from subprocess import check_output

  
def getInterfaces(text):
	markers = ["Ethernet adapter", "Адаптер беспроводной локальной сети"]
	params = ["IPv4-адрес", "DNS-серверы"]
	interfaces = [];
	for m in markers:
		currentPosition = text.find(m)
		while (currentPosition != -1):
			interfaces.append({"pos":currentPosition})
			currentPosition = currentPosition + len(m) + 1
			endPosition = text.find(":", currentPosition)
			interfaces[len(interfaces)-1]["name"] = text[currentPosition:endPosition]
			currentPosition = text.find(m, currentPosition+1)
	return interfaces

def setDnsAddr(name, addr, index):
	print(str(check_output("netsh interface ip add dns name=\"{}\" addr={} index={}".format(
		name, addr, index)), "cp866"))

def setDhcpDns(name):
	print(str(check_output("netsh interface ip set dnsservers name=\"{}\" source=dhcp".format(
		name)), "cp866"))

def setGoogleDns(name):
	setDnsAddr(name, "8.8.8.8", 1)
	setDnsAddr(name, "8.8.4.4", 2)

# CLI
def cliShowInterfaces(interfaces):
	for i in range(len(interfaces)):
		print(i, "-", interfaces[i])

def cliChooseInterface(interfaces):
	cliShowInterfaces(interfaces)
	i = -1
	while (i<0 or i>=len(interfaces)):
		i = int(input("\nChoose interface:\n> "))
	return i

def cliChooseDnsSettings():
	print()
	print("0 - DHCP DNS")
	print("1 - Google DNS")
	i = -1
	while (i<0 or i>=2):
		i = int(input("\nChoose dns settings:\n> "))
	return i

def cli():
	print("WARNING: app needs admin rights!\n")
	interfaces = getInterfaces(str(check_output("ipconfig /all"), "cp866"))
	i = cliChooseInterface(interfaces)
	print(interfaces[i]["name"])
	d = cliChooseDnsSettings()
	if (d == 0):
		setDhcpDns(interfaces[i]["name"])
	elif (d == 1):
		setGoogleDns(interfaces[i]["name"])


cli()

# todo: get interface params (ip, dns)
# todo: choose settings
# settings:
# 1. Google DNS
# netsh interface ip add dns name="Local Area Connection" addr=8.8.4.4 index=1
# netsh interface ip add dns name="Local Area Connection" addr=8.8.8.8 index=2
# 2. DHCP DNS
# netsh interface ip set dnsservers name="Local Area Connection" source=dhcp