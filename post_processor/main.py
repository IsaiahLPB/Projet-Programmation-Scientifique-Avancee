import numpy as np
import sys
import os
import json
import time
import vtk
from pyevtk.hl import imageToVTK

# Ajoute la racine du projet au path Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import database.databaseManager as db
import json_utils as js_uti

def create_vti_files(exp_name, state_list, nx, ny, output_dir="./output"):
    """Crée un fichier VTI pour chaque état temporel."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    dx, dy, dz = 1.0, 1.0, 1.0
    
    file_paths = []
    for idx, state in enumerate(state_list):
        t, psi_re, psi_im = state
        # Calcul de la densité de probabilité
        psi_squared = psi_re**2 + psi_im**2
        # Reshape pour avoir la bonne forme (nx, ny, 1)
        psi_squared = psi_squared.reshape((ny, nx, 1))
        
        # Nom du fichier avec l'index temporel
        filename = f"{output_dir}/wave_density_{idx:04d}"
        
        # Export en VTI
        imageToVTK(
            filename,
            origin=(0, 0, 0),
            spacing=(dx, dy, dz),
            pointData={"density": psi_squared}
        )
        
        file_paths.append(f"{filename}.vti")
        print(f"Fichier généré: {filename}.vti (t={t})")
    
    return file_paths

def main():
    # Vérification des arguments
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<path/to/json>")
        return 1
    
    json_path = sys.argv[1]
    print(f"Utilisation du fichier de configuration: {json_path}")
    
    try:
        # Récupération des paramètres depuis le fichier JSON
        exp_name, nx, ny, x_min, x_max, y_min, y_max, method, t_max, dt = js_uti.get_json(json_path)
        print(f"Nom de l'expérience: {exp_name}")
        print(f"Dimensions: {nx}x{ny}")
        
        # Récupération des états depuis la base de données
        state_list = db.GetStates(exp_name)
        if not state_list:
            print(f"Aucun état trouvé ou l'expérience '{exp_name}' n'existe pas.")
            return 1
        
        print(f"Nombre d'états temporels: {len(state_list)}")
        
        # Créer les fichiers VTI pour chaque état
        file_paths = create_vti_files(exp_name, state_list, nx, ny)
        
        return 0
        
    except FileNotFoundError as fnf:
        print(f"Erreur: Fichier non trouvé : {fnf}")
        return 1
    except json.JSONDecodeError:
        print(f"Erreur: Le fichier JSON '{json_path}' est mal formaté.")
        return 1
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())