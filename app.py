import tkinter as tk
from tkinter import colorchooser

# Initialize the main application window
root = tk.Tk()
root.title("Python Whiteboard")
root.geometry("800x600")

# Canvas for drawing
canvas = tk.Canvas(root, bg="white", width=800, height=600)
canvas.pack(fill="both", expand=True)

# Variables for drawing
last_x, last_y = None, None
color = "black"  # Default drawing color
brush_size = 5  # Default brush size
is_eraser = False  # Eraser mode is off by default

# Function to start drawing
def start_drawing(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

# Function to draw lines on the canvas
def draw(event):
    global last_x, last_y
    if last_x and last_y:
        # Use white as the color if eraser mode is active
        draw_color = "white" if is_eraser else color
        canvas.create_line(last_x, last_y, event.x, event.y, fill=draw_color, width=brush_size)
        last_x, last_y = event.x, event.y

# Function to reset the last coordinates after finishing a stroke
def reset_drawing(event):
    global last_x, last_y
    last_x, last_y = None, None

# Function to clear the canvas
def clear_canvas():
    canvas.delete("all")  # Clears everything on the canvas

# Function to choose color
def choose_color():
    global color, is_eraser
    color = colorchooser.askcolor()[1]  # Open color chooser dialog
    is_eraser = False  # Switch back to drawing mode after choosing a color
    eraser_button.config(text="Eraser OFF")  # Update button text to show eraser is off

# Function to toggle eraser mode
def toggle_eraser():
    global is_eraser
    is_eraser = not is_eraser  # Toggle the eraser mode
    if is_eraser:
        eraser_button.config(text="Eraser ON")  # Update button text to indicate eraser is on
    else:
        eraser_button.config(text="Eraser OFF")  # Update button text to indicate eraser is off

# Buttons for controls
color_button = tk.Button(root, text="Choose Color", command=choose_color)
color_button.pack(side="left", padx=10)

eraser_button = tk.Button(root, text="Eraser OFF", command=toggle_eraser)
eraser_button.pack(side="left", padx=10)

clear_button = tk.Button(root, text="Clear All", command=clear_canvas)
clear_button.pack(side="left", padx=10)

# Bind mouse events to the canvas
canvas.bind("<Button-1>", start_drawing)  # Start drawing when left mouse button is clicked
canvas.bind("<B1-Motion>", draw)  # Draw as the mouse moves with the button held down
canvas.bind("<ButtonRelease-1>", reset_drawing)  # Reset drawing on releasing the mouse button

# Run the application
root.mainloop()
