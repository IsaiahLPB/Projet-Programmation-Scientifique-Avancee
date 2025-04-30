import solver
import numpy as np
import math
import json
from solver import Solver, TimeStepInfo

# Read JSON file
with open("../consts.JSON", "r") as f:
    data = json.load(f)

# Get constants 
constants = data["constantes"]
param = data["paramètres utilisateurs"]

nx,ny = constants["n_x"], constants["n_y"]
x_min, x_max, y_min, y_max = constants["x_min"], constants["x_max"], constants["y_min"], constants["y_max"]
method = param["method"]
t_max = param["t_max"]
dt = param["dt"]
if dt == "default":
	match method:
		case "FTCS":
			dt = 0.02/800
			method_id = 0
		case "BTCS":
			dt = 0.02/40
			method_id = 1
		case "CTCS":
			dt = 0.02/4
			method_id = 2
		case default:
			print("Error : This method is not implemented")
			exit(1)

# Definition of V (will be retrived in the DB)
x_vec = np.linspace(x_min, x_max, nx)
y_vec = np.linspace(y_min, y_max, ny)
V = np.zeros((nx,ny))
for i in range (0, nx):
	for j in range(0, ny):
		x = x_vec[i]
		y = y_vec[j]
		V[i,j] = (x*x + y*y)/9

# Definition of psi_0 (will be retrived in the DB)
psi_real = np.zeros((nx,ny))
psi_imag = np.zeros((nx,ny))
sigma = 2.0
for i in range (0, nx):
	for j in range(0, ny):
		x = x_vec[i]
		y = y_vec[j]
		
		gauss = math.exp(-(x * x + y * y) / (2 * sigma * sigma))
		theta = math.atan2(y, x) # Angle de phase

		psi_real[i, j] = gauss * math.cos(theta)
		psi_imag[i, j] = gauss * math.sin(theta)


V = np.asfortranarray(V)
psi_real = np.asfortranarray(psi_real)
psi_imag = np.asfortranarray(psi_imag)

solver = solver.Solver(V)
info = TimeStepInfo()
info.t = 0.0
info.stepcounter = 0

match method:
	case "FTCS":
		while info.t < t_max:
			solver.FTCS_derivation(psi_real, psi_imag, info)
			# Write the files in the DB 
			re_filename = f"data/FTCS_psi_{info.stepcounter}_re.csv"
			im_filename = f"data/FTCS_psi_{info.stepcounter}_im.csv"
			np.savetxt(re_filename, psi_real, delimiter=',')
			np.savetxt(im_filename, psi_imag, delimiter=',')
			print("File", info.stepcounter, "written")
		print("FTCS completed")
	case "BTCS":
		while info.t < t_max:
			solver.BTCS_derivation(psi_real, psi_imag, info)
			# Write the files in the DB 
			re_filename = f"data/BTCS_psi_{info.stepcounter}_re.csv"
			im_filename = f"data/BTCS_psi_{info.stepcounter}_im.csv"
			np.savetxt(re_filename, psi_real, delimiter=',')
			np.savetxt(im_filename, psi_imag, delimiter=',')
			print("File", info.stepcounter, "written")
		print("BTCS completed")
	case "CTCS":
		while info.t < t_max:
			solver.CTCS_derivation(psi_real, psi_imag, info)
			re_filename = f"data/CTCS_psi_{info.stepcounter}_re.csv"
			im_filename = f"data/CTCS_psi_{info.stepcounter}_im.csv"
			np.savetxt(re_filename, psi_real, delimiter=',')
			np.savetxt(im_filename, psi_imag, delimiter=',')
			print("File", info.stepcounter, "written")
		print("CTCS completed")
	case default:
		print("This method is not implemented")
		exit(1)



