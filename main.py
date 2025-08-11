
# Main Script that is the only program directly ran by the user. Here the main interface lies along with the code for the simulations themselves.

# To note: Though some comments are repeated this was due to the size of the program...
# I felt it best to repeat comments rather than have someone search to find them, also may be over commented but that never hurt anyone!


# Importing the needed libraries.

from StellarBody import *
import numpy as np
import os
import copy
import time
import EulerGraphs, EulerCromerGraphs, VerletGraphs,CompPOS
from pathlib import Path

from app_paths import user_data_dir, APP_NAME
DATA_DIR = user_data_dir(APP_NAME)


# All Funcitons and Subroutines kept at the top to ensure linearaity and ease of reading of the program.

def file_handling2(filesList):

	"""

	A function checking to see if the data files exist.

	Parameters
	----------
	x: List, Array
		A list of all the files that are required for the loop.
	
	Returns
	----------
	True/False: Boolean
		A True/False value for the loop to check.

    """

	existing_files = [file for file in filesList if os.path.exists(file)] # New list of files that exist.

	if len(existing_files) == len(filesList):  # Check to see if there are 3 files within the list, i.e All the required files exist.
		return True
	elif len(existing_files) != len(filesList): # If they don't, remove the files that do exist to ensure the correct and relevant data is stored. 
		for file in existing_files:
			os.remove(file)

	for file in filesList: # Opens and then closes the new files that are required, ensuring that all the correct files are present in the directory.
		with open(file,"w") as f:
			pass


def file_handling(filesList) -> bool:
	"""
	Return True iff all target files exist and are valid .npy files.
	If any are missing or invalid, delete partials and return False
	so the caller regenerates cleanly.
	"""
	paths = [Path(p) for p in filesList]

	# Ensure parent dirs exist
	for p in paths:
		p.parent.mkdir(parents=True, exist_ok=True)

	# Check validity by trying to load (fast fail)
	def is_valid(p: Path) -> bool:
		if not p.exists() or p.stat().st_size == 0:
			return False
		try:
			np.load(p, allow_pickle=True)
			return True
		except Exception:
			return False

	ok = [is_valid(p) for p in paths]
	if all(ok):
		return True

	# Clean up bad ones so the sim can recreate them fresh
	for p, good in zip(paths, ok):
		if p.exists() and not good:
			try:
				p.unlink()
			except Exception:
				pass

	return False



def sim_Euler(filename,timeIntervals,iterationSim):

	"""

	A Subroutine that runs the simulation for Euler's Method.

	Parameters
	----------
	filename: String
		The name of the file that the data is being stored to.
	timeIntervals: Integer
		The 'deltaT" that will be used for the calculations. This is the time step between each calcualtion.
	iterationSim: Integer
		This is the amount of iterations the simulation runs for. In essence "time of simulation / time steps".

	Returns
	----------
	No Return as this is a subroutine. Exists to execute code.

    """

	planetObjects = Stellar_Body.get_all_instances() # Collects all objects that have been created into a list.

	timeTotal = timeIntervals * iterationSim # The amount of time the simulation runs for.
	DataToSave = [] # Initialising an empty array for the rest of the data to save to. 

	time = 0 # Initialising the time for the loop.

	print("\nGenerating Data:")

	for i in range(0,iterationSim): # The main Simulation Loop.
		for j in planetObjects: # Checking each object....

			j.acceleration = np.zeros(3) # Ensures the acceleration isn't cumulative.

			# Loop to update the gravotational accleration of the system at once.

			for k in planetObjects:#.... against each other object in the simulation.
				if j != k:
					j.updateGravitationalAcceleration(k)

		# separate loop that then iterates through each object to find the Total Energy, Linear and Angular Momentum.
		for z in planetObjects: 

			z.updateEuler(timeIntervals) # Runs method that updates the positions of the planets.

			totalEnergySys = Stellar_Body.calcualte_total_energy(planetObjects) # Runs the static method to find total energy of the system.

			# Static method for Total Momentum ran to enable both Linear and Angular Momentum to be saved to the data file.

			totalLinMomSys = (Stellar_Body.Momentumn(planetObjects))[0] 

			totalAngMomSys = (Stellar_Body.Momentumn(planetObjects))[1]


		if ((i*timeIntervals) % 2000 == 0) or (i==0): # Samples taken at a respectable amount to maintain accurate resolution.

			# Data saved with all 'conserved' values at the begining of data, with all objects values following.
			DataToSave.append([time,totalEnergySys,totalLinMomSys,totalAngMomSys] + [copy.deepcopy(obj) for obj in planetObjects])
			
	
		time += timeIntervals # Increasing time for the simulation.

		print(f"\r{round(((time/timeTotal)*100),3)}%",end="") # Percentage of completion so that user knows how long is left of simulation.


	np.save(filename,DataToSave,allow_pickle=True) # Save the data.

