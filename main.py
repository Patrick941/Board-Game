import pyglet
import math
import csv

debug_vars = ['camera_x', 'camera_y', 'camera_speed', 'zoom', 'last_click']

window = pyglet.window.Window(fullscreen=True, caption="Board Game")
background_image = pyglet.image.load("Images/Background_out.jpg")
background = pyglet.sprite.Sprite(background_image, x=0.0, y=0.0)

small_castle_image = pyglet.image.load("Images/Small_Castle_Icon.png")
medium_castle_image = pyglet.image.load("Images/Medium_Castle_Icon.png")
large_castle_image = pyglet.image.load("Images/Large_Castle_Icon.png")

camera_x = 0.0
camera_y = 0.0
camera_speed = 300
zoom = 1
min_zoom = 0.465
max_zoom = 3.0

last_click = (0.0, 0.0)

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

dragging = False
last_mouse_x, last_mouse_y = 0, 0
scroll_dx = 0.0
scroll_dy = 0.0

house_region = {
    "Tyrell": "The Reach",
    "Stark": "The North",
    "Arryn": "The Vale",
    "Tully": "The Riverlands",
    "Baratheon": "The Stormlands",
    "Martell": "Dorne",
    "Lannister": "The Westerlands",
    "Greyjoy": "The Iron Islands",
    "NA": "The Crownlands"
}

holds = []
with open("data/holds.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        region_name = row.get("region", "")
        house_name = next((house for house, region in house_region.items() if region == region_name), "NA")
        
        holds.append({
            "name": row.get("name", ""),
            "region": region_name,
            "x_cord": row.get("x_cord", "0"),
            "y_cord": row.get("y_cord", "0"),
            "defense_rating": row.get("defense_rating", "0"),
            "size": row.get("size", "Small"),
            "house": house_name
        })

debug_label = pyglet.text.Label(
    '', 
    font_name='Consolas', 
    font_size=14,
    x=window.width - 10, 
    y=window.height - 10, 
    anchor_x='right', 
    anchor_y='top', 
    multiline=True,
    width=300
)

def screen_to_world(sx, sy):
    return (camera_x + sx / zoom, camera_y + sy / zoom)

def world_to_screen(wx, wy):
    return ((wx - camera_x) * zoom, (wy - camera_y) * zoom)

house_colors = {
    "Tyrell": (150, 255, 150),
    "Stark": (200, 200, 200),
    "Arryn": (173, 216, 255),
    "Tully": (186, 85, 216),
    "Baratheon": (255, 255, 100),
    "Martell": (255, 165, 50),
    "Lannister": (255, 70, 70),
    "Greyjoy": (50, 160, 160),
    "NA": (128, 0, 128)
}

hold_markers = []
for h in holds:
    if all(h.get(k, "NA") != "NA" for k in ("name", "region", "x_cord", "y_cord")):
        try:
            wx = float(h["x_cord"])
            wy = float(h["y_cord"])
        except ValueError:
            continue
        size = h.get("size", "Small").lower()
        if size == "large":
            castle_img = large_castle_image
        elif size == "medium":
            castle_img = medium_castle_image
        else:
            castle_img = small_castle_image
        sprite = pyglet.sprite.Sprite(castle_img, x=0, y=0)
        sprite.scale = 0.5
        
        house = h.get("house", "")
        sprite.color = house_colors.get(house, (255, 255, 255)) 
        
        hold_markers.append({
            "world": (wx, wy),
            "sprite": sprite,
            "data": h,
            "size": size
        })

@window.event
def on_draw():
    window.clear()
    background.update(x=-camera_x, y=-camera_y, scale=zoom)
    background.draw()
    for m in hold_markers:
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

    debug_text = ''
    for var_name in debug_vars:
        value = globals().get(var_name, 'N/A')
        debug_text += f'{var_name}: {value}\n'
    debug_label.text = debug_text
    debug_label.draw()

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global scroll_dx, scroll_dy, zoom
    scroll_dx += scroll_x * 30.0 * camera_speed
    scroll_dy += scroll_y * 30.0 * camera_speed

@window.event
def on_mouse_press(x, y, button, modifiers):
    global dragging, last_mouse_x, last_mouse_y, last_click
    dragging = True
    last_mouse_x, last_mouse_y = x, y
    world_x, world_y = screen_to_world(x, y)
    last_click = (round(world_x, 2), round(world_y, 2))

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
    if keys[pyglet.window.key.DOWN]:  dy -= 1.0
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

pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()
