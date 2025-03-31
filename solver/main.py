import solver
import numpy as np
import ComplexMat
import matplotlib.pyplot as plt

# Constants
nx = 101
ny = 101
dt_vals = [0.02/800, 0.02/40, 0.02/4]
t_max = 10
which_method = 0 # 0-FTCS, 1-BTCS, 2-CTCS

# Lire la BDD pour récupérer la matrice de champs de potentiels

# Créer la matrice 0
re = np.zeros(nx,ny)
im = np.zeros(nx,ny)
psi_0 = ComplexMat(re, im)

psi_list = [psi_0]

# Appeler la fonction du solver (boucle en python ou C ?)
solver = solver.Solver()

def main_loop(method_id):
	dt = dt_vals[method_id]
	t = 0
	psi_t = psi_0
	match which_method:
		case 0:
			while t < t_max:
				psi_t_dt = solver.FTCS_derivation(psi_t)
				psi_list.append(psi_t_dt)
				psi_t = psi_t_dt
				t += dt
		case 1:
			while t < t_max:
				psi_t_dt = solver.BTCS_derivation(psi_t)
				psi_list.append(psi_t_dt)
				psi_t = psi_t_dt
				t += dt
		case 2:
			while t < t_max:
				psi_t_dt = solver.CTCS_derivation(psi_t)
				psi_list.append(psi_t_dt)
				psi_t = psi_t_dt
				t += dt


match which_method:
	case 0:
		main_loop(0)
	case 1:
		main_loop(1)
	case 2:
		main_loop(2)





