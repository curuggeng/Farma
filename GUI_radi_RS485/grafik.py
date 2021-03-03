import matplotlib.pyplot as plt
import f
import sys

radius = []
area = []
for x in range(1, int(sys.argv[1])):
	radius.append(x)

for x in range(1, int(sys.argv[1])):
	area.append(f.kilaza(x)*1000)
plt.plot(radius, area)
plt.title('Kilaza pilica po danima')
plt.xlabel('Dan')
plt.ylabel('Kilaza [g]')
#plt.show()
plt.savefig("Kilaza_po_danima.png")
