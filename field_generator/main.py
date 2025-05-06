import numpy as np
from numpy.polynomial.hermite import Hermite
import matplotlib.pyplot as plt
import json
import hashlib
from functools import reduce
import matplotlib.image as mpimg
import sys
import os
from pathlib import Path

# Adding root of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import database.databaseManager as db
import json_utils as js_uti

# Check the number of arguments
if len(sys.argv) != 2:
	print("Usage:", sys.argv[0], "<path/to/json>")
	exit(1)

json_path = Path(sys.argv[1])

if not json_path.is_file():
	print(f"{json_path} is not a valid file")
	exit(1) 

# Read JSON file
(exp_name, n_x, n_y, x_min, x_max, y_min, y_max, h, m, w, k_x, k_y, 
 psi_type, psi_nb, psi_2DH0_nx, psi_2DH0_ny, x0, y0, V_id, image_V, method, t_max, dt) = js_uti.get_json(json_path)


# Initialize the potential grid
Vmat = np.zeros((n_x, n_y))

# Initialize the wave function grid
psi0Re = np.zeros((n_x, n_y))
psi0Im = np.zeros((n_x, n_y))

# Calculate the potential centered in (0, 0) at each point in the grid following this equation:
# V = (x² + y²) / 9 without i and j loop
def calcHarmV():
	"""
	@brief Calculate the potential for a harmonic oscillator
	@details The potential is calculated using the equation V = (x² + y²) / 9 as given in the lecture notes.

	@param None
	@return Vmat : The potential matrix
	"""
	x = np.linspace(x0-10, x0+10, n_x)
	y = np.linspace(y0-10, y0+10, n_y)
	X, Y = np.meshgrid(x, y)
	global Vmat
	Vmat = (X**2 + Y**2) / 9
	return Vmat

def calcVFromImage():
	"""
	@brief Calculate the potential from an image given in the consts.JSON file
	@details The potential is calculated using the image given in the consts.JSON file if the user chose the "Image method". The image is read and converted to a matrix.

	@param None
	@return img : The potential matrix
	"""

	img = mpimg.imread(image_V)

    # Vérifier si l'image est en niveaux de gris ou en couleur
	if img.ndim == 2:
    # Image en niveaux de gris
		gray = img
	else:
		# Image en couleur (RGB ou RGBA)
		if img.shape[2] == 4:
			# Exclure le canal alpha
			img_rgb = img[:, :, :3]
		else:
			img_rgb = img

    	# Convertir en niveaux de gris
		gray = np.dot(img_rgb, [0.2989, 0.5870, 0.1140])

	return gray

