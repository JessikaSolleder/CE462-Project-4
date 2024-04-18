from math import tan
import math
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import numpy as np

# User Inputs
wall_height = simpledialog.askfloat("Input", "Enter wall height (m):")
gamma = simpledialog.askfloat("Input", "Enter soil unit weight (kN/m^3):")
gamma_sat = simpledialog.askfloat("Input", "Enter soil saturated unit weight (kN/m^3):")
phi = simpledialog.askfloat("Input", "Enter angle of internal friction (degrees):")
water_table_height = simpledialog.askfloat("Input", "Enter groundwater table height above dredge line (m):")
pile_total_length = simpledialog.askfloat("Input", "Enter the entire length of the pile:")

# Ensure all inputs are provided
if None in [wall_height, gamma, gamma_sat, phi, water_table_height, pile_total_length]:
    print("One or more inputs are missing. Please provide all inputs.")
else:
    # Define Constants
    gamma_water = 1000  # kg/m^3
    ka = (tan(45 - (phi / 2))) ** 25
    kp = (tan(45 + (phi / 2))) ** 2
    gamma_prime = gamma - gamma_water

    # Calculate embedment depth, max moment, etc
    l1 = wall_height - water_table_height
    l2 = wall_height - l1
    sigma1 = gamma * l1 * ka
    sigma2 = ((gamma * l1) + (gamma_prime * l2)) * ka
    l3 = sigma2 / (gamma_prime * (kp - ka))

    ############################################
    l4 = pile_total_length - wall_height - l3  # long complicated equation in ppt, but why necessary if you have l1, l2 and l3?
    ##########################################

    p = (l1 * sigma1 * 0.5) + (sigma1 * l1) + (((sigma2 - sigma1) * l2) * 0.5) + (sigma2 * l3 * 0.5)
    z_bar = (0.5 * l1 * sigma1 * ((l3 / 3) + l2 + l3) + (sigma1 * l2) * ((l2 / 2) + l3) + 0.5 * (
                sigma2 - sigma1) * (l2 / 3) * ((l2 / 3) + l3) + 0.5 * l3 * sigma2 * (2 * l3 * (1 / 3))) / p
    sigma8 = gamma_prime * (kp - ka) * l4

    # Determine F (anchor force)
    anchor_force = p - (0.5 * (gamma_prime * (kp - ka)) * l4)
    message_anchor = f"Anchor Force: {anchor_force}"
    
    # Determine embedment depth
    d_theoretical = l3 + l4
    d_actual = 1.35 * d_theoretical
    message_depth = f"Theoretical Depth: {d_theoretical}\nActual Depth: {d_actual}"

    # Determine maximum moment
    def solve_quadratic(a, b, c):
        # Calculate the discriminant
        discriminant = (b ** 2) - (4 * a * c)

        # Check if the discriminant is positive, negative, or zero
        if discriminant >= 0:
            # If the discriminant is non-negative, calculate the roots
            root1 = (-b + math.sqrt(discriminant)) / (2 * a)
            root2 = (-b - math.sqrt(discriminant)) / (2 * a)
            return root1, root2
        else:
            # If the discriminant is negative, return complex roots
            messagebox.showinfo("Error", "Discriminant is negative. Please input different values.")
            return None, None

    # Coefficients of the quadratic equation ax^2 + bx + c = 0
    a = 0.5 * ka * gamma_prime
    b = sigma1 - ka * gamma_prime * l1
    c = (anchor_force + 0.5 * sigma1 * l1) - (0.5 * ka * gamma_prime * (l1 ** 2))

    # Solve the quadratic equation

root1, root2 = solve_quadratic(a, b, c)

# Initialize m_max to None
m_max = None

# Check if root1 is a real number
if isinstance(root1, (int, float)):
    m_max = - (0.5 * sigma1 * l1) * (root1 - (2/3) * l1) + anchor_force * (root1 - (l1 * (1/3))) - (sigma1 * (root1 - l1)) * ((root1 - l1) / 2) - (0.5 * ka * gamma_prime * (root1 - l1) ** 2) * ((root1 - l1) / 3) 
    print("Using root1 for m_max calculation.")
