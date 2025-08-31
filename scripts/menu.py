import pyglet
import os

menu_bg_color = (228, 213, 183)
menu_padding = 10
icon_size = 50
icon_padding = 10

current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, '../Images')

icons = {
    "food": pyglet.image.load(os.path.join(images_dir, 'Food.png')),
    "wood": pyglet.image.load(os.path.join(images_dir, 'Wood.png')),
    "iron": pyglet.image.load(os.path.join(images_dir, 'Iron.png')),
    "gold": pyglet.image.load(os.path.join(images_dir, 'Gold.png'))
}

def is_point_inside(x, y, rect):
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh

all_city_buttons = ["Train Soldiers", "Upgrade Units", "Improve Farms", "Plant Forests", "Improve Iron Mines", "Improve Gold Mines"]
capital_buttons = ["Call Banners", "Declare Kingdom"]

def draw_menu_button(text, x, y, height, width, font_name):
    colour = (int(menu_bg_color[0] * 0.8), int(menu_bg_color[1] * 0.8), int(menu_bg_color[2] * 0.8))
    pyglet.shapes.RoundedRectangle(
        x, y, width, height,
        color=colour,
        batch=None,
        radius=25
    ).draw()
    
    pyglet.text.Label(
        text,
        font_name=font_name,
        font_size=50,
        x=x + width // 2,
        y=y + height // 2,
        anchor_x='center',
        anchor_y='center',
        color=(0, 0, 0, 255)
    ).draw()

def draw_menu(selected_hold, window_width, window_height, font_name, side):
    if not selected_hold:
        return
    
    menu_width = int(window_width * 0.3)
    menu_height = int(window_height * 0.05)
    menu_x = (window_width - menu_width) // 2
    menu_y = int(window_height * 0.9)
    
    pyglet.shapes.RoundedRectangle(
        menu_x, menu_y, menu_width, menu_height,
        color=menu_bg_color,
        batch=None,
        radius=25
    ).draw()
    
    pyglet.text.Label(
        selected_hold["name"],
        font_name=font_name,
        font_size=50,
        x=menu_x + menu_width // 2,
        y=menu_y + menu_height // 2,
        anchor_x='center',
        anchor_y='center',
        color=(0, 0, 0, 255)
    ).draw()
    
    width = int(window_width * 0.2)
    height = int(window_height * 0.95)
    
    if side == "left":
        menu_x_base = 10
        menu_y_base = (window_height - height) // 2
    else:
        menu_x_base = window_width - width - 10
        menu_y_base = (window_height - height) // 2
    
    pyglet.shapes.RoundedRectangle(
        menu_x_base, menu_y_base,
        width, height,
        color=menu_bg_color,
        batch=None,
        radius=20
    ).draw()
    
    icon_y = menu_y_base + height - icon_size - menu_padding
    for i, (name, sprite_image) in enumerate(icons.items()):
        resource_count = selected_hold.get(name, 0)
        icon_x = menu_x_base + (width / (2 * len(icons))) + (i * (width / len(icons))) - (icon_size / 2)
        count_label = pyglet.text.Label(
            str(resource_count),
            font_name='Arial',
            font_size=18,
            x=icon_x - 20,
            y=icon_y + icon_size / 2,
            anchor_x='right',
            anchor_y='center',
            color=(0, 0, 0, 255)
        )
        count_label.draw()
        sprite = pyglet.sprite.Sprite(sprite_image)
        scale = icon_size / max(sprite.image.width, sprite.image.height)
        sprite.scale = scale
        sprite.x = icon_x
        sprite.y = icon_y
        sprite.draw()

    button_margin = 15
    button_width = width - (button_margin * 2)
    button_height = 50
    button_x = menu_x_base + button_margin
    current_y = menu_y_base - button_margin + height - (2 * icon_size)

    buttons_to_draw = []
    if selected_hold["size"] == "Large":
        buttons_to_draw.extend(capital_buttons)
        buttons_to_draw.extend(all_city_buttons)
    else:
        buttons_to_draw.extend(all_city_buttons)

    for i, button_text in enumerate(buttons_to_draw):
        y = menu_y_base + height - (2 * icon_size) - (button_margin + (i * (button_height + button_margin)))
        draw_menu_button(button_text, button_x, y, button_height, button_width, font_name)