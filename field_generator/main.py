import numpy as np
from numpy.polynomial.hermite import Hermite
import matplotlib.pyplot as plt
import json
import hashlib
from functools import reduce
import matplotlib.image as mpimg
import sys
import os

# Ajoute la racine du projet au path Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import database.databaseManager as db 
import json_utils as js_uti

# Read JSON file
(exp_name, n_x, n_y, x_min, x_max, y_min, y_max, h, m, w, k_x, k_y, 
 psi_type, psi_nb, psi_2DH0_nx, psi_2DH0_ny, V_id, image_V, method, t_max, dt) = js_uti.get_json("../consts.JSON")
 

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
	img = mpimg.imread(image_V)
	return img

def plotV():
	global Vmat
	plt.imshow(Vmat, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.axis('off')
	plt.show()

def calcGaussPsi0():
	x0 = -1*consts["paramètres utilisateurs"]["psi"]["x0"]
	y0 = consts["paramètres utilisateurs"]["psi"]["y0"]
	A = np.sqrt(2 / np.pi * (w**2))
	x = np.linspace(x0-10, x0+10, n_x)
	y = np.linspace(y0-10, y0+10, n_y)
	X, Y = np.meshgrid(x, y)
	psi0Re = A * np.exp(- (X**2 + Y**2) / (2 * w**2)) * np.cos(k_x * X + k_y * Y)
	psi0Im = A * np.exp(- (X**2 + Y**2) / (2 * w**2)) * np.sin(k_x * X + k_y * Y)
	return psi0Re, psi0Im

def calc2DHOPsi0():
	coeff_x = [0 for i in range(psi_2DH0_nx - 1)]
	coeff_x.append(1)
	H3_x = Hermite([coeff_x])
	coeff_y = [0 for i in range(psi_2DH0_ny - 1)]
	coeff_y.append(1)
	H3_y = Hermite([coeff_y])

	x = np.linspace(-10, 10, n_x)
	y = np.linspace(-10, 10, n_y)
	X, Y = np.meshgrid(x, y)
	psi_x = (1/np.sqrt(2**psi_2DH0_nx * np.math.factorial(psi_2DH0_nx))) * ((m*w)/np.pi*h)**(1/4) * np.exp(-((m * w * X) /(2 * h) )) * H3_x(np.sqrt(m * w / h)* X)
	psi_y = (1/np.sqrt(2**psi_2DH0_ny * np.math.factorial(psi_2DH0_ny))) * ((m*w)/np.pi*h)**(1/4) * np.exp(-((m * w * Y) /(2 * h) )) * H3_y(np.sqrt(m * w / h)* Y)

	return psi_x * psi_y

def calcMult2DHOPsi0():
	if psi_nb == 1:
		return calc2DHOPsi0()
	psi_array = []
	for i in range(psi_nb):
		coeff_x = [0 for j in range(psi_2DH0_nx[i] - 1)]
		coeff_x.append(1)
		H3_x = Hermite([coeff_x])
		coeff_y = [0 for j in range(psi_2DH0_ny[i] - 1)]
		coeff_y.append(1)
		H3_y = Hermite([coeff_y])

		x = np.linspace(-10, 10, n_x)
		y = np.linspace(-10, 10, n_y)
		X, Y = np.meshgrid(x, y)
		psi_x = (1/np.sqrt(2**psi_2DH0_nx[i] * np.math.factorial(psi_2DH0_nx[i]))) * ((m*w)/np.pi*h)**(1/4) * np.exp(-((m * w * X) /(2 * h) )) * H3_x(np.sqrt(m * w / h)* X)
		psi_y = (1/np.sqrt(2**psi_2DH0_ny[i] * np.math.factorial(psi_2DH0_ny[i]))) * ((m*w)/np.pi*h)**(1/4) * np.exp(-((m * w * Y) /(2 * h) )) * H3_y(np.sqrt(m * w / h)* Y)
		psi_array.append(psi_x * psi_y)
	return reduce(np.multiply, psi_array)

def plotPsi0():
	psi0Real, psi0Comp = calcPsi()
	plt.subplot(1, 2, 1)
	plt.imshow(psi0Real, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.title('Partie réelle de psi0')
	plt.axis('on')

	plt.subplot(1, 2, 2)
	plt.imshow(psi0Comp, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.title('Partie imaginaire de psi0')
	plt.axis('on')

	plt.show()

# Calculate the potential according to the v value :
# if v = 0, use the image given in the consts.JSON file
# if v = 1, the potential is 0 everywhere
# if v = 2, the potential for a harmonic oscillator
def calcV():
	match V_id:
		case "Image":
			return calcVFromImage()
		case "Null":
			return Vmat
		case "Harmonic":
			return calcHarmV()
		case _:
			print("Not a valid value for v")

# Calculate the wave function according to the psi value :
# if psi = 0, use gaussian wave packet with initial speed
# if psi = 1, use a solution of the 2D-HO
# if psi = 2, use a combination of solution of the 2D-HO
def calcPsi():
	match psi_type:
		case 0:
			return calcGaussPsi0()
		case 1:
			return calc2DHOPsi0(), np.zeros((n_x, n_y))
		case 2:
			return calcMult2DHOPsi0(), np.zeros((n_x, n_y))
		
def dataCleaner(data):
	modified_data = dict(data)
	modified_data.pop("name", None)
	
	param = modified_data.get("paramètres utilisateurs")
	if param and "t_max" in param:
		param.pop("t_max", None)
	
	return modified_data
		
def calcJSONHash():
	file = "../consts.JSON"
	with open(file, "r", encoding="utf-8") as f:
		data = json.load(f)
	
	data = dataCleaner(data)

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
	plotPsi0()
	# Calculate the hash of the experiment
	hash = calcJSONHash()
	print("Hash of the experiment: ", hash)
	# if the name already exists : inform the user that an expriment with the same name already exists
	#if db.AlreadyExist(hash, db.):
		#print("An experiment with the same name already exists")
		# ask the user if he wants to overwrite the experiment
		# if yes, overwrite the experiment
		# if no, ask the user for a new name and end the program
		# -> ask the user if he wants to overwrite the experiment
		# -> if yes, overwrite the experiment
		# -> if no, ask the user for a new name and end the program
		#db.DeleteCollection(hash)
	# -> ask the user if he wants to overwrite the experiment
	# -> if yes, overwrite the experiment
	# -> if no, ask the user for a new name and end the program
	# Send the data in the database if the experiment is not already done
	# if the hash already exists : check the t_max value :
	# -> if t_max is the same, inform the user that an expriment with the same hash already exists
	# -> if the new t_max is lower than the old one, make a new experiment from the beginning
	# -> if the new t_max is higher than the old one, make a new experiment from the last point

main()