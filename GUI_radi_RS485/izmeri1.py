from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=1, stopbits = 1, bytesize = 8,  parity='N', baudrate= 9600)
client.connect()
addr = 4
import sys
fajl = ""

time.sleep(1)
try:
	response = client.read_holding_registers(0x00, 4, unit=1)
	temp1 = float(response.getRegister(0))/10
	hum1 = float(response.getRegister(1))/10
	print response.registers
except:
	temp1 = -99.9
	hum1 = -99.9
time.sleep(1)
try:
	response = client.read_holding_registers(0x00, 4, unit=2)
	temp2 = float(response.getRegister(0))/10
	hum2 = float(response.getRegister(1))/10
	print response.registers
except:
	temp2 = -99.9
	hum2 = -99.9
time.sleep(1)
try:
	response = client.read_holding_registers(0x00, 4, unit=3)
	temp3 = float(response.getRegister(0))/10
	hum3 = float(response.getRegister(1))/10
	print response.registers
except:
	temp3 = -99.9
	hum3 = -99.9
time.sleep(1)
try:
	response = client.read_holding_registers(0x00, 4, unit=4)
	temp_napolju = float(response.getRegister(0))/10
	hum_napolju = float(response.getRegister(1))/10
	print response.registers
except:
	temp_napolju = -99.9
	hum_napolju = -99.9


fajl = "temperatura1.txt"

if(temp1 > 50):
	pass
else:
	openn = open(fajl, "w")
	openn.write(str(round(temp1, 1)))
	openn.close()

fajl = "temperatura2.txt"

if(temp2 > 50):
	pass
else:
	openn = open(fajl, "w")
	openn.write(str(round(temp2, 1)))
	openn.close()

fajl = "temperatura3.txt"

if(temp3 > 50):
	pass
else:
	openn = open(fajl, "w")
	openn.write(str(round(temp3, 1)))
	openn.close()

fajl = "vlaga1.txt"

if(hum1 > 10 and hum1 < 101):
		openn = open(fajl, "w")
		openn.write(str(round(hum1, 1)))
		openn.close()
else:
		openn = open(fajl, "w")
		openn.write("-99.9")
		openn.close()

fajl = "vlaga2.txt"

if(hum2 > 0 and hum2 < 101):
		openn = open(fajl, "w")
		openn.write(str(round(hum2, 1)))
		openn.close()
else:
		openn = open(fajl, "w")
		openn.write("-99.9")
		openn.close()

fajl = "vlaga3.txt"

if(hum3 > 0 and hum3 < 101):
			openn = open(fajl, "w")
			openn.write(str(round(hum3, 1)))
			openn.close()
else:
	openn = open(fajl, "w")
	openn.write("-99.9")
	openn.close()

fajl = "spoljasnja.txt"

print str(temp_napolju)
if(temp_napolju > 50):
	pass
else:
	openn = open(fajl, "w")
	openn.write(str(temp_napolju) + "\n")
if(hum_napolju > 0 or hum_napolju < 101):
	openn.write(str(hum_napolju))
	openn.close()
else:
	openn.write("-99.9")
	openn.close()

