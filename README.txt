William Thompson 38946378

REQUIRED LIBRARIES:
    AstroPy.time
    AstroPy.units
    AstroPy.coordinates
    numPy
    os
    time
    copy
    matplotlib.pyplot
    app_paths
    pathlib

Main.py is the only script that needs to be run
	Type /help to get a list of functions once main.py is running.

EulerCromerGraphs, EulerGraphs,CompPOS and Verletgraphs all produces graphs



NOTES:
    SimplifiedSimulation is included here, but not referenced in main.py, here purely for evidence
    
    In order to add a body to the simulation, find Line 259 in the main.py script and add the body in the following format
    testBody = StellarBody("name",mass,[x,y,z],[v1,v2,v3])
    If this is done then the /comparison command will run but may crash as this specific command only compares against standard solar system.