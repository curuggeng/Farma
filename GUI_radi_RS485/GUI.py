#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import datetime
import os
#import RPi.GPIO as GPIO
import f
import vaga
import time
#import matplotlib.pyplot as plt
import vreme_dialog

#GPIO.setwarnings(False)

ventilacija1_pin = 5              # 1. relej 
ventilacija2_pin = 6	     # 2. relej
ventilacija3_pin = 13	     # 3. relej
tunel1_pin = 16		     # 4. relej
tunel2_pin = 	20		    # 5. relej
tunel3_pin = 	21		    # 6. relej	
grejanje_pin = 26		    # 7. relej		
hladjenje_pin =  19
alarm_pin = 24
grejanje_sonda_1_pin = 15
grejanje_sonda_3_pin = 18
vlaga_relej_pin = 23
#GPIO.setmode(GPIO.BCM)

"""GPIO.setup(ventilacija1_pin,GPIO.OUT)
GPIO.setup(ventilacija2_pin,GPIO.OUT)
GPIO.setup(ventilacija3_pin,GPIO.OUT)
GPIO.setup(tunel1_pin,GPIO.OUT)
GPIO.setup(tunel2_pin,GPIO.OUT)
GPIO.setup(tunel3_pin,GPIO.OUT)
GPIO.setup(grejanje_pin,GPIO.OUT)
GPIO.setup(hladjenje_pin,GPIO.OUT)
GPIO.setup(alarm_pin,GPIO.OUT)
GPIO.setup(grejanje_sonda_1_pin,GPIO.OUT)
GPIO.setup(grejanje_sonda_3_pin,GPIO.OUT)
GPIO.setup(vlaga_relej_pin,GPIO.OUT)

GPIO.output(5 ,1)
GPIO.output(6 ,1)
GPIO.output(13 ,1)
GPIO.output(16 ,1)
GPIO.output(20 ,1)
GPIO.output(21 ,1)
GPIO.output(26 ,1)
GPIO.output(19 ,1)
GPIO.output(24 ,1)
GPIO.output(15 ,1)
GPIO.output(18 ,1)
GPIO.output(23, 1)
"""
jesu_aktivirane_rucne_komande = 0
ventilacija1 = 1
ventilacija2 = 1
ventilacija3 = 1
tunel1 = 1
tunel2 = 1
tunel3 = 1
grejanje = 1
hladjenje = 1
male_klapne = 0
velike_klapne = 0 #1 ako ne radi, 0 ako radi
temperatura_1 = ''
temperatura_2 = ''
temperatura_3  = ''
vlaga_1 = ''
vlaga_2 = ''
vlaga_3 = ''
spoljasnja_temperatura = 0
avg_temperatura = 0
avg_vlaga = 0
zeljena_temperatura = 0
zeljena_temperatura_rucno = 0
gornja_granica = 1.2
donja_granica = 0.6
gornja_granica_alarma = 5
donja_granica_alarma = 5
count = 0
broj_zivih = 0
umrli = 0
dan = 0
kubikaza = 0
semafor_regulacija = 0
semafor_servo = 0
jel_treba_da_resetuje_glavni_tred = 0
min_vent_1_global = 0
min_vent_2_global = 0
min_vent_2_global = 0
tunel_1_global = 0
tunel_2_global = 0
tunel_3_global = 0
radi_alarm = 0
granica_vlage_za_alarm = 85
jel_alarm_aktiviran = 0
logo_string = "Jomapeks Farm Solution"

class Button1_Form(QMainWindow): #Temperatura
	def __init__(self, parent = None):
		super(Button1_Form, self).__init__(parent)
		self.resize(800, 480)
		self.setStyleSheet('''
	background-color:  black;
''')

		self.temp_image = QPixmap('temp1.png')
		self.icon = QIcon(self.temp_image)
	
		self.ztemp_image = QPixmap('ztemp.jpeg')
		self.zicon = QIcon(self.ztemp_image)


		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet('''
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn1 = QPushButton("Senzor 1",self)
		self.btn1.setIcon(self.icon)
		self.btn1.setIconSize(QSize(70, 70))
		self.btn1.resize(260, 190)
		self.btn1.move(5,85)
		self.btn1.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn2 = QPushButton("Senzor 2", self)
		self.btn2.setIcon(self.icon)
		self.btn2.setIconSize(QSize(70, 70))
		self.btn2.resize(260, 190)
		self.btn2.move(5+265 ,85)
		self.btn2.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.btn3 = QPushButton("Senzor 3", self)
		self.btn3.setIcon(self.icon)
		self.btn3.setIconSize(QSize(70, 70))
		self.btn3.resize(260, 190)
		self.btn3.move(5+265 + 265,85)
		self.btn3.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.btn4 = QPushButton(self)
		self.btn4.resize(260, 190)
		self.btn4.move(5,85 + 195)
		self.btn4.setIcon(self.zicon)
		self.btn4.setIconSize(QSize(120, 120))
		self.btn4.clicked.connect(self.temperatura)
		self.btn4.setStyleSheet('''
		border: 5px solid  #009933;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.btn5 = QPushButton("Gornja granica: " + str(gornja_granica) + " C" + "\nDonja granica: " + str(donja_granica)  + " C" , self)
		self.btn5.resize(260, 190)
		self.btn5.move(5+265 ,85 + 195)
		self.btn5.clicked.connect(self.histereza)
		self.btn5.setStyleSheet('''
		border: 5px solid  #009933;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn7 = QPushButton("SRM Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Temperatura", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		border: 5px solid  #009933;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
''')

		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.btn9.resize(260, 70)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.vreme = QTimer()
		self.vreme.timeout.connect(self.refresh)
		self.vreme.start(1000)

		self.temp_zapis_tred = QTimer()
		self.temp_zapis_tred.timeout.connect(self.refresh_temp)
		self.temp_zapis_tred.start(7000)

		self.btn1.setText(temperatura_1 + " C")
		self.btn2.setText(temperatura_2 + "  C")
		self.btn3.setText(temperatura_3 + " C")
		self.btn4.setText(str(zeljena_temperatura) + " C")

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
		if(zeljena_temperatura_rucno == 1):
			self.btn4.setText(str(zeljena_temperatura) + " C")
		else:
			self.btn4.setText(str(33.0 - 0.29*dan) + " C")
		self.btn5.setText("Gornja granica: " + str(gornja_granica) + " C" + "\nDonja granica: " + str(donja_granica)  + " C")
	def refresh_temp(self):
		self.btn1.setText(temperatura_1 + " C")
		self.btn2.setText(temperatura_2 + " C")
		self.btn3.setText(temperatura_3 + " C")

	def back_click(self):
		self.close()

	def histereza(self):
		self.popup = Tastatura_Form("Histereza")
		self.popup.showFullScreen()

	def temperatura(self):
		self.popup = Tastatura_Form("Temperatura")
		self.popup.showFullScreen()

class Button6_Form(QMainWindow): #Info
	def __init__(self, parent = None):
		super(Button6_Form, self).__init__(parent)
		self.resize(800, 480)
		self.setStyleSheet('''
	background-color:  black;
''')

		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet('''
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.statistika = QPushButton("Statistika", self) #buton za nazad
		self.statistika.resize(260, 70 + 40)
		self.statistika.move(5+265 + 265, 405- 120)
		self.statistika.clicked.connect(self.statistika_click)
		self.statistika.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn1 = QPushButton("Dan tova\nBroj zivih", self)
		self.btn1.resize(260, 190)
		self.btn1.move(5,85)
		self.btn1.clicked.connect(self.btn1_click)
		self.btn1.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn2 = QPushButton("Broj uginuca\nProcenat uginuca", self)
		self.btn2.resize(260, 190)
		self.btn2.move(5+265 ,85)
		self.btn2.clicked.connect(self.btn2_click)
		self.btn2.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.btn3 = QPushButton("Rezimi rada \nventilacije", self)
		self.btn3.resize(260, 190)
		self.btn3.move(5+265 + 265,85)
		self.btn3.clicked.connect(self.rezimi_rada_info)
		self.btn3.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
''')

		self.silos_image = QPixmap('silos1.png')
		self.icon = QIcon(self.silos_image)
		self.btn4 = QPushButton("Silos\nVaga", self)
		self.btn4.setIcon(self.icon)
		self.btn4.setIconSize(QSize(130, 130))
		self.btn4.resize(260, 190)
		self.btn4.move(5,85 + 195)
		self.btn4.clicked.connect(self.btn4_click)
		self.btn4.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')


		self.btn5 = QPushButton("Alarm", self)
		self.btn5.resize(260, 190)
		self.btn5.move(5+265 ,85 + 195)
		self.btn5.clicked.connect(self.otvori_alarm)
		self.btn5.setStyleSheet('''
		border: 5px solid #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 35px;

''')
		self.btn7 = QPushButton("SRM Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Info", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 40px;
''')

		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.btn9.resize(260, 70)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.vreme = QTimer()
		self.vreme.timeout.connect(self.refresh)
		self.vreme.start(1000)

		try:
			self.procenat = float(umrli)/float(umrli + broj_zivih)*100.0
			self.procenat = round(self.procenat , 1)
		except:
			self.procenat = 0
		self.btn2.setText("Broj uginuca: " + str(umrli) + "\nProcenat: " + str(self.procenat) + " %")
		self.btn1.setText("Dan tova: " + str(dan) + "\nBroj pilica: " + str(broj_zivih))

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
		try:
			self.procenat = float(umrli)/float(umrli + broj_zivih)*100.0
			self.procenat = round(self.procenat , 1)
		except:
			self.procenat = 0
		otvori = open("dan.txt", "r")
		self.dan_temp = int(otvori.read())
		otvori.close()
		global dan
		dan = self.dan_temp
		self.btn2.setText("Broj uginuca: " + str(umrli) + "\nProcenat: " + str(self.procenat) + " %")
		self.btn1.setText("Dan tova: " + str(dan) + "\nBroj pilica: " + str(broj_zivih))

	def back_click(self):
		self.close()

	def rezimi_rada_info(self):
		self.popup = Rezimi_rada_Ventilacije_Form()
		self.popup.showFullScreen()

	def btn1_click(self):
		self.popup = Tastatura_Form("Zivi")
		self.popup.showFullScreen()

	def btn2_click(self):
		self.popup = Tastatura_Form("Mrtvi")
		self.popup.showFullScreen()

	def btn4_click(self):
		self.popup = Silos_Form()
		self.popup.showFullScreen()

	def otvori_alarm(self):
		self.popup =  Alarm_Form()
		self.popup.showFullScreen()

	def statistika_click(self):
		self.popup = Statistika_Form()
		self.popup.showFullScreen()

class Button4_Form(QMainWindow): #Vlaga
	def __init__(self, parent = None):
		super(Button4_Form, self).__init__(parent)
		self.resize(800, 480)
		self.setStyleSheet('''
	background-color:  black;
''')

		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet('''
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.vlaga_image = QPixmap('hum.png')
		self.icon = QIcon(self.vlaga_image)

		
		self.btn1 = QPushButton("Senzor 1", self)
		self.btn1.setIcon(self.icon)
		self.btn1.setIconSize(QSize(70, 70))
		self.btn1.resize(260, 190)
		self.btn1.move(5,85)
		self.btn1.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn2 = QPushButton("Senzor 2", self)
		self.btn2.setIcon(self.icon)
		self.btn2.setIconSize(QSize(70, 70))
		self.btn2.resize(260, 190)
		self.btn2.move(5+265 ,85)
		self.btn2.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.btn3 = QPushButton("Senzor 3", self)
		self.btn3.setIcon(self.icon)
		self.btn3.setIconSize(QSize(70, 70))
		self.btn3.resize(260, 190)
		self.btn3.move(5+265 + 265,85)
		self.btn3.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')



		self.btn7 = QPushButton("SRM Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;

		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Vlaga", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.btn9.resize(260, 70)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.vreme = QTimer()
		self.vreme.timeout.connect(self.refresh)
		self.vreme.start(1000)

		self.vlaga_zapis_tred = QTimer()
		self.vlaga_zapis_tred.timeout.connect(self.refresh_vlaga)
		self.vlaga_zapis_tred.start(15000)

		self.btn1.setText(vlaga_1 + " %")
		self.btn2.setText(vlaga_2 + " %")
		self.btn3.setText(vlaga_3 + " %")

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

	def refresh_vlaga(self):
		self.btn1.setText(vlaga_1 + " %")
		self.btn2.setText(vlaga_2 + " %")
		self.btn3.setText(vlaga_3 + " %")

	def back_click(self):
		self.close()


class Button5_Form(QMainWindow): #Rucne komande
	def __init__(self, parent = None):
		super(Button5_Form, self).__init__(parent)

		global jesu_aktivirane_rucne_komande
		global ventilacija1
		global ventilacija2
		global ventilacija3
		global tunel1
		global tunel2
		global tunel3
		global grejanje
		global hladjenje
		global male_klapne
		global velike_klapne

		self.resize(800, 480)
		self.setStyleSheet('''
	background-color:  black;
''')

		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet('''
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn1 = QPushButton("Aktiviraj", self)
		if(jesu_aktivirane_rucne_komande == 1):
			self.btn1.setText("Rucno")
		else:
			self.btn1.setText("Automatski")

		self.btn1.resize(260, 190)
		self.btn1.move(5,85)
		self.btn1.clicked.connect(self.aktivirano)
		self.btn1.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn7 = QPushButton("SRM Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Rucne komande", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
''')

		self.relej1 = QPushButton("Rucne komande", self)
		self.relej1.resize(171, 70)
		self.relej1.move(5 + 265,5 + 75)
		self.relej1.clicked.connect(self.relej1_click)
		self.relej1.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 15px;
''')

		self.relej2 = QPushButton("Rucne komande", self)
		self.relej2.resize(171, 70)
		self.relej2.move(5 + 265 + 176,5 + 75)
		self.relej2.clicked.connect(self.relej2_click)
		self.relej2.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 15px;
''')

		self.relej3 = QPushButton("Rucne komande", self)
		self.relej3.resize(171, 70)
		self.relej3.move(5 + 265 + 176 + 176,5 + 75)
		self.relej3.clicked.connect(self.relej3_click)
		self.relej3.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 15px;
''')
		self.relej4 = QPushButton("Rucne komande", self)
		self.relej4.resize(171, 70)
		self.relej4.move(5 + 265,5 + 75 + 75)
		self.relej4.clicked.connect(self.relej4_click)
		self.relej4.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 15px;
''')

		self.relej5 = QPushButton("Rucne komande", self)
		self.relej5.resize(171, 70)
		self.relej5.move(5 + 265 + 176,5 + 75 + 75)
		self.relej5.clicked.connect(self.relej5_click)
		self.relej5.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 15px;
''')

		self.relej6 = QPushButton("Rucne komande", self)
		self.relej6.resize(171, 70)
		self.relej6.move(5 + 265 + 176 + 176,5 + 75 + 75)
		self.relej6.clicked.connect(self.relej6_click)
		self.relej6.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 15px;
''')

		self.relej7 = QPushButton("Rucne komande", self)
		self.relej7.resize(260, 70)
		self.relej7.move(5 + 265,5 + 75 + 75 + 75)
		self.relej7.clicked.connect(self.relej7_click)
		self.relej7.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
