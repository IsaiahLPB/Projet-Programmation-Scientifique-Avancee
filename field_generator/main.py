import numpy as np
import matplotlib.pyplot as plt

# Constants
n_x = 101
n_y = 101

h = 1
m = 1

kx = 0
ky = 2

w = 1


# Initialize the potential grid
V = [[0 for i in range(n_x)] for j in range(n_y)]

# Calculate the potential centered in (0, 0) at each point in the grid following this equation:
# V = (x² + y²) / 9
def calcV():
	x = np.linspace(-10, 10, n_x)
	y = np.linspace(-10, 10, n_y)
	for i in range(n_x//2+1):
		for j in range(n_y//2+1):
			V[i][j] = (x[i]**2 + y[j]**2) / 9 #optimisable
			V[i][n_y - j - 1] = V[i][j]
			V[n_x - i - 1][j] = V[i][j]
			V[n_x - i - 1][n_y - j - 1] = V[i][j]
	return V

def plotV():
	plt.imshow(V, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.axis('off')
	plt.show()

def calvpsi0real():
	A = np.sqrt(2 / np.pi * (w**2))
	x = np.linspace(-10, 10, n_x)
	y = np.linspace(-10, 10, n_y)
	psi0 = np.zeros((n_x, n_y))
	for i in range(n_x):
		for j in range(n_y):
			psi0[i][j] = A * np.exp(- (x[i]**2 + y[j]**2) / (2 * w**2)) * np.cos(kx * x[i] + ky * y[j])
	return psi0

def calvpsi0comp():
	A = np.sqrt(2 / np.pi * (w**2))
	x = np.linspace(-10, 10, n_x)
	y = np.linspace(-10, 10, n_y)
	psi0 = np.zeros((n_x, n_y))
	for i in range(n_x):
		for j in range(n_y):
			psi0[i][j] = A * np.exp(- (x[i]**2 + y[j]**2) / (2 * w**2)) * np.sin(kx * x[i] + ky * y[j])
	return psi0

def plotpsi0():
	psi0real = calvpsi0real()
	psi0comp = calvpsi0comp()
	
	plt.subplot(1, 2, 1)
	plt.imshow(psi0real, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.title('Partie réelle de psi0')
	plt.axis('off')

	plt.subplot(1, 2, 2)
	plt.imshow(psi0comp, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.title('Partie imaginaire de psi0')
	plt.axis('off')

	plt.show()

def calcG()

def main():
	V = calcV()
	plotV()
	plotpsi0()

main()