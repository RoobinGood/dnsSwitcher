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

def cli():
	interfaces = getInterfaces(str(check_output("ipconfig /all"), "cp866"))
	i = cliChooseInterface(interfaces)
	print(interfaces[i]["name"])
	

cli()

# todo: get interface params (ip, dns)
# todo: choose settings
# settings:
# 1. Google DNS
# netsh interface ip add dns name="Local Area Connection" addr=8.8.4.4 index=1
# netsh interface ip add dns name="Local Area Connection" addr=8.8.8.8 index=2
# 2. DHCP DNS
# netsh interface ip set dnsservers name="Local Area Connection" source=dhcp