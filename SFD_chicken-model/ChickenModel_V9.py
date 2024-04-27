import streamlit as st
import pysd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set the directory where your model is located
os.chdir("https://github.com/rssalazarr/Chickens-and-Eggs-model")

# Function to run the model
def run_model(normal_fertility_rate, normal_death_risk, max_chicken_capacity, initial_chicken_population, initial_eggs_population):
    model = pysd.read_vensim("https://github.com/rssalazarr/Chickens-and-Eggs-model/SFD chicken model V2.mdl")
    params = {
        'Normal fertility rate': normal_fertility_rate,
        'Normal death risk': normal_death_risk,
        'Max chicken capacity': max_chicken_capacity,
        'Initial chicken population': initial_chicken_population,
        'Initial number of eggs': initial_eggs_population
    }
    return_columns = ['Chickens', 'Eggs', 'Births', 'Deaths']
    return_timestamps = range(51)

    results = model.run(params=params, return_columns=return_columns, return_timestamps=return_timestamps)
    
    return results

# Streamlit UI
st.title("Chicken Model Simulation")

# Creating sliders
normal_fertility_rate = st.slider("Normal Fertility Rate", 0.0, 1.0, 0.2, 0.01)
normal_death_risk = st.slider("Normal Death Risk", 0.0, 1.0, 0.2, 0.01)
max_chicken_capacity = st.slider("Max Chicken Capacity", 0, 2000, 1000, 10)
initial_chicken_population = st.slider("Initial Chicken Population", 0, 4000, 1000, 10)
initial_eggs_population = st.slider("Initial Number of Eggs", 0, 2000, 1000, 10)

# Button to run the model
if st.button("Run Simulation"):
    results = run_model(normal_fertility_rate, normal_death_risk, max_chicken_capacity, initial_chicken_population, initial_eggs_population)

    # Displaying the results
    st.header("Simulation Results")
    
    fig, ax = plt.subplots()
    results['Chickens'].plot(ax=ax, figsize=(10, 5))
    results['Eggs'].plot(ax=ax, figsize=(10, 5))
    plt.xlabel('Time (Days)')
    plt.ylabel('Number of Chickens and Eggs')
    plt.legend(loc='upper left')
    st.pyplot(fig)

    fig, ax = plt.subplots()
    results['Births'].plot(ax=ax, figsize=(10, 5), color='green', label='Births')
    results['Deaths'].plot(ax=ax, figsize=(10, 5), color='red', label='Deaths')
    plt.xlabel('Time (Days)')
    plt.ylabel('Number of Chickens per Day')
    plt.legend(loc='upper left')
    st.pyplot(fig)

    # Displaying a part of the DataFrame as a table
    concatenated_results = pd.concat([results.head(6), results.tail(6)])
    st.write(concatenated_results)

# Resetting the sliders is not directly available in Streamlit, but you can simply refresh the page to reset values.
