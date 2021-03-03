#import Adafruit_MCP4725 as MCP
#import RPi.GPIO as GPIO
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)

procenat = 0
sekunde_servo = 0
sek = 0 #globalne sekunde koliko dugo radi min ventilacije
minimum_ventilacije_radi = 0
rezim = 0
jel_greje = 0

ventilacija1 = 5              # 1. relej 
ventilacija2 = 6	     # 2. relej
ventilacija3 = 13	     # 3. relej
tunel1 = 16		     # 4. relej
tunel2= 	20		    # 5. relej
tunel3= 	21		    # 6. relej	
grejanje = 26		    # 7. relej		
hladjenje =  19	


"""GPIO.setup(ventilacija1,GPIO.OUT)
GPIO.setup(ventilacija2,GPIO.OUT)
GPIO.setup(ventilacija3,GPIO.OUT)
GPIO.setup(tunel1,GPIO.OUT)
GPIO.setup(tunel2,GPIO.OUT)
GPIO.setup(tunel3,GPIO.OUT)
GPIO.setup(grejanje,GPIO.OUT)
GPIO.setup(hladjenje,GPIO.OUT)
"""
def procenat_servo(p, addr):
	
	if(addr == 1):
		pass#dac = MCP.MCP4725(0x60)
	else:
		pass#dac = MCP.MCP4725(0x63)
	if(p < 0 and p > 100):
		p = 0

	x = 4096.0/5 # napon od 1 V
	x = 4096 - x #napon ide od 1 do 5, a ne od 0 do 5 pa skracujemo interval za 1 V
	x = x/100.0*p # klasicna proporcija od 0 do 100%
	x = x + 4096.0/5 # povecavamo interval za petinu za bi dobili opseg od 1 do 5 V a ne od 0 do 4 V
	#dac.set_voltage(long(round(x,0)))   # MORA DA BUDE LONG DA BI RADILO NA KONVERTORU
	#dac.set_voltage(2000)
def vrati_servo(procenat):
	if(procenat == 5):
		procenat_servo(0, 1)
		procenat_servo(0, 2)
	if(procenat == 10):
		procenat_servo(5, 1)
		procenat_servo(0, 2)
	if(procenat == 15):
		procenat_servo(10, 1)
		procenat_servo(0, 2)
	if(procenat == 20):
		procenat_servo(15, 1)
		procenat_servo(0, 2)
	if(procenat == 30):
		procenat_servo(20, 1)
		procenat_servo(0, 2)

def min_ventilacija_interval(kubikaza, broj, dan): #vraca koliko sekundi u intervalu od 6 minuta treba daradi minimalna ventilacija
	masa = broj*kilaza(dan)
	ciklus = 0.1 #sekunda
	potrebno_kiseonika = masa*6.0
	potrebno_ciklus = potrebno_kiseonika/kubikaza
	radi = potrebno_ciklus*ciklus
	radi = round(radi, 3)
	if(dan == 0 or broj == 0):
		return 1
	else:
		return radi*360
		
zeljena = 0

def regulacija(temp, dan, broj, kubikaza, spoljasnja_temperatura, gornja_granica, donja_granica, optimal, optimal_rucno):

	if(optimal_rucno == 1):
		pass
	else:
		optimal = 33.0 - 0.29*dan
	global zeljena
	zeljena = optimal
	global procenat
	global sekunde_servo
	global sek
	global minimum_ventilacije_radi
	global rezim
	global jel_greje

	sekunde = min_ventilacija_interval(kubikaza, broj, dan)
	sek = sekunde

	if((optimal - temp) > donja_granica):
		#GPIO.output(grejanje, 0)
		print "pali grejanje"
		jel_greje = 1
	else:
		#GPIO.output(grejanje, 1)
		print "gasi grejanje"
		jel_greje = 0

	if(temp < optimal + gornja_granica):
			print "Usao u min ventilacije"
			minimum_ventilacije_radi = 1
			rezim = 1
			if(dan != 0 and broj != 0):
				dodeli(0, 1, 1, 1, 1, 1, 1)

			print "sekunde: " + str(sekunde)
			sek = sekunde
			if(sekunde > 360):
				sekunde = 360
				sek = sekunde

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
			procenat_servo(procenat, 1)
			procenat_servo(0, 2)

	elif(temp > optimal + 1.2):

		#	GPIO.output(grejanje, 1)
			minimum_ventilacije_radi = 0
			sek = 30
			jel_greje = 0
			if(temp > optimal + gornja_granica and temp < optimal + 0.8 + gornja_granica):
				print('relej 1 rad konstantno. gasi grejanje')
				procenat = 30
				procenat_servo(procenat, 1)
				procenat_servo(0, 2)
				dodeli(0,1,1,1,1,1,1)
				rezim = 2
			elif(temp > optimal + 0.8 + gornja_granica and temp < optimal + 1.8 + gornja_granica):
				print('radi relej 3 i relej 2 konstantno')
				procenat = 60
				procenat_servo(procenat, 1)
				procenat_servo(0, 2)
				dodeli(1,0,0,1,1,1,1)
				rezim = 3
			elif(temp > optimal + 1.8  + gornja_granica and temp < optimal + 2.8 + gornja_granica):
				print('rade relej 1, relej 2 i relej 3') # rade prva tri ostale gasimo
				dodeli(0,0,0,1,1,1,1)
				procenat = 100
				procenat_servo(procenat, 1)
				procenat_servo(0, 2)
				rezim = 4
			elif(temp > optimal + 2.8 + gornja_granica and temp < optimal + 3.8 + gornja_granica):
				print('radi relej 3 i relej tunel 1')
				dodeli(1,1,0,0,1,1,1)
				procenat_servo(70, 1)
				procenat_servo(30, 2)
				rezim = 5
			elif(temp > optimal + 3.8 + gornja_granica and temp < optimal + 4.8 + gornja_granica):
				print('radi tunel 1 i tunel 2')
				dodeli(1,1,1,0,0,1,1)
				procenat_servo(0, 1)
				procenat_servo(70, 2)
				rezim = 6
			elif(temp > optimal + 4.8 + gornja_granica and temp < optimal + 5.4 + gornja_granica):
				print('radi tunel 1, tunel 2 i tunel 3')
				dodeli(1,1,1,0,0,0,1)
				procenat_servo(0, 1)
				procenat_servo(100, 2)
				rezim = 7
			elif(temp > optimal + 5.4 + gornja_granica):
				dodeli(1,1,1,0,0,0,1)
				procenat_servo(0, 1)
				procenat_servo(100, 2)
				rezim = 7
				print('rade tunel 1, tunel 2, tunel 3')

				if(spoljasnja_temperatura > 21):
					print('radi i klima') # palimo klimu i sva tri tunelca
					dodeli(1,1,1,0,0,0,0)
					procenat = 0
					jel_greje = -1

def dodeli(relej1, relej2, relej3, relej4, relej5, relej6, relej7): # dodeljuje radno stanje relejima, 0=radi, 1=ne radi
	pass
	"""GPIO.output(ventilacija1, relej1)
	GPIO.output(ventilacija2, relej2)
	GPIO.output(ventilacija3, relej3)
	GPIO.output(tunel1, relej4) 
	GPIO.output(tunel2, relej5)
	GPIO.output(tunel3, relej6)
	GPIO.output(hladjenje, relej7)
	"""
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
	else:
		return 0
