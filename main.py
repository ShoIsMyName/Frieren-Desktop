import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import random
from pystray import Icon, Menu, MenuItem
import threading
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "white")

WIDTH, HEIGHT = 200, 200

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0)
canvas.pack()



# create hidden icons
def quit_all(icon, item):
    icon.stop() 
    root.destroy() 
    sys.exit() 
 
def setup_tray():
    menu = Menu(MenuItem('Exit', quit_all))
    icon_image = Image.open(resource_path("FrierenIcon.ico"))
    icon = Icon("Frieren", icon_image, "Frieren Desktop", menu)
    icon.run()

tray_thread = threading.Thread(target=setup_tray, daemon=True)
tray_thread.start()



# physics
x, y = 500, 100
vy = 0            # Vertical velocity
gravity = 1 

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
floor = screen_height - (HEIGHT + 50)



# drag
dragging = False
offset_x = 0
offset_y = 0

def on_click(event):
    global dragging, offset_x, offset_y
    dragging = True
    offset_x = event.x
    offset_y = event.y

def on_drag(event):
    global x, y
    x = root.winfo_pointerx() - offset_x
    y = root.winfo_pointery() - offset_y
    root.geometry(f"+{x}+{y}")

def on_release(event):
    global dragging
    dragging = False



# leave function
def greet(event):
    if messagebox.askyesno("Hi", "Do you want to say hi?"):
        result_greet = result = random.choices([True, False], weights=[25, 75])[0]

        if result_greet:
            greeting = random.choice(["Hello there", "Hi", "Hello", "Hey"])
            messagebox.showinfo("...", greeting)
        else:
            messagebox.showinfo("...", "Frieren still sleepy...")


canvas.bind("<Button-1>", on_click)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)
canvas.bind("<Double-Button-1>", greet)



# character state
state = "idle"
walk_timer = 0
walk_duration = 0

speed = 3



# character image sprites
default_image = resource_path("Sprite/SleepyFrieren.png") # second = resource_path("SleepyFrieren2.png")

def sprite(sprite=default_image):
    image = Image.open(sprite)
    image = image.resize((200, 200))
    img = ImageTk.PhotoImage(image)

    return img

def set_sprite():
    global img
    img = sprite(default_image)
    canvas.create_image(WIDTH//2, HEIGHT//2, image=img)



# loop
def update():
    global x, y, vy, state, walk_timer, walk_duration, default_image

    if dragging == True: default_image = resource_path("Sprite/SleepyFrieren3.png")
    elif state== "walk_right": default_image = resource_path("Sprite/SleepyFrieren2.png")
    else: default_image = resource_path("Sprite/SleepyFrieren.png")

    set_sprite()

    if not dragging:

        walk_timer += 1

        if state == "idle":
            if walk_timer > 300: # set time before walking
                walk_timer = 0

                if random.random() < 0.5:
                    state = random.choice(["walk_left", "walk_right"])
                    walk_duration = random.randint(50, 150)

        elif state.startswith("walk"):
            walk_duration -= 1

            if state == "walk_left":
                x -= speed
            elif state == "walk_right":
                x += speed

            if walk_duration <= 0:
                state = "idle"

        # gravity
        vy += gravity
        y += vy

        if y >= floor:
            y = floor
            vy = 0
        
        # screen bounds
        if x < 0:
            x = 0
            state = "walk_right"

        elif x > screen_width - WIDTH:
            x = screen_width - WIDTH
            state = "walk_left"

    root.geometry(f"+{int(x)}+{int(y)}")
    root.after(30, update)


update()
root.mainloop()