def plotV():
	"""
	@brief Plot the potential matrix
	@details The potential matrix is plotted using matplotlib. The color map is set to 'hot' and the axis are turned off. Should not be used in the final project.

	@param None, the matrix used is a global variable
	@return None
	"""
	global Vmat
	plt.imshow(Vmat, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.axis('off')
	plt.show()

def calcGaussPsi0():
	"""
	@brief Calculate the wave function for a gaussian wave packet
	@details The wave function is calculated using the equation psi(x, y) = A * exp(- (x² + y²) / (2 * w²)) * cos(k_x * x + k_y * y) + i * A * exp(- (x² + y²) / (2 * w²)) * sin(k_x * x + k_y * y)

	@param None
	@return psi0Re : The real part of the wave function
	@return psi0Im : The imaginary part of the wave function
	"""
	A = np.sqrt(2 / np.pi * (w**2))
	x = np.linspace(x0-10, x0+10, n_x)
	y = np.linspace(y0-10, y0+10, n_y)
	X, Y = np.meshgrid(x, y)
	psi0Re = A * np.exp(- (X**2 + Y**2) / (2 * w**2)) * np.cos(k_x * X + k_y * Y)
	psi0Im = A * np.exp(- (X**2 + Y**2) / (2 * w**2)) * np.sin(k_x * X + k_y * Y)
	return psi0Re, psi0Im

def calc2DHOPsi0():
	"""
	@brief Calculate the wave function for a 2D harmonic oscillator
	@details The wave function is calculated using the equation psi(x, y) = A * exp(- (x² + y²) / (2 * w²)) * H_n(x) * H_m(y) where H_n and H_m are the Hermite polynomials of order n and m.

	@param None
	@return psi0 : The wave function
	"""
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
	"""
	@brief Calculate the wave function for a combination of 2D harmonic oscillator
	@details The wave function is calculated using the equation psi(x, y) = A * exp(- (x² + y²) / (2 * w²)) * H_n(x) * H_m(y) where H_n and H_m are the Hermite polynomials of order n and m.

	@param None
	@return psi0 : The combination of multiple waves functions
	"""
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
	"""
	@brief Plot the wave function matrix
	@details The wave function matrix is plotted using matplotlib. The color map is set to 'hot' and the axis are turned off. Should not be used in the final project.

	@param None, the matrix used is a global variable
	@return None
	"""
	global psi0Re, psi0Im
	plt.subplot(1, 2, 1)
	plt.imshow(psi0Re, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.title('Partie réelle de psi0')
	plt.axis('on')

	plt.subplot(1, 2, 2)
	plt.imshow(psi0Im, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.title('Partie imaginaire de psi0')
	plt.axis('on')

	plt.show()

def calcV():
	"""
	@brief Calculate the potential according to the v value
	@details If v = "Image", use the image given in the consts.JSON file. If v = "Null", the potential is 0 everywhere. If v = "Harmonic", the potential for a harmonic oscillator.

	@param None
	@return Vmat : The potential matrix calculated by the appropriate function
	"""
	match V_id:
		case "Image":
			return calcVFromImage()
		case "Null":
			return Vmat
		case "Harmonic":
			return calcHarmV()
		case _:
			print("Not a valid value for v")
			exit

# Calculate the wave function according to the psi value :
# if psi = 0, use gaussian wave packet with initial speed
# if psi = 1, use a solution of the 2D-HO
# if psi = 2, use a combination of solution of the 2D-HO
def calcPsi():
	"""
	@brief Calculate the wave function according to the psi value
	@details If psi = 0, use gaussian wave packet with initial speed. If psi = 1, use a solution of the 2D-HO. If psi = 2, use a combination of solution of the 2D-HO.

	@param None
	@return psi0Re : The real part of the wave function
	@return psi0Im : The imaginary part of the wave function
	"""
	match psi_type:
		case 0:
			return calcGaussPsi0()
		case 1:
			return calc2DHOPsi0(), np.zeros((n_x, n_y))
		case 2:
			return calcMult2DHOPsi0(), np.zeros((n_x, n_y))
		
def dataCleaner(data):
	"""
	@brief Clean the data from the JSON file
	@details The data is cleaned by removing the name and t_max from the data. The name is not needed in the database and t_max is not needed for the hash.

	@param data : The data from the JSON file
	@return modified_data : the cleaned data
	"""
	modified_data = dict(data)
	modified_data.pop("name", None)
	
	param = modified_data.get("paramètres utilisateurs")
	if param and "t_max" in param:
		param.pop("t_max", None)
	
	return modified_data
		
def calcJSONHash():
	"""
	@brief Calculate the hash of the JSON file
	@details The hash is calculated using the SHA256 algorithm. The data is cleaned before the hash is calculated.

	@param None
	@return hash : The hash of the JSON file
	"""
	file = "../consts.JSON"
	with open(file, "r", encoding="utf-8") as f:
		data = json.load(f)
	
	data = dataCleaner(data)

	json_normalized = json.dumps(data, sort_keys=True, separators=(',', ':'))

	hash = hashlib.sha256(json_normalized.encode("utf-8"))

	return hash.hexdigest()


def main():
	global Vmat, psi0Re, psi0Im, exp_name, data, hash
	# Calculate the potential according to the V value :
	Vmat = calcV()
	#plotV()
	# Calculate the wave function according to the psi value :
	psi0Re, psi0Im = calcPsi()
	#plotPsi0()
	# Calculate the hash of the experiment
	hash = calcJSONHash()
	#print("Hash of the experiment: ", hash)

	# if the name already exists : inform the user that an expriment with the same name already exists
	val = True
	if db.AlreadyExist(exp_name):
		print("An experiment with the same name already exists.")
		if db.AlreadyExistHash(hash):
			print("An experiment with the same name and the same hash already exists.")
			print("Will use the results of this experiment to continue.")
			val = False
		while val:
			u_input = input("Do you want to overwrite it ? (y/N) : ")
			if u_input == "y":
				db.DeleteCollection(exp_name)
				val = False
			elif u_input == "N":
				exp_name = input("Please choose a new name for the experiment: ")
				val = False
			elif u_input == "exit":
				exit(1)
			else:
				print("Invalid input, please choose y or n")

	if not db.AlreadyExistHash(hash):
		file = "../consts.JSON"
		with open(file, "r", encoding="utf-8") as f:
			data = json.load(f)
		db.CreateExperience(exp_name, data, hash, Vmat)
		db.InsertMatrix(exp_name, 0, psi0Re, psi0Im)
		print("Experience initialized")

main()