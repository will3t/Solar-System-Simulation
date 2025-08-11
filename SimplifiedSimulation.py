# William Thompson 38946378

# This is a simplified version of the solar system simulation
# This is not referenced or opened within the main.py file
# Here as evidence


# Importing relevant libraries.
import numpy as np
import copy
import matplotlib.pyplot as plt

# Set up the basic class for a particle affected by gravitational forces.
class Planetary_Body:
    _instances = []

    def __init__(self, name, mass, pos, vel): 
        """

        A Method that runs when the object is created, or instantiated.

        Parameters
        ----------
        name: String
            The name of the object that can be referenced later on.
        mass: Float
            The name of the object that can be referenced later on. If one of the bodies in the dictionary planet_mass then this gets re-written.
        pos: Array
            This is a 3D array that contains the inital x,y and z positions of the object.
        vel: Array
            This is a 3D array that contains the inital x,y and z velocities of the object.

        Returns
        ----------
        No Return, it is the __init__ function.

        """

        # The code below is simply the set up for the object being instantiated
        self.name = name
        self.mass = mass
        self.position = np.array(pos,dtype=float)
        self.velocity = np.array(vel,dtype=float)
        self.G = 6.67408E-20
        self.acceleration = np.zeros(3,dtype=float)
        self._instances.append(self)

    def get_all_instances(className): # cls is just a class
        """
        A Class Method that returns all of the objects of that class.

        Parameters
        ----------
        className : Array
             A list of all the objects instantiated from this class.

        Returns
        ----------
        An array of all of the objects instantiated from this class.
       """
        return className._instances # Returns the list of added objects

    def updateEuler(self, deltaT):
        """
        A Method that uses Euler's Method to update the positions and velocity of a body.

        Parameters
        ----------
        self : The obejcts self.

        deltaT : Integer
            The value that will be used as the deltaT for the simulation.

        Returns
        ----------
        Objects position and velocity updated by using Euler's Method
       """
        self.position += self.velocity * deltaT # Updating the position using Euler's Formula's
        self.velocity += self.acceleration * deltaT  # Updating the velocity using Euler's Formula's

    def updateGravitationalAcceleration(self, body):
        """
        A Method that uses Newtons Equations of Force due to gravity between two objects to determine an objects acceleration due to this force.

        Parameters
        ----------
        self : The obejcts self.

        body : Object
            The other object of this class that is going to be used when calculating the gravitational acceleration due to gravity.

        Returns
        ----------
        0 if mr == 0, meaning the objects are the same
        Updates the objects acceleration
       """
        

        # Defining the two bodies positions and masses 

        position1 = self.position
        position2 = np.array(body.position)
        mass1 = self.mass
        mass2 = body.mass

        # Magnitude of the difference between the vectors.
        mr = np.linalg.norm(position1 - position2)

        if mr == 0 or mr < 1e-10:# If the two bodies are the same, return.
            return

        r = (position1 - position2) / mr # Establishing formula values

        force = -1 * (((self.G * (mass2 * mass1)) / (mr ** 2)) * r) # Calculation of force

        self.acceleration += force / self.mass # Final return of updating the accleration using F = ma.

    @staticmethod
    def calculate_total_energy(nBodys):
        """
        A Static Method that calcuates the total kinetic energy of the system at a given time.

        Parameters
        ----------
        nBodys : Array
            The list of objects that have been instantiated from this class. 

        Returns
        ----------
        Total Energy Value : Float
       """
        
        # Initialising the key variables used within this Static Method

        total_KE = 0
        total_PE = 0
        total_energy = 0
        G = 6.67408E-20 # This has to be defined again given the lack of 'self' being passed through.


        # Formula used for calucating the total Kinetic Energy at a single time/simulation iteration.
        for planet in nBodys:
            vel_mag = np.linalg.norm(planet.velocity) # Magnitude ensures scalar is gained.
            total_KE += 0.5 * planet.mass * vel_mag ** 2 # KE formula

        # Code below iterates through the list of gravotational bodies passed through
        for i, planet1 in enumerate(nBodys):
            for j, planet2 in enumerate(nBodys):
                if i != j: # If the two bodies are the same
                    dist_mag = np.linalg.norm(planet1.position - planet2.position) # Ensures scalar value
                    total_PE += ((-G * planet1.mass * planet2.mass) / dist_mag) / 2  # Calculation of Potential Energy 
                    # PE is divided by two to avoid double counting.

        total_energy += total_KE + total_PE # This is the law of conservation that this is constant. Thus we use it to check the effetiveness of the method.
        return total_energy

    @staticmethod
    def Momentumn(nBodys):
        """
        A Static Method that calcuates the total Linear and Angular momentum of the system and returns each value as a magnitude of the respected vector.

        Parameters
        ----------
        nBodys : Array
            The list of objects that have been instantiated from this class. 

        Returns
        ----------
        np.linalg.norm(total_Lin_Mom) : Float
        np.linalg.norm(total_Ang_Mom) : Float
       """
        # Ensures that there is no carry over and that the value is zero'd before the loops start.
        total_Lin_Mom = np.zeros(3)
        total_Ang_Mom = np.zeros(3)
    
        for planet in nBodys: # Iterate through each body
            # Assign Values of mass and velocity.
            mass = planet.mass
            velocity  = np.array(planet.velocity)

            total_Lin_Mom += mass * velocity # Calculation for Linear Momentum that is summed over all of the bodies

            total_Ang_Mom += np.cross(planet.position, mass*velocity) # Calculation for Angular Momentum that is summed over all of the bodies

            
        return np.linalg.norm(total_Lin_Mom), np.linalg.norm(total_Ang_Mom) # Returns the magnitude (to ensure single values) of two variables that can be indexed to be accessed if desired. 
 

