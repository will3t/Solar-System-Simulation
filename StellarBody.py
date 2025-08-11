
# This is the Class script for the Simulation. Contains the Stellar Body class along with the relevant methods.

# Importing the relevant libraries

from astropy.time import *
from astropy.coordinates import *
import numpy as np
import astropy.units as u

# Using astropy, save the time at a specific moment.

t = Time("2025-8-7 17:55:00.0", scale="tdb")
# ---------- You can put in your own time here if you'd like! ---------


#Dictionary Containing planets names and respective masses.
#This is here to check for a predetermined selection of bodies, however individual mass can be specified.

planet_mass = {
    "sun": 1.989e30,       # in kilograms
    "mercury": 3.3011e23,  # in kilograms
    "venus": 4.8675e24,    # in kilograms
    "earth": 5.97237e24,   # in kilograms
    "mars": 6.4171e23,     # in kilograms
    "jupiter": 1.8982e27,  # in kilograms
    "saturn": 5.6834e26,   # in kilograms
    "uranus": 8.6810e25,   # in kilograms
    "neptune": 1.02413e26  # in kilograms
}

class Stellar_Body: # The Stellar Body Class.

    _instances = [] # Initialises up list of all of the instances (objects) of this class.
    
    def __init__(self,name,mass,pos,vel): # Init method sets up each instance of the class.

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

        # Define all the objects values.

        self.mass = mass
        self.name = name.lower()
        self.velocity = np.array(vel,dtype=float)
        self.position = np.array(pos,dtype=float)
        
         # This is a process that checks to see if the name of the obejct is within the JPL Ephemeris and if so it uses the position and velocity from that.
         # If not it uses the data that the user provided.
        try:
            pos,vel = get_body_barycentric_posvel(self.name,t,ephemeris="jpl")
            self.velocity = np.array(vel.xyz.to(u.km / u.s)) # Ensures the units are in km/s (due to the scale this seemed appropriate)
            self.position = np.array(pos.xyz.to(u.km)) # Ensures the units are in km (also seemed approprite given the sheer scale)
        except Exception as x:
            print(f"\nThis body {self.name}, will not have its values taken from the JPL, will use provided values... ")

        # This checks to see if the object being created has its name within the premade dictionary to aid in providing mass.
        for i,j in planet_mass.items():
            if i == self.name:
                self.mass = j

        self.G = 6.67408E-20 # Gravitational Constant value made accessible by any body, very handy.
        self.acceleration = np.zeros(3)  # Default to zero acceleration to ensure no acceleration is carred.
        self.previous_acceleration = np.zeros(3) # This is to copy the acceleration during the verlet method. 
        Stellar_Body._instances.append(self) # Add the objects self to the _instances array
    
    def __str__(self): # The Method that formats how the data of the object is stored and can be printed.
       """
        A Method that outlines the format of the objec

        Parameters
        ----------
        self : The obejct itself.

        Returns
        ----------
        The string of the formatted data for storage or printing. 
       """
       return (
          f"Particle: {self.name}, Mass: {self.mass:.3e}, Position: {self.position}, Velocity: {self.velocity}, Acceleration: {self.acceleration}"
       )
    
    @classmethod
    def get_all_instances(className):
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
        self.position += self.velocity*deltaT # Updating the position using Euler's Formula's
        self.velocity += self.acceleration*deltaT # Updating the velocity using Euler's Formula's

    def updateEulerCr(self, deltaT): 
        """
        A Method that uses The Euler-Cromer Method to update the positions and velocity of a body.

        Parameters
        ----------
        self : The obejcts self.

        deltaT : Integer
            The value that will be used as the deltaT for the simulation.
        
        Returns
        ----------
        Objects position and velocity updated by using The Euler-Cromer Method
       """
        self.velocity += self.acceleration*deltaT # Updating the velocity using Euler-Cromer's Formula's
        self.position += self.velocity*deltaT # Updating the position using Euler-Cromer's Formula's

    def copy_accleration(self):
        self.previous_acceleration = self.acceleration.copy()

    def updateVerlet(self,deltaT):
        """
        A Method that uses Verlet's Method to update the positions and velocity of a body. 
        This uses the updateGravitationalAcceleration method within this class to contain the update loop.

        Parameters
        ----------
        self : The obejcts self.

        deltaT : Integer
            The value that will be used as the deltaT for the simulation.

        Returns
        ----------
        Objects position and velocity updated by using Verlet's Method
       """
        # Comments are explaining what each line effectively does in this section.

        prev_acceleration = self.acceleration.copy() # Takes a copy of the value of the accleration initally

        self.position += self.velocity * deltaT + 0.5 * self.acceleration * deltaT**2 # Updates the position using the current velocity and acceleration

        self.acceleration = np.zeros(3) # Sets the current acceleration back to zero to ensure to addtional values are included

        for i in Stellar_Body.get_all_instances(): # For each of the objects that have been made
            if i != self: # As long as the body isn't trying to calucalte with itself
                self.updateGravitationalAcceleration(i) # Calculate the new current value of acceleration due to gravity.

        self.velocity += 0.5 * (prev_acceleration + self.acceleration) * deltaT # Use the old and current accleration to update the velocity.

    def update_verlet_position(self, deltaT): # This Method updates the position of t
        self.position += (self.velocity*deltaT) + (0.5*self.acceleration*deltaT**2)

    def update_verlet_velocity(self, deltaT):
        self.velocity += (0.5*((self.previous_acceleration + self.acceleration))*deltaT)
        
    def updateGravitationalAcceleration(self,body):
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

        position1 = np.array(self.position) # Both ensured to be numpy arrays to aid in handling.
        position2 = np.array(body.position)
        mass1 = self.mass
        mass2 = body.mass

        mr = np.linalg.norm(position1-position2) # Magnitude of the difference between the vectors.

        if mr == 0 or mr < 1e-10: # If the two bodies are the same, check happens several times.
            return
        
        r = (position1-position2)/(mr) # Establishing formula values
        
        force = -1*(((self.G*(mass2)*(mass1))/(mr**2))*r) # Calculation of force


        self.acceleration += force / self.mass # Final return of updating the accleration using F = ma.

    @staticmethod
    def calcualte_total_energy(nBodys):

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
            total_KE += 0.5*planet.mass*vel_mag**2  # KE formula

        # Code below iterates through the list of gravotational bodies passed through
        for i,planet1 in enumerate(nBodys):
            for j,planet2 in enumerate(nBodys):
                if i != j: # If the two bodies are the same
                    dist_mag = np.linalg.norm(planet1.position - planet2.position) # Ensures scalar value
                    total_PE += ((-G * planet1.mass * planet2.mass)/dist_mag)/2 # Calculation of Potential Energy 
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
    
    @staticmethod
    def newAcceleration_calc():
        for body in Stellar_Body._instances:
            body.acceleration = np.zeros(3)

        for i, body1 in enumerate(Stellar_Body._instances):
            for j, body2 in enumerate(Stellar_Body._instances):
                if i != j:
                    body1.updateGravitationalAcceleration(body2)
