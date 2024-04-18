from math import tan
import cmath
import tkinter as tk
from tkinter import simpledialog

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
    f = p - (0.5 * (gamma_prime * (kp - ka)) * l4)

    # Determine embedment depth
    d_theoretical = l3 + l4
    d_actual = 1.35 * d_theoretical

    # Determine maximum moment
    def solve_quadratic(a, b, c):
        # Calculate the discriminant
        discriminant = (b ** 2) - (4 * a * c)

        # Check if the discriminant is positive, negative, or zero
        if discriminant >= 0:
            # If the discriminant is non-negative, calculate the roots
            root1 = (-b + cmath.sqrt(discriminant)) / (2 * a)
            root2 = (-b - cmath.sqrt(discriminant)) / (2 * a)
            return root1, root2
        else:
            # If the discriminant is negative, return complex roots
            root1 = (-b + cmath.sqrt(discriminant)) / (2 * a)
            root2 = (-b - cmath.sqrt(discriminant)) / (2 * a)
            return root1, root2

    # Coefficients of the quadratic equation ax^2 + bx + c = 0
    a = 0.5 * ka * gamma_prime
    b = sigma1 - ka * gamma_prime * l1
    c = (f + 0.5 * sigma1 * l1) - (0.5 * ka * gamma_prime * (l1 ** 2))

    # Solve the quadratic equation
    root1, root2 = solve_quadratic(a, b, c)

    print("Root 1:", root1)
    print("Root 2:", root2)
