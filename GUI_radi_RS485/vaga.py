from PyQt4.QtGui import *
from PyQt4.QtCore import *
import datetime
#import RPi.GPIO as GPIO
import time
import sys
#from hx711 import HX711
import f

logo_string = "Jomapeks Farm Solution"

greska = 0
tara = 144
jel_pise = 0

class Vaga_Form(QMainWindow): #Temperatura
	def __init__(self, dan, parent = None):
		super(Vaga_Form, self).__init__(parent)
		self.resize(800, 480)
		self.setStyleSheet('''
	background-color:  black;
''')
#		self.hx = HX711(25, 8)
#		self.hx.set_reference_unit(tara) #bilo je 92
#		self.hx.reset()

		self.dan = dan

		openn = open("tara.txt", "r")
		self.g = openn.read()
		global greska
		greska = int(self.g)
		openn.close()

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

		self.btn1 = QPushButton("Vaga: 0g",self)
		self.btn1.resize(260, 190)
		self.btn1.move(5,85)
		self.btn1.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn2 = QPushButton("Srednja vrednost", self)
		self.btn2.resize(260, 190)
		self.btn2.move(5+265 ,85)
		self.btn2.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 25px;

''')
		self.btn3 = QPushButton("Tara", self)
		self.btn3.clicked.connect(self.tariraj)
		self.btn3.resize(260, 190)
		self.btn3.move(5+265 + 265,85)
		self.btn3.setStyleSheet('''
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
		self.btn8 = QPushButton("Vaga", self)
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

		self.meri_tred = QTimer()
		self.meri_tred.timeout.connect(self.meri)
		self.meri_tred.start(5000)

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
		
	def meri(self):
		self.val = 5#self.hx.get_weight(5) - greska
		self.val = self.val/10
		self.val = self.val*10
		self.val = float(self.val)
		self.btn1.setText(str(self.val) + " g")
		self.hx.power_down()
		self.hx.power_up()
		
		self.ocekivana_kilaza = f.kilaza(self.dan)
		self.ocekivana_kilaza = self.ocekivana_kilaza * 1000
		self.ocekivana_kilaza = float(self.ocekivana_kilaza )
		if (time.strftime("%H:%M") != "00:00"):
			if(self.val > self.ocekivana_kilaza*0.5 and self.val < self.ocekivana_kilaza*1.5):
				global jel_pise
				print "Usao je u pisanje"
				jel_pise = 1
				self.f = open('masa_pilica.txt', 'a+')
				self.f.write(str(self.val) + "\n")
				self.f.close()
				jel_pise = 0

			self.f = open('masa_pilica.txt', 'r')
			niz = []
			line = self.f.readline()
			suma = 0
			while line:
				x = float(line)
				suma = suma + x
				niz.append(x)
				line = self.f.readline()
				self.avg = float(suma)/float(len(niz))
				self.avg = round(self.avg, 0)
			self.f.close()
			self.btn2.setText(str(self.avg) + " g")

			if(len(niz) > 20):
				fajl = open("masa_pilica.txt", "w")
				fajl.write(str(self.avg) + "\n")
				fajl.close()

	def back_click(self):
		self.close()

	def tariraj(self):
		self.popup = Tara_Form()
		self.popup.showFullScreen()

class Tara_Form(QMainWindow): #Temperatura
	def __init__(self, parent = None):
		super(Tara_Form, self).__init__(parent)
		self.resize(800, 480)
		self.setStyleSheet('''
	background-color:  black;
''')

		"""self.hx = HX711(25, 8)
		self.hx.set_reference_unit(tara) #bilo je 92
		self.hx.reset()"""

		openn = open("tara.txt", "r")
		self.g = openn.read()
		global greska
		greska = int(self.g)
		openn.close()

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

		self.btn1 = QPushButton("Tariraj",self)
		self.btn1.resize(260, 190)
		self.btn1.move(5,85)
		self.btn1.clicked.connect(self.tariraj)
		self.btn1.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;

''')

		self.btn2 = QPushButton("Rezultat", self)
		self.btn2.resize(260, 190)
		self.btn2.move(5+265 ,85)
		self.btn2.setStyleSheet('''
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
		self.btn8 = QPushButton("Tara", self)
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
		self.val =33 # self.hx.get_weight(5) - greska
		self.btn2.setText(str(self.val) + " g")
		#self.hx.power_down()
		#self.hx.power_up()

	def back_click(self):
		self.close()

	def tariraj(self):
		self.val = 1#self.hx.get_weight(5)

		#self.hx.power_down()
		#self.hx.power_up()
		global greska
		greska = self.val
		openn = open("tara.txt", "w")
		openn.write(str(greska))
		openn.close()