''')

		self.relej8 = QPushButton("Rucne komande",self)
		self.relej8.resize(260, 70)
		self.relej8.move(5 + 265 + 265,5 + 75 + 75 + 75)
		self.relej8.clicked.connect(self.relej8_click)
		self.relej8.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
''')

		self.slider1Label = QLabel("Male klapne", self)
		self.slider1Label.resize(260, 30)
		self.slider1Label.move(280 + 30 + 30 + 50, 330)
		self.slider1Label.setStyleSheet('''
		color: white;
		font-size: 25px;
''')

		self.slider1Vrednost = QLabel("0%", self)
		self.slider1Vrednost.resize(260, 30)
		self.slider1Vrednost.move(55, 330)
		self.slider1Vrednost.setStyleSheet('''
		color: white;
		font-size: 25px;
''')


		self.slider1 = QSlider(Qt.Horizontal, self)
		self.slider1.resize(260, 30)
		self.slider1.move(5 + 30 + 30 + 50, 330)
		self.slider1.setValue(male_klapne)
		self.slider1Vrednost.setText(str(self.slider1.value()) + '%')
		self.slider1.valueChanged.connect(self.slajder1)

		self.slider2Label = QLabel("Velike klapne", self)
		self.slider2Label.resize(150, 30)
		self.slider2Label.move(280 + 30 + 30 + 50, 330 + 50)
		self.slider2Label.setStyleSheet('''
		color: white;
		font-size: 25px;
''')

		self.slider2Vrednost = QLabel("0%", self)
		self.slider2Vrednost.resize(260, 30)
		self.slider2Vrednost.move(55, 330 + 50)
		self.slider2Vrednost.setStyleSheet('''
		color: white;
		font-size: 25px;
''')


		self.slider2 = QSlider(Qt.Horizontal, self)
		self.slider2.resize(260, 30)
		self.slider2.move(5 + 30 + 30 + 50, 330 + 50)
		self.slider2.setValue(velike_klapne)
		self.slider2Vrednost.setText(str(self.slider2.value()) + '%')
		self.slider2.valueChanged.connect(self.slajder2)


		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.btn9.resize(260, 70)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		if(ventilacija1 == 1):
			self.relej1.setText("Min. Vent. 1: OFF")
		else:
			self.relej1.setText("Min. Vent. 1:  ON")
		if(ventilacija2 == 1):
			self.relej2.setText("Min. Vent. 2:  OFF")
		else:
			self.relej2.setText("Min. Vent. 2: ON")
		if(ventilacija3 == 1):
			self.relej3.setText("Min. Vent. 3: OFF")
		else:
			self.relej3.setText("Min. Vent. 3: ON")
		if(tunel1 == 1):
			self.relej4.setText("Tunel 1: OFF")
		else:
			self.relej4.setText("Tunel 1:  ON")
		if(tunel2 == 1):
			self.relej5.setText("Tunel 2:  OFF")
		else:
			self.relej5.setText("Tunel 2: ON")
		if(tunel3 == 1):
			self.relej6.setText("Tunel 3: OFF")
		else:
			self.relej6.setText("Tunel 3: ON")
		if(grejanje == 1):
			self.relej7.setText("Grejanje: OFF")
		else:
			self.relej7.setText("Grejanje: ON")
		if(hladjenje == 1):
			self.relej8.setText("Hladjenje: OFF")
		else:
			self.relej8.setText("Hladjenje: ON")

		self.vreme = QTimer()
		self.vreme.timeout.connect(self.refresh)
		self.vreme.start(1000)
		
		self.vreme_komande = QTimer()
		self.vreme_komande.timeout.connect(self.refresh_komande)
		self.vreme_komande.start(1)

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

	def refresh_komande(self):

		global jesu_aktivirane_rucne_komande
		global ventilacija1
		global ventilacija2
		global ventilacija3
		global tunel1
		global tunel2
		global tunel3
		global grejanje
		global hladjenje
		global male_klapne
		global velike_klapne

		if(jesu_aktivirane_rucne_komande == 1):
			GPIO.output(ventilacija1_pin, ventilacija1)
			GPIO.output(ventilacija2_pin, ventilacija2)
			GPIO.output(ventilacija3_pin, ventilacija3)
			GPIO.output(tunel1_pin, tunel1)
			GPIO.output(tunel2_pin, tunel2)
			GPIO.output(tunel3_pin, tunel3)
			GPIO.output(grejanje_pin, grejanje)
			GPIO.output(hladjenje_pin, hladjenje)
			self.slider2.setValue(velike_klapne)
			self.slider1.setValue(male_klapne)

		if(ventilacija1 == 1):
			self.relej1.setText("Min. Vent. 1: OFF")
		else:
			self.relej1.setText("Min. Vent. 1:  ON")
		if(ventilacija2 == 1):
			self.relej2.setText("Min. Vent. 2:  OFF")
		else:
			self.relej2.setText("Min. Vent. 2: ON")
		if(ventilacija3 == 1):
			self.relej3.setText("Min. Vent. 3: OFF")
		else:
			self.relej3.setText("Min. Vent. 3: ON")
		if(tunel1 == 1):
			self.relej4.setText("Tunel 1: OFF")
		else:
			self.relej4.setText("Tunel 1:  ON")
		if(tunel2 == 1):
			self.relej5.setText("Tunel 2:  OFF")
		else:
			self.relej5.setText("Tunel 2: ON")
		if(tunel3 == 1):
			self.relej6.setText("Tunel 3: OFF")
		else:
			self.relej6.setText("Tunel 3: ON")
		if(grejanje == 1):
			self.relej7.setText("Grejanje: OFF")
		else:
			self.relej7.setText("Grejanje: ON")
		if(hladjenje == 1):
			self.relej8.setText("Hladjenje: OFF")
		else:
			self.relej8.setText("Hladjenje: ON")

	def back_click(self):
		self.close()

	def aktivirano(self):
		global jesu_aktivirane_rucne_komande
		if(jesu_aktivirane_rucne_komande == 0):
			self.btn1.setText("Rucno")
			jesu_aktivirane_rucne_komande = 1
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Upaljenje rucne komande\n")
			detekcija.close()
		else:
			jesu_aktivirane_rucne_komande = 0
			global jel_treba_da_resetuje_glavni_tred
			jel_treba_da_resetuje_glavni_tred = 1
			global semafor_regulacija
			global semafor_servo
			semafor_regulacija = 0
			semafor_servo = 0
			self.btn1.setText("Automatski")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Upaljene automatske komande\n")
			detekcija.close()

	def relej1_click(self):
		global ventilacija1
		if(ventilacija1 == 1):
			ventilacija1 = 0
			self.relej1.setText("Min. Vent. 1: ON")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno upaljen relej 1\n")
			detekcija.close()
		else:
			ventilacija1 = 1
			self.relej1.setText("Min. Vent. 1:  OFF")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno ugasen relej 1\n")
			detekcija.close()

	def relej2_click(self):
		global ventilacija2
		if(ventilacija2 == 1):
			ventilacija2 = 0
			self.relej2.setText("Min. Vent. 2: ON")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno upaljen relej 2\n")
			detekcija.close()
		else:
			ventilacija2 = 1
			self.relej2.setText("Min. Vent. 2:  OFF")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno ugasen relej 2\n")
			detekcija.close()

	def relej3_click(self):
		global ventilacija3
		if(ventilacija3 == 1):
			ventilacija3 = 0
			self.relej3.setText("Min. Vent. 3: ON")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno upaljen relej 3\n")
			detekcija.close()
		else:
			ventilacija3 = 1
			self.relej3.setText("Min. Vent. 3:  OFF")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno ugasen relej 3\n")
			detekcija.close()

	def relej4_click(self):
		global tunel1
		if(tunel1 == 1):
			tunel1 = 0
			self.relej4.setText("Tunel 1: ON")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno upaljen relej 4\n")
			detekcija.close()
		else:
			tunel1 = 1
			self.relej4.setText("Tunel 1:  OFF")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno ugasen relej 4\n")
			detekcija.close()
	def relej5_click(self):
		global tunel2
		if(tunel2 == 1):
			tunel2 = 0
			self.relej5.setText("Tunel 2: ON")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno upaljen relej 5\n")
			detekcija.close()
		else:
			tunel2 = 1
			self.relej5.setText("Tunel 2:  OFF")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno ugasen relej 5\n")
			detekcija.close()

	def relej6_click(self):
		global tunel3
		if(tunel3 == 1):
			tunel3 = 0
			self.relej6.setText("Tunel 3: ON")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno upaljen relej 6\n")
			detekcija.close()
		else:
			tunel3 = 1
			self.relej6.setText("Tunel 3:  OFF")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno ugasen relej 6\n")
			detekcija.close()

	def relej7_click(self):
		global grejanje
		if(grejanje == 1):
			grejanje = 0
			self.relej7.setText("Grejanje: ON")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno upaljeno GREJANJE\n")
			detekcija.close()
		else:
			grejanje = 1
			self.relej7.setText("Grejanje:  OFF")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno ugaseno GREJANJE\n")
			detekcija.close()

	def relej8_click(self):
		global hladjenje
		if(hladjenje == 1):
			hladjenje = 0
			self.relej8.setText("Hladjenje: ON")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno upaljeno HLADJENJE\n")
			detekcija.close()
		else:
			hladjenje = 1
			self.relej8.setText("Hladjenje:  OFF")
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Rucno upaljeno HLADJENJE\n")
			detekcija.close()

	def crkli(self):
		self.popup = Tastatura_Form("Uginuca")
		self.popup.showFullScreen()

	def kubikaza(self):
		self.popup = Tastatura_Form("Kubikaza")
		self.popup.showFullScreen()

	def slajder1(self):
		global male_klapne
		self.slider1Vrednost.setText(str(self.slider1.value()) + '%')
		f.procenat_servo(int(self.slider1.value()), 1)
		male_klapne = self.slider1.value()

	def slajder2(self):
		global velike_klapne
		self.slider2Vrednost.setText(str(self.slider2.value()) + '%')
		f.procenat_servo(int(self.slider2.value()), 2)
		velike_klapne = self.slider2.value()

