import time as t
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
import Adafruit_MCP4725 as MCP
import Adafruit_DHT as DHT

pin1 = 4    #senzor import time as t
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
import Adafruit_MCP4725 as MCP
import Adafruit_DHT as DHT

pin1 = 4    #senzor 1
pin2 = 17  #senzor 2
pin3 = 27  #senzor3

sensor = DHT.DHT22

ventilacija1 = 5              # 1. relej 
ventilacija2 = 6	     # 2. relej
ventilacija3 = 13	     # 3. relej
tunel1 = 16		     # 4. relej
tunel2= 	20		    # 5. relej
tunel3= 	21		    # 6. relej	
grejanje = 26		    # 7. relej		
hladjenje =  19

GPIO.setup(ventilacija1,GPIO.OUT)
GPIO.setup(ventilacija2,GPIO.OUT)
GPIO.setup(ventilacija3,GPIO.OUT)
GPIO.setup(tunel1,GPIO.OUT)
GPIO.setup(tunel2,GPIO.OUT)
GPIO.setup(tunel3,GPIO.OUT)
GPIO.setup(grejanje,GPIO.OUT)
GPIO.setup(hladjenje,GPIO.OUT)

def procenat_servo(p):
	if(p < 0 and p > 100):
		p = 0
	x = 4096.0/5 # napon od 1 V
	x = 4096 - x #napon ide od 1 do 5, a ne od 0 do 5 pa skracujemo interval za 1 V
	x = x/100.0*p # klasicna proporcija od 0 do 100%
	x = x + 4096.0/5 # povecavamo interval za petinu za bi dobili opseg od 1 do 5 V a ne od 0 do 4 V
	return long(round(x,0))   # MORA DA BUDE LONG DA BI RADILO NA KONVERTORU

def servo_radi_uz_min_ventilacije(procenat):
	dac = MCP.MCP4725()
	if(procenat == 5):
		procenat = procenat_servo(procenat)
		dac.set_voltage(procenat)
		dac.set_voltage(0)
	if(procenat == 10):
		procenat = procenat_servo(procenat)
		dac.set_voltage(procenat)
		dac.set_voltage(procenat_servo(5))
	if(procenat == 15):
		procenat = procenat_servo(procenat)
		dac.set_voltage(procenat)
		dac.set_voltage(10)
	if(procenat == 25):
		procenat = procenat_servo(procenat)
		dac.set_voltage(procenat)
		dac.set_voltage(15)
	if(procenat == 30):
		procenat = procenat_servo(procenat)
		dac.set_voltage(procenat)
		dac.set_voltage(25)
	print str(procenat), str(sekunde_servo)



def min_ventilacija_interval(kubikaza, broj, dan): #vraca koliko sekundi u intervalu od 6 minuta treba daradi minimalna ventilacija
	masa = broj*kilaza(dan)
	ciklus = 0.1 #sekunda
	potrebno_kiseonika = masa*6.0
	potrebno_ciklus = potrebno_kiseonika/kubikaza
	radi = potrebno_ciklus*ciklus
	radi = round(radi, 3)
	return radi*360

procenat = 0
sekunde_servo = 0
sek = 0 #globalne sekunde koliko dugo radi min ventilacije
usao_u_minimum_ventilacije = True
def min_ventilacija_radi(sekunde, temp, dan):
	optimal = 33.0 - 0.29*dan
	global procenat
	global sekunde_servo
	global sek
	global usao_u_minimum_ventilacije

	sek = sekunde

	print str(sek)

	if(sekunde > 360):
		sekunde = 360
		sek = sekunde

	if(temp < optimal + 1.2):

		usao_u_minimum_ventilacije = True

		if(sekunde < 50):
			print("5%")
			sekunde_servo = 3*sekunde
			procenat = 5

		if(sekunde > 50 and sekunde < 100):
			print("10%")
			procenat = 10
			sekunde_servo = 2*sekunde

		if(sekunde > 100 and sekunde < 200):
			print("15%")
			procenat = 15
			sekunde_servo = sekunde

		if(sekunde > 200 and sekunde < 300):
			print("25%")
			sekunde_servo = sekunde
			procenat = 25

		if(sekunde > 300):
			print("30%")
			sekunde_servo = sekunde
			procenat = 30

		#cekaj(sekunde) #treba da bude sekunde

