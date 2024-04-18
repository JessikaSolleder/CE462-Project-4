import tkinter as tk
from tkinter import simpledialog

# Jessika Solleder - Dr. Hudyma - CE462 -  Project 4: Anchored Pile Walls

# Define Constants #

# User Inputs #
wall_height = simpledialog.askfloat("Input", "Enter wall height (m):")
gamma = simpledialog.askfloat("Input", "Enter soil unit weight (kN/m^3):")
phi = simpledialog.askfloat("Input", "Enter angle of internal friction (degrees):")
water_table_height = simpledialog.askfloat("Input", "Enter groundwater table height above dredge line (m):")