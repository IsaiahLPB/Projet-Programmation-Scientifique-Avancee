// Used only to test the functions while the field generator and access to the DB are not available
#include <iostream>
#include <armadillo>
#include <sstream>
#include <assert.h>
#include <cmath>
#include <stdio.h>

#include "../include/solver.h"
#include "../include/complexmat.h"

using namespace arma;

int main(int argc, char* argv[])
{
	if(argc != 2)
	{
		perror("Error: usage <int>\n");
		exit(1);
	}
	
	Solver solver;

	int i = 0;

	solver.V.zeros(nx, ny);

	complex_mat psi_0 = init_c_mat(nx, ny);
	complex_mat psi_t = init_c_mat(nx, ny);

  	std::cout << "SIZE of psi_0 : " << size(psi_0.re) << endl;
  	std::cout << "SIZE of psi_t : " << size(psi_t.re) << endl;

	std::ostringstream filename_re;
	std::ostringstream filename_im;

	arma::vec x_vec = arma::linspace(x_min, x_max, nx);
	arma::vec y_vec = arma::linspace(y_min, y_max, ny);

	// Initialization of the potential matrix
	for(uword i = 0; i < nx; ++i) {
		for(uword j = 0; j < nx; ++j) {
			double x = x_vec(i);
			double y = y_vec(j);
			// Double-well along x-axis (where your Gaussians are positioned)
			//solver.V(i,j) = 0.1 * ((x*x - 9.0)*(x*x - 9.0) + 2.0*y*y);
			solver.V(i,j) = (x*x + y*y)/9;
		}
	}

	// Initialization of psi
	double sigma = 2.0;
	double k = 1.5;  // Momentum magnitude
	double x1 = -3.0, y1 = 0.0;  // Position of first packet
	double x2 = 3.0, y2 = 0.0;   // Position of second packet

	for(uword i = 0; i < nx; ++i) {
		for(uword j = 0; j < nx; ++j) {
			double x = x_vec(i);
			double y = y_vec(j);
			
			// First wave packet moving right
			double gauss1 = exp(-((x-x1)*(x-x1) + (y-y1)*(y-y1)) / (2 * sigma * sigma));
			double phase1 = k * x;
			
			// Second wave packet moving left
			double gauss2 = exp(-((x-x2)*(x-x2) + (y-y2)*(y-y2)) / (2 * sigma * sigma));
			double phase2 = -k * x;
			
			// Superposition
			psi_0.re(i, j) = gauss1 * cos(phase1) + gauss2 * cos(phase2);
			psi_0.im(i, j) = gauss1 * sin(phase1) + gauss2 * sin(phase2);
		}
	}

	int alg_id = atoi(argv[1]);
	printf("Alg_id = %d\n", alg_id);
	assert(alg_id <= 2);
	assert(alg_id >= 0);
	double dt = solver.dt_vals[alg_id];
	psi_t = psi_0;
	switch (alg_id)
	{
	case 0:
		for(double t = 0; t < t_max; t+=dt)
		{
			psi_t = solver.FTCS_derivation(psi_t);
			if(i%10000 == 0)
			{
				filename_re.str("");
				filename_im.str("");
				filename_re << "data/FTCS_psi_" << i << "_re.csv";
				filename_im << "data/FTCS_psi_" << i << "_im.csv";
				psi_t.re.save(filename_re.str(), arma::csv_ascii);
				psi_t.im.save(filename_im.str(), arma::csv_ascii);
				//std::cout << "Saved files nb°" << i << endl; 
			}
			i++;
 		}
		std::cout << "FTCS completed" << endl;
		break;
	case 1:
		for(double t = 0; t < t_max; t+=dt)
		{
			psi_t = solver.BTCS_derivation(psi_t);
			if(i%500 == 0)
			{
				filename_re.str("");
				filename_im.str("");
				filename_re << "data/BTCS_psi_" << i << "_re.csv";
				filename_im << "data/BTCS_psi_" << i << "_im.csv";
				psi_t.re.save(filename_re.str(), arma::csv_ascii);
				psi_t.im.save(filename_im.str(), arma::csv_ascii);
				//std::cout << "Saved files nb°" << i << endl; 
			}
			i++;
 		}
		std::cout << "BTCS completed" << endl;
		break;
	case 2:
		for(double t = 0; t < t_max; t+=dt)
		{
			psi_t = solver.CTCS_derivation(psi_t);
			if(i%50 == 0)
			{
				filename_re.str("");
				filename_im.str("");
				filename_re << "data/CTCS_psi_" << i << "_re.csv";
				filename_im << "data/CTCS_psi_" << i << "_im.csv";
				psi_t.re.save(filename_re.str(), arma::csv_ascii);
				psi_t.im.save(filename_im.str(), arma::csv_ascii);
				std::cout << "Saved files nb°" << i << endl; 
			}
			i++;
 		}
		std::cout << "CTCS completed" << endl;
		break;
	default:
		std::cerr << "No such algorithm" << std::endl;
		exit(2);
		break;
	}
	return 0;
}
