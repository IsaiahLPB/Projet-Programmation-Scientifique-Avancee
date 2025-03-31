import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import os
import glob
import re
import sys

def load_wavefunction_data(alg_id, iteration, base_dir='data/'):
    """
    Load real and imaginary parts of the wavefunction for a specific iteration
    """
    match(alg_id):
        case 0:
            real_file = os.path.join(base_dir, f'FTCS_psi_{iteration}_re.csv')
            imag_file = os.path.join(base_dir, f'FTCS_psi_{iteration}_im.csv')
        case 1:
            real_file = os.path.join(base_dir, f'BTCS_psi_{iteration}_re.csv')
            imag_file = os.path.join(base_dir, f'BTCS_psi_{iteration}_im.csv')
        case 2:
            real_file = os.path.join(base_dir, f'CTCS_psi_{iteration}_re.csv')
            imag_file = os.path.join(base_dir, f'CTCS_psi_{iteration}_im.csv')
    try:
        real_part = np.loadtxt(real_file, delimiter=',')
        imag_part = np.loadtxt(imag_file, delimiter=',')
        return real_part, imag_part
    except FileNotFoundError as e:
        print(f"Error loading iteration {iteration}: {e}")
        return None, None

def calculate_probability_density(real_part, imag_part):
    """
    Calculate the probability density |ψ|² = ψ*ψ = Re(ψ)² + Im(ψ)²
    """
    if real_part is None or imag_part is None:
        return None
    
    # |ψ|² = Re(ψ)² + Im(ψ)²
    probability_density = real_part**2 + imag_part**2
    return probability_density

def plot_probability_density_3d(probability_density, iteration, ax=None, colormap='viridis'):
    """
    Create a 3D surface plot of probability density
    """
    if probability_density is None:
        return
    
    # Create grid for x and y coordinates
    x = np.arange(0, probability_density.shape[1])
    y = np.arange(0, probability_density.shape[0])
    x_grid, y_grid = np.meshgrid(x, y)
    
    # Create plot
    if ax is None:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
    
    # Plot surface with updated colormap access method
    surf = ax.plot_surface(
        x_grid, y_grid, probability_density,
        cmap=plt.colormaps[colormap],  # Updated line
        linewidth=0,
        antialiased=True
    )
    
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Probability Density |ψ|²')
    ax.set_title(f'Probability Density at Iteration {iteration}')
    
    return ax

def get_available_iterations(alg_id, base_dir='data/'):
    """
    Find all available iterations in the data directory
    """
    match(alg_id):
        case 0:
            pattern = re.compile(r'FTCS_psi_(\d+)_re\.csv')
            iterations = []
            for filename in glob.glob(os.path.join(base_dir, 'FTCS_psi_*_re.csv')):
                match = pattern.search(filename)
                if match:
                    iterations.append(int(match.group(1)))
        case 1:
            pattern = re.compile(r'BTCS_psi_(\d+)_re\.csv')
            iterations = []
            for filename in glob.glob(os.path.join(base_dir, 'BTCS_psi_*_re.csv')):
                match = pattern.search(filename)
                if match:
                    iterations.append(int(match.group(1)))
        case 2:
            pattern = re.compile(r'CTCS_psi_(\d+)_re\.csv')
            iterations = []
            for filename in glob.glob(os.path.join(base_dir, 'CTCS_psi_*_re.csv')):
                match = pattern.search(filename)
                if match:
                    iterations.append(int(match.group(1)))

    return sorted(iterations)

