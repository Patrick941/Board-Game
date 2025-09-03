import pyglet
from pyglet.window import key
import math
import os
from scripts import holds, menu, scoreboard, turn_control, army

debug_vars = ['camera_x', 'camera_y', 'camera_speed', 'zoom', 'last_click']

window = pyglet.window.Window(fullscreen=True, caption="Board Game")

current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, 'Images')

background_image = pyglet.image.load(os.path.join(images_dir, "Background_Cleaned.jpg"))
background = pyglet.sprite.Sprite(background_image, x=0.0, y=0.0)

arrow_image = pyglet.image.load(os.path.join(images_dir, 'arrow_out.png'))
arrow = pyglet.sprite.Sprite(arrow_image)

player_house = "Tully"

camera_x = 0.0
camera_y = 0.0
camera_speed = 50
zoom = 1
min_zoom = 0.465
max_zoom = 3.0
font_name = "Edwardian Script ITC"
mouse_x = 0
mouse_y = 0

last_click = (0.0, 0.0)

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

dragging = False
last_mouse_x, last_mouse_y = 0, 0
scroll_dx = 0.0
scroll_dy = 0.0
scoreboard_pressed = False

CSV_REFRESH_INTERVAL = -1

debug_label = pyglet.text.Label(
    '', 
    font_name=font_name, 
    font_size=24,
    x=window.width - 10, 
    y=window.height - 10, 
    anchor_x='right', 
    anchor_y='top', 
    multiline=True,
    width=300
)

selected_hold = None
turn_counter = [1]


def screen_to_world(sx, sy):
    return (camera_x + sx / zoom, camera_y + sy / zoom)

def world_to_screen(wx, wy):
    return ((wx - camera_x) * zoom, (wy - camera_y) * zoom)

def draw_line(x1, y1, x2, y2, width=30, opacity=255):
    dx = x2 - x1
    dy = y2 - y1
    length = (dx**2 + dy**2)**0.5
    if length == 0 or arrow.image.width == 0:
        return
    angle = math.atan2(dy, dx)
    arrow.anchor_x = 0
    arrow.anchor_y = arrow.image.height // 2
    arrow.x = x1
    arrow.y = y1
    arrow.rotation = -math.degrees(angle)
    arrow.scale_x = length / arrow.image.width
    arrow.scale_y = width / arrow.image.height
    arrow.opacity = opacity
    arrow.color = (255, 0, 0)
    arrow.draw()

def show_borders(selected_name=None):
    hold_lookup = {h["name"]: (float(h["x_cord"]), float(h["y_cord"])) for h in holds.holds}
    borders_lookup = {h["name"]: set(h.get("borders", "").split("|")) for h in holds.holds}
    for hold in holds.holds:
        name = hold["name"]
        if selected_name and name != selected_name:
            continue
        wx1, wy1 = hold_lookup[name]
        for border_region in borders_lookup[name]:
            border_region = border_region.strip()
            if border_region not in hold_lookup:
                continue
            wx2, wy2 = hold_lookup[border_region]
            if name in borders_lookup.get(border_region, set()):
                colour = (50, 200, 50)
            else:
                colour = (200, 50, 50)
            sx1, sy1 = world_to_screen(wx1, wy1)
            sx2, sy2 = world_to_screen(wx2, wy2)
            draw_line(sx1, sy1, sx2, sy2)
            
@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y

