import numpy as np
import vtk
import sys
import os

# Ajoute la racine du projet au path Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import database.databaseManager as db 
import json_utils as js_uti
    
def main():
    # Vérification des arguments
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<path/to/json>")
        return 1
    
    try:
        # Récupération des paramètres depuis le fichier JSON
        exp_name, nx, ny, x_min, x_max, y_min, y_max, method, t_max, dt = js_uti.get_json(sys.argv[1])
        
        # Récupération des états depuis la base de données
        state_list = db.GetStates(exp_name)
        
		# Faire des trucs

        return 0
    except FileNotFoundError:
        print(f"Erreur: Le fichier JSON '{sys.argv[1]}' n'a pas été trouvé.")
        return 1
    except json.JSONDecodeError:
        print(f"Erreur: Le fichier JSON '{sys.argv[1]}' est mal formaté.")
        return 1
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
