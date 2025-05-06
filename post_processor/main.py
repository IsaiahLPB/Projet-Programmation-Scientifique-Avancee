import numpy as np
import sys
import os
import json
from pyevtk.hl import gridToVTK
from pathlib import Path

# Adding root of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import database.databaseManager as db
import json_utils as js_uti

def create_vtr_files(exp_name, state_list, x_min, x_max, y_min, y_max, nx, ny, output_dir="./vtr_files"):
    """
	@brief Create a VTR file for each temporal state

	@param exp_name, the name of the experience
	@param state_list, a list of tuple containing the time and the matrixes for a state
	@param x_min
	@param x_max
	@param y_min
	@param y_max
	@param nx, number of points on the x axis
	@param ny, number of points on the y axis
	@param output_dir, the directory where the .vtr files are written
	@return None
	"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_paths = []
    
    for idx, state in enumerate(state_list):
        t, psi_re, psi_im = state
        
        # Probability density
        psi_squared = (psi_re**2 + psi_im**2).reshape((ny, nx, 1))
        
        # Name of the file 
        filename = f"{output_dir}/{exp_name}_{idx:04d}"
        
        # Export to VTR
        x = np.linspace(x_min, x_max, nx, dtype=np.float32)
        y = np.linspace(y_min, y_max, ny, dtype=np.float32)
        z = np.linspace(0.0, np.max(psi_squared), 1, dtype=np.float32)
        
        gridToVTK(
            filename,
            x, y, z,
            pointData={"density": psi_squared}
        )
        file_paths.append(f"{filename}.vtr")
        #print(f"File generated: {filename}.vtr (t={t})")
    
def main():
    # Check the number of arguments
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<path/to/json>")
        return 1
    
    json_path = Path(sys.argv[1])

    if not json_path.is_file():
        print(f"{json_path} is not a valid file")
    
    try:
        # Get parameters from the JSON file
        (exp_name, nx, ny, x_min, x_max, y_min, y_max, h, m, w, k_x, k_y,
         psi_type, psi_nb, psi_2DH0_nx, psi_2DH0_ny, x0, y0, V_id, image_V, method, t_max, dt) = js_uti.get_json(json_path)
        
        #print(f"Name of the experience: {exp_name}")
        #print(f"Dimensions: {nx}x{ny}")
        
        # Get the list of states from the database
        state_list = db.GetStates(exp_name)
        if not state_list:
            print(f"No state found or the experience '{exp_name}' doesn't exists")
            return 1
        
        # Create VTR files for each state
        create_vtr_files(exp_name, state_list, x_min, x_max, y_min, y_max, nx, ny)
        
        return 0
    
    except FileNotFoundError as fnf:
        print(f"Error: File not found : {fnf}")
        return 1
    except json.JSONDecodeError:
        print(f"Error: The JSON file '{json_path}' is not formatted correctly")
        return 1
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())