@window.event
def on_draw():
    global scoreboard_pressed, selected_hold, mouse_y, mouse_x
    window.clear()
    background.update(x=-camera_x, y=-camera_y, scale=zoom)
    background.draw()
    
    for m in holds.hold_markers:
        sx, sy = world_to_screen(*m["world"])
        if m["size"] == "large":
            m["sprite"].scale = zoom * 0.125
            m["sprite"].x = sx - 50
            m["sprite"].y = sy - 50
        elif m["size"] == "medium":
            m["sprite"].scale = zoom * 0.075
            m["sprite"].x = sx - 40
            m["sprite"].y = sy - 40
        else:
            m["sprite"].scale = zoom * 0.05
            m["sprite"].x = sx - 30
            m["sprite"].y = sy - 30
        m["sprite"].draw()
        
    holds.show_titles(holds.holds, world_to_screen, zoom, font_name, holds.house_colours)

    debug_text = ''
    for var_name in debug_vars:
        value = globals().get(var_name, 'N/A')
        debug_text += f'{var_name}: {value}\n'
    debug_label.text = debug_text
    debug_label.draw()
    
    if (not scoreboard_pressed) and (not selected_hold):
        turn_control.display_UI(window.width, window.height, font_name, False, turn_counter, False, holds.house_colours, player_house)
    else:
        turn_control.display_UI(window.width, window.height, font_name, False, turn_counter, True, holds.house_colours, player_house)
    
    if scoreboard_pressed:
        scoreboard.open_scoreboard(holds.holds, holds.house_colours, window.width, window.height, font_name)
        return
    
    if selected_hold is not None:
        show_borders(selected_hold["name"])
        if (int(selected_hold["x_cord"]) < (window.width / 2)):
            menu.draw_menu(selected_hold, window.width, window.height, font_name, "right", mouse_x, mouse_y)
        else:
            menu.draw_menu(selected_hold, window.width, window.height, font_name, "left", mouse_x, mouse_y)
        result = menu.get_true_button(selected_hold)
        if result is not None:
            breakpoint
    holds.highlight_hold(window.width, window.height, camera_x, camera_y, zoom, mouse_x, mouse_y, 50, font_name)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global scroll_dx, scroll_dy, zoom
    scroll_dx += scroll_x * 30.0 * camera_speed
    scroll_dy += scroll_y * 30.0 * camera_speed

@window.event
def on_mouse_press(x, y, button, modifiers):
    global dragging, last_mouse_x, last_mouse_y, last_click, selected_hold
    dragging = True
    last_mouse_x, last_mouse_y = x, y
    world_x, world_y = screen_to_world(x, y)
    last_click = (round(world_x, 2), round(world_y, 2))
    
    clicked_hold = None
    if selected_hold:
        if (int(selected_hold["x_cord"]) < (window.width / 2)):
            if menu.is_point_inside(mouse_x, mouse_y, menu.get_menu_rect(window.width, window.height, "right")) or menu.is_point_inside(mouse_x, mouse_y, menu.get_menu_rect(window.width, window.height, "left")):
                clicked_hold = selected_hold
                menu.on_mouse_press()
    
    if not clicked_hold:
        for m in holds.hold_markers:
            sx, sy = world_to_screen(*m["world"])
            sprite = m["sprite"]
            sx1, sy1 = sprite.x, sprite.y
            sx2, sy2 = sx1 + sprite.width, sy1 + sprite.height
            if sx1 <= x <= sx2 and sy1 <= y <= sy2:
                clicked_hold = m["data"]
                break

    if clicked_hold:
        if clicked_hold["house"] == player_house:
            selected_hold = clicked_hold
            return
        else:
            selected_hold = None
    else:
        selected_hold = None
    
    selected_hold = None

    last_turn = turn_counter[0]
    turn_control.handle_mouse_press(x, y, button, modifiers, turn_counter)
    new_turn = turn_counter[0]
    if new_turn == last_turn:
        pass
    elif new_turn == last_turn + 1:
        holds.load_holds(turn_counter)
    else:
        print("ERROR turn counter mishandled, exiting")
        exit(2)
        

@window.event
def on_mouse_release(x, y, button, modifiers):
    global dragging
    dragging = False

def update(dt):
    global camera_x, camera_y, scroll_dx, scroll_dy
    base_speed = 300.0
    dx = dy = 0.0
    if keys[pyglet.window.key.LEFT]:  dx -= 1.0
    if keys[pyglet.window.key.RIGHT]: dx += 1.0
    if keys[pyglet.window.key.UP]:    dy += 1.0
    if keys[pyglet.window.key.DOWN]:  dy += 1.0
    length = math.hypot(dx, dy)
    if length > 0:
        dx /= length; dy /= length
    dx *= base_speed * dt * camera_speed
    dy *= base_speed * dt * camera_speed
    dx += scroll_dx * dt; dy += scroll_dy * dt
    scroll_dx = 0.0; scroll_dy = 0.0
    camera_x += dx; camera_y += dy
    camera_x = max(0.0, min(camera_x, background.width - window.width))
    camera_y = max(0.0, min(camera_y, background.height - window.height))
    
@window.event
def on_key_press(symbol, modifiers):
    global scoreboard_pressed
    if symbol == key.TAB:
        scoreboard_pressed = not scoreboard_pressed

holds.load_holds(turn_counter)
army.army_init()

if CSV_REFRESH_INTERVAL != -1:
    pyglet.clock.schedule_interval(holds.load_holds(turn_counter), CSV_REFRESH_INTERVAL)
pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()
