from math import tan
import cmath
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate embedment depth
def calculate_embedment_depth(phi):
    ka_phi = (tan(45 - (phi / 2))) ** 25
    kp_phi = (tan(45 + (phi / 2))) ** 2
    sigma1_phi = gamma * l1 * ka_phi
    sigma2_phi = ((gamma * l1) + (gamma_prime * l2)) * ka_phi
    l3_phi = sigma2_phi / (gamma_prime * (kp_phi - ka_phi))
    l4_phi = pile_total_length - wall_height - l3_phi
    embedment_depths_phi = 1.35 * (l3_phi + l4_phi)
    return embedment_depths_phi

# Function to calculate anchor force
def calculate_anchor_force(phi):
    ka_phi = (tan(45 - (phi / 2))) ** 25
    kp_phi = (tan(45 + (phi / 2))) ** 2
    sigma1_phi = gamma * l1 * ka_phi
    sigma2_phi = ((gamma * l1) + (gamma_prime * l2)) * ka_phi
    l3_phi = sigma2_phi / (gamma_prime * (kp_phi - ka_phi))
    l4_phi = pile_total_length - wall_height - l3_phi
    anchor_force_phi = p - (0.5 * (gamma_prime * (kp_phi - ka_phi)) * l4_phi)
    return anchor_force_phi

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
    l4 = pile_total_length - wall_height - l3
    p = (l1 * sigma1 * 0.5) + (sigma1 * l1) + (((sigma2 - sigma1) * l2) * 0.5) + (sigma2 * l3 * 0.5)

    # Calculate embedment depth for each phi value
    phi_range_str = simpledialog.askstring("Input", "Enter range of phi values (start, stop, step):")
    start, stop, step = map(float, phi_range_str.split(','))
    phi_values = np.arange(start, stop, step)
    embedment_depths = [calculate_embedment_depth(phi) for phi in phi_values]
    
    # Calculate anchor force for each phi value
    anchor_forces = [calculate_anchor_force(phi) for phi in phi_values]

    # Plot the results
    plt.plot(phi_values, embedment_depths, label='Embedment Depth', marker='o')
    plt.plot(phi_values, anchor_forces, label='Anchor Force', marker='o')
    plt.title("Sensitivity Analysis")
    plt.xlabel("Phi Values (degrees)")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()
