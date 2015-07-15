from subprocess import check_output, CalledProcessError
from os.path import isfile, join, dirname, realpath
import json

MARKERS = ["Ethernet adapter", "Адаптер беспроводной локальной сети"]
PARAMS = ["IPv4", "DNS-серверы"]

# cmd routine
def getInterfaces(text):

	def getParam(paramName, start, end):
		startPos = text.find(paramName, start, end);
		if (startPos != -1):
			startPos = text.find(":", startPos) + 2
			endPos = text.find("\n", startPos)
			pos = text.find("\n", endPos+1)
			while (pos != -1  and  text.find(":", endPos, pos) == -1):
				endPos = pos
				pos = text.find("\n", endPos+1)
			param = text[startPos:endPos]
			param = param.replace(" ", "").replace("\r", "").replace("\n", ", ")
		else:
			param = None
		return param

	interfaces = [];
	for m in MARKERS:
		currentPosition = text.find(m)
		while (currentPosition != -1):
			interfaces.append({"pos":currentPosition})
			currentPosition = currentPosition + len(m) + 1
			endPosition = text.find(":", currentPosition)
			interfaces[len(interfaces)-1]["name"] = text[currentPosition:endPosition]
			currentPosition = text.find(m, currentPosition+1)

	for i in range(len(interfaces)):
		for p in PARAMS:
			param = getParam(p, interfaces[i]["pos"],
				interfaces[i+1] if (i+1<len(interfaces)) else len(text))
			if (param != None):
				interfaces[i][p] = param

	return interfaces

def setDnsAddr(name, addr, index):
	try:
		check_output("netsh interface ip add dns name=\"{}\" addr={} index={}".format(name, addr, index))
		print("Success!")
		return 1
	except CalledProcessError:
		print("\nCannot set DNS addr\nMaybe app doesn't have admin rights or settings is wrong:")
		print("\tname: {}\n\taddr: {}\n\tindex: {}".format(name, addr, index))
		return 0

def setDhcpDns(name):
	try:
		check_output("netsh interface ip set dnsservers name=\"{}\" source=dhcp".format(name))
		print("Success!")
	except CalledProcessError:
		print("\nCannot set DNS addr\nMaybe app doesn't have admin rights or settings is wrong")
		print("\tname: {}".format(name))

# settings routine
def loadSettings(fileName):
	return json.load(open(fileName))

def setFromSettings(name, settings):
	for i in range(len(settings["settings"])):
		if (setDnsAddr(name, settings["settings"][i], i+1) == 0):
			break

# CLI
def cliChooseInterface(interfaces):
	for i in range(len(interfaces)):
		print("{} - {}".format(i, interfaces[i]["name"]))
		for p in PARAMS:
			if (p in interfaces[i].keys()):
				print("\t{}: {}".format(p, interfaces[i][p]))
	i = -1
	while (i<0 or i>=len(interfaces)):
		i = int(input("\nChoose interface:\n> "))
	return i

def cliChooseDnsSettings(settings):
	print()
	print("0 - DHCP DNS")
	for i in range(len(settings)):
		print(i+1, "-", settings[i]["name"])
	i = -1
	while (i<0 or i>len(settings)):
		i = int(input("\nChoose dns settings:\n> "))
	return i

def cli(interfaces, settings):
	print("\nWARNING: app needs admin rights!\n")
	i = cliChooseInterface(interfaces)
	print(interfaces[i]["name"])
	d = cliChooseDnsSettings(settings)
	if (d == 0):
		setDhcpDns(interfaces[i]["name"])
	else:
		setFromSettings(interfaces[i]["name"], settings[d-1])


settingsFileName = "settings.conf"
interfaces = getInterfaces(str(check_output("ipconfig /all"), "cp866"))
settings = [] if not isfile(join(dirname(realpath(__file__)), settingsFileName)) else loadSettings(settingsFileName)
cli(interfaces, settings)
