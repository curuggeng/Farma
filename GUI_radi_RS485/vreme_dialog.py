import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import datetime
import os

mesec_string = ''

class Vreme_Form(QMainWindow): #Temperatura
	def __init__(self, parent = None):
		super(Vreme_Form, self).__init__(parent)
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

		self.vreme_btn = QRadioButton("Vreme", self) #buton za nazad
		self.vreme_btn.resize(260, 70)
		self.vreme_btn.clicked.connect(self.vreme_click)
		self.vreme_btn.move(5, 75)
		self.vreme_btn.setChecked(True)
		self.vreme_btn.setStyleSheet("""
		border: 5px solid  #009933;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.datum = QRadioButton("Datum", self) #buton za nazad
		self.datum.resize(260, 70)
		self.datum.clicked.connect(self.datum_click)
		self.datum.move(5, 75 + 75)
		self.datum.setStyleSheet("""
		border: 5px solid  #009933;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 25px;
""")

		self.btn7 = QPushButton("Jomapex Farm Solution", self)
		self.btn7.resize(260, 70)
		self.btn7.move(5,5)
		self.btn7.setStyleSheet('''
		background-color:  black;
		color:  white;
		font-size: 20px;
		font-style: italic;

''')
		self.btn8 = QPushButton("Vreme", self)
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

		self.unos = QPushButton(datetime.datetime.now().strftime("%H:%M:%S"), self)
		self.unos.resize(525, 70)
		self.unos.move(270, 75 + 75)
		self.unos.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 50px;

''')

		self.sat_plus = QPushButton("+", self)
		self.sat_plus.resize(70, 70)
		self.sat_plus.clicked.connect(self.sat_plus_click)
		self.sat_plus.move(270 + 150, 78 )
		self.sat_plus.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 50px;

''')
		self.minut_plus = QPushButton("+", self)
		self.minut_plus.resize(70, 70)
		self.minut_plus.clicked.connect(self.minut_plus_click)
		self.minut_plus.move(270 + 150 + 75, 78 )
		self.minut_plus.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 50px;

''')

		self.sekund_plus = QPushButton("+", self)
		self.sekund_plus.resize(70, 70)
		self.sekund_plus.clicked.connect(self.sekund_plus_click)
		self.sekund_plus.move(270 + 150 + 75 + 75, 78 )
		self.sekund_plus.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 50px;

''')

		self.sat_minus = QPushButton("-", self)
		self.sat_minus.resize(70, 70)
		self.sat_minus.clicked.connect(self.sat_minus_click)
		self.sat_minus.move(270 + 150, 78 + 148 )
		self.sat_minus.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 80px;

''')
		self.minut_minus = QPushButton("-", self)
		self.minut_minus.resize(70, 70)
		self.minut_minus.clicked.connect(self.minut_minus_click)
		self.minut_minus.move(270 + 150 + 75, 78 + 148 )
		self.minut_minus.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 80px;

''')

		self.sekund_minus = QPushButton("-", self)
		self.sekund_minus.resize(70, 70)
		self.sekund_minus.clicked.connect(self.sekund_minus_click)
		self.sekund_minus.move(270 + 150 + 75 + 75, 78 + 148)
		self.sekund_minus.setStyleSheet('''
		border: 5px solid  #e6e600;
		border-radius: 25px;
		background-color:  black;
		color:  white;
		font-size: 80px;

''')

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
		self.sat = datetime.datetime.now().strftime("%H")
		self.sat_int = int(self.sat)

		print self.vrati_mesec(5)

		self.minut = datetime.datetime.now().strftime("%M")
		self.minut_int = int(self.minut)

		self.sekund = datetime.datetime.now().strftime("%S")
		self.sekund_int = int(self.sekund)

		self.dan = datetime.datetime.now().strftime("%d")
		self.dan_int = int(self.dan)

		self.godina = datetime.datetime.now().strftime("%Y")
		self.godina_int = int(self.godina)

		self.mesec = datetime.datetime.now().strftime("%m")
		self.mesec_int = int(self.mesec)

		self.vreme = QTimer()
		self.vreme.timeout.connect(self.refresh)
		self.vreme.start(1000)

	def refresh(self):
		self.btn9.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

	def vreme_click(self):
		self.unos.setText(str(self.sat_int) + ":" + str(self.minut_int) + ":" + str(self.sekund_int))

	def datum_click(self):
		self.unos.setText(str(self.godina_int) + "-" + str(self.mesec_int) + "-" + str(self.dan_int))

	def	sat_plus_click(self):
		if(self.vreme_btn.isChecked()):
			self.sat_int = self.sat_int + 1

			if(self.sat_int >23):
				self.sat_int = 0
			if(self.sat_int < 0):
				self.sat_int = 23

			self.unos.setText(str(self.sat_int) + ":" + str(self.minut_int) + ":" + str(self.sekund_int))
		else:
			self.godina_int = self.godina_int + 1

			if(self.godina_int < 2018):
				self.godina_int = 2018

			self.unos.setText(str(self.godina_int) + "-" + str(self.mesec_int) + "-" + str(self.dan_int))

	def	minut_plus_click(self):
		if(self.vreme_btn.isChecked()):
			self.minut_int = self.minut_int + 1


			if(self.minut_int >59):
				self.minut_int = 0
			if(self.minut_int < 0):
				self.minut_int = 59

			self.unos.setText(str(self.sat_int) + ":" + str(self.minut_int) + ":" + str(self.sekund_int))
		else:
			self.mesec_int = self.mesec_int + 1

			if(self.mesec_int >12):
				self.mesec_int = 1
			if(self.mesec_int < 1):
				self.mesec_int = 12

			self.unos.setText(str(self.godina_int) + "-" + str(self.mesec_int) + "-" + str(self.dan_int))


	def	sekund_plus_click(self):
		if(self.vreme_btn.isChecked()):
			self.sekund_int = self.sekund_int + 1

			if(self.sekund_int >59):
				self.sekund_int = 0
			if(self.sekund_int < 0):
				self.sekund_int = 59

			self.unos.setText(str(self.sat_int) + ":" + str(self.minut_int) + ":" + str(self.sekund_int))
		else:
			self.dan_int = self.dan_int + 1

			if(self.dan_int >31):
				self.dan_int = 1
			if(self.dan_int < 1):
				self.dan_int = 31

			self.unos.setText(str(self.godina_int) + "-" + str(self.mesec_int) + "-" + str(self.dan_int))



	def	sat_minus_click(self):
		if(self.vreme_btn.isChecked()):
			self.sat_int = self.sat_int - 1

			if(self.sat_int >23):
				self.sat_int = 0
			if(self.sat_int < 0):
				self.sat_int = 23

			self.unos.setText(str(self.sat_int) + ":" + str(self.minut_int) + ":" + str(self.sekund_int))
		else:
			self.godina_int = self.godina_int - 1

			if(self.godina_int < 2018):
				self.godina_int = 2018

			self.unos.setText(str(self.godina_int) + "-" + str(self.mesec_int) + "-" + str(self.dan_int))

	def	minut_minus_click(self):
		if(self.vreme_btn.isChecked()):
			self.minut_int = self.minut_int - 1

			if(self.minut_int >59):
				self.minut_int = 0
			if(self.minut_int < 0):
				self.minut_int = 59

			self.unos.setText(str(self.sat_int) + ":" + str(self.minut_int) + ":" + str(self.sekund_int))
		else:
			self.mesec_int = self.mesec_int - 1

			if(self.mesec_int >12):
				self.mesec_int = 1
			if(self.mesec_int < 1):
				self.mesec_int = 12

			self.unos.setText(str(self.godina_int) + "-" + str(self.mesec_int) + "-" + str(self.dan_int))

	def	sekund_minus_click(self):
		if(self.vreme_btn.isChecked()):
			self.sekund_int = self.sekund_int - 1

			if(self.sekund_int >59):
				self.sekund_int = 0
			if(self.sekund_int < 0):
				self.sekund_int = 59

			self.unos.setText(str(self.sat_int) + ":" + str(self.minut_int) + ":" + str(self.sekund_int))
		else:
			self.dan_int = self.dan_int -1

			if(self.dan_int >31):
				self.dan_int = 1
			if(self.dan_int < 1):
				self.dan_int = 31

			self.unos.setText(str(self.godina_int) + "-" + str(self.mesec_int) + "-" + str(self.dan_int))

	def vrati_mesec(mesec,self):
		global mesec_string
		if(mesec == 1):
			mesec_string =  "JAN"
		if(mesec == 2):
			mesec_string = "FEB"
		if(mesec == 3):
			mesec_string = "MAR"
		if(mesec == 4):
			mesec_string =  "APR"
		if(mesec == 5):
			mesec_string = "MAY"
		if(mesec == 6):
			mesec_string = "JUN"
		if(mesec == 7):
			mesec_string = "JUL"
		if(mesec == 8):
			mesec_string = "AUG"
		if(mesec == 9):
			mesec_string = "SEP"
		if(mesec == 10):
			mesec_string = "OCT"
		if(mesec == 11):
			mesec_string = "NOV"
		if(mesec == 12):
			mesec_string = "DEC"


	def potvrdi_click(self):		
		self.komanda = "sudo date -s " + "\"" + str(self.sat_int) + ":" + str(self.minut_int) + ":" +  str(self.sekund_int) + "\""
		print self.komanda
		os.system(self.komanda)
		
		global mesec_string
		if(self.mesec_int == 1):
			mesec_string =  "JAN"
		if(self.mesec_int == 2):
			mesec_string = "FEB"
		if(self.mesec_int == 3):
			mesec_string = "MAR"
		if(self.mesec_int == 4):
			mesec_string =  "APR"
		if(self.mesec_int == 5):
			mesec_string = "MAY"
		if(self.mesec_int == 6):
			mesec_string = "JUN"
		if(self.mesec_int == 7):
			mesec_string = "JUL"
		if(self.mesec_int == 8):
			mesec_string = "AUG"
		if(self.mesec_int == 9):
			mesec_string = "SEP"
		if(self.mesec_int == 10):
			mesec_string = "OCT"
		if(self.mesec_int == 11):
			mesec_string = "NOV"
		if(self.mesec_int == 12):
			mesec_string = "DEC"		


		self.komanda = "sudo date -s" + "\"" +str(self.dan_int) + " " + mesec_string + " " + str(self.godina_int) + " " + str(self.sat_int) + ":" + str(self.minut_int) + ":" +  str(self.sekund_int) + "\""
		os.system(self.komanda)
		os.system("sudo hwclock -w")
	
	def back_click(self):
		self.close()










