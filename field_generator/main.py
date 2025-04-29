import numpy as np
from numpy.polynomial.hermite import Hermite
import matplotlib.pyplot as plt
import json
import hashlib
from functools import reduce
import matplotlib.image as mpimg

with open("../consts.JSON", "r", encoding="utf-8") as file:
    consts = json.load(file)

n_x = consts["constantes"]["n_x"]
n_y = consts["constantes"]["n_y"]
h = consts["constantes"]["h"]
m = consts["constantes"]["m"]
kx = consts["constantes"]["k_x"]
ky = consts["constantes"]["k_y"]
w = consts["constantes"]["w"]

# Initialize the potential grid
Vmat = np.zeros((n_x, n_y))

# Initialize the wave function grid
psi0Re = np.zeros((n_x, n_y))
psi0Im = np.zeros((n_x, n_y))

# Calculate the potential centered in (0, 0) at each point in the grid following this equation:
# V = (x² + y²) / 9 without i and j loop
def calcHarmV():
	x = np.linspace(-10, 10, n_x)
	y = np.linspace(-10, 10, n_y)
	X, Y = np.meshgrid(x, y)
	global Vmat
	Vmat = (X**2 + Y**2) / 9
	return Vmat

def calcVFromImage():
	img_path = consts["paramètres utilisateurs"]["image_V"]
	img = mpimg.imread(img_path)
	return img

def plotV():
	global Vmat
	plt.imshow(Vmat, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.axis('off')
	plt.show()

def calcGaussPsi0():
	A = np.sqrt(2 / np.pi * (w**2))
	x = np.linspace(-10, 10, n_x)
	y = np.linspace(-10, 10, n_y)
	X, Y = np.meshgrid(x, y)
	psi0Re = A * np.exp(- (X**2 + Y**2) / (2 * w**2)) * np.cos(kx * X + ky * Y)
	psi0Im = A * np.exp(- (X**2 + Y**2) / (2 * w**2)) * np.sin(kx * X + ky * Y)
	return psi0Re, psi0Im

def calc2DHOPsi0():
	nx = consts["paramètres utilisateurs"]["psi"]["2DH0_nx"]
	ny = consts["paramètres utilisateurs"]["psi"]["2DH0_ny"]

	coeff_x = [0 for i in range(nx - 1)]
	coeff_x.append(1)
	H3_x = Hermite([coeff_x])
	coeff_y = [0 for i in range(ny - 1)]
	coeff_y.append(1)
	H3_y = Hermite([coeff_y])

	x = np.linspace(-10, 10, n_x)
	y = np.linspace(-10, 10, n_y)
	X, Y = np.meshgrid(x, y)
	psi_x = (1/np.sqrt(2**nx * np.math.factorial(nx))) * ((m*w)/np.pi*h)**(1/4) * np.exp(-((m * w * X) /(2 * h) )) * H3_x(np.sqrt(m * w / h)* X)
	psi_y = (1/np.sqrt(2**ny * np.math.factorial(ny))) * ((m*w)/np.pi*h)**(1/4) * np.exp(-((m * w * Y) /(2 * h) )) * H3_y(np.sqrt(m * w / h)* Y)

	return psi_x * psi_y

def calcMult2DHOPsi0():
	nb = consts["paramètres utilisateurs"]["psi"]["nb"]
	if nb == 1:
		return calc2DHOPsi0()
	nx = consts["paramètres utilisateurs"]["psi"]["2DH0_nx"]
	ny = consts["paramètres utilisateurs"]["psi"]["2DH0_ny"]
	psi_array = []
	for i in range(nb):
		coeff_x = [0 for j in range(nx[i] - 1)]
		coeff_x.append(1)
		H3_x = Hermite([coeff_x])
		coeff_y = [0 for j in range(ny[i] - 1)]
		coeff_y.append(1)
		H3_y = Hermite([coeff_y])

		x = np.linspace(-10, 10, n_x)
		y = np.linspace(-10, 10, n_y)
		X, Y = np.meshgrid(x, y)
		psi_x = (1/np.sqrt(2**nx[i] * np.math.factorial(nx[i]))) * ((m*w)/np.pi*h)**(1/4) * np.exp(-((m * w * X) /(2 * h) )) * H3_x(np.sqrt(m * w / h)* X)
		psi_y = (1/np.sqrt(2**ny[i] * np.math.factorial(ny[i]))) * ((m*w)/np.pi*h)**(1/4) * np.exp(-((m * w * Y) /(2 * h) )) * H3_y(np.sqrt(m * w / h)* Y)
		psi_array.append(psi_x * psi_y)
	return reduce(np.multiply, psi_array)

def plotPsi0():
	psi0Real, psi0Comp = calcPsi()
	plt.subplot(1, 2, 1)
	plt.imshow(psi0Real, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.title('Partie réelle de psi0')
	plt.axis('off')

	plt.subplot(1, 2, 2)
	plt.imshow(psi0Comp, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.title('Partie imaginaire de psi0')
	plt.axis('off')

	plt.show()

# Calculate the potential according to the v value :
# if v = 0, use the image given in the consts.JSON file
# if v = 1, the potential is 0 everywhere
# if v = 2, the potential for a harmonic oscillator
def calcV():
	v = consts["paramètres utilisateurs"]["V"]
	match v:
		case 0:
			return calcVFromImage()
		case 1:
			return Vmat
		case 2:
			return calcHarmV()
		case _:
			print("Not a valid value for v")

# Calculate the wave function according to the psi value :
# if psi = 0, use gaussian wave packet with initial speed
# if psi = 1, use a solution of the 2D-HO
# if psi = 2, use a combination of solution of the 2D-HO
def calcPsi():
	match consts["paramètres utilisateurs"]["psi"]["type"]:
		case 0:
			return calcGaussPsi0()
		case 1:
			return calc2DHOPsi0(), np.zeros((n_x, n_y))
		case 2:
			return calcMult2DHOPsi0(), np.zeros((n_x, n_y))
		
def calcJSONHash():
	file = "../consts.JSON"
	with open(file, "r", encoding="utf-8") as f:
		data = json.load(f)
	
	json_normalized = json.dumps(data, sort_keys=True, separators=(',', ':'))

	hash = hashlib.sha256(json_normalized.encode("utf-8"))

	return hash.hexdigest()


def main():
	global Vmat, psi0Re, psi0Im
	# Calculate the potential according to the V value :
	Vmat = calcV()
	plotV()
	# Calculate the wave function according to the psi value :
	psi0Re, psi0Im = calcPsi()
	# Calculate the hash of the experiment
	hash = calcJSONHash()
	print("Hash of the experiment: ", hash)
	# Send the data in the database if the experiment is not already done

main()