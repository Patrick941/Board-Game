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

def show_units(house_region, hold, window_width, window_height, camera_x, camera_y, zoom):
    house = hold["house"]
    image_name = house + "_soldier"
    sprite_image = army_images[image_name.lower()]
    
    icon_size = 150
    sprite = pyglet.sprite.Sprite(sprite_image)
    scale = icon_size / max(sprite.image.width, sprite.image.height)
    sprite.scale = scale

    sprite.x = ((int(hold["x_cord"]) - camera_x) * zoom) - (icon_size / 2)
    sprite.y = (int(hold["y_cord"]) - camera_y) * zoom

    sprite.scale *= zoom

    sprite.draw()
