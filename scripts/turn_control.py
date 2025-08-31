import pyglet
import os
import math

bar_height = 40
circle_button = None

bar_color = (200, 180, 150)
circle_color = (180, 150, 120)
circle_hover_color = (200, 170, 140)

current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, '../Images')

icons = {
    "food": pyglet.image.load(os.path.join(images_dir, 'Food.png')),
    "wood": pyglet.image.load(os.path.join(images_dir, 'Wood.png')),
    "iron": pyglet.image.load(os.path.join(images_dir, 'Iron.png')),
    "gold": pyglet.image.load(os.path.join(images_dir, 'Gold.png'))
}


def draw_menu_bar(window_width, window_height, font_name, turn_counter_ref, house_colours, player_house):
    pyglet.shapes.Rectangle(
        0, window_height - bar_height,
        window_width, bar_height,
        color=house_colours[player_house][0]
    ).draw()

    x_base = window_width * 0.02
    pyglet.text.Label(
        f"Turn: {turn_counter_ref[0]}",
        font_name=font_name,
        font_size=20,
        x=x_base,
        y=window_height - bar_height // 2,
        anchor_x="left",
        anchor_y="center",
        color=(0, 0, 0, 255)
    ).draw()
    
    icons_width = 400
    icons_x_base = x_base + window_width * 0.05
    icon_size = 35
    padding = 10
    
    for i, (name, sprite_image) in enumerate(icons.items()):
        icon_x = icons_x_base + (icons_width / (2 * len(icons))) + (i * (icons_width / len(icons))) - (icon_size / 2)
        text_x = icon_x - icon_size - padding
        text_string = str(house_colours[player_house][3][i])
        
        pyglet.text.Label(
            text_string,
            font_name=font_name,
            font_size=20,
            x=text_x,
            y=window_height - bar_height // 2,
            anchor_x="left",
            anchor_y="center",
            color=(0, 0, 0, 255)
        ).draw()
        
        
        sprite = pyglet.sprite.Sprite(sprite_image)
        scale = icon_size / max(sprite.image.width, sprite.image.height)
        sprite.scale = scale
        sprite.x = icon_x
        sprite.y = window_height - (bar_height * 0.95)
        sprite.draw()


def display_UI(window_width, window_height, font_name, is_hovering, turn_counter_ref, menu_only, house_colours, player_house):
    global circle_button

    draw_menu_bar(window_width, window_height, font_name, turn_counter_ref, house_colours, player_house)

    if menu_only:
        return

    radius = window_width * 0.06
    bx = window_width - radius - 20
    by = radius + 20
    circle_button = (bx, by, radius)

    circle_col = house_colours[player_house][1] if is_hovering else house_colours[player_house][0]
    circle = pyglet.shapes.Circle(bx, by, radius, color=circle_col)
    circle.draw()

    pyglet.text.Label(
        "Next Turn",
        font_name=font_name,
        font_size=50,
        x=bx,
        y=by,
        anchor_x="center",
        anchor_y="center",
        color=(0, 0, 0)
    ).draw()


def handle_mouse_press(x, y, button, modifiers, turn_counter_ref):
    global circle_button
    if circle_button is None:
        return

    bx, by, radius = circle_button
    dist = math.hypot(x - bx, y - by)

    if dist <= radius:
        turn_counter_ref[0] += 1
