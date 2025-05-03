import solver
import numpy as np
from solver import TimeStepInfo
import sys
import os

# Ajoute la racine du projet au path Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import database.databaseManager as db 
import json_utils as js_uti

if (len(sys.argv) != 2):
	print("Usage;", sys.atgv[0], "<path/to/json>")
json_path = sys.argv[1]

# Read JSON file
exp_name, nx, ny, x_min, x_max, y_min, y_max, method, t_max, dt = js_uti.get_json(json_path)

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
#db.CreateExperience(exp_name, "json_path", V)

# Retrive data from de DB
#V = db.GetPotential(exp_name)
info = TimeStepInfo()
info.stepcounter = 0
info.t = 0.0
#info.t, psi_real, psi_imag = db.GetLastState(exp_name)

V = np.asfortranarray(V)
psi_real = np.asfortranarray(psi_real)
psi_imag = np.asfortranarray(psi_imag)

solver = solver.Solver(V, sys.argv[1])

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
			#db.InsertMatrix(exp_name, info.t, psi_real, psi_imag)
			#print("File", info.stepcounter, "written in the database")
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



