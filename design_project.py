import matplotlib.pyplot as plt
import numpy as np
import math


import user_csv as us


def invalid_input():
    """
    A function to print invalid input.
    """
    print("\n--Invalid input please try again--")


def avg_endangered_species(region_name, country_name):
    """
    Function that finds the average number of threatened species of each country in the sub-region and prints it
    out in a nice looking table. Also has the option to display a bar graph of the threatened species in each country.


    Parameters:
    - region_name (string): name of the sub region
    - country_name (string): name of the country


    """
    # Reads data from the species and country file and stores them as seperate a NumPy arrays and 2D lists
    species_data = us.read_csv("data_files/Threatened_Species.csv", False)
    species_array = np.array(species_data)
    country_data = us.read_csv("data_files/Country_Data.csv", False)
    country_array = np.array(country_data)


    # Finds which countries are in the sub region
    countries = np.where(country_array[:,2] == region_name) # Finds the indices of the countries that are in the sub region
    country_indices = countries[0].tolist() # Converts countries from a NumPy array to a list
    country_list = [country_data[country_indices[i]][0] for i in range(len(country_indices))] # Returns the names of the countries in a list


    # Finds data for the number of species in each country of the sub region
    data = [] # Creates an empty list
    for i in range(len(country_list)): # Loops through each country in the sub region
        index = int(np.where(species_array[:,0] == country_list[i])[0]) # Finds the index where the the species_array matches the current country
        data.append(species_data[index]) # Adds the found data as a row to the empty list
   
    num_columns = species_array.shape[1] # Finds the number of columns
   
    # Averages the number of species in each country of the sub region
    row_avgs = []
    for row in data:
        row_avg = sum(row[1:]) / (num_columns - 1) # Sums the first row excluding the country name and divides it by the number of species
        row_avgs.append(row_avg)
   
    # Calculates the overall average of the number of species for the sub region
    average_region = 0 # Initializes average_region
    iterator = 0 # Counter
    for i in range(len(row_avgs)): # Iterates through all the avgs
        average_region += float(row_avgs[i])
        iterator += 1
    average_region /= iterator


    # Final data for display
    data_final = []
    for i in range(len(country_list)):
        data_final.append([region_name] + [country_list[i]] + [row_avgs[i]])


    headers = ["UN Sub-region", "Country", ""] # Column headers
    # col_widths creates a list of widths for each column
    col_widths = [max(len(str(row[i])) for row in data_final + [headers]) for i in range(len(headers))]
    # "<" symbol ensures that the header is left-aligned, the width of each term is determined by col_widths[i]
    header_row = "   ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers))) # "   " is the gap between columns


    # Prints the table
    print(f"\nThe average number of threatened species in each country of the sub-region is: \n")
    print(header_row)
    print("-" * len(header_row)) # Line beneath the headers
    for row in data_final: # Formats and prints each row of data
        print("   ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(row))))


    # Prints the overall average of the sub region
    print(f"\nThe average number of threatened species in the sub-region {region_name} is: {average_region:0.2f}")
   
    # Asks the user if they want to display a graph
    user_input = input(f"\nWould you like to display a bar graph showing the threatened species in each country? (yes/no): ").lower()


    if user_input != "no" and user_input != "yes":
        invalid_input()
        avg_endangered_species(region_name, country_name) # Recursively calls the function
    elif user_input == "yes":
        # Extract individual species data for each country
        mammals = []
        for i in range(len(data)):
            mammals.append(data[i][1])
        birds = []
        for i in range(len(data)):
            birds.append(data[i][2])
        fish = []
        for i in range(len(data)):
            fish.append(data[i][3])
        plants = []
        for i in range(len(data)):
            plants.append(data[i][4])


        # Set up the figure
        plt.figure(figsize=[22,10])
        x_axis = np.arange(len(country_list)) # Creates an array of evenly spaced numbers to be used for the x_axis postions for the bars in the chart
        width = 0.2 # Sets the width of the bars in the chart
       
        # x_axis - 1.5 * width adjusts the x_axis positons of the bars by shifting them, width=width ensures that the width of the bars is 0.2
        plt.bar(x_axis - 1.5 * width, mammals, color ='maroon', width=width,  label = "Mammals")
        plt.bar(x_axis - 0.5 * width, birds, color ='red', width=width, label = "Birds")
        plt.bar(x_axis + 0.5 * width, fish, color ='blue', width=width, label = "Fish")
        plt.bar(x_axis + 1.5 * width, plants, color ='pink', width=width, label = "Plants")
       
        plt.title(f"Endangered Species in {region_name}", fontsize = 20, fontweight = "bold")
        plt.xlabel("Countries")
        plt.ylabel("Number of Species")
        plt.xticks(x_axis,country_list) # Will show the names of the countries instead of like 1, 2, 3 at positions specified by x_axis
        plt.legend()
        plt.savefig("final_plots/species_plot.png")
        plt.show()
       
   


def calculate_population_time(country_name, region_name): # for the country
    """
    Function that calculates the change in population from 2020 to 2000 in the selected country and the average population in said country.
    Also presents a graph to the user of population vs time for the given country if the user so wishes.


    Parameters
    - country_name (string): name of the country
    """
    # Reads data from the population file and stores them as a NumPy array and a 2D list
    population_data = us.read_csv("data_files/Population_Data.csv", True)
    array_data = np.array(population_data)
    country_data = us.read_csv("data_files/Country_Data.csv", False)
    array_country = np.array(country_data)
   
    # Finds the index in the first column where the country name matches the users input
    index = int(np.where(array_data[:,0] == country_name)[0])


    population_change = population_data[index][1] - population_data[index][21] # Calculates the change in population
    population_row = array_data[index, 1:].astype(float) # Extracts all population data of the country and stores it as a float array
    avg_population = np.mean(population_row) # Uses an NumPy function to find the mean of population_row
   
    print(f"\nThe change in population from 2020 to 2000 in {country_name} is: {round(population_change)} people")
    print(f"The average population in {country_name} from 2020 to 2000 is: {round(avg_population)} people")


    user_input = input(f"\nWould you like two graphs one of population vs time for {country_name} and"
                        "\nthe other for the 2020 population of each country in the sub-region? (yes/no): ").lower()
   
    if user_input != "no" and user_input != "yes":
        invalid_input()
        calculate_population_time(country_name, region_name)
    elif user_input == "yes":
        # Finding x-values for first subplot
        time_row = array_data[0,1:] # From the first row it extracts all the '2000 Pop' data
        time_row = np.char.replace(time_row, " Pop", "") # Replaces all ' Pop' in the row with an empty string
        time_row = time_row[::-1] # Reverses time_row
       
        # Finding x and y values for second subplot
        # Find which countries are in the region
        countries = np.where(array_country[:,2] == region_name)
        country_indices = countries[0].tolist()
        country_list = [country_data[country_indices[i]][0] for i in range(len(country_indices))] # x-values


        # Finds data for the 2020 population in each country of the sub region
        data = [] # Creates an empty list, will be y-values
        for i in range(len(country_list)): # Loops through each country in the sub region
            index = np.where(array_data[:,0] == country_list[i])[0][0] # Finds the index where the the array_data matches the current country
            data.append(array_data[index][1]) # Adds the found data as a row to the empty list,


        # Creating the plots
        plt.figure(figsize=[20,15])
        plt.subplot(2,1,1)
        plt.plot(time_row, population_row)
        plt.title(f"Population as a Function of Time for {country_name} throughout 2000 to 2020", fontsize = 14, fontweight = "bold")
        plt.xlabel("Time (year)", fontsize = 14)
        plt.ylabel("Population (people)", fontsize = 14)
       
        plt.subplot(2,1,2)
        x_axis = np.arange(len(country_list))
        plt.bar(x_axis, data)
        plt.xticks()
        plt.xticks(x_axis,country_list)
        plt.xlabel("Countries", fontsize = 14)
        plt.ylabel("Population (people)", fontsize = 14)
        plt.title(f"Population of Each Country in {region_name}", fontsize = 14, fontweight = "bold")


        plt.subplots_adjust(hspace = 0.5)
        plt.savefig("final_plots/population_plot.png")
        plt.show()
    # Here will be two subplots one of population vs time and the other 2020 population of each country in sub region


def calculate_population_density(year, country_name):
    """
    Function that calculates population density for the selected country based on the year the user selects.


    Parameters:
    - year (int): the year the user selected
    - country_name (string): name of the country
    """
    # Reads data from the population and country files and stores them as seperate a NumPy arrays and 2D lists
    population_data = us.read_csv("data_files/Population_Data.csv", True)
    array_population = np.array(population_data)
    country_data = us.read_csv("data_files/Country_Data.csv", False)
    array_country = np.array(country_data)


    string_year = str(year) + ' Pop' # Converts it to this string to be able to find the column
    index_year = int(np.where(array_population[0,:] == string_year)[0]) # Finds the index of the column that matches to the year


    index_population = int(np.where(array_population[:,0] == country_name)[0]) # Finds the index of the row that matches to the country
    total_population = population_data[index_population][index_year] # Finds the population data


    index_area = int(np.where(array_country[:,0] == country_name)[0]) # Finds the index of the area that matches to the country name
    land_area = country_data[index_area][3]


    density = float(total_population) / float(land_area)


    print(f"\nThe population density for the year {year} in {country_name} is: {density:0.2f} people per square kilometer")


    user_input = input("\nWould you like to save this data as a CSV file? (yes/no): ").lower()


    if user_input == "yes":
        new_file = input("\nEnter the name of the file (ex. Density_Data.csv): ").strip()
        new_data = [[str(country_name), int(year), round(density, 2)]]
        try:
            us.write_csv(new_file, new_data, overwrite=True)
            print(f"\nData saved to {new_file}")
        except Exception as e:
            print("\n---Error saving data---")


    elif user_input != "yes" and user_input != "no":
        invalid_input()
        calculate_population_density(year, country_name)


def calculate_min_max(user_input, region_name):
    """
    Function that finds which country has the least/most number of endangered species.


    Parameters:
    - user_input (string): is either "min" or "max"
    - region_name (string): name of the sub region
    """
    species_data = us.read_csv("data_files/Threatened_Species.csv", False)
    species_array = np.array(species_data)
    country_data = us.read_csv("data_files/Country_Data.csv", False)
    country_array = np.array(country_data)


    # Find which countries are in the region
    countries = np.where(country_array[:,2] == region_name)
    country_indices = countries[0].tolist()
    country_list = [country_data[country_indices[i]][0] for i in range(len(country_indices))]


    # Finds data for the number of species in each country of the sub region
    data = [] # Creates an empty list
    for i in range(len(country_list)): # Loops through each country in the sub region
        index = int(np.where(species_array[:,0] == country_list[i])[0]) # Finds the index where the the species_array matches the current country
        data.append(species_data[index]) # Adds the found data as a row to the empty list


    # Computes the total number of threatened species for each country
    row_sums = []
    for row in data:
        row_sum = sum(row[1:]) # Sums all the terms together except the first row
        row_sums.append(row_sum)
   
    # Final data for display
    data_final = []
    for i in range(len(country_list)):
        data_final.append([country_list[i]] + [row_sums[i]])


    data_final_array = np.array(data_final)


    values = data_final_array[:,1].astype(float) # Extracts the number of threatened species as a NumPy array of floats


    if user_input == "min":
        # Finds the index of the country with the minimum value
        min_index = np.argmin(values)
        country_min = data_final[min_index][0] # Retrieves the corresponding country name
        min_value = values[min_index] # Retrives the minimum value
        print(f"\nThe country {country_min} in the region {region_name} has the least number of total threatened species.")
   
    elif user_input == "max":
        # Finds the index of the country with the maximum value
        max_index = np.argmax(values)
        country_max = data_final[max_index][0]
        max_value = values[max_index]
        print(f"\nThe country {country_max} in the region {region_name} has the greatest number of total threatened species.")






def print_options():
    """
    Displays the menu options and returns the selected option.


    Returns:
    - option (int): the option the user selects
   
    """
    while True:
        try:
            option = int(input("\nPlease select an option: (or type 0 to restart)"
                    "\n\t1. Average number of threatened species"
                    "\n\t2. The change in population over time"
                    "\n\t3. Population density"
                    "\n\t4. Find which country in the selected region has the min/max number of threatened plants"
                    "\n>> "))
   
            if option in (0, 1, 2, 3, 4):
                return int(option)
            else:
                invalid_input()
        except ValueError:
            invalid_input()


def handle_options(option, region_name, country_name):
    """
    A function that handles the option that the user selects by calling other functions.


    Parameters:
    - option (int): the option the user selected
    - region_name (string): the name of the sub region
    - country_name (String): the name of the country
   
    """
    if option == 1:
        print(f"\nCalculating average number of threatened species in the {region_name} and in {country_name}...")
        avg_endangered_species(region_name, country_name)
   
    elif option == 2:
        print(f"\nAnalyzing population change over time for {country_name}...")
        calculate_population_time(country_name, region_name)
   
    elif option == 3:
        year = int(input("\nWhich year? (Input a year from 2000 to 2020): "))
        print(f"\nCalculating population density for the year {year} for {country_name}...")
        calculate_population_density(year, country_name)
   
    elif option == 4:
        user_input = input("\nMin or max? ").lower() # Accepts all mIn MIN and stores it as min
        if user_input != "max" and user_input != "min":
            invalid_input()
            handle_options(option, region_name, country_name)
        print(f"\nFinding the country with the {user_input} of threatened plants in {region_name}...")
        calculate_min_max(user_input, region_name)
   
    elif option not in (0,1,2,3,4):
        print_invalid_input()
        handle_options(option, region_name, country_name) # Calls the function again recursively


# User Interface


while True: # Program continues until the user ends it
    # Loads country data and converts it to a NumPy array
    country_data = us.read_csv("data_files/Country_Data.csv", False)
    array_country = np.array(country_data)
    region_name = (input("\nPlease enter a sub-region (or type 0 to quit): ")).title() # Capitalizes each first letter of the sub-region
    if region_name == "0":
        print("\nThank you for using our program!")
        break # Exits out of the program


    if not np.isin(region_name, array_country[:,2]): # Checks if it is a valid region
        invalid_input()
        continue # Restarts the loop


    while True:
        # Prompts the user for a country in the sub-region
        country_name = (input("\nPlease enter a country in the sub-region (or type 0 to go back): ")).capitalize()
       
        if country_name == "0":
            break
       
        # Finds the row for the entered country
        country_row = array_country[array_country[:, 0] == country_name]
        if country_row.size == 0: # Country not found
            invalid_input()
            continue # Restart inner loop


        elif country_row[0, 2] != region_name: # If the country is not in the given region
            print("\n--Country is not in region please try again--")
            continue
       
        # Display options to user
        option = print_options()
       
        if option == 0:
            break
       
        handle_options(option, region_name, country_name)
        break


       











