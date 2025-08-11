

# File for cross checking positional data from JPL and from the Simulations

# Import all of these libraries that are required.
import numpy as np
import matplotlib.pyplot as plt 
from astropy.coordinates import *
from astropy.time import *
import astropy.units as u
from app_paths import data_path  # or user_data_dir if you prefer

def run():
    
	#Initialsiing and loading all of these .npy files in order to access the data and have it well maintained. 
	E_DataIn2500= np.load(data_path("E_1Year_2500.npy"),allow_pickle=True)
	E_DataIn5000 = np.load(data_path("E_1Year_5000.npy"),allow_pickle=True)
	E_DataIn10000 = np.load(data_path("E_1Year_10000.npy"),allow_pickle=True)

	EC_DataIn2500= np.load(data_path("EC_1Year_2500.npy"),allow_pickle=True)
	EC_DataIn5000 = np.load(data_path("EC_1Year_5000.npy"),allow_pickle=True)
	EC_DataIn10000 = np.load(data_path("EC_1Year_10000.npy"),allow_pickle=True)

	V_DataIn2500= np.load(data_path("V_1Year_2500.npy"),allow_pickle=True)
	V_DataIn5000 = np.load(data_path("V_1Year_5000.npy"),allow_pickle=True)
	V_DataIn10000 = np.load(data_path("V_1Year_10000.npy"),allow_pickle=True)

	t = Time("2025-12-12 17:24:00",scale="tdb") # Setting the JPL time for a year ahead in order to calcualte percentage differences.

	fig, ax = plt.subplots(3,1, figsize =(8,12)) # Creating the 3x1 matrix that is containing all of the graphs.


	# These lines set up all of the nescecary arrays that contian the individual data

	names = []
	jpl_positions = []

	E10_position = []
	E5_position = []
	E25_position = []

	EC10_position = []
	EC5_position = []
	EC25_position = []

	V10_position = []
	V5_position = []
	V25_position = []



	# This iterates across all of the collumns  in the data set, ignroing teh first four and then continuing on as the first four aren't objects but the conserved values.
	for col in range(4,E_DataIn10000.shape[1]): # Hence the range from 4 and the use of .shape[] for the number of rows in the table

		Eitem10 = E_DataIn10000[-1,col] # This just grabs the last data entry in the data set so a name can be grabbed for each perosn.
		names.append(Eitem10.name)

		jpl_positions.append((get_body_barycentric_posvel(Eitem10.name,t,ephemeris="jpl")[0]).xyz.to(u.km).value)	# We use the name of the object to iterate through and find the last positions of the planets at the same time.
		
		# The following lines simply take the last data row of each of the data sets.

		Eitem10 = E_DataIn10000[-1,col]
		Eitem5 = E_DataIn5000[-1,col]
		Eitem25 = E_DataIn2500[-1,col]

		ECitem10 = EC_DataIn10000[-1,col]
		ECitem5 = EC_DataIn5000[-1,col]
		ECitem25 = EC_DataIn2500[-1,col]

		Vitem10 = V_DataIn10000[-1,col]
		Vitem5 = V_DataIn5000[-1,col]
		Vitem25 = V_DataIn2500[-1,col]

		# All below lines ensuring data sets are np.arrays and also take the position of the object the col is currently on
		# And then appends it to a list.
		
		E10_position.append((np.array(Eitem10.position)))
		E5_position.append((np.array(Eitem5.position)))
		E25_position.append((np.array(Eitem25.position)))

		EC10_position.append((np.array(ECitem10.position)))
		EC5_position.append((np.array(ECitem5.position)))
		EC25_position.append((np.array(ECitem25.position)))
		
		V10_position.append((np.array(Vitem10.position)))
		V5_position.append((np.array(Vitem5.position)))
		V25_position.append((np.array(Vitem25.position)))


	jpl_positions = np.array(jpl_positions) # Ensure the array is an numpy array for ease of handling.


	# The following functions that are identical, except for their names, and finds the percentage difference between the magnitude of the difference of the position vecotrs.

	diffP_E10 = [((np.linalg.norm(jpl_positions[i]-E10_position[i]))/(np.linalg.norm(jpl_positions[i])))*100
				for i in range(len(jpl_positions))]
	diffP_E5 = [((np.linalg.norm(jpl_positions[i]-E5_position[i]))/(np.linalg.norm(jpl_positions[i])))*100
				for i in range(len(jpl_positions))]
	diffP_E25 = [((np.linalg.norm(jpl_positions[i]-E25_position[i]))/(np.linalg.norm(jpl_positions[i])))*100
				for i in range(len(jpl_positions))]


	diffP_EC10 = [((np.linalg.norm(jpl_positions[i]-EC10_position[i]))/(np.linalg.norm(jpl_positions[i])))*100
				for i in range(len(jpl_positions))]
	diffP_EC5 = [((np.linalg.norm(jpl_positions[i]-EC5_position[i]))/(np.linalg.norm(jpl_positions[i])))*100
				for i in range(len(jpl_positions))]
	diffP_EC25 = [((np.linalg.norm(jpl_positions[i]-EC25_position[i]))/(np.linalg.norm(jpl_positions[i])))*100
				for i in range(len(jpl_positions))]


	diffP_V10 = [((np.linalg.norm(jpl_positions[i]-V10_position[i]))/(np.linalg.norm(jpl_positions[i])))*100
				for i in range(len(jpl_positions))]
	diffP_V5 = [((np.linalg.norm(jpl_positions[i]-V5_position[i]))/(np.linalg.norm(jpl_positions[i])))*100
				for i in range(len(jpl_positions))]
	diffP_V25 = [((np.linalg.norm(jpl_positions[i]-V25_position[i]))/(np.linalg.norm(jpl_positions[i])))*100
				for i in range(len(jpl_positions))]


	# We set a bar width for the bar
	bar_width = 0.25  # Width of each bar
	x = np.arange(len(names))  # Arranges the planets names evenly accross the access axis, when applied

	# The following code then arragnes the histogram with the bars either side of the arranged loactions to provide a better UI
	# And better data distribution so it is easier to see

	ax[0].bar(x - bar_width, diffP_E10, bar_width, label="DeltaT = 10000 (s)") 
	ax[0].bar(x, diffP_E5, bar_width, label="DeltaT = 5000 (s)")
	ax[0].bar(x + bar_width, diffP_E25, bar_width, label="DeltaT = 2500 (s)")
	ax[0].set_title("% Difference of Euler Final Positions of Planets per DeltaT")
	ax[0].set_xticks(x)
	ax[0].set_xticklabels(names)
	ax[0].legend(loc = "upper right")

	# Plot for Euler Cromer
	ax[2].bar(x - bar_width, diffP_EC10, bar_width, label="DeltaT = 10000 (s)")
	ax[2].bar(x, diffP_EC5, bar_width, label="DeltaT = 5000 (s)")
	ax[2].bar(x + bar_width, diffP_EC25, bar_width, label="DeltaT = 2500 (s)")
	ax[2].set_title("% Difference of Euler Cromer Final Positions of Planets per DeltaT")
	ax[2].set_xticks(x)
	ax[2].set_xticklabels(names)
	ax[2].legend(loc = "upper right")

	# Plot for Verlet
	ax[1].bar(x - bar_width, diffP_V10, bar_width, label="DeltaT = 10000 (s)")
	ax[1].bar(x, diffP_V5, bar_width, label="DeltaT = 5000 (s)")
	ax[1].bar(x + bar_width, diffP_V25, bar_width, label="DeltaT = 2500 (s)")
	ax[1].set_title("% Difference of Verlet Final Positions of Planets per DeltaT")
	ax[1].set_xticks(x)
	ax[1].set_xticklabels(names)
	ax[1].legend(loc = "upper right")

	# Enabkes the multiple plots to coexist and look presentable together in one single image.
	plt.tight_layout()

	plt.show() # Displays the figure.

	print("\nHere is the percentage difference for each object in each method: ")

	print("\n")
	# Print header
	print(f"{'Planet':<12} {'Euler (Δt=10000/5000/2500)':<40} {'Euler-Cromer (Δt=10000/5000/2500)':<40} {'Verlet (Δt=10000/5000/2500)':<40}")

	# Iterate through each planet and print the data for all methods
	for i, planet in enumerate(names): # This format :>10 enables the lines to be spaced out on one line so more data can be printed!
		print(f"{planet:<12} "
			f"{diffP_E10[i]:>10.2f}/{diffP_E5[i]:>10.2f}/{diffP_E25[i]:>10.2f} "  
			f"{diffP_EC10[i]:>10.2f}/{diffP_EC5[i]:>10.2f}/{diffP_EC25[i]:>10.2f} "
			f"{diffP_V10[i]:>10.2f}/{diffP_V5[i]:>10.2f}/{diffP_V25[i]:>10.2f}")
			# Those lines above allows the data to present so easily. 
				# This is only done here due to the small size of the data, other sets are too large for this.


	print("\nIt should be noted that these percentage differences are from where the jpl dataset predicted against my own; the values are signficant for some cases and that will be due to my simulation only containing part of the main bodies in our solar system that jpl considers and I do not! \n \nInteresting to see the difference.....")

if __name__ == "__main__":
    run()
