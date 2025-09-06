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

def get_menu_rect(window_width, window_height, side):
    width = int(window_width * 0.2)
    height = int(window_height * 0.95)

    if side == "left":
        menu_x_base = 10
        menu_y_base = (window_height - height) // 2
    else:
        menu_x_base = window_width - width - 10
        menu_y_base = (window_height - height) // 2
        
    return(menu_x_base, menu_y_base, width, height)

all_city_buttons = {
    "Train Archer": {"pressed": False, "hover_text": "Train new archers for your garrison.", "hovering": False},
    "Train Soldier": {"pressed": False, "hover_text": "Train new soldiers for your garrison.", "hovering": False},
    "Train Knight": {"pressed": False, "hover_text": "Train new knights for your garrison.", "hovering": False},
    "Appoint Kingsguard": {"pressed": False, "hover_text": "Appoint a kingsguard to protect your king.", "hovering": False},
    "Improve Farms": {"pressed": False, "hover_text": "Increase food production from farms.", "hovering": False},
    "Plant Forests": {"pressed": False, "hover_text": "Increase wood production and forestry capacity.", "hovering": False},
    "Improve Iron Mines": {"pressed": False, "hover_text": "Increase iron production from mines.", "hovering": False},
    "Improve Gold Mines": {"pressed": False, "hover_text": "Increase gold production from mines.", "hovering": False}
}

capital_buttons = {
    "Call Banners": {"pressed": False, "hover_text": "Call your vassals to raise a larger army.", "hovering": False},
    "Declare Kingdom": {"pressed": False, "hover_text": "Declare independence and form a new kingdom.", "hovering": False}
}

def draw_menu_button(text, x, y, height, width, font_name, selected):
    if not selected:
        tint = 0.8
    else:
        tint = 0.6
    colour = (int(menu_bg_color[0] * tint), int(menu_bg_color[1] * tint), int(menu_bg_color[2] * tint))
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

def draw_hover_text(text, x, y):
    label = pyglet.text.Label(
        text,
        font_name='Arial',
        font_size=16,
        x=x, y=y,
        anchor_x='left', anchor_y='bottom',
        color=(255, 255, 255, 255),
        batch=None
    )
    
    # Draw a background for the hover text for better readability
    padding = 5
    bg_width = label.content_width + 2 * padding
    bg_height = label.content_height + 2 * padding
    bg_x = x - padding
    bg_y = y - padding
    
    pyglet.shapes.Rectangle(
        bg_x, bg_y, bg_width, bg_height,
        color=(0, 0, 0, 180)
    ).draw()
    
    label.draw()

def draw_menu(selected_hold, window_width, window_height, font_name, side, mouse_x, mouse_y):
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
    
    menu_x_base, menu_y_base, width, height = get_menu_rect(window_width, window_height, side)

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

    buttons_to_draw = {}
    if selected_hold["size"] == "Large":
        buttons_to_draw.update(capital_buttons)
        buttons_to_draw.update(all_city_buttons)
    else:
        buttons_to_draw.update(all_city_buttons)

    for i, (button_text, status) in enumerate(buttons_to_draw.items()):
        y = menu_y_base + height - (3 * icon_size) - (button_margin + (i * (button_height + button_margin)))
        is_hovering = is_point_inside(mouse_x, mouse_y, (button_x, y, button_width, button_height))
        # Update the hovering status
        if button_text in all_city_buttons:
            all_city_buttons[button_text]["hovering"] = is_hovering
        elif button_text in capital_buttons:
            capital_buttons[button_text]["hovering"] = is_hovering
            
        draw_menu_button(button_text, button_x, y, button_height, button_width, font_name, is_hovering or status["pressed"])
        if is_hovering:
            draw_hover_text(buttons_to_draw[button_text]["hover_text"], mouse_x + 10, mouse_y + 10)
            
def get_button_status(selected_hold):
    buttons_to_return = {}
    
    # Get the status of all buttons relevant to the selected_hold
    if selected_hold["size"] == "Large":
        buttons_to_return.update(capital_buttons)
        buttons_to_return.update(all_city_buttons)
    else:
        buttons_to_return.update(all_city_buttons)

    # Set all buttons to unpressed after their status is retrieved
    for button_name in all_city_buttons:
        all_city_buttons[button_name]["pressed"] = False
    for button_name in capital_buttons:
        capital_buttons[button_name]["pressed"] = False
    
    return buttons_to_return

def on_mouse_press():
    # Update the pressed status based on which button is currently hovering
    for button_text, status in all_city_buttons.items():
        if status["hovering"]:
            status["pressed"] = True
    for button_text, status in capital_buttons.items():
        if status["hovering"]:
            status["pressed"] = True
            
def get_true_button(selected_hold):
    buttons_to_check = {}
    if selected_hold["size"] == "Large":
        buttons_to_check.update(capital_buttons)
        buttons_to_check.update(all_city_buttons)
    else:
        buttons_to_check.update(all_city_buttons)
        
    true_buttons = [name for name, status in buttons_to_check.items() if status["pressed"]]
    
    if len(true_buttons) > 1:
        print("Error: More than one button is True.")
        exit(2)
    elif len(true_buttons) == 1:
        return true_buttons[0]
    else:
        return None