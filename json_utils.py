import json
import sys
import os

def get_json(path):
	with open(path, "r") as f:
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
			case "BTCS":
				dt = 0.02/40
			case "CTCS":
				dt = 0.02/4
			case default:
				print("Error : This method is not implemented")
				exit(1)

	return exp_name, nx, ny, x_min, x_max, y_min, y_max, method, t_max, dt
