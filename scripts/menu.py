import pyglet
import os

menu_height = 50
menu_padding = 10
menu_bg_color = (228, 213, 183)  

current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, '../Images')

food_image = pyglet.image.load(os.path.join(images_dir, 'Food.png'))

wood_image = pyglet.image.load(os.path.join(images_dir, 'Wood.png'))

iron_image = pyglet.image.load(os.path.join(images_dir, 'Iron.png'))

gold_image = pyglet.image.load(os.path.join(images_dir, 'Gold.png'))

icons = [food_image, wood_image, iron_image, gold_image]

def is_point_inside(x, y, rect):
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh

def draw_menu(selected_hold, window_width, window_height, font_name, side):
    if not selected_hold:
        return
        
    menu_width = int(window_width * 0.3)
    menu_height = int(window_height * 0.05)
    x = (window_width - menu_width) // 2
    y = int(window_height * 0.9)

    pyglet.shapes.RoundedRectangle(
        x, y, menu_width, menu_height,
        color=menu_bg_color,
        batch=None,
        radius=25
    ).draw()

    pyglet.text.Label(
        selected_hold["name"],
        font_name=font_name,
        font_size=50,
        x=x + menu_width // 2,
        y=y + menu_height // 2,
        anchor_x='center',
        anchor_y='center',
        color=(0, 0, 0, 255)
    ).draw()

    width = int(window_width * 0.2)
    height = int(window_height * 0.95)
        
    icon_y = ((window_height - height) // 2) + (height * 0.95)
    if side == "left":
        pyglet.shapes.RoundedRectangle(
            10, (window_height - height) // 2,
            width, height,
            color=menu_bg_color,
            batch=None,
            radius=20
        ).draw()
        icon_x_base = 10
    else:
        pyglet.shapes.RoundedRectangle(
            window_width - width - 10,
            (window_height - height) // 2,
            width, height,
            color=menu_bg_color,
            batch=None,
            radius=20
        ).draw()
        icon_x_base = window_width - width - 10
    
    icon_size = 50
    padding = 10

    for i, sprite_image in enumerate(icons):
        icon_x = icon_x_base + (width / (2 * len(icons))) + (i * (width / len(icons))) - (icon_size / 2)
        print(selected_hold["resources"])
        sprite = pyglet.sprite.Sprite(sprite_image)
        scale = icon_size / max(sprite.image.width, sprite.image.height)

        sprite.scale = scale

        sprite.x = icon_x
        sprite.y = icon_y
        sprite.draw()

        icon_x += icon_size + padding