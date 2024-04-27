#!/usr/bin/env python
# coding: utf-8

# <div style="font-family: 'Arial', sans-serif; margin: 0px; padding: 30px; background-color: #FFF3CD; border-left: 5px solid #FFECB3; border-radius: 50px;">
#     <h2 style="color: #856404; font-size: 24px; margin-top: 0;">🐔 Chickens and Eggs: A System Dynamics Model 🥚</h2>
#     <p style="color: #6c757d; font-size: 16px;">
#         Welcome to the interactive <strong>Chickens and Eggs</strong> model! This tool was designed by Robinson Salazar Rua and Peter Hovmand to help you understand the fascinating dynamics of a chicken population.
#     </p>
#     <p style="color: #6c757d; font-size: 16px;">
#         In this model, you'll explore how different factors (such as fertility rate, death risk, and capacity level) affect the population of chickens in our virtual farm.
#     </p>
#     <h3 style="color: #856404; font-size: 18px;"> Your Tasks:</h3>
#     <ul style="color: #6c757d; font-size: 16px;">
#         <li><strong>Adjust the Parameters:</strong> Use the sliders to change the model initial conditions.</li>
#         <li><strong>Observe the Changes:</strong> Watch how these adjustments impact the chicken population over time.</li>
#         <li><strong>Discover the Dynamics:</strong> Notice the feedback loops and delays that characterize this system.</li>
#     </ul>
#     <p style="color: #6c757d; font-size: 16px;">
#         By playing with these parameters, you'll gain insights into the principles of system dynamics and understand how even simple systems can exhibit complex behaviors. Enjoy your journey into the world of chickens and eggs!
#     </p>
# </div>
# 

# In[4]:


import streamlit as st
import pysd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# In[5]:


os.chdir("C:/Users/rss188/Desktop/Chicken model/SFD chicken model")


# In[6]:


# Function to run the model
def run_model(normal_fertility_rate, normal_death_risk, max_chicken_capacity, initial_chicken_population, initial_eggs_population):
    model = pysd.read_vensim("C:/Users/rss188/Desktop/Chicken model/SFD chicken model/SFD chicken model V2.mdl")
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


# In[7]:


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