def servo_set(procenat):
	dac = MCP.MCP4725()
	procenat = procenat_servo(procenat)
	dac.set_voltage(procenat)
	print str(procenat), str(sekunde_servo)

def ukupna_masa(broj_zivih, dan):
	return broj_zivih*kilaza(dan)

def kilaza(dan): #na osnovu dana starosti vraca kilazu pileta
	if(dan == 1):
		return 0.042
	if(dan == 2):
		return 0.052
	if(dan == 3):
		return 0.065
	if(dan == 4):
		return 0.081
	if(dan == 5):
		return 0.108
	if(dan == 6):
		return 0.130
	if(dan == 7):
		return 0.164
	if(dan == 8):
		return 0.204
	if(dan == 9):
		return 0.250
	if(dan == 10):
		return 0.290
	if(dan == 11):
		return 0.320
	if(dan == 12):
		return 0.340
	if(dan == 13):
		return 0.380
	if(dan == 14):
		return 0.430
	if(dan == 15):
		return 0.460
	if(dan == 16):
		return 0.502
	if(dan == 17):
		return 0.550
	if(dan == 18):
		return 0.600
	if(dan == 19):
		return 0.670
	if(dan == 20):
		return 0.750
	if(dan == 21):
		return 0.843
	if(dan == 22):
		return 0.950
	if(dan == 23):
		return 1.100
	if(dan == 24):
		return 1.220
	if(dan == 25):
		return 1.280
	if(dan == 26):
		return 1.340
	if(dan == 27):
		return 1.380
	if(dan == 28):
		return 1.397
	if(dan == 29):
		return 1.442
	if(dan == 30):
		return 1.542
	if(dan == 31):
		return 1.642
	if(dan == 32):
		return 1.742
	if(dan == 33):
		return 1.842
	if(dan == 34):
		return 1.942
	if(dan == 35):
		return 2.017
	if(dan == 36):
		return 2.142
	if(dan == 37):
		return 2.142
	if(dan == 38):
		return 2.142
	if(dan == 39):
		return 2.242
	if(dan == 40):
		return 2.342
	if(dan == 41):
		return 2.542
	if(dan == 42):
		return 2.626
	if(dan == 43):
		return 2.742
	if(dan == 44):
		return 2.942
	if(dan == 45):
		return 3.042

temperatura = 0
vlaga = 0

def meri_temperaturu():

	error_code = 0

	global temperatura
	global vlaga

	try:
		hum1, temp1 = DHT.read_retry(sensor, pin1)
		print 'Temp1={0:0.1f} C  Humidity={1:0.1f}%'.format(temp1, hum1)
	except:
		error_code = 1  # ne radi prvi
		print "Ne radi senzor 1"

	try:
		hum2, temp2 = DHT.read_retry(sensor, pin2)
		print 'Temp2={0:0.1f} C  Humidity={1:0.1f}%'.format(temp2,hum2)
	except:
		if(error_code == 1): # ne rade prvi i drugi
			error_code = 4
		else: 
			error_code = 2  # ne radi drugi
		print "Ne radi senzor 2"

	try:
		hum3, temp3 = DHT.read_retry(sensor, pin3)
		print 'Temp3={0:0.1f} C  Humidity={1:0.1f}%\n'.format(temp3, hum3)
	except:
		if(error_code == 1):
			error_code == 5 # ne rade prvi i treci
		elif(error_code == 2): 
			error_code = 6 # ne rade drugi i treci
		elif(error_code == 4): 
			error_code = 7 # ne radi nista
		else:
			error_code = 3
		print "Ne radi senzor 3"

	if(error_code == 7): print'Zovi majstora' 
	
	temperatura = avg_temp(temp1, temp2, temp3, error_code)
	vlaga = avg_temp(hum1, hum2, hum3, error_code)