def visualize_multiple_iterations(iterations=None, base_dir='data/', 
                                 layout=None, colormap='viridis'):
    """
    Visualize multiple iterations in a grid layout
    """
    # If iterations not specified, get all available
    if iterations is None:
        iterations = get_available_iterations(alg_id, base_dir)
    
    if not iterations:
        print("No iterations found!")
        return
    
    # Determine layout if not specified
    if layout is None:
        n_plots = len(iterations)
        cols = min(3, n_plots)  # Max 3 columns
        rows = (n_plots + cols - 1) // cols  # Ceiling division
        layout = (rows, cols)
    
    fig = plt.figure(figsize=(6*layout[1], 5*layout[0]))
    
    for i, iteration in enumerate(iterations):
        real_part, imag_part = load_wavefunction_data(alg_id, iteration, base_dir)
        probability_density = calculate_probability_density(real_part, imag_part)
        
        if probability_density is not None:
            ax = fig.add_subplot(layout[0], layout[1], i+1, projection='3d')
            plot_probability_density_3d(probability_density, iteration, ax, colormap)
    
    plt.tight_layout()
    plt.show()

def create_animation(iterations=None, base_dir='data/', 
                    filename='probability_density_animation.mp4', 
                    fps=5, colormap='viridis'):
    """
    Create an animation of probability density evolution over iterations
    Requires matplotlib.animation and ffmpeg
    """
    import matplotlib.animation as animation
    
    # If iterations not specified, get all available
    if iterations is None:
        iterations = get_available_iterations(alg_id, base_dir)
    
    if not iterations:
        print("No iterations found!")
        return
    
    # Load the first iteration to get dimensions
    real_part, imag_part = load_wavefunction_data(alg_id, iterations[0], base_dir)
    probability_density = calculate_probability_density(real_part, imag_part)
    
    if probability_density is None:
        print(f"Couldn't load data for iteration {iterations[0]}")
        return
    
    # Setup figure and 3D axis
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create grid for x and y coordinates
    x = np.arange(0, probability_density.shape[1])
    y = np.arange(0, probability_density.shape[0])
    x_grid, y_grid = np.meshgrid(x, y)
    
    # Initial surface plot with updated colormap access
    surf = ax.plot_surface(
        x_grid, y_grid, probability_density,
        cmap=plt.colormaps[colormap],  # Updated line
        linewidth=0,
        antialiased=True
    )
    
    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Probability Density |ψ|²')
    title = ax.set_title(f'Probability Density at Iteration {iterations[0]}')
    
    # Function to update the plot for each frame
    def update_plot(frame):
        ax.clear()
        iteration = iterations[frame]
        
        real_part, imag_part = load_wavefunction_data(alg_id, iteration, base_dir)
        probability_density = calculate_probability_density(real_part, imag_part)
        
        if probability_density is not None:
            surf = ax.plot_surface(
                x_grid, y_grid, probability_density,
                cmap=plt.colormaps[colormap],  # Updated line
                linewidth=0,
                antialiased=True
            )
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Probability Density |ψ|²')
            ax.set_title(f'Probability Density at Iteration {iteration}')
        
        return surf,
    
    # Create animation
    anim = animation.FuncAnimation(
        fig, update_plot, frames=len(iterations),
        interval=1000/fps, blit=False
    )
    
    # Save animation
    anim.save(filename, writer='ffmpeg', fps=fps)
    print(f"Animation saved as {filename}")
    
    plt.show()

