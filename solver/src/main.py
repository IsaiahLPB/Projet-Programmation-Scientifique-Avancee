import solver
import numpy as np
import math
import json
from solver import TimeStepInfo
import sys
import os

# Ajoute la racine du projet au path Python
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
#import database.databaseManager as db 

# Read JSON file
with open("../consts.JSON", "r") as f:
    data = json.load(f)

# Get constants 
constants = data["constantes"]
param = data["paramètres utilisateurs"]

exp_name = param["experience_name"]
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
X, Y = np.meshgrid(x_vec, y_vec)

m = 1.0
omega = 1.0
# Potentiel harmonique 2D
V = 0.5 * m * omega**2 * (X**2 + Y**2)

x0, y0 = -3.0, -3.0         # centre de la gaussienne
sigma = 1.0           # largeur
kx, ky = 0.0, 0.0     # impulsion (met 0 pour onde stationnaire)

# Amplitude gaussienne
A = 1.0 / (sigma * np.sqrt(2 * np.pi))

# Fonction d'onde complexe
gaussian_envelope = A * np.exp(-((X - x0)**2 + (Y - y0)**2) / (2 * sigma**2))
phase = np.exp(1j * (kx * X + ky * Y))
psi = gaussian_envelope * phase

# Partie réelle et imaginaire
psi_real = np.real(psi)
psi_imag = np.imag(psi)
psi_abs2 = np.abs(psi)**2

# TEMPORARY 
#db.CreateExperience(exp_name, "../consts.JSON", V)

# Retrive data from de DB
#V = db.GetPotential(exp_name)
info = TimeStepInfo()
info.stepcounter = 0
info.t = 0.0
#info.t, psi_real, psi_imag = db.GetLastState(exp_name)

V = np.asfortranarray(V)
psi_real = np.asfortranarray(psi_real)
psi_imag = np.asfortranarray(psi_imag)

solver = solver.Solver(V)

match method:
	case "FTCS":
		while info.t < t_max:
			solver.FTCS_derivation(psi_real, psi_imag, info)
			# Write the files in the DB
			re_filename = f"data/FTCS_psi_{info.stepcounter}_re.csv"
			im_filename = f"data/FTCS_psi_{info.stepcounter}_im.csv"
			np.savetxt(re_filename, psi_real, delimiter=',')
			np.savetxt(im_filename, psi_imag, delimiter=',')
			#db.InsertMatrix(exp_name, info.t, psi_real, psi_imag)
			#print("File", info.stepcounter, "written in the database")
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



