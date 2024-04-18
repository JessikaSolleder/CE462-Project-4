from cmath import tan
import tkinter as tk
from tkinter import simpledialog

# Jessika Solleder - Dr. Hudyma - CE462 -  Project 4: Anchored Pile Walls



# User Inputs #
wall_height = simpledialog.askfloat("Input", "Enter wall height (m):")
gamma = simpledialog.askfloat("Input", "Enter soil unit weight (kN/m^3):")
gamma_sat = simpledialog.askfloat("Input", "Enter soil saturated unit weight (kN/m^3):")
phi = simpledialog.askfloat("Input", "Enter angle of internal friction (degrees):")
water_table_height = simpledialog.askfloat("Input", "Enter groundwater table height above dredge line (m):")
pile_total_length = simpledialog.askfloat("Input", "Enter the entire length of the pile:")

# Define Constants #
gamma_water = 1000 #kg/m^3
ka = (tan(45 - (phi / 2)))**2
kp = (tan(45 + (phi/2)))**2
gamma_prime = gamma - gamma_water

# Calculate embedment depth, max moment, etc
l1 = wall_height - water_table_height
l2 = wall_height -l1
sigma1 = gamma * l1 * ka
sigma2 = ((gamma * l1) + (gamma_prime * l2)) * ka
l3 = sigma2 / ((gamma_prime) * (kp - ka))

############################################
l4 = pile_total_length - wall_height - l3 # long complicated equation in ppt, but why necessary if you have l1, l2 and l3?
##########################################

p = (l1 * sigma1 * 0.5) + (sigma1 * l1) + (((sigma2 - sigma1) * l2)*0.5) + (sigma2 * l3 * 0.5)
z_bar = (0.5 * l1 * sigma1 * ((l3 / 3) + l2 + l3) + (sigma1 * l2) * ((l2/2) + l3) + 0.5(sigma2 - sigma1) * (l2/3) * ((l2 /3) + l3) + 0.5 * l3 * sigma2 * (2 * l3 * (1/3))) / p
sigma8 = gamma_prime(kp - ka) * l4

# Determine F (anchor force)
f = p - (0.5(gamma_prime(kp-ka))*l4)

# Determine embedment depth
d_theoretical = l3 + l4
d_actual = 1.35 * d_theoretical

# Determine maximum moment
