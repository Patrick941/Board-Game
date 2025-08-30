import pyglet

menu_height = 50
menu_padding = 10
menu_bg_color = (228, 213, 183)  

def is_point_inside(x, y, rect):
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh

def draw_menu(selected_hold, window_width, window_height, font_name, side):
    if not selected_hold:
        return
        
    # Center menu
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
        
    if side == "left":
        pyglet.shapes.RoundedRectangle(
            10, (window_height - height) // 2,
            width, height,
            color=menu_bg_color,
            batch=None,
            radius=20
        ).draw()
    else:
        pyglet.shapes.RoundedRectangle(
            window_width - width - 10,
            (window_height - height) // 2,
            width, height,
            color=menu_bg_color,
            batch=None,
            radius=20
        ).draw()