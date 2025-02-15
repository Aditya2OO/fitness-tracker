import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from datetime import datetime
from tkinter import ttk

class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date}: {self.exercise_type} for {self.duration} minutes, {self.calories_burned} calories burned"

class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def view_workouts(self):
        return "\n".join(str(workout) for workout in self.workouts)

    def save_data(self, filename):
        with open(filename, 'w') as file:
            for workout in self.workouts:
                file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")

    def load_data(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                date, exercise_type, duration, calories_burned = line.strip().split(',')
                workout = Workout(date, exercise_type, int(duration), int(calories_burned))
                self.workouts.append(workout)

class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Fitness Tracker")

        self.user = None

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 14))
        style.configure("TButton", font=("Helvetica", 14))

        self.name_label = ttk.Label(self.root, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.name_entry = ttk.Entry(self.root, font=("Helvetica", 14))
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.age_label = ttk.Label(self.root, text="Age:")
        self.age_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.age_entry = ttk.Entry(self.root, font=("Helvetica", 14))
        self.age_entry.grid(row=1, column=1, padx=10, pady=10)

        self.weight_label = ttk.Label(self.root, text="Weight:")
        self.weight_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.weight_entry = ttk.Entry(self.root, font=("Helvetica", 14))
        self.weight_entry.grid(row=2, column=1, padx=10, pady=10)

        self.create_user_button = ttk.Button(self.root, text="Create User", command=self.create_user)
        self.create_user_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.add_workout_button = ttk.Button(self.root, text="Add Workout", command=self.add_workout, state=tk.DISABLED)
        self.add_workout_button.grid(row=4, column=0, padx=10, pady=10)

        self.view_workouts_button = ttk.Button(self.root, text="View Workouts", command=self.view_workouts, state=tk.DISABLED)
        self.view_workouts_button.grid(row=4, column=1, padx=10, pady=10)

        self.save_data_button = ttk.Button(self.root, text="Save Data", command=self.save_data, state=tk.DISABLED)
        self.save_data_button.grid(row=5, column=0, padx=10, pady=10)

        self.load_data_button = ttk.Button(self.root, text="Load Data", command=self.load_data, state=tk.DISABLED)
        self.load_data_button.grid(row=5, column=1, padx=10, pady=10)

    def create_user(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        weight = self.weight_entry.get()

        if not name or not age or not weight:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            age = int(age)
            weight = float(weight)
        except ValueError:
            messagebox.showerror("Error", "Age must be an integer and weight must be a float")
            return

        self.user = User(name, age, weight)
        messagebox.showinfo("Success", "User created successfully")

        self.add_workout_button.config(state=tk.NORMAL)
        self.view_workouts_button.config(state=tk.NORMAL)
        self.save_data_button.config(state=tk.NORMAL)
        self.load_data_button.config(state=tk.NORMAL)

    def add_workout(self):
        if not self.user:
            messagebox.showerror("Error", "Please create a user first")
            return

        date = datetime.now().strftime("%Y-%m-%d")
        exercise_type = simpledialog.askstring("Input", "Enter the exercise type:")
        duration = simpledialog.askinteger("Input", "Enter the duration (minutes):")
        calories_burned = simpledialog.askinteger("Input", "Enter the calories burned:")

        if not exercise_type or not duration or not calories_burned:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        workout = Workout(date, exercise_type, duration, calories_burned)
        self.user.add_workout(workout)
        messagebox.showinfo("Success", "Workout added successfully")

    def view_workouts(self):
        if not self.user:
            messagebox.showerror("Error", "Please create a user first")
            return

        workouts = self.user.view_workouts()
        messagebox.showinfo("Workouts", workouts)

    def save_data(self):
        if not self.user:
            messagebox.showerror("Error", "Please create a user first")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not filename:
            return

        self.user.save_data(filename)
        messagebox.showinfo("Success", "Data saved successfully")

    def load_data(self):
        if not self.user:
            messagebox.showerror("Error", "Please create a user first")
            return

        filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not filename:
            return

        self.user.load_data(filename)
        messagebox.showinfo("Success", "Data loaded successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()