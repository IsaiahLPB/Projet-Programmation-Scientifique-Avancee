import solver
import numpy as np
import math
import sys

# Constants
nx, ny = 101, 101
x_min, x_max, y_min, y_max = -10, 10, -10, 10
dt_vals = [0.02/800, 0.02/40, 0.02/4]
t_max = 10
which_method = 0 # 0-FTCS, 1-BTCS, 2-CTCS

# Read JSON file

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


if(len(sys.argv) != 2):
	print("Error: usage <int>")
methode_id = int(sys.argv[1])
assert(methode_id <= 2)
assert(methode_id >= 0)

V = np.asfortranarray(V)
psi_real = np.asfortranarray(psi_real)
psi_imag = np.asfortranarray(psi_imag)

solver = solver.Solver(methode_id, V)
dt = dt_vals[methode_id]
t = 0
stepcounter = 0
match methode_id:
	case 0:
		while t < t_max:
			solver.FTCS_derivation(psi_real, psi_imag)
			if stepcounter % 10000 == 0:
			# Write the files in the DB 
				re_filename = f"data/FTCS_psi_{stepcounter}_re.csv"
				im_filename = f"data/FTCS_psi_{stepcounter}_im.csv"
				np.savetxt(re_filename, psi_real, delimiter=',')
				np.savetxt(im_filename, psi_imag, delimiter=',')
				print("File", stepcounter, "written")
			stepcounter +=1 
			t += dt
		print("FTCS completed")
	case 1:
		while t < t_max:
			solver.BTCS_derivation(psi_real, psi_imag)
			if stepcounter % 500 == 0:
			# Write the files in the DB 
				re_filename = f"data/BTCS_psi_{stepcounter}_re.csv"
				im_filename = f"data/BTCS_psi_{stepcounter}_im.csv"
				np.savetxt(re_filename, psi_real, delimiter=',')
				np.savetxt(im_filename, psi_imag, delimiter=',')
			stepcounter +=1 
			t += dt
		print("BTCS completed")
	case 2:
		while t < t_max:
			solver.CTCS_derivation(psi_real, psi_imag)
			if stepcounter % 50 == 0:
			# Write the files in the DB 
				re_filename = f"data/CTCS_psi_{stepcounter}_re.csv"
				im_filename = f"data/CTCS_psi_{stepcounter}_im.csv"
				np.savetxt(re_filename, psi_real, delimiter=',')
				np.savetxt(im_filename, psi_imag, delimiter=',')
			stepcounter +=1 
			t += dt
		print("CTCS completed")