# Setting up data that will be saved to file

dataToSave = []


# Creating objects of the Planetary Body, with Data from NASA
Earth = Planetary_Body("Earth",5.97237e24,[0,0,0],[0,0,0])
Moon = Planetary_Body("Moon", 0.07346e24, [384400, 0, 0], [0, 1.022, 0])

# Get all objects of the class...
planetaryObjects = Planetary_Body.get_all_instances(Planetary_Body)


# Set up 2 Moon Period Time with decent intervals to maintain accuracy
timeInterval = 200
iterationSim = 11803

# Setup Total Time running
timeTotal = timeInterval * iterationSim

time = 0


# Main loop for the simulation to take place.
for i in range(0, iterationSim):
    for j in planetaryObjects:
        j.acceleration = np.zeros(3) # Ensures no carry-over and the acceleration per object is correctly summed.
        
        for k in planetaryObjects: # Checking objects against objects.
            if j != k: # If they are the same don't proceed... another check.
                j.updateGravitationalAcceleration(k) # Running the method to get acceleration changes.

    for j in planetaryObjects:
        j.updateEuler(timeInterval) # Updating the postiion and velocity of the planet after calucalting the affect of gravity from all other planetary boides.
        #Here that is the other one of two
    
    # Running the three methods to calucalte the constant values.
    
    totalEnergySys = Planetary_Body.calculate_total_energy(planetaryObjects)

    totalLinMomSys = (Planetary_Body.Momentumn(planetaryObjects))[0]

    totalAngMomSys = (Planetary_Body.Momentumn(planetaryObjects))[1]

    # Loop for taking data, keeping a constant rate of data despite timeIntvervals or iterationSim is important for comparisons.
    if ((i*timeInterval) % 1000 == 0) or (i == 0):
        dataToSave.append([time,totalEnergySys,totalLinMomSys,totalAngMomSys]+[copy.deepcopy(obj) for obj in planetaryObjects]) # Data is now stored.


    time += timeInterval # Update Time


dataToSave = np.array(dataToSave)

# Set up 2x2 Plots for Grapherical Work.

fig, ax = plt.subplots(2,2, figsize =(10,8))


#Extracting the position data
for col in range(4,dataToSave.shape[1]): # Range dictated by line 236, 4 becuase it skips the first three irrelevent numbers for plotting orbits.
    x_pos = []
    y_pos = []

    for row in range(dataToSave.shape[0]):
        item = dataToSave[row,col]

        x_pos.append(item.position[0])
        y_pos.append(item.position[1])

    # Ensuring numpy is used for ease of work.
    x_pos = np.array(x_pos)
    y_pos = np.array(y_pos)

    ax[0,0].plot(x_pos,y_pos,label = f"{item.name}") # Plot each objects motion in the simulation.

# Set-ups to make it look nicer.

ax[0,0].legend(loc = "upper right")
ax[0, 0].set_title("2D Plot 2 Year Euler ")


#Total Energy Graph Setup.

EN_list = []   
for row in dataToSave: # Extracting all of the y-data for the total Energy over time.
    EN_list.append(row[1])
EN_list = np.array(EN_list)


#Total Linear Momentum Graph Setup.

LM_list = []   
for row in dataToSave:
    LM_list.append(row[2]) # Extracting all of the y-data for the total linear momentum over time.
LM_list = np.array(LM_list)

#Total Angular Momentum Setup.

AM_list = []   
for row in dataToSave:
    AM_list.append(row[3]) # Extracting all of the y-data for the total angular momentum over time.
AM_list = np.array(AM_list)


# Extracting the time out of the data so that it can be reused for several graphs easily.
time_list = []   
for row in dataToSave:
    time_list.append(row[0])
time_list = np.array(time_list)

# Plotting all Three of the Conservation graphs

ax[1,0].plot(time_list,EN_list,label = "Total Energy")
ax[0,1].plot(time_list,LM_list,label = "Total Linear Momentum")
ax[1,1].plot(time_list,AM_list,label = "Total Angular Momentum")

ax[1,0].legend(loc = "upper right")
ax[0,1].legend(loc = "upper right")
ax[1,1].legend(loc = "upper right")

ax[1, 0].set_title("Total Energy 2 Year Euler ")
ax[0, 1].set_title("Total Linear Momentum Year Euler ")
ax[1, 1].set_title("Total Angular Momentum Year Euler ")

# POINT OF INTEREST : [1,0],[0,1] etc, all show where the graph is going to go on the plot when the code runs.

# Show the plot.
plt.show()

# Grabbing Maximum and Minimum Values for all conserved values.

max_EN = np.amax(EN_list)
min_EN = np.amin(EN_list)
max_LM = np.amax(LM_list)
min_LM = np.amin(LM_list)
max_AM = np.amax(AM_list)
min_AM = np.amin(AM_list)


# Printing out their values and percentage differences to see if conservation was upheld.

print("\n")
print("For Total Energy (J)")
print(f"The maximum and minimum are as such, Max : {max_EN}  Min : {min_EN}")
print(f"With a difference of {round((((max_EN-min_EN)/max_EN)*100),12)}%")

print("For Total Linear Momentum (kg*km/s)")
print(f"The minimum Linear Momentums were as such, Max : {max_LM}  Min : {min_LM}")
print(f"With a difference of {round((((max_LM-min_LM)/max_LM)*100),12)}%")

print("For Total Angular Momentum (kg*kg*km/s^2)")
print(f"The minimum Linear Momentums were as such, Max : {max_AM}  Min : {min_AM}")
print(f"With a difference of {round((((max_AM-min_AM)/max_AM)*100),12)}%")