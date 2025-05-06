import solver
import numpy as np
from solver import TimeStepInfo
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
(exp_name, nx, ny, x_min, x_max, y_min, y_max, h, m, w, kx, ky, 
 psi_type, psi_nb, psi_2DH0_nx, psi_2DH0_ny, x0, y0, V_id, image_V, method, t_max, dt) = js_uti.get_json(json_path)

# Retrive data from de DB
V = db.GetPotential(exp_name)
info = TimeStepInfo()
info.stepcounter = 0
info.t, psi_real, psi_imag = db.GetLastState(exp_name)

# Converts Numpy matrixes so that they have the same pattern in memory as Armadillo matrixes
psi_real = np.array(psi_real, dtype=np.float64, order="F")
psi_imag = np.array(psi_imag, dtype=np.float64, order="F")
V = np.array(V, dtype=np.float64, order="F")

solver = solver.Solver(V, json_path)

match method:
	case "FTCS":
		while info.t < t_max:
			# Call C++ function
			solver.FTCS_derivation(psi_real, psi_imag, info)

			norm = solver.getNorm(psi_real, psi_imag)
			print("Norm:", norm)
			if norm > 3.0:
				print("Too high norm, stopping simulation")
				break
			elif norm < 0.1:
				print("Too low norm, stopping simulation")
				break
			elif norm < 0:
				print("Negative norm, stopping simulation")
				break
			
			# Write the files in the DB
			db.InsertMatrix(exp_name, info.t, psi_real, psi_imag)
			#print("File", info.stepcounter, "written in the database")

		print("FTCS completed")
	case "BTCS":
		while info.t < t_max:
			# Call C++ function
			solver.BTCS_derivation(psi_real, psi_imag, info)

			# Write the files in the DB 
			db.InsertMatrix(exp_name, info.t, psi_real, psi_imag)
			#print("File", info.stepcounter, "written in the database")

		print("BTCS completed")
	case "CTCS":
		while info.t < t_max:
			# Call C++ function
			solver.CTCS_derivation(psi_real, psi_imag, info)

			# Write the files in the DB 
			db.InsertMatrix(exp_name, info.t, psi_real, psi_imag)
			#print("File", info.stepcounter, "written in the database")

		print("CTCS completed")
	case default:
		print("This method is not implemented")
		exit(1)