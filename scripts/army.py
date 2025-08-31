import os
import pyglet

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
army_dir = os.path.join(current_dir, "Images", "army")

army_images = {}


def army_init():
    for filename in os.listdir(army_dir):
        if filename.endswith(".png"):
            image_name = filename.replace(".png", "")
            path = os.path.join(army_dir, filename)
            army_images[image_name] = pyglet.image.load(path)
            
unit_types = ["_soldier", "_archer", "_knight", "_kingsguard"]

def show_units(house_region, hold, window_width, window_height, camera_x, camera_y, zoom):
    house = hold["house"]
    units = hold["army"]
    total_army = 0
    for unit in units:
        total_army += int(unit)
    icon_size = 150    
    compactor = 0.4
    unit_count = 0

    for i, unit in enumerate(units):
        image_name = house + unit_types[i]
        y = (int(hold["y_cord"]) - camera_y) * zoom + (icon_size * i * 2.2 * compactor)
        for idx in range(int(units[i])):
            x = ((int(hold["x_cord"]) - camera_x) * zoom) - (0.5 * compactor * int(unit) * icon_size) - (icon_size * compactor) + (compactor * icon_size * idx)
            
            sprite_image = army_images[image_name.lower()]
            
            sprite = pyglet.sprite.Sprite(sprite_image)
            scale = icon_size / max(sprite.image.width, sprite.image.height)
            sprite.scale = scale

            sprite.x = x
            sprite.y = y

            sprite.scale *= zoom

            sprite.draw()