class Rezimi_rada_Ventilacije_Form(QMainWindow): #Rezimi Rada Ventilacije u info sekciji
	def __init__(self, parent = None):
		super(Rezimi_rada_Ventilacije_Form, self).__init__(parent)
		self.resize(800, 480)
		self.setStyleSheet('''
	background-color:  black;
''')

		self.label = QLabel("\nRezim 1: Minimum ventilacije na vreme\nRezim 2: Minimum ventilacije relej 1\nRezim 3:  Minimum ventilacije relej 2 i 3\nRezim 4: Minimum ventilacije relej 1, 2 i 3\nRezim 5: Tunel 1 i relej 3\nRezim 6: Tunel 1 i 2\nRezim 7: tunel 1, 2 i 3\n", self)
		self.label.move(20, 80)
		self.label.resize(500, 250)
		self.label.setStyleSheet('''
		color: white;
		font-size: 25px;
''')
		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet('''
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn7 = QPushButton("SRM Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Rezim ventilacije", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
''')

		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.btn9.resize(260, 70)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.vreme = QTimer()
		self.vreme.timeout.connect(self.refresh)
		self.vreme.start(1000)

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

	def back_click(self):
		self.close()

class Tastatura_Form(QMainWindow): #TASTATURA
	def __init__(self, naslov, parent = None):
		super(Tastatura_Form, self).__init__(parent)
		self.resize(800, 480)
		self.setStyleSheet('''
	background-color:  black;
''')
		global potvrdi_cmd
		potvrdi_cmd = naslov
		self.y = 85
		self.x = 5 + 265 + 265

		self.btn1 = QPushButton("1", self)
		self.btn1.move(self.x, self.y)
		self.btn1.resize(81, 70)
		self.btn1.clicked.connect(self.btn1_click)
		self.btn1.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")
		self.btn2 = QPushButton("2", self)
		self.btn2.move(self.x + 86, self.y)
		self.btn2.resize(81, 70)
		self.btn2.clicked.connect(self.btn2_click)
		self.btn2.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")

		self.btn3 = QPushButton("3", self)
		self.btn3.move(self.x + 86 + 86, self.y)
		self.btn3.resize(81, 70)
		self.btn3.clicked.connect(self.btn3_click)
		self.btn3.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")
		self.btn4 = QPushButton("4", self)
		self.btn4.move(self.x, self.y + 75)
		self.btn4.resize(81, 70)
		self.btn4.clicked.connect(self.btn4_click)
		self.btn4.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")

		self.btn5 = QPushButton("5", self)
		self.btn5.clicked.connect(self.btn5_click)
		self.btn5.move(self.x + 86, self.y + 75)
		self.btn5.resize(81, 70)
		self.btn5.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")

		self.btn6 = QPushButton("6", self)
		self.btn6.move(self.x + 86 + 86, self.y + 75)
		self.btn6.resize(81, 70)
		self.btn6.clicked.connect(self.btn6_click)
		self.btn6.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")

		self.btn7 = QPushButton("7", self)
		self.btn7.move(self.x, self.y + 75 + 75)
		self.btn7.resize(81, 70)
		self.btn7.clicked.connect(self.btn7_click)
		self.btn7.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")

		self.btn8 = QPushButton("8", self)
		self.btn8.move(self.x + 86, self.y + 75 + 75)
		self.btn8.resize(81, 70)
		self.btn8.clicked.connect(self.btn8_click)
		self.btn8.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")

		self.btn9 = QPushButton("9", self)
		self.btn9.move(self.x + 86 + 86, self.y + 75 + 75)
		self.btn9.resize(81, 70)
		self.btn9.clicked.connect(self.btn9_click)
		self.btn9.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")

		self.btn0 = QPushButton("0", self)
		self.btn0.move(self.x, self.y + 75 + 75 + 75)
		self.btn0.resize(167, 70 )
		self.btn0.clicked.connect(self.btn0_click)
		self.btn0.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")

		self.btnzarez = QPushButton(".", self)
		self.btnzarez.move(self.x + 86 + 86, self.y + 75 + 75 + 75)
		self.btnzarez.resize(81, 70)
		self.btnzarez.clicked.connect(self.btnzarez_click)
		self.btnzarez.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
