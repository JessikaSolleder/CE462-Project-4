import math
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import numpy as np

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
    ka = (np.tan(np.radians(45 - (phi / 2)))) ** 2
    kp = (np.tan(np.radians(45 + (phi / 2)))) ** 2
    gamma_prime = gamma - gamma_water

    # Step 1: Calculate sigma1
    def get_sigma1(gamma, wall_height, water_table_height, ka):
        sigma1 = gamma * (wall_height - water_table_height) * ka
        return sigma1

    # Step 2: Calculate sigma2
    def get_sigma2(gamma, wall_height, gamma_prime, water_table_height):
        sigma2 = (gamma * (wall_height - water_table_height) + (gamma_prime * water_table_height))
        return sigma2

    # Step 3: Calculate sigma6
    def get_sigma6(c, gamma, wall_height, water_table_height, gamma_prime):
        sigma6 = ((4 * c) - (gamma * (wall_height - water_table_height)) + (gamma_prime * water_table_height))
        return sigma6

    # Step 4: Calculate P1
    def get_p1(sigma1, water_table_height, wall_height, sigma2):
        p1 = (0.5 * sigma1 * (wall_height - water_table_height)) + (sigma1 * water_table_height) + (0.5 * (sigma2 - sigma1) * water_table_height)
        return p1

    # Step 5: Calculate zbar1
    def get_zbar1(p1, wall_height, water_table_height, sigma1, sigma2):
        zbar1 = ((0.5 * sigma1 * (wall_height - water_table_height)) * (water_table_height + 0.5 * (wall_height - water_table_height)) + ((sigma1 * water_table_height) * (0.5 / water_table_height)) + ((0.5 * (sigma2 - sigma1) * water_table_height) * ((1/3) * water_table_height))) / p1
        return zbar1

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

    # Calculate sigma1, sigma2, sigma6, p1, and zbar1
    sigma1 = get_sigma1(gamma, wall_height, water_table_height, ka)
    sigma2 = get_sigma2(gamma, wall_height, gamma_prime, water_table_height)
    sigma6 = get_sigma6(cohesion, gamma, wall_height, water_table_height, gamma_prime)
    p1 = get_p1(sigma1, water_table_height, wall_height, sigma2)
    zbar1 = get_zbar1(p1, wall_height, water_table_height, sigma1, sigma2)
    # Define the coefficients of the quadratic equation
    a = sigma6
    b = 2 * sigma6 * (wall_height - l1)
    c = 2 * p1 * wall_height - l1 - zbar1

    # Call the quadratic equation solver
    root = solve_quadratic(a, b, c)

    if root is not None:
        print("The real and positive root for D is:", root)
    else:
        print("There are no real roots or both roots are negative.")
        
# Calculate embedment depth (m)
def get_embed_depth (root):
    embed_depth = root * 1.75
    return embed_depth
   
# Calculate the Anchor Force - f (kN / m)
def get_f(p1, sigma6, root):
    f = p1 - sigma6 * root
    return f

# Calculate Mmaxx (maxmimum moment in terms of x)
def solve_quadratic2(a2, b2, c2):
        discriminant2 = b2 ** 2 - 4 * a2 * c2

        if discriminant2 < 0:
            return None  # No real roots

        root1a = (-b2 + math.sqrt(discriminant2)) / (2 * a2)
        root2a = (-b2 - math.sqrt(discriminant2)) / (2 * a2)

        if root1a > 0:
            return root1a
        elif root2a > 0:
            return root2a
        else:
            return None
        
f = get_f(p1, sigma6, root)

   # Define the coefficients of the quadratic equation
a2 = (0.5 * ka * gamma_prime)
b2 = sigma1
c2 = (0.5 * sigma1 * (wall_height - water_table_height) - f)
    # Call the quadratic equation solver
roota = solve_quadratic(a2, b2, c2)

if roota is not None:
    print("The real and positive root for x is:", roota)
else:
    print("There are no real roots or both roots are negative.")

# Calculate Mmax_x (kN * m/m)
    # Define the coefficients of the polynomial equation ax^3 + bx^2 + cx + d = 0
a3 = - ((1/6) * ka * gamma_prime)
b3 = -(0.5 * sigma1)
c3 = -(0.5 * sigma1 * (wall_height - water_table_height)) + f
d3 = f * l2 + (0.5 * sigma1 * wall_height - water_table_height) * (0.3 * wall_height - water_table_height)

# Find the roots of the polynomial equation
roots = np.roots([a3, b3, c3, d3])
real_roots = [root for root in roots if np.isreal(root)]

print("Real roots of the polynomial equation:", real_roots)
largest_root = max(real_roots, key=abs)

# Print the largest real root
if largest_root is not None:
    print("Root with the largest absolute value:", largest_root)
else:
    print("No real roots found.")
    
embed_depth = get_embed_depth (root)

        # Create the summary message
summary_message = f"Actual Embedment Depth Below Dredge Line (m): {embed_depth}\nAnchor Force (kN/m): {f}\nMaximum Moment (kN * m/m): {largest_root}"

        # Show the summary message in a pop-up window
messagebox.showinfo("Summary", summary_message)