def avg_temp(temp1, temp2, temp3, error_code):
	if(error_code == 0): #svi rade
		return (temp1+temp2+temp3)/3.0
	if(error_code == 1): #crko prvi senzor
		return (temp2+temp3)/2.0
	if(error_code == 2): #crko drugi senzor
		return (temp1+temp3)/2.0
	if(error_code == 3): #crko treci senzor
		return (temp2+temp1)/2.0
	if(error_code == 4): # crkli prvi i drugi
		return temp3
	if(error_code == 5): # crkli prvi i treci
		return temp2
	if(error_code == 6): #crkli drugi i treci
		return temp1
	if(error_code == 7): #sve u kurac
		return -99.9   # OVDE DODATI DA SE TRAZI UNETA TRENUTNA TEMPERATURA


def dodeli(relej1, relej2, relej3, relej4, relej5, relej6, relej7, relej8): # dodeljuje radno stanje relejima, 0=radi, 1=ne radi
		GPIO.output(ventilacija1, relej1)
		GPIO.output(ventilacija2, relej2)
		GPIO.output(ventilacija3, relej3)
		GPIO.output(tunel1, relej4) 
		GPIO.output(tunel2, relej5)
		GPIO.output(tunel3, relej6)
		GPIO.output(hladjenje, relej7)
		GPIO.output(grejanje, relej8)

dodeli(1,1,1,1,1,1,1,1)

def regulacija(temp, dan, spoljnja_temperatura):
	global procenat
	global sek
	global usao_u_minimum_ventilacije
	if(dan == 0):
		pocetna_temperatura = 33.0
	optimal = 33.0 - 0.29*dan
	print optimal
	if(temp > optimal + 1.2):
		usao_u_minimum_ventilacije = False
		sek = 10
		if(temp > optimal + 1.2 and temp < optimal + 2.0):
			print('relej 1 rad konstantno. gasi grejanje')
			procenat = 30
			dodeli(0,1,1,1,1,1,1,1)
		elif(temp > optimal + 2.0 and temp < optimal + 3.0):
			print('radi relej 3 i relej 2 konstantno')
			procenat = 60
			dodeli(1,0,0,1,1,1,1,1)
		elif(temp > optimal + 3.0 and temp < optimal + 4.0):
			print('rade relej 1, relej 2 i relej 3') # rade prva tri ostale gasimo
			dodeli(0,0,0,1,1,1,1,1)
			procenat = 100
		elif(temp > optimal + 4.0 and temp < optimal + 5.0):
			print('radi relej 3 i relej tunel 1')
			dodeli(1,1,0,0,1,1,1,1)
			procenat = 100
		elif(temp > optimal + 5.0 and temp < optimal + 6.0):
			print('radi tunel 1 i tunel 2')
			dodeli(1,1,1,0,0,1,1,1)
			procenat = 0
		elif(temp > optimal + 6.0 and temp < optimal + 6.6):
			print('radi tunel 1, tunel 2 i tunel 3')
			dodeli(1,1,1,0,0,0,1,1)
			procenat = 0
		elif(temp > optimal + 6.6):
			dodeli(1,1,1,0,0,0,1,1)
			procenat = 0
			print('rade tunel 1, tunel 2, tunel 3')
			if(spoljnja_temperatura > 21):
				print('radi i klima') # palimo klimu i sva tri tunelca
				dodeli(1,1,1,0,0,0,0,1)
				procenat = 0
	x = 6.0/10
	if((optimal - temp) > x):
		print('pali grejanje')
		GPIO.output(grejanje, 0)

def cekaj(sekunde):
	t.sleep(sekunde)

def citaj_temperaturu1():
	try:
		hum1, temp1 = DHT.read_retry(sensor, pin1)
		print 'Temp1={0:0.1f} C  Humidity={1:0.1f}%'.format(temp1, hum1)
	except:
		error_code = 1  # ne radi prvi
		print "Ne radi senzor 1"
	return temp1
def citaj_temperaturu2():
	try:
		hum1, temp1 = DHT.read_retry(sensor, pin2)
		print 'Temp1={0:0.1f} C  Humidity={1:0.1f}%'.format(temp1, hum1)
	except:
		error_code = 1  # ne radi prvi
		print "Ne radi senzor 1"
	return temp1
def citaj_temperaturu3():
	try:
		hum1, temp1 = DHT.read_retry(sensor, pin3)
		print 'Temp1={0:0.1f} C  Humidity={1:0.1f}%'.format(temp1, hum1)
	except:
		error_code = 1  # ne radi prvi
		print "Ne radi senzor 1"
	return temp1