def sim_EulerCromer(filename,timeIntervals,iterationSim):

	"""

	A Subroutine that runs the simulation for the Euler Comer Method.

	Parameters
	----------
	filename: String
		The name of the file that the data is being stored to.
	timeIntervals: Integer
		The 'deltaT" that will be used for the calculations. This is the time step between each calcualtion.
	iterationSim: Integer
		This is the amount of iterations the simulation runs for. In essence "time of simulation / time steps".

	Returns
	----------
	No Return as this is a subroutine. Exists to execute code.

    """

	planetObjects = Stellar_Body.get_all_instances() # Collects all objects that have been created into a list.

	timeTotal = timeIntervals * iterationSim # The amount of time the simulation runs for.
	DataToSave = [] # Initialising an empty array for the rest of the data to save to. 

	time = 0 # Initialising the time for the loop.

	print("\nGenerating Data:.")

	for i in range(0,iterationSim): # The main Simulation Loop.
		for j in planetObjects: # Checking each object....

			j.acceleration = np.zeros(3) # Ensures the acceleration isn't cumulative.

			# Loop to update the gravotational accleration of the system at once.

			for k in planetObjects:#.... against each other object in the simulation.
				if j != k:
					j.updateGravitationalAcceleration(k)

		# separate loop that then iterates through each object to find the Total Energy, Linear and Angular Momentum.
		for z in planetObjects:

			z.updateEulerCr(timeIntervals) # Runs method that updates the positions of the planets.

			totalEnergySys = Stellar_Body.calcualte_total_energy(planetObjects)  # Runs the static method to find total energy of the system.

			# Static method for Total Momentum ran to enable both Linear and Angular Momentum to be saved to the data file.

			totalLinMomSys = (Stellar_Body.Momentumn(planetObjects))[0]

			totalAngMomSys = (Stellar_Body.Momentumn(planetObjects))[1]


		if ((i*timeIntervals) % 2000 == 0) or (i==0): # Samples taken at a respectable amount to maintain accurate resolution.

			# Data saved with all 'conserved' values at the begining of data, with all objects values following.
			DataToSave.append([time,totalEnergySys,totalLinMomSys,totalAngMomSys] + [copy.deepcopy(obj) for obj in planetObjects])
			
	
		time += timeIntervals # Increasing time for the simulation.
		
		print(f"\r{round(((time/timeTotal)*100),3)}%",end="") # Percentage of completion so that user knows how long is left of simulation.

	np.save(filename,DataToSave,allow_pickle=True) # Save the data.