# Example usage:
if __name__ == "__main__":

    if(len(sys.argv) != 2):
        print("Error: usage <int>")
        exit(1)

    alg_id = int(sys.argv[1])

    if(alg_id > 2):
        print("Error: <int> must be between 0 and 2")
        exit(2)

    # Get all available iterations
    iterations = get_available_iterations(alg_id)
    
    if not iterations:
        print("No data files found. Make sure your CSV files are in the 'data/' directory.")
        exit(1)
    
    print(f"Found {len(iterations)} iterations: {iterations[:5]}{'...' if len(iterations) > 5 else ''}")
    
    # Create a simple menu for the user
    print("\nQuantum Probability Density Visualization")
    print("----------------------------------------")
    print("1. Visualize single iteration (3D plot)")
    print("2. Visualize multiple iterations (grid of 3D plots)")
    print("3. Create animation (requires ffmpeg)")
    print("4. Exit")
    
    choice = input("\nSelect an option (1-4): ")
    
    if choice == '1':
        # Single iteration visualization
        if len(iterations) > 0:
            print(f"\nAvailable iterations: {min(iterations)} to {max(iterations)}")
            iter_num = input(f"Enter iteration number (default={iterations[0]}): ")
            if not iter_num:
                iter_num = iterations[0]
            else:
                iter_num = int(iter_num)
            
            colormap = input("Enter colormap name (default=viridis): ")
            if not colormap:
                colormap = "viridis"
            
            print(f"Visualizing iteration {iter_num}...")
            real_part, imag_part = load_wavefunction_data(alg_id, iter_num)
            probability_density = calculate_probability_density(real_part, imag_part)
            
            if probability_density is not None:
                fig = plt.figure(figsize=(10, 8))
                ax = fig.add_subplot(111, projection='3d')
                plot_probability_density_3d(probability_density, iter_num, ax, colormap)
                plt.show()
    
    elif choice == '2':
        # Multiple iterations visualization
        print("\nVisualize multiple iterations")
        
        # Get range of iterations to visualize
        start_iter = input(f"Start iteration (default={iterations[0]}): ")
        if not start_iter:
            start_iter = iterations[0]
        else:
            start_iter = int(start_iter)
        
        max_iter_default = min(iterations[-1], start_iter + 8)  # Default to showing up to 9 plots
        end_iter = input(f"End iteration (default={max_iter_default}): ")
        if not end_iter:
            end_iter = max_iter_default
        else:
            end_iter = int(end_iter)
        
        step = input("Step size (default=1): ")
        if not step:
            step = 1
        else:
            step = int(step)
        
        # Get subset of iterations within range
        selected_iterations = [i for i in iterations if start_iter <= i <= end_iter and (i - start_iter) % step == 0]
        if not selected_iterations:
            print("No iterations selected in that range!")
            exit(1)
        
        print(f"Selected {len(selected_iterations)} iterations")
        
        colormap = input("Enter colormap name (default=viridis): ")
        if not colormap:
            colormap = "viridis"
        
        visualize_multiple_iterations(iterations=selected_iterations, colormap=colormap)
    
    elif choice == '3':
        # Animation
        print("\nCreate animation")
        
        # Get range of iterations to include
        start_iter = input(f"Start iteration (default={iterations[0]}): ")
        if not start_iter:
            start_iter = iterations[0]
        else:
            start_iter = int(start_iter)
        
        end_iter = input(f"End iteration (default={iterations[-1]}): ")
        if not end_iter:
            end_iter = iterations[-1]
        else:
            end_iter = int(end_iter)
        
        step = input("Step size (default=1): ")
        if not step:
            step = 1
        else:
            step = int(step)
        
        # Get subset of iterations within range
        selected_iterations = [i for i in iterations if start_iter <= i <= end_iter and (i - start_iter) % step == 0]
        if not selected_iterations:
            print("No iterations selected in that range!")
            exit(1)
        
        print(f"Selected {len(selected_iterations)} iterations")
        
        fps = input("Frames per second (default=5): ")
        if not fps:
            fps = 5
        else:
            fps = int(fps)
        
        colormap = input("Enter colormap name (default=viridis): ")
        if not colormap:
            colormap = "viridis"
        
        filename = input("Output filename (default=probability_density_animation.mp4): ")
        if not filename:
            filename = "probability_density_animation.mp4"
        
        create_animation(iterations=selected_iterations, fps=fps, colormap=colormap, filename=filename)
        print(f"\nAnimation created as '{filename}'")
        print("You can view it with a media player like VLC, or with a command such as:")
        print(f"  xdg-open {filename}")
    
    elif choice == '4':
        print("Exiting...")
        exit(0)
    
    else:
        print("Invalid choice!")
