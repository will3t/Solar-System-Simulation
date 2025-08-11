# William Thompson 38946378

# File for Creating the Euler Graphs
# This program is very similar to others so comments may appear again here.

# Importing the correct libraries
import numpy as np
import matplotlib.pyplot as plt 
from app_paths import data_path  # or user_data_dir if you prefer


def run():

    # Loading the Data
    DataIn2500= np.load(data_path("E_1Year_2500.npy"),allow_pickle=True)
    DataIn5000 = np.load(data_path("E_1Year_5000.npy"),allow_pickle=True)
    DataIn10000 = np.load(data_path("E_1Year_10000.npy"),allow_pickle=True)

    times = []# Set up time list

    # Appends all the times in the data to the data list.
    for itemRow in DataIn2500:
        times.append(itemRow[0])

    times = np.array(times)

    # Create a 2x2 grid of subplots for the graphs
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))


    #The following code checks each column in the list, and then each item on the row
    # From here it will append the x and y positions of all the bodies within the data set.
    for col in range(4,(DataIn2500.shape[1])-5):
        
        # Resets the xy positions for each object.
        x_positions = []
        y_positions = []

        for row in range(DataIn2500.shape[0]):
            # Provides each item in the data set, which is each object.
            item = DataIn2500[row,col]

            #Appending the data to axis dependant list 
            x_positions.append(item.position[0])
            y_positions.append(item.position[1])
            
        # Ensure arrays are numpy arrays for ease of handling.
        x_positions = np.array(x_positions) 
        y_positions = np.array(y_positions)

        # Plot the data for the item that is currently being iterated through (will do each stellar body). The [0,0] indicates plot position.
        ax[0,0].plot(x_positions,y_positions,label = f"{item.name}") # Can use the .name attribute of the object for the label!

    # Sets the title of the graph, the [0,0] indicates the plots position on the 2x2 plane.   
    ax[0, 0].set_title("2D Plot 1 Year Euler 2500(s) dT")

    # Adding the legend and positioning it in the top right.
    ax[0,0].legend(loc = "upper right")


    # This is the code for the Total Angular Momentum Graph

    # Initialise the lists for each of the time steps
    Ang_E_2500_list = []
    Ang_E_5000_list = []
    Ang_E_10000_list = []

    # Each iteration goes through each item in the row, and appends the Total Angular Momentum Value, to the corresponding list.
    for itemRow in DataIn2500:
        Ang_E_2500_list.append(itemRow[3])

    for itemRow in DataIn5000:
        Ang_E_5000_list.append(itemRow[3])

    for itemRow in DataIn10000:
        Ang_E_10000_list.append(itemRow[3])
        
    # Ensuring the arrays are numpy arrays for ease of handling.
    Ang_E_2500_list = np.array(Ang_E_2500_list)
    Ang_E_5000_list = np.array(Ang_E_5000_list)
    Ang_E_10000_list = np.array(Ang_E_10000_list)

    # Formatting the title and the graphs axis, the [0,1] indicates where on the 2x2 this plot will sit.
    ax[0,1].set(title="Total Angular Momentum Over 1 Year Euler", xlabel="Time (s)", ylabel="Total Angular Momentum (kg*kg*km/s^2)")

    # Plots all the data on separate lines, ensuring labels and colours are correct.
    ax[0,1].plot(times,Ang_E_2500_list,label = "2500(s) dT",color = "black")
    ax[0,1].plot(times,Ang_E_5000_list,label = "5000(s) dT",color = "blue")
    ax[0,1].plot(times,Ang_E_10000_list,label = "10000(s) dT",color = "red")

    # Adding the legend and positioning it in the top right.
    ax[0,1].legend(loc = "upper right")


    # Initialise the lists for each of the time steps
    Lin_E_2500_list = []
    Lin_E_5000_list = []
    Lin_E_10000_list = []

    # Each iteration goes through each item in the row, and appends the Total Linear Momentum Value, to the corresponding list.
    for itemRow in DataIn2500:
        Lin_E_2500_list.append(itemRow[2])

    for itemRow in DataIn5000:
        Lin_E_5000_list.append(itemRow[2])

    for itemRow in DataIn10000:
        Lin_E_10000_list.append(itemRow[2])


    # Ensuring the arrays are numpy arrays for ease of handling.
    Lin_E_2500_list = np.array(Lin_E_2500_list)
    Lin_E_5000_list= np.array(Lin_E_5000_list)
    Lin_E_10000_list= np.array(Lin_E_10000_list)

    # Formatting the title and the graphs axis, the [1,0] indicates where on the 2x2 this plot will sit.
    ax[1,0].set(title="Total Linear Momentum Over 1 Year Euler ", xlabel="Time (s)", ylabel="Total Linear Momentum (kg*km/s)")

    # Plots all the data on separate lines, ensuring labels and colours are correct.
    ax[1,0].plot(times,Lin_E_2500_list,label = "2500(s) dT ",color = "black")
    ax[1,0].plot(times,Lin_E_5000_list,label = "5000(s) dT",color = "blue")
    ax[1,0].plot(times,Lin_E_10000_list,label = "10000(s) dT",color = "red")

    # Adding the legend and positioning it in the top right.
    ax[1,0].legend(loc = "upper right")


    # This set of code is what produces the energy graph

    # Initialise the lists for each of the time steps
    En_E_2500_list = []
    En_E_5000_list = []
    En_E_10000_list = []

    # Each iteration goes through each item in the row, and appends the Total Energy Value to the corresponding list.

    for itemRow in DataIn2500:
        En_E_2500_list.append(itemRow[1])

    for itemRow in DataIn5000:
        En_E_5000_list.append(itemRow[1])

    for itemRow in DataIn10000:
        En_E_10000_list.append(itemRow[1])

    # Ensuring the arrays are numpy arrays for ease of handling.
    En_E_2500_list = np.array(En_E_2500_list)
    En_E_5000_list = np.array(En_E_5000_list)
    En_E_10000_list = np.array(En_E_10000_list)

    # Formatting the title and the graphs axis, the [1,1] indicates where on the 2x2 this plot will sit.
    ax[1,1].set(title="Total Energy Over 1 Year Euler ", xlabel="Time (s)", ylabel="Total Energy (10^6 J)") 

    # Plots all the data on separate lines, ensuring labels and colours are correct.
    ax[1,1].plot(times,En_E_2500_list,label = "2500(s) dT ",color = "black")
    ax[1,1].plot(times,En_E_5000_list,label = "5000(s) dT",color = "blue")
    ax[1,1].plot(times,En_E_10000_list,label = "10000(s) dT",color = "red")

    # Adding the legend and positioning it in the top right.
    ax[1,1].legend(loc = "upper right")

    # Allows the layout to sit nicer and more professional 
    plt.tight_layout()

    # Show the figure
    plt.show()


    # Print Statements for the user to visually see the numerics of the results
    print("\nHere is the data for you:")


    # These are just massive print statements that find the max value and min values and prints out the % differenet.
    # There are for sure better ways of doing this but this kept it simple and easy for me read and managed lol


    # For Energy

    # Ensuring the arrays are numpy arrays for ease of handling.
    max_yEn10 = np.amax(En_E_10000_list)
    min_yEn10 = np.amin(En_E_10000_list)
    max_yEn5 = np.amax(En_E_5000_list)
    min_yEn5 = np.amin(En_E_5000_list)
    max_yEn25 = np.amax(En_E_2500_list)
    min_yEn25 = np.amin(En_E_2500_list)


    print("\nTotal Energy:")
    print("For steps of 10,000 (s)")
    print(f"The maximum and min energy were as such, Max : {max_yEn10}  Min : {min_yEn10}")
    print(f"With a difference of {round((((max_yEn10-min_yEn10)/max_yEn10)*100),12)}%")
    print("For steps of 5,000 (s)")
    print(f"The maximum and min energy were as such, Max : {max_yEn5}  Min : {min_yEn5}")
    print(f"With a difference of {round((((max_yEn5-min_yEn5)/max_yEn5)*100),12)}%")
    print("For steps of 2,500 (s)")
    print(f"The maximum and min energy were as such, Max : {max_yEn25}  Min : {min_yEn25}")
    print(f"With a difference of {round((((max_yEn25-min_yEn25)/max_yEn25)*100),12)}%")

    # For Linear Momentum

    max_yLM10 = np.amax(Lin_E_10000_list)
    min_yLM10 = np.amin(Lin_E_10000_list)
    max_yLM5 = np.amax(Lin_E_5000_list)
    min_yLM5 = np.amin(Lin_E_5000_list)
    max_yLM25 = np.amax(Lin_E_2500_list)
    min_yLM25 = np.amin(Lin_E_2500_list)

    print("\n")
    print("Linear Momentum:")
    print("For steps of 10,000 (s)")
    print(f"The maximum and minimum Linear Momentums were as such, Max : {max_yLM10}  Min : {min_yLM10}")
    print(f"With a difference of {round((((max_yLM10-min_yLM10)/max_yLM10)*100),12)}%")
    print("For steps of 5,000 (s)")
    print(f"The minimum Linear Momentums were as such, Max : {max_yLM5}  Min : {min_yLM5}")
    print(f"With a difference of {round((((max_yLM5-min_yLM5)/max_yLM5)*100),12)}%")
    print("For steps of 2,500 (s)")
    print(f"The minimum Linear Momentums were as such, Max : {max_yLM5}  Min : {min_yLM25}")
    print(f"With a difference of {round((((max_yLM25-min_yLM25)/max_yLM25)*100),12)}%")
    print("\n")

    # For Angular Momentum

    max_yAM10 = np.amax(Ang_E_10000_list)
    min_yAM10 = np.amin(Ang_E_10000_list)
    max_yAM5 = np.amax(Ang_E_5000_list)
    min_yAM5 = np.amin(Ang_E_5000_list)
    max_yAM25 = np.amax(Ang_E_2500_list)
    min_yAM25 = np.amin(Ang_E_2500_list)

    print("Angular Momentum:")
    print("For steps of 10,000 (s)")
    print(f"The maximum and minimum Angular Momentums were as such, Max : {max_yAM10}  Min : {min_yAM10}")
    print(f"With a difference of {round((((max_yAM10-min_yAM10)/max_yAM10)*100),12)}%")
    print("For steps of 5,000 (s)")
    print(f"The minimum Angular Momentums were as such, Max : {max_yAM5}  Min : {min_yAM5}")
    print(f"With a difference of {round((((max_yAM5-min_yAM5)/max_yAM5)*100),12)}%")
    print("For steps of 2,500 (s)")
    print(f"The minimum Angular Momentums were as such, Max : {max_yAM5}  Min : {min_yAM25}")
    print(f"With a difference of {round((((max_yAM25-min_yAM25)/max_yAM25)*100),12)}%")


if __name__ == "__main__":
    run()