""")
		self.setStyleSheet('''
			background-color: black;
''')
		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet("""
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.obrisi = QPushButton("Obrisi", self) #buton za nazad
		self.obrisi.resize(260, 70)
		self.obrisi.move(5+265, 405)
		self.obrisi.clicked.connect(self.obrisi_click)
		self.obrisi.setStyleSheet("""
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.potvrdi = QPushButton("Potvrdi", self) #buton za nazad
		self.potvrdi.resize(260, 70)
		self.potvrdi.move(5, 405)
		self.potvrdi.clicked.connect(self.potvrdi_click)
		self.potvrdi.setStyleSheet("""
		border: 5px solid  #2a52a2;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")
		self.jomapex = QPushButton("SRM Farm Solution", self)
		self.jomapex.setText(logo_string)
		self.jomapex.resize(260, 70)
		self.jomapex.move(5,5)
		self.jomapex.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.naslov = QPushButton("Unesite dan", self)
		self.naslov.resize(260, 70)
		self.naslov.move(5 + 265,5)
		self.naslov.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		if(naslov == 'Temperatura'):
			self.naslov.setText("Zeljena temperatura")

			self.vrati = QPushButton("Podrazumevano", self)
			self.vrati.resize(260, 70)
			self.vrati.clicked.connect(self.vrati_temperaturu)
			self.vrati.move(5 , 85)
			self.vrati.setStyleSheet('''
			border: 5px solid  white;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;

''')

		self.unos = QPushButton("0", self)
		self.unos.resize(260, 70)
		self.unos.move(5 + 265, 85)
		self.unos.setStyleSheet('''
		border: 5px solid  white;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		if(naslov == 'Histereza'):
			self.naslov.setText("Granice temperature")
			
			self.gornja = QRadioButton("Gornja granica", self) #buton za nazad
			self.gornja.resize(260, 70)
			self.gornja.move(5, self.y)
			self.gornja.setChecked(True)
			self.gornja.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")

			self.donja = QRadioButton("Donja granica", self) #buton za nazad
			self.donja.resize(260, 70)
			self.donja.clicked.connect(self.radio1)
			self.donja.move(5, self.y + 75)
			self.donja.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")

			self.vrati = QPushButton("Podrazumevano", self)
			self.vrati.resize(260, 70)
			self.vrati.clicked.connect(self.vrati_granice)
			self.vrati.move(5, 85 + 75 + 75)
			self.vrati.setStyleSheet('''
			border: 5px solid  white;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;

	''')
		if(naslov == 'Zivi'):
			self.naslov.setText("Tov")
			
			self.gornja = QRadioButton("Dan zivota", self) #buton za nazad
			self.gornja.resize(260, 70)
			self.gornja.clicked.connect(self.radio2)
			self.gornja.move(5, self.y)
			self.gornja.setChecked(True)
			self.gornja.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")
			self.donja = QRadioButton("Broj zivih", self) #buton za nazad
			self.donja.resize(260, 70)
			self.donja.clicked.connect(self.radio1)
			self.donja.move(5, self.y + 75)
			self.donja.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")
		if(naslov == 'Mrtvi'):

			self.naslov.setText("Broj uginuca")
			self.unos = QPushButton("0", self)
			self.unos.resize(260, 70)
			self.unos.move(5 + 265, 85)
			self.unos.setStyleSheet('''
			border: 5px solid  white;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;

	''')
		if(naslov == 'Kubikaza'):
			self.naslov.setText("Kubikaza")
			self.m1 = QRadioButton("Min. Vent 1", self) #buton za nazad
			self.m1.resize(260, 70)
			self.m1.clicked.connect(self.min_vent_1)
			self.m1.move(5 , self.y + 75)
			self.m1.setChecked(True)
			self.m1.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")
			self.m2 = QRadioButton("Min. Vent 2", self) #buton za nazad
			self.m2.resize(260, 70)
			self.m2.clicked.connect(self.min_vent_2)
			self.m2.move(5, self.y + 75 + 75)
			self.m2.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")

			self.m3 = QRadioButton("Min. Vent 3", self) #buton za nazad
			self.m3.resize(260, 70)
			self.m3.clicked.connect(self.min_vent_3)
			self.m3.move(5, self.y + 75 + 75 + 75)
			self.m3.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")

			self.t1 = QRadioButton("Tunel 1", self) #buton za nazad
			self.t1.resize(260, 70)
			self.t1.clicked.connect(self.tunel_1)
			self.t1.move(5 + 265, self.y + 75)
			self.t1.setChecked(True)
			self.t1.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")
			self.t2 = QRadioButton("Tunel 2", self) #buton za nazad
			self.t2.resize(260, 70)
			self.t2.clicked.connect(self.tunel_2)
			self.t2.move(5 + 265, self.y + 75 + 75)
			self.t2.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")

			self.t3 = QRadioButton("Tunel 3", self) #buton za nazad
			self.t3.resize(260, 70)
			self.t3.clicked.connect(self.tunel_3)
			self.t3.move(5 + 265, self.y + 75 + 75 + 75)
			self.t3.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")
		if(naslov == "Alarm"):
			self.naslov.setText("Alarm")
			self.gornja_granica_temperature_alarm = QRadioButton("Gornja granica temp", self) #buton za nazad
			self.gornja_granica_temperature_alarm.resize(260, 70)
			self.gornja_granica_temperature_alarm.clicked.connect(self.gornja_granica_temperature_alarm_click)
			self.gornja_granica_temperature_alarm.move(5 , self.y)
			self.gornja_granica_temperature_alarm.setChecked(True)
			self.gornja_granica_temperature_alarm.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")
			self.donja_granica_temperature_alarm = QRadioButton("Dornja granica temp", self) #buton za nazad
			self.donja_granica_temperature_alarm.resize(260, 70)
			self.donja_granica_temperature_alarm.clicked.connect(self.donja_granica_temperature_alarm_click)
			self.donja_granica_temperature_alarm.move(5, self.y + 75)
			self.donja_granica_temperature_alarm.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")

			self.granica_vlage_alarm = QRadioButton("Gornja granica vlage", self) #buton za nazad
			self.granica_vlage_alarm.resize(260, 70)
			self.granica_vlage_alarm.clicked.connect(self.gornja_granica_vlage_alarm_click)
			self.granica_vlage_alarm.move(5, self.y + 75 + 75)
			self.granica_vlage_alarm.setStyleSheet("""
			border: 5px solid  #009933;
			border-radius: 25px;
			background-color:  black;
			color:  white;
			font-size: 25px;
	""")

		self.datum = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.datum.resize(260, 70)
		self.datum.move(5 + 265 + 265,5)
		self.datum.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.vreme = QTimer()
		self.vreme.timeout.connect(self.refresh)
		self.vreme.start(1000)

		self.type = ''


	def refresh(self):
		self.datum.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

	def back_click(self):
		self.close()

	def btn1_click(self):
		self.type = self.type + '1'
		self.unos.setText(self.type)

	def btn2_click(self):
		self.type = self.type + '2'
		self.unos.setText(self.type)

	def btn3_click(self):
		self.type = self.type + '3'
		self.unos.setText(self.type)

	def btn4_click(self):
		self.type = self.type + '4'
		self.unos.setText(self.type)

	def btn5_click(self):
		self.type = self.type + '5'
		self.unos.setText(self.type)

	def btn6_click(self):
		self.type = self.type + '6'
		self.unos.setText(self.type)

	def btn7_click(self):
		self.type = self.type + '7'
		self.unos.setText(self.type)

	def btn8_click(self):
		self.type = self.type + '8'
		self.unos.setText(self.type)

	def btn9_click(self):
		self.type = self.type + '9'
		self.unos.setText(self.type)

	def btnzarez_click(self):
		self.type = self.type + '.'
		self.unos.setText(self.type)

	def btn0_click(self):
		self.type = self.type + '0'
		self.unos.setText(self.type)

	def obrisi_click(self):
		self.type = ''
		self.unos.setText(self.type)

	def potvrdi_click(self):

		global jel_treba_da_resetuje_glavni_tred
		global semafor_regulacija
		global semafor_servo
		jel_treba_da_resetuje_glavni_tred = 1
		semafor_regulacija = 0
		semafor_servo = 0
		if(potvrdi_cmd == "Mrtvi"):
			fajl = open("uginuli.txt", "r")
			self.crkli = int(fajl.read())
			print self.crkli
			fajl.close()
			fajl = open("uginuli.txt", "w")
			if(self.unos.text() == ''):
				self.unos.setText("0")
			self.crkli = self.crkli + int(self.unos.text())
			fajl.write(str(self.crkli))
			fajl.close()
			detekcija = open("detekcija.txt", "a")
			detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Uneto "+ str(self.unos.text()) + " mrtvih pilica \n")
			detekcija.close()
		if(potvrdi_cmd == "Zivi"):

			if(self.gornja.isChecked()):
				fajl = open("dan.txt", "w")
				self.string = self.unos.text()
				if(self.string == ''):
					self.string = '0'
				fajl.write(self.string)
				fajl.close()
				jel_treba_da_resetuje_glavni_tred = 1
				semafor_regulacija = 0
				semafor_servo = 0
				detekcija = open("detekcija.txt", "a")
				detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Podeseno na "+ str(self.unos.text()) + ". dan \n")
				detekcija.close()

			if(self.donja.isChecked()):
				fajl = open("broj.txt", "w")
				self.string = self.unos.text()
				if(self.string == ''):
					self.string = '0'
				fajl.write(self.string)
				fajl.close()
				fajl = open("uginuli.txt", "w")
				fajl.write("0")
				fajl.close()
				detekcija = open("detekcija.txt", "a")
				detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Uneto "+ str(self.unos.text()) + " zivih pilica \n")
				detekcija.close()
				jel_treba_da_resetuje_glavni_tred = 1
				semafor_regulacija = 0
				semafor_servo = 0
			

		if(potvrdi_cmd == "Histereza"):
			if(self.gornja.isChecked()):
				try:
					global gornja_granica
	 				gornja_granica = float(self.unos.text())
					gornja_granica = round(gornja_granica ,1)
					detekcija = open("detekcija.txt", "a")
					detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Gornja granica podesena na "+ str(self.unos.text()) + "\n")
					detekcija.close()
				except:
					pass
			if(self.donja.isChecked()):
				try:
					global donja_granica
	 				donja_granica = float(self.unos.text())
					donja_granica = round(donja_granica ,1)
					detekcija = open("detekcija.txt", "a")
					detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Donja granica podesena na "+ str(self.unos.text()) + "\n")
					detekcija.close()
				except:
					pass
		if(potvrdi_cmd == "Temperatura"):
				try:
					global zeljena_temperatura
					global zeljena_temperatura_rucno
					zeljena_temperatura = float(self.unos.text())
					zeljena_temperatura = round(zeljena_temperatura ,1)
					zeljena_temperatura_rucno = 1
					jel_treba_da_resetuje_glavni_tred = 1
					semafor_regulacija = 0
					semafor_servo = 0
					detekcija = open("detekcija.txt", "a")
					detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Promenili su zeljenu temperaturu na "+ str(zeljena_temperatura) + "\n")
					detekcija.close()
				except:
					pass
		if(potvrdi_cmd == "Kubikaza"):
			if(self.m1.isChecked()):
				try:
					global min_vent_1_global
	 				min_vent_1_global = int(self.unos.text())
					openn = open("min_vent_1.txt", "w")
					openn.write(str(min_vent_1_global))
					openn.close()
					detekcija = open("detekcija.txt", "a")
					detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Promenje min. vent. 1 na "+ str(self.unos.text()) + "\n")
					detekcija.close()
				except:
					pass
			if(self.m2.isChecked()):
				try:
					global min_vent_2_global
	 				min_vent_2_global = int(self.unos.text())
					openn = open("min_vent_2.txt", "w")
					openn.write(str(min_vent_2_global))
					openn.close()
					detekcija = open("detekcija.txt", "a")
					detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Promenje min. vent. 2 na "+ str(self.unos.text()) + "\n")
					detekcija.close()		
				except:
					pass
			if(self.m3.isChecked()):
				try:
					global min_vent_3_global
	 				min_vent_3_global = int(self.unos.text())
					openn = open("min_vent_3.txt", "w")
					openn.write(str(min_vent_3_global))
					openn.close()
					detekcija = open("detekcija.txt", "a")
					detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Promenje min. vent. 3 na "+ str(self.unos.text()) + "\n")
					detekcija.close()
				except:
					pass
			if(self.t1.isChecked()):
				try:
					global tunel_1_global
	 				tunel_1_global = int(self.unos.text())
					openn = open("tunel_1.txt", "w")
					openn.write(str(tunel_1_global))
					openn.close()
					detekcija = open("detekcija.txt", "a")
					detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Promenje tunel 1 na "+ str(self.unos.text()) + "\n")
					detekcija.close()
				except:
					pass
			if(self.t2.isChecked()):
				try:
					global tunel_2_global
	 				tunel_2_global = int(self.unos.text())
					openn = open("tunel_2.txt", "w")
					openn.write(str(tunel_2_global))
					openn.close()
					detekcija = open("detekcija.txt", "a")
					detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Promenje tunel 2 na "+ str(self.unos.text()) + "\n")
					detekcija.close()
				except:
					pass
			if(self.t3.isChecked()):
				try:
					global tunel_3_global
	 				tunel_3_global = int(self.unos.text())
					openn = open("tunel_3.txt", "w")
					openn.write(str(tunel_3_global))
					openn.close()
					detekcija = open("detekcija.txt", "a")
					detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Promenje 3 na "+ str(self.unos.text()) + "\n")
					detekcija.close()
				except:
					pass
		if(potvrdi_cmd == "Alarm"):
			if(self.gornja_granica_temperature_alarm.isChecked()):
				try:
					global gornja_granica_alarma
					gornja_granica_alarma = int(self.unos.text())
				except:
					pass
			if(self.donja_granica_temperature_alarm.isChecked()):
				try:
					global donja_granica_alarma
					donja_granica_alarma = int(self.unos.text())
				except:
					pass
			if(self.granica_vlage_alarm.isChecked()):
				try:
					global granica_vlage_za_alarm
					granica_vlage_za_alarm = int(self.unos.text())
				except:
					pass

		self.type = ''
		self.unos.setText(self.type)

	def radio1(self):
		pass

	def radio2(self):
		pass

	def min_vent_1(self):
		self.naslov.setText("Min. Vent 1")

	def min_vent_2(self):
		self.naslov.setText("Min. Vent 2")

	def min_vent_3(self):
		self.naslov.setText("Min. Vent 3")

	def tunel_1(self):
		self.naslov.setText("Tunel 1")

	def tunel_2(self):
		self.naslov.setText("Tunel 2")

	def tunel_3(self):
		self.naslov.setText("Tunel 3")

	def gornja_granica_temperature_alarm_click(self):
		self.naslov.setText("Gornja granica temp")

	def donja_granica_temperature_alarm_click(self):
		self.naslov.setText("Donja granica")

	def gornja_granica_vlage_alarm_click(self):
		self.naslov.setText("Gornja granica vlaga")

	def vrati_temperaturu(self):
		global zeljena_temperatura
		global zeljena_temperatura_rucno
		zeljena_temperatura = 33.0 - 0.29*dan
		zeljena_temperatura_rucno = 0
		global jel_treba_da_resetuje_glavni_tred
		jel_treba_da_resetuje_glavni_tred = 1
		global semafor_regulacija
		semafor_regulacija = 0
		global semafor_servo
		semafor_servo = 0
		detekcija = open("detekcija.txt", "a")
		detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ ": Temperatura vracena na podrazumevano.\n")
		detekcija.close()
		self.close()

	def vrati_granice(self):
		global gornja_granica
		global donja_granica
		detekcija = open("detekcija.txt", "a")
		detekcija.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+": Granice vracene na podrazumevano.\n")
		detekcija.close()
		gornja_granica = 1.2
		donja_granica = 0.6
		self.close()

class Silos_Form(QMainWindow):
	def __init__(self, parent = None):
		super(Silos_Form, self).__init__(parent)
		self.resize(800, 480)
		#self.setCursor(QCursor(Qt.BlankCursor)) #da nema strelicu
		self.setStyleSheet('''
		background-color:  black;
''')
		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet("""
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")
		self.btn1 = QPushButton("Silos", self)
		self.btn1.resize(260, 190)
		self.btn1.move(5,85)
		self.btn1.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
''')

		self.btn2 = QPushButton("Vaga",self)
		self.btn2.resize(260, 190)
		self.btn2.move(5+265 ,85)
		self.btn2.clicked.connect(self.otvori_vagu)
		self.btn2.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
''')

		self.btn7 = QPushButton("SRM Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Silos i vaga", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
''')
		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.btn9.resize(260, 70)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.vreme = QTimer()
		self.vreme.timeout.connect(self.refresh)
		self.vreme.start(1000)

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

	def back_click(self):
		self.close()

	def otvori_vagu(self):
		self.popup = vaga.Vaga_Form(dan)
		self.popup.showFullScreen()


