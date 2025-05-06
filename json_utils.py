import json

def get_json(path):
    with open(path, "r") as f:
        data = json.load(f)
        
    # Get experiment name
    exp_name = data["name"]
    
    # Get constants
    constants = data["constantes"]
    nx = constants["n_x"]
    ny = constants["n_y"]
    x_min = constants["x_min"] 
    x_max = constants["x_max"]
    y_min = constants["y_min"]
    y_max = constants["y_max"]
    h = constants["h"]
    m = constants["m"]
    w = constants["w"]
    k_x = constants["k_x"]
    k_y = constants["k_y"]
    
    # Get user parameters
    param = data["user parameters"]
    psi = param["psi"]
    psi_type = psi["type"]
    psi_nb = psi["nb"]
    psi_2DH0_nx = psi["2DH0_nx"]
    psi_2DH0_ny = psi["2DH0_ny"]
    psi_x0 = psi["x0"]
    psi_y0 = psi["y0"]
    
    V = param["V"]
    image_V = param["image_V"]
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
    
    return (exp_name, nx, ny, x_min, x_max, y_min, y_max, h, m, w, k_x, k_y, 
            psi_type, psi_nb, psi_2DH0_nx, psi_2DH0_ny, psi_x0, psi_y0, V, image_V, method, t_max, dt)