def sim_Verlet(filename, timeIntervals, iterationSim):

	"""
	A Subroutine that runs the simulation for Verlet's Method.
	This is the updated correct

	Parameters
	----------
	filename: String
		The name of the file that the data is being stored to.
	timeIntervals: Integer
		The 'deltaT' that will be used for the calculations. This is the time step between each calculation.
	iterationSim: Integer
		This is the amount of iterations the simulation runs for. In essence 'time of simulation / time steps'.

	Returns
	----------
	No Return as this is a subroutine. Exists to execute code.
	"""

	planetObjects = Stellar_Body.get_all_instances()  # Collects all objects into a list.
	timeTotal = timeIntervals * iterationSim          # Total simulation time.
	DataToSave = []                                   # Array for storing simulation data.
	time = 0                                          # Initialize time variable.

	print("\nGenerating Data:")


	for i in range(0,iterationSim):
		for body in planetObjects:
			body.copy_accleration()

			body.update_verlet_position(timeIntervals)

		for body in planetObjects:
			body.acceleration = np.zeros(3) # Ensures the acceleration isn't cumulative.
		
			for k in planetObjects:#.... against each other object in the simulation.
					if body != k:
						body.updateGravitationalAcceleration(k)
		
		for body in planetObjects:
			body.update_verlet_velocity(timeIntervals)
	
			totalEnergySys = Stellar_Body.calcualte_total_energy(planetObjects)  # Runs the static method to find total energy of the system.

			# Static method for Total Momentum ran to enable both Linear and Angular Momentum to be saved to the data file.

			totalLinMomSys = (Stellar_Body.Momentumn(planetObjects))[0]

			totalAngMomSys = (Stellar_Body.Momentumn(planetObjects))[1]
	

		if ((i*timeIntervals) % 2000 == 0) or (i==0): # Samples taken at a respectable amount to maintain accurate resolution.

				# Data saved with all 'conserved' values at the begining of data, with all objects values following.
				DataToSave.append([time,totalEnergySys,totalLinMomSys,totalAngMomSys] + [copy.deepcopy(obj) for obj in planetObjects])

		time += timeIntervals
		print(f"\r{round(((time/timeTotal)*100),3)}%",end="") # Percentage of completion so that user knows how long is left of simulation.

	# Save the simulation data to a file
	np.save(filename, DataToSave, allow_pickle=True)
	print("\nSimulation complete!")


if __name__ == "__main__":
	running = True # Condition for the main program to run, enables and exit and a run environment

planetObjects = [] # List for collecting all objects, helps enable N-Bodies to be added.

# This is where additional bodies can be added to the program. 
# Here I am setting up the main bodies I desired for the simulation... check .readme for additional information.

Sun = Stellar_Body("Sun",0,0,0)
Mercury = Stellar_Body("Mercury",0,0,0)
Venus = Stellar_Body("Venus",0,0,0)
Earth = Stellar_Body("Earth",0,0,0)
Moon = Stellar_Body("Moon",7.34767309e+22,0,0)
Mars = Stellar_Body("Mars",0,0,0)
Jupiter = Stellar_Body("Jupiter",0,0,0)
Saturn = Stellar_Body("Saturn",0,0,0)
Uranus = Stellar_Body("Uranus",0,0,0)
Neptune = Stellar_Body("Neptune",0,0,0)
# ----------------- SPACE IF YOU WANT TO ADD ANOTHER BODY -------------------


# Here is the dictionary of commands that can be run in my UI, makes it feel like a mini operating system terminal
# A dicitonary was very useful here as it allows me to keep relevant data together.

commands = {
	"/euler": "Performs Euler's Method and Provides graphs for analytics! The graphs will show some of the planets orbits together (not all as this looks more presentable!) along with total linear momentum, total angular momentum and total energy (to check conservation laws!)", 
	"/eulerCromer": "Performs Euler Cromer's Method and Provides graphs for analytics! The graphs will show some of the planets orbits together (not all as this looks more presentable!) along with total linear momentum, total angular momentum and total energy (to check conservation laws!)", 
	"/verlet": "Performs Verlet Method and Provides graphs for analytics! The graphs will show some of the planets orbits together (not all as this looks more presentable!) along with total linear momentum, total angular momentum and total energy (to check conservation laws!)",
	"/compare": "Compares all three methods against each other, ensure you have run all the simulations to get the comparison!",
	"/help": "The command to show all commands!",
	"/exit": "Exit out of the program"
	#"simplifiedSimulationAnimation" : "Shows a simplified simulation that is animated as a test!"
	
}

planetObjects = Stellar_Body.get_all_instances() # Runs the method to collect all bodies in the simulation.