def citaj_vlagu1():
	try:
		hum1, temp1 = DHT.read_retry(sensor, pin1)
		print 'Temp1={0:0.1f} C  Humidity={1:0.1f}%'.format(temp1, hum1)
	except:
		error_code = 1  # ne radi prvi
		print "Ne radi senzor 1"
	return hum1
def citaj_vlagu2():
	try:
		hum1, temp1 = DHT.read_retry(sensor, pin2)
		print 'Temp1={0:0.1f} C  Humidity={1:0.1f}%'.format(temp1, hum1)
	except:
		error_code = 1  # ne radi prvi
		print "Ne radi senzor 1"
	return hum1
def citaj_vlagu3():
	try:
		hum1, temp1 = DHT.read_retry(sensor, pin3)
		print 'Temp1={0:0.1f} C  Humidity={1:0.1f}%'.format(temp1, hum1)
	except:
		error_code = 1  # ne radi prvi
		print "Ne radi senzor 1"
	return hum1
















1
pin2 = 17  #senzor 2
pin3 = 27  #senzor3

sensor = DHT.DHT22

ventilacija1 = 5              # 1. relej 
ventilacija2 = 6	     # 2. relej
ventilacija3 = 13	     # 3. relej
tunel1 = 16		     # 4. relej
tunel2= 	20		    # 5. relej
tunel3= 	21		    # 6. relej	
grejanje = 26		    # 7. relej		
hladjenje =  19

GPIO.setup(ventilacija1,GPIO.OUT)
GPIO.setup(ventilacija2,GPIO.OUT)
GPIO.setup(ventilacija3,GPIO.OUT)
GPIO.setup(tunel1,GPIO.OUT)
GPIO.setup(tunel2,GPIO.OUT)
GPIO.setup(tunel3,GPIO.OUT)
GPIO.setup(grejanje,GPIO.OUT)
GPIO.setup(hladjenje,GPIO.OUT)

def procenat_servo(p):
	if(p < 0 and p > 100):
		p = 0
	x = 4096.0/5 # napon od 1 V
	x = 4096 - x #napon ide od 1 do 5, a ne od 0 do 5 pa skracujemo interval za 1 V
	x = x/100.0*p # klasicna proporcija od 0 do 100%
	x = x + 4096.0/5 # povecavamo interval za petinu za bi dobili opseg od 1 do 5 V a ne od 0 do 4 V
	return long(round(x,0))   # MORA DA BUDE LONG DA BI RADILO NA KONVERTORU

def servo_radi_uz_min_ventilacije(procenat):
	dac = MCP.MCP4725()
	if(procenat == 5):
		procenat = procenat_servo(procenat)
		dac.set_voltage(procenat)
		dac.set_voltage(0)
	if(procenat == 10):
		procenat = procenat_servo(procenat)
		dac.set_voltage(procenat)
		dac.set_voltage(procenat_servo(5))
	if(procenat == 15):
		procenat = procenat_servo(procenat)
		dac.set_voltage(procenat)
		dac.set_voltage(10)
	if(procenat == 25):
		procenat = procenat_servo(procenat)
		dac.set_voltage(procenat)
		dac.set_voltage(15)
	if(procenat == 30):
		procenat = procenat_servo(procenat)
		dac.set_voltage(procenat)
		dac.set_voltage(25)
	print str(procenat), str(sekunde_servo)



def min_ventilacija_interval(kubikaza, broj, dan): #vraca koliko sekundi u intervalu od 6 minuta treba daradi minimalna ventilacija
	masa = broj*kilaza(dan)
	ciklus = 0.1 #sekunda
	potrebno_kiseonika = masa*6.0
	potrebno_ciklus = potrebno_kiseonika/kubikaza
	radi = potrebno_ciklus*ciklus
	radi = round(radi, 3)
	return radi*360

