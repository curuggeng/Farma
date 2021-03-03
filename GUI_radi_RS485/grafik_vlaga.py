import matplotlib.pyplot as plt
import f
import sys

radius = []
area = []
niz = []

fajl = open("avg_vlaga_za_grafik.txt", "r")
string = fajl.read()
radius = string.split("\n")
fajl.close()


for x in range(0, len(radius)-1):
	niz.append(float(radius[x]))

for x in range(0, len(radius)-1):
	area.append(x)


plt.plot(area, niz)
plt.title('Trenutna vlaga')
plt.ylabel('Vlaga [%]')
#plt.show()
plt.savefig("Vlaga.png")