while running == True: # Sets up a loop for the UI to run 

	# The following lines provide the main interface that allows the user to type into the UI and enter the commands listed previously.

	print("\nWelcome to my Simulation! Please type /help to get a list of commands!")

	userCommandChoice = input(">>> ")
	while userCommandChoice not in commands: # Prevents the user from typing anything and it crashing the software. They have to type a command.
		userCommandChoice = input(">>> ")
	
	if userCommandChoice == "/euler": # If the user selects to run the Euler Simulation.
	
		# For this simulation I set the three simulation data-holding files with the relevant names for the time-step that they are.

		#filename2500 = "E_1Year_2500.npy"
		#filename5000 = "E_1Year_5000.npy"
		#filename10000 = "E_1Year_10000.npy"

		from pathlib import Path
		filename2500 = DATA_DIR / "E_1Year_2500.npy"
		filename5000 = DATA_DIR / "E_1Year_5000.npy"
		filename10000 = DATA_DIR / "E_1Year_10000.npy"



		filesList = [filename2500,filename5000,filename10000] # A list for the file_handling function I wrote.

		if file_handling(filesList): # If the files are already there... this stops the user having to run the simulation each time they want the results.

			# This line is purely in becuase I think it looks cool... an animation for fun...
			for i in range(1,5):
				print(f"\rLoading Data{'.' * i}", end="") # The line that re-write a printed line rather than prints underneath
				time.sleep(0.5)

			EulerGraphs.run()
			#os.system("python EulerGraphs.py") # Runs the Euler Graphs Script to show the user the results.

		else:
			# This is where the Euler Simulations are called.
			# Three individaul calls that change the time step, but make sure that the 1-Year Period is maintained. 

			print("\nCreating the data.... this may take quite some time, grab a drink!\nYou're going to see three different simulations occur at three different time steps; 2500s, 5000s and 10000s respectively, then a window will pop up with the data!")
			planetObjects = Stellar_Body.get_all_instances() # Though I call to this afterwards... doesn't help to be safe tha all bodies are accounted for.
			
			# The three simulation calls with varying time-step.
			
			sim_Euler(filename2500,2500,12623)
			sim_Euler(filename5000,5000,6312)
			sim_Euler(filename10000,10000,3156)
			
			print("\n")
			for i in range(1,5):
				print(f"\rLoading Data{'.' * i}", end="") # The line that re-write a printed line rather than prints underneath
				time.sleep(0.5)

			EulerGraphs.run()
			#os.system("python EulerGraphs.py") # Runs the Euler Graphs Script to show the user the results.

	elif userCommandChoice == "/eulerCromer": # If the user selects to run the Euler Cromer Simulation.
		
		# For this simulation I set the three simulation data-holding files with the relevant names for the time-step that they are..

		#filename2500 = "EC_1Year_2500.npy"
		#filename5000 = "EC_1Year_5000.npy"
		#filename10000 = "EC_1Year_10000.npy"

		from pathlib import Path
		filename2500 = DATA_DIR / "EC_1Year_2500.npy"
		filename5000 = DATA_DIR / "EC_1Year_5000.npy"
		filename10000 = DATA_DIR / "EC_1Year_10000.npy"
		

		filesList = [filename2500,filename5000,filename10000] # A list for the file_handling function I wrote.
		
		
		if file_handling(filesList): # If the files are already there... this stops the user having to run the simulation each time they want the results.

			# This line is purely in becuase I think it looks cool... makes the UX feel more polished. An animation for fun..
			for i in range(1,5):
				print(f"\rLoading Data{'.' * i}", end="") # The line that re-write a printed line rather than prints underneath.
				time.sleep(0.5)

			#os.system("python EulerCromerGraphs.py") # Runs the Euler Graphs Script to show the user the results.
			EulerCromerGraphs.run()
		else:


			# This is where the Euler Simulations are called
			# Three individaul calls that change the time step, but make sure that the 1-Year Period is maintained. 

			print("\nCreating the data.... this may quite some time, grab a drink!\nYou're going to see three different simulations occur at three different time steps; 2500s, 5000s and 10000s respectively, then a window will pop up with the data!")
			planetObjects = Stellar_Body.get_all_instances() # Though I call to this afterwards... doesn't help to be safe tha all bodies are accounted for.

			# The three simulation calls with varying time-step.
			
			sim_EulerCromer(filename2500,2500,12623)
			sim_EulerCromer(filename5000,5000,6312)
			sim_EulerCromer(filename10000,10000,3156)

			print("\n")
			for i in range(1,5):
				print(f"\rLoading Data{'.' * i}", end="") # The line that re-write a printed line rather than prints underneath
				time.sleep(0.5)

			EulerCromerGraphs.run()
			#os.system("python EulerCromerGraphs.py") # Runs the Euler Graphs Script to show the user the results.

	elif userCommandChoice == "/verlet": # If the user selects to run the Verlet Simulation

		# For this simulation I set the three simulation data-holding files with the relevant names for the time-step that they are.

		#filename2500 = "V_1Year_2500.npy"
		#filename5000 = "V_1Year_5000.npy"
		#filename10000 = "V_1Year_10000.npy"

		from pathlib import Path
		filename2500 = DATA_DIR / "V_1Year_2500.npy"
		filename5000 = DATA_DIR / "V_1Year_5000.npy"
		filename10000 = DATA_DIR / "V_1Year_10000.npy"


		filesList = [filename2500,filename5000,filename10000] # A list for the file_handling function I wrote.
		
		if file_handling(filesList): # If the files are already there... this stops the user having to run the simulation each time they want the results.

			# This line is purely in becuase I think it looks cool... makes the UX feel more polished. An animation for fun...
			for i in range(1,5):
				print(f"\rLoading Data{'.' * i}", end="") # The line that re-write a printed line rather than prints underneath.
				time.sleep(0.5)

			VerletGraphs.run()
			#os.system("python VerletGraphs.py") # Running the python script that shows the graphs
		else:
			# This is where the Euler Simulations are called
			# Three individaul calls that change the time step, but make sure that the 1-Year Period is maintained. 
			
			print("\nCreating the data.... this may take some time, grab a drink!\nYou're going to see three different simulations occur at three different time steps; 2500s, 5000s and 10000s respectively, then a window will pop up with the data!")

			planetObjects = Stellar_Body.get_all_instances()
			
			# The three simulation calls with varying time-step.
			
			sim_Verlet(filename2500,2500,12623)
			sim_Verlet(filename5000,5000,6312)
			sim_Verlet(filename10000,10000,3156)


			print("\n")
			for i in range(1,5):
				print(f"\rLoading Data{'.' * i}", end="") # The line that re-write a printed line rather than prints underneath
				time.sleep(0.5)

			#os.system("python VerletGraphs.py")
			VerletGraphs.run()

	elif userCommandChoice == "/compare": # This command runs the Python script that shows the positional difference compared with the jpl ephemeris

		# It should be noted, as in the .readme file, this command can only work with the standrard set of objects given that they are standard solar system bodies
		# The rest of the program works as expected but this command cannot run if that is the case.
		
		# This list grabs all the data files and allows their names to be iterated through
		#filesList = ["E_1Year_2500.npy","E_1Year_5000.npy","E_1Year_10000.npy","EC_1Year_2500.npy","EC_1Year_5000.npy","EC_1Year_10000.npy","V_1Year_2500.npy","V_1Year_5000.npy","V_1Year_10000.npy"]
		files_names = [
		"E_1Year_2500.npy","E_1Year_5000.npy","E_1Year_10000.npy",
		"EC_1Year_2500.npy","EC_1Year_5000.npy","EC_1Year_10000.npy",
		"V_1Year_2500.npy","V_1Year_5000.npy","V_1Year_10000.npy",
		]
		filesList = [DATA_DIR / n for n in files_names]


		if file_handling(filesList):

			# This line is purely in becuase I think it looks cool... makes the UX feel more polished. An animation for fun...
			for i in range(1,5):
				print(f"\rLoading Data{'.' * i}", end="") # The line that re-write a printed line rather than prints underneath.
				time.sleep(0.5)

			#os.system("python CompPOS.py") # Runs the Python script that generates the three graphs for the user.
			CompPOS.run()
		else: # Doesn't allow the user to progress if they haven't got the relevant files.
			print("Please ensure that you have run all the relevant simulations first...")

	elif userCommandChoice == "/help": # Help section enables anyone to remember what commands are available along with providing a nice user experience (UX)

		print("\nHere is the set of commands avaialable:")

		# Printing out the items within the dictionary 
		for i,j in commands.items():
			print(f"\n{i} : {j}")


	elif userCommandChoice == "/exit": # This command exits the loop, its simplicity is appealing...
		running = False # Exits out of the main loop.