procenat = 0
sekunde_servo = 0
sek = 0 #globalne sekunde koliko dugo radi min ventilacije
usao_u_minimum_ventilacije = True
def min_ventilacija_radi(sekunde, temp, dan):
	optimal = 33.0 - 0.29*dan
	global procenat
	global sekunde_servo
	global sek
	global usao_u_minimum_ventilacije

	sek = sekunde

	print str(sek)

	if(sekunde > 360):
		sekunde = 360
		sek = sekunde

	if(temp < optimal + 1.2):

		usao_u_minimum_ventilacije = True

		if(sekunde < 50):
			print("5%")
			sekunde_servo = 3*sekunde
			procenat = 5

		if(sekunde > 50 and sekunde < 100):
			print("10%")
			procenat = 10
			sekunde_servo = 2*sekunde

		if(sekunde > 100 and sekunde < 200):
			print("15%")
			procenat = 15
			sekunde_servo = sekunde

		if(sekunde > 200 and sekunde < 300):
			print("25%")
			sekunde_servo = sekunde
			procenat = 25

		if(sekunde > 300):
			print("30%")
			sekunde_servo = sekunde
			procenat = 30

		#cekaj(sekunde) #treba da bude sekunde

def servo_set(procenat):
	dac = MCP.MCP4725()
	procenat = procenat_servo(procenat)
	dac.set_voltage(procenat)
	print str(procenat), str(sekunde_servo)

def ukupna_masa(broj_zivih, dan):
	return broj_zivih*kilaza(dan)

def kilaza(dan): #na osnovu dana starosti vraca kilazu pileta
	if(dan == 1):
		return 0.042
	if(dan == 2):
		return 0.052
	if(dan == 3):
		return 0.065
	if(dan == 4):
		return 0.081
	if(dan == 5):
		return 0.108
	if(dan == 6):
		return 0.130
	if(dan == 7):
		return 0.164
	if(dan == 8):
		return 0.204
	if(dan == 9):
		return 0.250
	if(dan == 10):
		return 0.290
	if(dan == 11):
		return 0.320
	if(dan == 12):
		return 0.340
	if(dan == 13):
		return 0.380
	if(dan == 14):
		return 0.430
	if(dan == 15):
		return 0.460
	if(dan == 16):
		return 0.502
	if(dan == 17):
		return 0.550
	if(dan == 18):
		return 0.600
	if(dan == 19):
		return 0.670
	if(dan == 20):
		return 0.750
	if(dan == 21):
		return 0.843
	if(dan == 22):
		return 0.950
	if(dan == 23):
		return 1.100
	if(dan == 24):
		return 1.220
	if(dan == 25):
		return 1.280
	if(dan == 26):
		return 1.340
	if(dan == 27):
		return 1.380
	if(dan == 28):
		return 1.397
	if(dan == 29):
		return 1.442
	if(dan == 30):
		return 1.542
	if(dan == 31):
		return 1.642
	if(dan == 32):
		return 1.742
	if(dan == 33):
		return 1.842
	if(dan == 34):
		return 1.942
	if(dan == 35):
		return 2.017
	if(dan == 36):
		return 2.142
	if(dan == 37):
		return 2.142
	if(dan == 38):
		return 2.142
	if(dan == 39):
		return 2.242
	if(dan == 40):
		return 2.342
	if(dan == 41):
		return 2.542
	if(dan == 42):
		return 2.626
	if(dan == 43):
		return 2.742
	if(dan == 44):
		return 2.942
	if(dan == 45):
		return 3.042

temperatura = 0
vlaga = 0

def meri_temperaturu():

	error_code = 0

	global temperatura
	global vlaga

	try:
		hum1, temp1 = DHT.read_retry(sensor, pin1)
		print 'Temp1={0:0.1f} C  Humidity={1:0.1f}%'.format(temp1, hum1)
	except:
		error_code = 1  # ne radi prvi
		print "Ne radi senzor 1"

	try:
		hum2, temp2 = DHT.read_retry(sensor, pin2)
		print 'Temp2={0:0.1f} C  Humidity={1:0.1f}%'.format(temp2,hum2)
	except:
		if(error_code == 1): # ne rade prvi i drugi
			error_code = 4
		else: 
			error_code = 2  # ne radi drugi
		print "Ne radi senzor 2"

	try:
		hum3, temp3 = DHT.read_retry(sensor, pin3)
		print 'Temp3={0:0.1f} C  Humidity={1:0.1f}%\n'.format(temp3, hum3)
	except:
		if(error_code == 1):
			error_code == 5 # ne rade prvi i treci
		elif(error_code == 2): 
			error_code = 6 # ne rade drugi i treci
		elif(error_code == 4): 
			error_code = 7 # ne radi nista
		else:
			error_code = 3
		print "Ne radi senzor 3"

	if(error_code == 7): print'Zovi majstora' 
	
	temperatura = avg_temp(temp1, temp2, temp3, error_code)
	vlaga = avg_temp(hum1, hum2, hum3, error_code)

