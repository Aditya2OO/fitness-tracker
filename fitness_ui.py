import streamlit as st
import pandas as pd
from datetime import datetime
import os

# User and Workout Classes
class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def to_dict(self):
        return {
            "Date": self.date,
            "Exercise Type": self.exercise_type,
            "Duration (min)": self.duration,
            "Calories Burned": self.calories_burned
        }

class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def get_workout_df(self):
        return pd.DataFrame([w.to_dict() for w in self.workouts])

    def save_data(self, filename):
        df = self.get_workout_df()
        df.to_csv(filename, index=False)

    def load_data(self, filename):
        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            workout = Workout(row['Date'], row['Exercise Type'], row['Duration (min)'], row['Calories Burned'])
            self.workouts.append(workout)

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None

# Streamlit UI
st.title("Personal Fitness Tracker")

# User Input Section
st.header("User Information")
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, step=1)
weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)

if st.button("Create User"):
    st.session_state.user = User(name, age, weight)
    st.success("User created successfully!")

# Workout Input Section
if st.session_state.user:
    st.header("Add Workout")
    exercise_type = st.text_input("Exercise Type")
    duration = st.number_input("Duration (minutes)", min_value=1, step=1)
    calories_burned = st.number_input("Calories Burned", min_value=1, step=1)

    if st.button("Add Workout"):
        workout = Workout(datetime.now().strftime("%Y-%m-%d"), exercise_type, duration, calories_burned)
        st.session_state.user.add_workout(workout)
        st.success("Workout added successfully!")

    # View Workouts
    if st.session_state.user.workouts:
        st.header("Workout History")
        df = st.session_state.user.get_workout_df()
        st.dataframe(df)

    # Save Data
    if st.button("Save Data"):
        filename = f"{st.session_state.user.name}_workouts.csv"
        st.session_state.user.save_data(filename)
        st.success(f"Data saved as {filename}")

    # Load Data
    uploaded_file = st.file_uploader("Load Previous Data", type=["csv"])
    if uploaded_file is not None:
        st.session_state.user.load_data(uploaded_file)
        st.success("Data loaded successfully!")