# If root1 is not real, check if root2 is real
elif isinstance(root2, (int, float)):
    m_max = - (0.5 * sigma1 * l1) * (root2 - (2/3) * l1) + anchor_force * (root2 - (l1 * (1/3))) - (sigma1 * (root2 - l1)) * ((root2 - l1) / 2) - (0.5 * ka * gamma_prime * (root2 - l1) ** 2) * ((root2 - l1) / 3) 
    print("Using root2 for m_max calculation.")
else:
    print("No real roots found, cannot calculate m_max.")

# If m_max is calculated, print the value
if m_max is not None:
    message_max = f"Maximum Moment: {m_max}"
    print(message_max)  
    # Solve for max moment, assuming root 1 is always positive
m_max = - (0.5 * sigma1 * l1) * (root1 - (2/3) * l1) + anchor_force * (root1 - (l1 * (1/3))) - (sigma1 * (root1 - l1)) * ((root1 - l1) / 2) - (0.5 * ka * gamma_prime * (root1 - l1) ** 2) * ((root1 - l1) / 3) 
m_max = - (0.5 * sigma1 * l1) * (root2 - (2/3) * l1) + anchor_force * (root2 - (l1 * (1/3))) - (sigma1 * (root2 - l1)) * ((root2 - l1) / 2) - (0.5 * ka * gamma_prime * (root2 - l1) ** 2) * ((root2 - l1) / 3) 
message_max = f"Maximum Moment: {m_max}"

# Convert complex numbers to floats before rounding
if isinstance(m_max, complex):
    m_max_real = m_max.real
else:
    m_max_real = m_max

if isinstance(anchor_force, complex):
    anchor_force_real = anchor_force.real
else:
    anchor_force_real = anchor_force

# Round m_max_real and anchor_force_real to two decimal places
m_max_rounded = round(m_max_real, 2)
anchor_force_rounded = round(anchor_force_real, 2)

# Solutions Box
messagebox.showinfo("Embedment Depth Results", message_depth)
messagebox.showinfo("Anchor Force Results (kN)", message_anchor)
messagebox.showinfo("Maximum Moment Results (Kn-m)", message_max)

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

# Function to calculate embedment depth
def calculate_embedment_depth(phi):
    embedment_depths_phi = 1.35 * (l3 + l4)
    return embedment_depths_phi

# Prompt user for range of phi values
root = tk.Tk()
root.withdraw()  # Hide the root window

phi_range_str = simpledialog.askstring("Input", "Enter range of phi values (start, stop, step):")
start, stop, step = map(float, phi_range_str.split(','))

# Generate phi values within the specified range
phi_values = np.arange(start, stop, step)

# Calculate embedment depth for each phi value
embedment_depths = [calculate_embedment_depth(phi) for phi in phi_values]

# Plot the results
plt.plot(phi_values, embedment_depths, marker='o')
plt.title("Embedment Depth vs. Phi Values")
plt.xlabel("Phi Values (degrees)")
plt.ylabel("Embedment Depth")
plt.grid(True)
plt.show()

# Function to calculate anchor force
def anchor_force_depth(phi):
    anchor_force_phi =  p - (0.5 * (gamma_prime * (kp - ka)) * l4)
    return anchor_force_phi

# Prompt user for range of phi values
root = tk.Tk()
root.withdraw()  # Hide the root window

phi_range_str = simpledialog.askstring("Input", "Enter range of phi values (start, stop, step):")
start, stop, step = map(float, phi_range_str.split(','))

# Generate phi values within the specified range
phi_values = np.arange(start, stop, step)

# Calculate embedment depth for each phi value
anchor_force = [calculate_embedment_depth(phi) for phi in phi_values]

# Plot the results
plt.plot(phi_values, anchor_force, marker='o')
plt.title("Anchor Force vs. Phi Values")
plt.xlabel("Phi Values (degrees)")
plt.ylabel("Anchor Force")
plt.grid(True)
plt.show()