def avg_temp(temp1, temp2, temp3, error_code):
	if(error_code == 0): #svi rade
		return (temp1+temp2+temp3)/3.0
	if(error_code == 1): #crko prvi senzor
		return (temp2+temp3)/2.0
	if(error_code == 2): #crko drugi senzor
		return (temp1+temp3)/2.0
	if(error_code == 3): #crko treci senzor
		return (temp2+temp1)/2.0
	if(error_code == 4): # crkli prvi i drugi
		return temp3
	if(error_code == 5): # crkli prvi i treci
		return temp2
	if(error_code == 6): #crkli drugi i treci
		return temp1
	if(error_code == 7): #sve u kurac
		return -99.9   # OVDE DODATI DA SE TRAZI UNETA TRENUTNA TEMPERATURA


def dodeli(relej1, relej2, relej3, relej4, relej5, relej6, relej7, relej8): # dodeljuje radno stanje relejima, 0=radi, 1=ne radi
		GPIO.output(ventilacija1, relej1)
		GPIO.output(ventilacija2, relej2)
		GPIO.output(ventilacija3, relej3)
		GPIO.output(tunel1, relej4) 
		GPIO.output(tunel2, relej5)
		GPIO.output(tunel3, relej6)
		GPIO.output(hladjenje, relej7)
		GPIO.output(grejanje, relej8)

dodeli(1,1,1,1,1,1,1,1)

def regulacija(temp, dan, spoljnja_temperatura):
	global procenat
	global sek
	global usao_u_minimum_ventilacije
	if(dan == 0):
		pocetna_temperatura = 33.0
	optimal = 33.0 - 0.29*dan
	print optimal
	if(temp > optimal + 1.2):
		usao_u_minimum_ventilacije = False
		sek = 10
		gornja_granica = 1.2
		if(temp > optimal + gornja_granica and temp < optimal + 0.8 + gornja_granica):
			print('relej 1 rad konstantno. gasi grejanje')
			procenat = 30
			dodeli(0,1,1,1,1,1,1,1)
		elif(temp > optimal + 0.8 + gornja_granica and temp < optimal + 1.8 + gornja_granica):
			print('radi relej 3 i relej 2 konstantno')
			procenat = 60
			dodeli(1,0,0,1,1,1,1,1)
		elif(temp > optimal + 1.8  + gornja_granica and temp < optimal + 2.8 + gornja_granica):
			print('rade relej 1, relej 2 i relej 3') # rade prva tri ostale gasimo
			dodeli(0,0,0,1,1,1,1,1)
			procenat = 100
		elif(temp > optimal + 2.8 + gornja_granica and temp < optimal + 3.8 + gornja_granica):
			print('radi relej 3 i relej tunel 1')
			dodeli(1,1,0,0,1,1,1,1)
			procenat = 100
		elif(temp > optimal + 3.8 + gornja_granicaand temp < optimal + 4.8 + gornja_granica):
			print('radi tunel 1 i tunel 2')
			dodeli(1,1,1,0,0,1,1,1)
			procenat = 0
		elif(temp > optimal + 4.8 + gornja_granica and temp < optimal + 5.4 + gornja_granica):
			print('radi tunel 1, tunel 2 i tunel 3')
			dodeli(1,1,1,0,0,0,1,1)
			procenat = 0
		elif(temp > optimal + 5.4 + gornja_granica):
			dodeli(1,1,1,0,0,0,1,1)
			procenat = 0
			print('rade tunel 1, tunel 2, tunel 3')
			if(spoljnja_temperatura > 21):
				print('radi i klima') # palimo klimu i sva tri tunelca
				dodeli(1,1,1,0,0,0,0,1)
				procenat = 0
	donja_granica = 6.0/10
	if((optimal - temp) > donja_granica):
		print('pali grejanje')
		GPIO.output(grejanje, 0)

def cekaj(sekunde):
	t.sleep(sekunde)




















