import math
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

# User Inputs
wall_height = simpledialog.askfloat("Input", "Enter wall height above dredge line (m):")
gamma = simpledialog.askfloat("Input", "Enter soil unit weight (kN/m^3):")
gamma_sat = simpledialog.askfloat("Input", "Enter soil saturated unit weight (kN/m^3):")
phi = simpledialog.askfloat("Input", "Enter angle of internal friction (degrees):")
water_table_height = simpledialog.askfloat("Input", "Enter groundwater table height above dredge line (m):")
cohesion = simpledialog.askfloat("Input", "Enter the cohesion of the clay soil layer (Pa):")

# Constants
l1 = (wall_height - water_table_height) / 2
l2 = (wall_height - water_table_height) - l1

# Ensure all inputs are provided
if None in [wall_height, gamma, gamma_sat, phi, water_table_height]:
    print("One or more inputs are missing. Please provide all inputs.")
else:
    # Define Constants
    gamma_water = 1000  # kg/m^3

    # Function to calculate coefficients based on phi
    def get_coefficients(phi):
        ka = (np.tan(np.radians(45 - (phi / 2)))) ** 2
        gamma_prime = gamma - gamma_water
        return ka, gamma_prime

    # Step 6: Determine the Theoretical Depth (m)
    def solve_quadratic(a, b, c):
        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return None  # No real roots

        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)

        if root1 > 0:
            return root1
        elif root2 > 0:
            return root2
        else:
            return None

    # Calculate Anchor Force (f) for a given phi value
    def get_f(phi, root):
        ka, gamma_prime = get_coefficients(phi)
        sigma1 = get_sigma1(gamma, wall_height, water_table_height, ka)
        sigma2 = get_sigma2(gamma, wall_height, gamma_prime, water_table_height)
        sigma6 = get_sigma6(cohesion, gamma, wall_height, water_table_height, gamma_prime)
        p1 = get_p1(sigma1, water_table_height, wall_height, sigma2)
        zbar1 = get_zbar1(p1, wall_height, water_table_height, sigma1, sigma2)
        f = p1 - sigma6 * root
        return f

    # Step 5: Calculate functions of phi (f and embedment depth)
    def calculate_phi_functions(phi_range):
        f_values = []
        embedment_depth_values = []
        for phi in phi_range:
            ka, gamma_prime = get_coefficients(phi)

            # Calculate other parameters
            sigma1 = get_sigma1(gamma, wall_height, water_table_height, ka)
            sigma2 = get_sigma2(gamma, wall_height, gamma_prime, water_table_height)
            sigma6 = get_sigma6(cohesion, gamma, wall_height, water_table_height, gamma_prime)
            p1 = get_p1(sigma1, water_table_height, wall_height, sigma2)
            zbar1 = get_zbar1(p1, wall_height, water_table_height, sigma1, sigma2)

            # Solve quadratic equation (assuming it's related to f or embedment depth)
            root = solve_quadratic(a, b, c)  # Replace a, b, c with appropriate coefficients

            if root is not None:
                f = get_f(phi, root)
                embedment_depth = get_embed_depth(root)
                f_values.append(f)
                embedment_depth_values.append(embedment_depth)
