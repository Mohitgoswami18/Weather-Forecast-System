# Weather Forecast System... 

# Importing the necessary libraries.
import requests
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# Function for fetching the weather data from the API
def Fetch_Weather_data(city):
    url = "http://api.weatherstack.com/current"
    params = {
        "access_key": "a682de4feef3daaef445bec5899ae648",  # Replace with your API key
        "query": f"{city}"
    }
    response = requests.get(url=url, params=params)  # Generating the response
    data = response.json()  # Parsing the JSON response
    if "current" in data and "location" in data:  # Matching the required keywords
        return {  # Returning the weather details
            "City": data["location"]["name"],
            "Temperature": data["current"]["temperature"],
            "Humidity": data["current"]["humidity"],
            "Wind Speed": data["current"]["wind_speed"],
            "Country": data["location"]["country"]
        }
    return None

# Creating an empty weather DataFrame using pandas
Weather_df = pd.DataFrame(columns=['City', 'Country', 'Temperature', 'Humidity', 'Wind Speed'])

# Function for updating the DataFrame 
def Update_Weather_data(weather_details):
    global Weather_df
    Weather_df = pd.concat([Weather_df, pd.DataFrame([weather_details])], ignore_index=True)

# Function for displaying the weather data on the GUI window
def Display_weather_data():
    city = City_Entry.get()
    if city.strip() == "":
        status_label.config(text="Please enter a city name.", foreground="red")
        return

    weather_data = Fetch_Weather_data(city)  # Fetching the data from the Fetch_Weather_data function

    if weather_data:  # If the DataFrame is not empty, then access the following details
        city_name = weather_data["City"]
        temperature = weather_data["Temperature"]
        humidity = weather_data["Humidity"]
        wind_speed = weather_data["Wind Speed"]
        country = weather_data["Country"]

        # Display weather details in the GUI
        weather_label.config(
            text=f"City: {city_name}, {country}\n"
                 f"Temperature: {temperature}°C\n"
                 f"Humidity: {humidity}%\n"
                 f"Wind Speed: {wind_speed} m/s"
        )
        # Update DataFrame
        Update_Weather_data(weather_data)
        status_label.config(text="Weather data updated successfully.", foreground="green")
    else:
        status_label.config(text="Failed to fetch weather data. Try again.", foreground="red")

# Function to display the weather statistics using NumPy
def Display_Weather_Statistics():
    if Weather_df.empty:
        Show_statistics_label.config(text="There is no information to show.")
    else:
        temperature = Weather_df['Temperature'].to_numpy()  # Converting the Temperature column of the DataFrame into NumPy array
        max_temp = np.max(temperature)  # Calculating maximum temperature
        min_temp = np.min(temperature)  # Calculating minimum temperature
        mean_temp = np.mean(temperature)  # Calculating average temperature

        # Updating the weather statistics on the GUI window
        Show_statistics_label.config(
            text=f"Average Temperature: {mean_temp:.2f}°C\n"
                 f"Maximum Temperature: {max_temp:.2f}°C\n"
                 f"Minimum Temperature: {min_temp:.2f}°C"
        )

# Function for creating a scatter plot graph
def PLot_Weather_Graph():
    if Weather_df.empty:
        plt.title("No data to plot.")
        plt.show()
        return

    x_axis = Weather_df['City']
    y_axis = Weather_df['Temperature']

    plt.plot(x_axis, y_axis, label='City_vs_temperature')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.title('City vs Temperature')
    plt.legend()
    plt.show()

# Creating the GUI window
root = tk.Tk()
root.title('Weather Forecast')
root.geometry("400x400")  # Adjusted size for better layout

# Creating the main label
Greet_Label = tk.Label(root, text="Welcome to the Weather Forecast Application", font=("Helvetica", 14))
Greet_Label.grid(row=0, column=0, columnspan=2, pady=10)

# Label and entry for city input
City_Label = tk.Label(root, text='Enter the City', font=("Helvetica", 12))
City_Label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

City_Entry = tk.Entry(root, width=30)
City_Entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Button to display weather data
city_button = tk.Button(root, text='Display', command=Display_weather_data, bg="blue", fg="white")
city_button.grid(row=2, column=0, columnspan=2, pady=10)

# Label to show fetched weather data
weather_label = ttk.Label(root, text="", font=("Arial", 12))
weather_label.grid(row=3, column=0, columnspan=2, pady=10)

# Label and button to show weather statistics
Show_statistics_label = tk.Label(root, text='', font=("Helvetica", 12))
Show_statistics_label.grid(row=4, column=0, columnspan=2, pady=10)

Statistics_button = tk.Button(root, text='Show Stats', command=Display_Weather_Statistics, bg="green", fg="white")
Statistics_button.grid(row=5, column=0, columnspan=2, pady=10)

# Label and button to show weather graph
Show_Graph_label = tk.Label(root, text="Show Graph", font=("Helvetica", 12))
Show_Graph_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")

Graph_button = tk.Button(root, text='Show', command=PLot_Weather_Graph, bg="purple", fg="white")
Graph_button.grid(row=6, column=1, padx=10, pady=5, sticky="w")

# Status label for messages
status_label = tk.Label(root, text='', font=("Helvetica", 10))
status_label.grid(row=7, column=0, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()