class Ventilacija_Form(QMainWindow): #VENTILACIJA
	def __init__(self, parent = None):
		super(Ventilacija_Form, self).__init__(parent)
		self.resize(800, 480)
		#self.setCursor(QCursor(Qt.BlankCursor)) #da nema strelicu
		self.setStyleSheet('''
		background-color:  black;
''')		
	

		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet("""
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")
		self.m1 = QPushButton("M1", self) #buton za nazad
		self.m1.resize(260, 70)
		self.m1.move(5, 5 + 75)
		self.m1.setStyleSheet("""
		border: 5px solid  #2a52a2;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.m2 = QPushButton("M2", self) #buton za nazad
		self.m2.resize(260, 70)
		self.m2.move(5, 5 + 75 + 75)
		self.m2.setStyleSheet("""
		border: 5px solid  #2a52a2;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.m3 = QPushButton("M3", self) #buton za nazad
		self.m3.resize(260, 70)
		self.m3.move(5, 5 + 75 + 75 + 75)
		self.m3.setStyleSheet("""
		border: 5px solid  #2a52a2;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.t1 = QPushButton("T1", self) #buton za nazad
		self.t1.resize(260, 70)
		self.t1.move(5 + 265, 5 + 75)
		self.t1.setStyleSheet("""
		border: 5px solid  #2a52a2;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.t2 = QPushButton("T2", self) #buton za nazad
		self.t2.resize(260, 70)
		self.t2.move(5 + 265, 5 + 75 + 75)
		self.t2.setStyleSheet("""
		border: 5px solid  #2a52a2;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.t3 = QPushButton("T3", self) #buton za nazad
		self.t3.resize(260, 70)
		self.t3.move(5 + 265, 5 + 75 + 75 + 75)
		self.t3.setStyleSheet("""
		border: 5px solid  #2a52a2;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.podesi = QPushButton("Podesi", self) #buton za nazad
		self.podesi.resize(260, 70)
		self.podesi.move(5 + 265 + 265, 5 + 75)
		self.podesi.clicked.connect(self.podesi_click)
		self.podesi.setStyleSheet("""
		border: 5px solid  #2a52a2;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.btn7 = QPushButton("SRM Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Ventilacija", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		border: 5px solid  #2a52a2;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
, self)
		self.btn9.resize(260, 70)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.vreme = QTimer()
		self.vreme.timeout.connect(self.refresh)
		self.vreme.start(1000)

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

		try:
			openn = open("min_vent_1.txt", "r")
			self.m1.setText("Min. Vent. 1: " + openn.read())
			openn.close()
		except:
			pass
		try:
			openn = open("min_vent_2.txt", "r")
			self.m2.setText("Min. Vent. 2: " + openn.read())
			openn.close()
		except:
			pass
		try:
			openn = open("min_vent_3.txt", "r")
			self.m3.setText("Min. Vent. 3: " + openn.read())
			openn.close()
		except:
			pass
		try:
			openn = open("tunel_1.txt", "r")
			self.t1.setText("Tunel 1: " + openn.read())
			openn.close()
		except:
			pass
		try:
			openn = open("tunel_2.txt", "r")
			self.t2.setText("Tunel 2: " + openn.read())
			openn.close()
		except:
			pass
		try:
			openn = open("tunel_3.txt", "r")
			self.t3.setText("Tunel 3: " + openn.read())
			openn.close()
		except:
			pass
		

	def podesi_click(self):
		self.popup = Tastatura_Form("Kubikaza")
		self.popup.showFullScreen()

	def back_click(self):
		self.close()

class Uzbuna_Form(QMainWindow): #VENTILACIJA
	def __init__(self, parent = None):
		super(Uzbuna_Form, self).__init__(parent)
		self.resize(800, 480)
		#self.setCursor(QCursor(Qt.BlankCursor)) #da nema strelicu
		self.setStyleSheet('''
		background-color:  black;
''')

		self.btn1 = QPushButton("ALARM", self)
		self.btn1.resize(800, 480)
		self.btn1.move(0 ,0)
		self.btn1.clicked.connect(self.destroy)
		self.btn1.setStyleSheet('''
		background-color:  black;
		color:  red;
		font-size: 150px;
		font-style: bold;
''')
		global semafor_za_igranje
		semafor_za_igranje = 0
		self.timer = QTimer()
		self.timer.timeout.connect(self.igraj)
		self.timer.start(250)

		GPIO.output(alarm_pin, 0)

	def destroy(self):
		global radi_alarm
		radi_alarm = 0
		self.timer.stop()
		GPIO.output(alarm_pin, 1)
		self.close()
	
	def igraj(self):
		global semafor_za_igranje
		if(semafor_za_igranje == 0):
			self.btn1.setStyleSheet('''
		background-color:  red;
		color:  black;
		font-size: 150px;
		font-style: bold;
''')
			semafor_za_igranje = 1
		else:
			self.btn1.setStyleSheet('''
		background-color:  black;
		color:  red;
		font-size: 150px;
		font-style: bold;
''')
			semafor_za_igranje = 0		

class Alarm_Form(QMainWindow):
	def __init__(self, parent = None):
		super(Alarm_Form, self).__init__(parent)
		self.resize(800, 480)
		#self.setCursor(QCursor(Qt.BlankCursor)) #da nema strelicu
		self.setStyleSheet('''
		background-color:  black;
''')		

		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet("""
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.btn1 = QPushButton(self)
		self.btn1.resize(260, 190)
		self.btn1.move(5,85)
		self.btn1.clicked.connect(self.btn1_click)
		self.btn1.setStyleSheet('''
		border: 5px solid #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn2 = QPushButton("Gornja: " + str(gornja_granica_alarma) + "\nDonja: " + str(donja_granica_alarma) + "\nVlaga: " + str(granica_vlage_za_alarm) , self)
		self.btn2.resize(260, 190)
		self.btn2.move(5+265 ,85)
		self.btn2.clicked.connect(self.btn2_click)
		self.btn2.setStyleSheet('''
		border: 5px solid #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.btn3 = QPushButton("Listing", self)
		self.btn3.resize(260, 190)
		self.btn3.move(5+265 + 265,85)
		self.btn3.clicked.connect(self.btn3_click)
		self.btn3.setStyleSheet('''
		border: 5px solid #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn7 = QPushButton("SRM Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Alarm", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		border: 5px solid #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.btn9.resize(260, 70)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		if(jel_alarm_aktiviran == 0):
			self.btn1.setText("Aktiviran")
		else:
			self.btn1.setText("Nije aktiviran")

		self.timer = QTimer()
		self.timer.timeout.connect(self.refresh)
		self.timer.start(1000)

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
		self.btn2.setText("Gornja: " + str(gornja_granica_alarma) + "\nDonja: " + str(donja_granica_alarma) + "\nVlaga: " + str(granica_vlage_za_alarm))

	def btn1_click(self):
			global jel_alarm_aktiviran
			if(jel_alarm_aktiviran == 0):
				jel_alarm_aktiviran = 1
				self.btn1.setText("Nije aktiviran")
			else:
				self.btn1.setText("Aktiviran")
				jel_alarm_aktiviran = 0

	def btn2_click(self):
		self.popup = Tastatura_Form("Alarm")
		self.popup.showFullScreen()

	def btn3_click(self):
		self.popup = Alarm_Listing_Form()
		self.popup.showFullScreen()

	def back_click(self):
		self.close()

class Statistika_Form(QMainWindow):
	def __init__(self, parent = None):
		super(Statistika_Form, self).__init__(parent)
		self.resize(800, 480)
		#self.setCursor(QCursor(Qt.BlankCursor)) #da nema strelicu
		self.setStyleSheet('''
		background-color:  black;
''')		

		self.temp_image = QPixmap('Temperatura_grafik.png')
		self.icon_temp = QIcon(self.temp_image)

		self.vlaga_image = QPixmap('Vlaga.png')
		self.icon_vlaga = QIcon(self.vlaga_image)

		self.masa = QPixmap('Kilaza_po_danima.png')
		self.icon_masa = QIcon(self.masa)

		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet("""
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.btn1 = QPushButton("Temperatura", self)
		self.btn1.resize(260, 70)
		self.btn1.move(5,85)
		self.btn1.clicked.connect(self.btn1_click)
		self.btn1.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn2 = QPushButton("Vlaga" , self)
		self.btn2.resize(260, 70)
		self.btn2.move(5+265 ,85)
		self.btn2.clicked.connect(self.btn2_click)
		self.btn2.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.btn3 = QPushButton("Kilaza", self)
		self.btn3.resize(260, 70)
		self.btn3.move(5+265 + 265,85)
		self.btn3.clicked.connect(self.btn3_click)
		self.btn3.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;;

''')

		self.grafik = QPushButton(self)
		self.grafik.resize(530, 300)
		self.grafik.move(5 ,160)
		self.grafik.setIcon(self.icon_temp)
		self.grafik.setIconSize(QSize(530, 340))

		self.btn7 = QPushButton("Jomapex Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Statistika", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.btn9.resize(260, 70)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.timer = QTimer()
		self.timer.timeout.connect(self.refresh)
		self.timer.start(1000)

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
		self.temp_image = QPixmap('Temperatura_grafik.png')
		self.icon_temp = QIcon(self.temp_image)

		self.vlaga_image = QPixmap('Vlaga.png')
		self.icon_vlaga = QIcon(self.vlaga_image)

		self.masa = QPixmap('Kilaza_po_danima.png')
		self.icon_masa = QIcon(self.masa)

	def btn1_click(self):
		self.grafik.setIcon(self.icon_temp)

	def btn2_click(self):
		self.grafik.setIcon(self.icon_vlaga)

	def btn3_click(self):
		os.system("python grafik.py " + str(dan))
		self.grafik.setIcon(self.icon_masa)

	def back_click(self):
		self.close()



class Alarm_Listing_Form(QMainWindow):
	def __init__(self, parent = None):
		super(Alarm_Listing_Form, self).__init__(parent)
		self.resize(800, 480)
		#self.setCursor(QCursor(Qt.BlankCursor)) #da nema strelicu
		self.setStyleSheet('''
		background-color:  black;
''')		

		self.back = QPushButton("Nazad", self) #buton za nazad
		self.back.resize(260, 70)
		self.back.move(5+265 + 265, 405)
		self.back.clicked.connect(self.back_click)
		self.back.setStyleSheet("""
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.btn7 = QPushButton("SRM Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Alarm", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		border: 5px solid #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.btn9.resize(260, 70)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.f = open('alarm.txt', 'r')
		self.niz = []
		line = self.f.readline()
		while line:
			self.niz.append(line)
			line = self.f.readline()
		self.string = ''
		self.f.close()
		if(len(self.niz) > 9):
			for i in range(0, 9):
				self.string = self.string + self.niz[len(self.niz) - i - 1]
			self.f = open('alarm.txt', 'w')
			self.f.close()
			self.f = open('alarm.txt', 'a')
			for i in range(len(self.niz)- 9, len(self.niz)):
				self.f.write(self.niz[i])
			self.f.close()
		else:
			for i in range(0, len(self.niz)):
				self.string = self.string + self.niz[len(self.niz) - i - 1]

		self.label = QLabel("asdasdasd", self)
		self.label.setText(self.string)
		self.label.move(5, 75)
		self.label.resize(800, 330)
		self.label.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
	def back_click(self):
		self.close()

class Window(QMainWindow):
	def __init__(self, parent = None):
		super(Window, self).__init__(parent)
		self.resize(800, 480)
		#self.setCursor(QCursor(Qt.BlankCursor)) #da nema strelicu
		self.setStyleSheet('''
		background-color:  black;
''')		

		self.temp_image = QPixmap('Utemp.jpeg')
		self.icon_temp = QIcon(self.temp_image)

		self.vlaga_image = QPixmap('zhum.jpeg')
		self.icon_vlaga = QIcon(self.vlaga_image)

		self.vent_image = QPixmap('vent.jpg')
		self.icon_vent = QIcon(self.vent_image)

		self.info_image = QPixmap('info.png')
		self.icon_info = QIcon(self.info_image)

		self.napolju_image = QPixmap('Napolju.png')
		self.icon_napolju = QIcon(self.napolju_image)

		self.rucne_image = QPixmap('Settings.png')
		self.icon_rucne = QIcon(self.rucne_image)

		self.btn1 = QPushButton("", self)
		self.btn1.resize(260, 190)
		self.btn1.move(5,85)
		self.btn1.setIcon(self.icon_temp)
		self.btn1.setIconSize(QSize(120, 120))
		self.btn1.clicked.connect(self.btn1_click)
		self.btn1.setStyleSheet('''
		border: 5px solid  #009933;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn2 = QPushButton(self)
		self.btn2.resize(260, 190)
		self.btn2.move(5+265 ,85)
		self.btn2.setText("Rezim: " + str(f.rezim))
		self.btn2.setIcon(self.icon_vent)
		self.btn2.clicked.connect(self.ventilacija)
		self.btn2.setIconSize(QSize(150, 150))
		self.btn2.setStyleSheet('''
		border: 5px solid  #2a52a2;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 20px;

''')
		self.btn3 = QPushButton(self)
		self.btn3.resize(260, 190)
		self.btn3.move(5+265 + 265,85)
		self.btn3.setIcon(self.icon_napolju)
		self.btn3.setIconSize(QSize(120, 120))
		self.btn3.setStyleSheet('''
		border: 5px solid  #e68a00;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn4 = QPushButton( self)
		self.btn4.resize(260, 190)
		self.btn4.move(5,85 + 195)
		self.btn4.setIcon(self.icon_vlaga)
		self.btn4.setIconSize(QSize(120, 120))
		self.btn4.clicked.connect(self.btn4_click)
		self.btn4.setStyleSheet('''
		border: 5px solid  #cc0000;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.btn5 = QPushButton(self)
		self.btn5.resize(260, 190)
		self.btn5.move(5+265 ,85 + 195)
		self.btn5.setIcon(self.icon_rucne)
		self.btn5.setIconSize(QSize(130, 130))
		self.btn5.clicked.connect(self.btn5_click)
		self.btn5.setStyleSheet('''
		border: 5px solid #800080;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 35px;

''')

		self.btn6 = QPushButton(self)
		self.btn6.resize(260, 190)
		self.btn6.move(5+265 + 265,85 + 195)
		self.btn6.setIcon(self.icon_info)
		self.btn6.setIconSize(QSize(140, 140))
		self.btn6.clicked.connect(self.btn6_click)
		self.btn6.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 40px;

''')
		self.btn7 = QPushButton("SRM Farm Solution", self)
		self.btn7.setText(logo_string)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Broj pilica", self)
		self.btn8.resize(260, 70)
		self.btn8.move(5 + 265,5)
		self.btn8.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn9 = QPushButton(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self)
		self.btn9.resize(260, 70)
		self.btn9.clicked.connect(self.vreme_click)
		self.btn9.move(5 + 265 + 265,5)
		self.btn9.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.vreme = QTimer()
		self.vreme.timeout.connect(self.refresh)
		self.vreme.start(1000)

		self.dan = QTimer()
		self.dan.timeout.connect(self.povecaj_dan)
		self.dan.start(60*1000)

		self.izmeri_temperaturu1 = QTimer()
		self.izmeri_temperaturu1.timeout.connect(self.izmeri_temperaturu_1)
		self.izmeri_temperaturu1.start(7000)

		self.izmeri_temperaturu2 = QTimer()
		self.izmeri_temperaturu2.timeout.connect(self.izmeri_temperaturu_2)
		self.izmeri_temperaturu2.start(12000)

		self.izmeri_temperaturu3 = QTimer()
		self.izmeri_temperaturu3.timeout.connect(self.izmeri_temperaturu_3)
		self.izmeri_temperaturu3.start(12000)

		self.izmeri_vlagu1 = QTimer()
		self.izmeri_vlagu1.timeout.connect(self.izmeri_vlagu_1)
		self.izmeri_vlagu1.start(12000)

		self.izmeri_vlagu2 = QTimer()
		self.izmeri_vlagu2.timeout.connect(self.izmeri_vlagu_2)
		self.izmeri_vlagu2.start(12000)

		self.izmeri_vlagu3 = QTimer()
		self.izmeri_vlagu3.timeout.connect(self.izmeri_vlagu_3)
		self.izmeri_vlagu3.start(12000)

		self.izmeri_avg_tred = QTimer()
		self.izmeri_avg_tred.timeout.connect(self.avg)
		self.izmeri_avg_tred.start(7000)

		self.izmeri_napolju_tred = QTimer()
		self.izmeri_napolju_tred.timeout.connect(self.izmeri_napolju)
		self.izmeri_napolju_tred.start(7000)

		self.regulacija_tred = QTimer()
		self.regulacija_tred.timeout.connect(self.regulacija)
		self.regulacija_tred.start(10000)

		self.servo_tred = QTimer()
		self.servo_tred.timeout.connect(self.servo)
		self.servo_tred.start(10000)

		self.glavni_parametri_tred = QTimer()
		self.glavni_parametri_tred.timeout.connect(self.parametri)
		self.glavni_parametri_tred.start(1)

		self.alarm_tred = QTimer()
		self.alarm_tred.timeout.connect(self.jel_treba_da_ukljuci_alarm)
		self.alarm_tred.start(60*1000)

		self.avg_vrednosti_za_grafik_tred = QTimer()
		self.avg_vrednosti_za_grafik_tred.timeout.connect(self.avg_vrednosti_za_grafik)
		self.avg_vrednosti_za_grafik_tred.start(30000)
		
	def refresh(self):

		global umrli
		global dan
		global broj_zivih
		if(f.jel_greje == 1):
			self.btn2.setText("Rezim: " + str(f.rezim) + "\n  Greje")
		elif(f.jel_greje == -1):
			self.btn2.setText("Rezim: " + str(f.rezim) + "\n  Klima")
		else:
			self.btn2.setText("Rezim: " + str(f.rezim))
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
		try:
			openn = open("broj.txt", "r")
			self.broj_pilica_str = openn.read()
			self.broj_pilica = int(self.broj_pilica_str)
			openn.close()
		except:
			pass
		try:
			openn = open("uginuli.txt", "r")
			self.broj_pilica_str = openn.read()
			umrli = int(self.broj_pilica_str)
			self.broj_pilica = self.broj_pilica - int(self.broj_pilica_str)
			if(self.broj_pilica < 1):
				self.broj_pilica = 0
			openn.close()
			broj_zivih = self.broj_pilica
		except:
			broj_zivih = 0
		self.btn8.setText("Broj pilica: " + str(broj_zivih))
		
		try:
			openn = open("dan.txt", "r")
			self.broj_pilica_str = openn.read()
			dan = int(self.broj_pilica_str)
			openn.close()
		except:
			dan = 0

		openn = open("min_vent_1.txt", "r")
		global kubikaza
		kubikaza = int(openn.read())
		openn.close()

	def regulacija(self):

		global semafor_regulacija
		if(jesu_aktivirane_rucne_komande == 0):

			self.temp1 = float(temperatura_1)
			self.temp3 = float(temperatura_3)

			f.dodeli(1,1,1,1,1,1,1)
			f.regulacija(avg_temperatura, dan, broj_zivih, kubikaza, spoljasnja_temperatura, gornja_granica, donja_granica, zeljena_temperatura, zeljena_temperatura_rucno)
			global zeljena_temperatura
			zeljena_temperatura = f.zeljena

			if((zeljena_temperatura - self.temp1) > donja_granica):
				GPIO.output(grejanje_sonda_1_pin, 0)
			else:
				GPIO.output(grejanje_sonda_1_pin, 1)

			if((zeljena_temperatura - self.temp3) > donja_granica):
				GPIO.output(grejanje_sonda_3_pin, 0)
			else:
				GPIO.output(grejanje_sonda_3_pin, 1)

			if(avg_vlaga > 75 and dan > 17):
				GPIO.output(vlaga_relej_pin, 0)
			else:
				GPIO.output(vlaga_relej_pin, 1)

			if(f.sek != 1):
				if(f.minimum_ventilacije_radi == 1):
					if(semafor_regulacija == 0):
						self.regulacija_tred.setInterval(f.sek*1000) #koliko radi minimum ventilacije
						semafor_regulacija = 1
					else:
						semafor_regulacija = 0
						f.dodeli(1,1,1,1,1,1,1)
						self.regulacija_tred.setInterval(360*1000 - f.sek*1000) #koliko ne radi minimum ventilacije
				else:
						self.regulacija_tred.setInterval(f.sek*1000)
			else:
				f.dodeli(1,1,1,1,1,1,1)
				self.regulacija_tred.setInterval(1)

	def servo(self):
		global semafor_servo
		if(jesu_aktivirane_rucne_komande == 0):
			if(f.minimum_ventilacije_radi == 1):
					if(semafor_servo == 0):
						self.servo_tred.setInterval(f.sekunde_servo*1000)
						semafor_servo = 1
					else:
						semafor_servo = 0
						f.vrati_servo(f.procenat)
						self.servo_tred.setInterval(360*1000 - f.sekunde_servo*1000)

	def parametri(self):
		
		global jel_treba_da_resetuje_glavni_tred
		if(jel_treba_da_resetuje_glavni_tred == 1):
			if(jesu_aktivirane_rucne_komande == 0):
				self.regulacija_tred.start(1)
				self.servo_tred.start(1)
				jel_treba_da_resetuje_glavni_tred = 0

	def	jel_treba_da_ukljuci_alarm(self):
		global radi_alarm
		if(jel_alarm_aktiviran == 0):
			if(radi_alarm == 0):
				if(zeljena_temperatura - avg_temperatura  > gornja_granica_alarma):
					print("DEBUG: " + str(avg_temperatura) + "    " + str(zeljena_temperatura))
					self.popup = Uzbuna_Form()
					self.popup.showFullScreen()
					radi_alarm = 1
					fajl = open("alarm.txt", "a")
					fajl.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ": Zeljena temperatura veca za " + str(gornja_granica_alarma) + " od prosecne\n")
					fajl.close()
				elif(avg_temperatura - zeljena_temperatura > donja_granica_alarma):
					self.popup = Uzbuna_Form()
					self.popup.showFullScreen()
					radi_alarm = 1
					fajl = open("alarm.txt", "a")
					fajl.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ": Zeljena temperatura manja za " + str(donja_granica_alarma) + " od prosecne\n")
					fajl.close()
				elif(avg_vlaga > granica_vlage_za_alarm):
					self.popup = Uzbuna_Form()
					self.popup.showFullScreen()
					radi_alarm = 1
					fajl = open("alarm.txt", "a")
					fajl.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ": prosecna vlaga presla " + str(granica_vlage_za_alarm) + " %\n")
					fajl.close()
				elif(temperatura_1 == "-99.9" and temperatura_2 == "-99.9" and temperatura_3 == "-99.9"):
					self.popup = Uzbuna_Form()
					self.popup.showFullScreen()
					radi_alarm = 1
					fajl = open("alarm.txt", "a")
					fajl.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ": Sva tri senzora neispravna\n")
					fajl.close()

	def avg_vrednosti_za_grafik(self):
		fajl = open("avg_temperatura_za_grafik.txt", "a")
		fajl.write(str(avg_temperatura) + "\n")
		fajl.close()
		
		os.system("python grafik_temperatura.py &")

		fajl = open("avg_vlaga_za_grafik.txt", "a")
		fajl.write(str(avg_vlaga) + "\n")
		fajl.close()

		os.system("python grafik_vlaga.py &")

	def izmeri_temperaturu_1(self):
		global temperatura_1
		os.system("python izmeri1.py &")
		fajl = open("temperatura1.txt", "r")
		self.string = fajl.read()
		if(self.string != None and self.string != ''):
			temperatura_1 = self.string
		fajl.close()

	def izmeri_temperaturu_2(self):
		global temperatura_2
		fajl = open("temperatura2.txt", "r")
		self.string = fajl.read()
		if(self.string != None and self.string != ''):
			temperatura_2 = self.string
		fajl.close()

	def izmeri_temperaturu_3(self):
		global temperatura_3
		fajl = open("temperatura3.txt", "r")
		self.string = fajl.read()
		if(self.string != None and self.string != ''):
			temperatura_3 = self.string
		fajl.close()

	def izmeri_vlagu_1(self):
		global vlaga_1
		fajl = open("vlaga1.txt", "r")
		self.string = fajl.read()
		if(self.string != None and self.string != ''):
			vlaga_1 = self.string
		if(self.string == ''):
			vlaga_1 = "-99.9"
		fajl.close()

	def izmeri_vlagu_2(self):
		global vlaga_2
		fajl = open("vlaga2.txt", "r")
		self.string = fajl.read()
		if(self.string != None and self.string != ''):
			vlaga_2 = self.string
		if(self.string == ''):
			vlaga_2 = "-99.9"
		fajl.close()

	def izmeri_vlagu_3(self):
		global vlaga_3
		fajl = open("vlaga3.txt", "r")
		self.string = fajl.read()
		if(self.string != None and self.string != ''):
			vlaga_3 = self.string
		if(self.string == ''):
			vlaga_3 = "-99.9"
		fajl.close()


	def izmeri_napolju(self):
		global spoljasnja_temperatura
		fajl = open("spoljasnja.txt", "r")
		self.string = fajl.readline()
		spoljasnja_temperatura = float(self.string)
		self.string = fajl.readline()
		self.btn3.setText("\n" + str(spoljasnja_temperatura) + " C\n" + self.string + " %")
		fajl.close()

	def avg(self):
		self.sum_temp = 0
		self.count = 0

		global avg_temperatura
		global count

		if(float(temperatura_1) > 0):
			self.sum_temp = self.sum_temp + float(temperatura_1)
			self.count = self.count + 1
		if(float(temperatura_2) > 0):
			self.sum_temp = self.sum_temp + float(temperatura_2)
			self.count = self.count + 1
		if(float(temperatura_3) > 0):
			self.sum_temp = self.sum_temp + float(temperatura_3)
			self.count = self.count + 1
		if(self.count > 0):
			if(count == 0):
				avg_temperatura = float(self.sum_temp)/float(self.count)
				avg_temperatura = round(avg_temperatura,1)
				self.btn1.setText(str(avg_temperatura) + " C")
				count = 1
				print "avg_temperatura: " + str(avg_temperatura)
			else:
				if(abs(avg_temperatura - float(self.sum_temp)/float(self.count)) < 2):
					print "racuna"
					avg_temperatura = float(self.sum_temp)/float(self.count)
					avg_temperatura = round(avg_temperatura,1)
					self.btn1.setText(str(avg_temperatura) + " C")
				else: 
					print "Nije sracunao, avg = " + str(float(self.sum_temp)/float(self.count)) + "prosla je: " + str(avg_temperatura)

		self.sum_temp = 0
		self.count = 0

		global avg_vlaga

		if(float(vlaga_1) > 0):
			self.sum_temp = self.sum_temp + float(vlaga_1)
			self.count = self.count + 1
		if(float(vlaga_2) > 0):
			self.sum_temp = self.sum_temp + float(vlaga_2)
			self.count = self.count + 1
		if(float(vlaga_3) > 0):
			self.sum_temp = self.sum_temp + float(vlaga_3)
			self.count = self.count + 1
		if(self.count > 0):
			avg_vlaga = float(self.sum_temp)/float(self.count)
			avg_vlaga = round(avg_vlaga,1)
			self.btn4.setText(str(avg_vlaga) + " %")

	def btn1_click(self):
		self.popup =  Button1_Form()
		self.popup.showFullScreen()

	def btn4_click(self):
		self.popup =  Button4_Form()
		self.popup.showFullScreen()

	def btn5_click(self):
		self.popup = Button5_Form()
		self.popup.showFullScreen()

	def btn6_click(self):
		self.popup =  Button6_Form()
		self.popup.showFullScreen()

	def ventilacija(self):
		self.popup =  Ventilacija_Form()
		self.popup.showFullScreen()

	def vreme_click(self):
		self.popup =  vreme_dialog.Vreme_Form()
		self.popup.showFullScreen()

	def povecaj_dan(self):
		if (time.strftime("%H:%M") == "00:00"):
			otvori = open("dan.txt", "r")
			self.dan_temp = int(otvori.read())
			self.dan_temp = self.dan_temp + 1
			otvori.close()
			print str(self.dan_temp)
			if(self.dan_temp - 1 != 0):
				otvori = open("dan.txt","w")
				otvori.write(str(self.dan_temp))
				otvori.close()

				otvori = open("masa_pilica.txt", "r")
				self.masa_pilica_danas = otvori.read()
				otvori.close()

				otvori = open("masa_pilica.txt", "w")
				otvori.close()

				otvori = open("masa_pilica_po_danima.txt", "a")
				otvori.write(self.masa_pilica_danas)
				otvori.close()

				otvori = open("avg_temperatura_za_grafik.txt", "w")
				otvori.close()
			
				otvori = open("avg_vlaga_za_grafik.txt", "w")
				otvori.close()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Window()
	main.showFullScreen()
	app.exec_()
