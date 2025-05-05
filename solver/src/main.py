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
	print("Usage;", sys.argv[0], "<path/to/json>")
	exit(1)
json_path = sys.argv[1]

# Read JSON file
(exp_name, nx, ny, x_min, x_max, y_min, y_max, h, m, w, kx, ky, 
 psi_type, psi_nb, psi_2DH0_nx, psi_2DH0_ny, V_id, image_V, method, t_max, dt) = js_uti.get_json(json_path)

# Retrive data from de DB
V = db.GetPotential(exp_name)
info = TimeStepInfo()
info.stepcounter = 0
info.t, psi_real, psi_imag = db.GetLastState(exp_name)
print(info.t)

# Converti les matrices Numpy pour quelles aient le même ordre de stockage que les matrices Armadillon en mémoire
V = np.asfortranarray(V)
psi_real = np.asfortranarray(psi_real)
psi_imag = np.asfortranarray(psi_imag)

solver = solver.Solver(V, json_path)

match method:
	case "FTCS":
		while info.t < t_max:
			# Call C++ function
			solver.FTCS_derivation(psi_real, psi_imag, info)

			# Write the files in the DB
			#re_filename = f"data/FTCS_psi_{info.stepcounter}_re.csv"
			#im_filename = f"data/FTCS_psi_{info.stepcounter}_im.csv"
			#np.savetxt(re_filename, psi_real, delimiter=',')
			#np.savetxt(im_filename, psi_imag, delimiter=',')
			#print("File", info.stepcounter, "written")
			db.InsertMatrix(exp_name, info.t, psi_real, psi_imag)
			print("File", info.stepcounter, "written in the database")

		print("FTCS completed")
	case "BTCS":
		while info.t < t_max:
			# Call C++ function
			solver.BTCS_derivation(psi_real, psi_imag, info)

			# Write the files in the DB 
			db.InsertMatrix(exp_name, info.t, psi_real, psi_imag)
			print("File", info.stepcounter, "written in the database")

		print("BTCS completed")
	case "CTCS":
		while info.t < t_max:
			# Call C++ function
			solver.CTCS_derivation(psi_real, psi_imag, info)

			# Write the files in the DB 
			db.InsertMatrix(exp_name, info.t, psi_real, psi_imag)
			print("File", info.stepcounter, "written in the database")

		print("CTCS completed")
	case default:
		print("This method is not implemented")
		exit(1)



