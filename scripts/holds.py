import pyglet
import csv
import os
from scripts import army
from pyglet import shapes

current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, '..', 'Images')
data_dir = os.path.join(current_dir, '..', 'data')
menu_bg_color = (228, 213, 183)

icons = {
    "food": pyglet.image.load(os.path.join(images_dir, 'Food.png')),
    "wood": pyglet.image.load(os.path.join(images_dir, 'Wood.png')),
    "iron": pyglet.image.load(os.path.join(images_dir, 'Iron.png')),
    "gold": pyglet.image.load(os.path.join(images_dir, 'Gold.png'))
}

house_region = {
    "Tyrell": "The Reach",
    "Stark": "The North",
    "Arryn": "The Vale",
    "Tully": "The Riverlands",
    "Baratheon": "The Stormlands",
    "Martell": "Dorne",
    "Lannister": "The Westerlands",
    "Greyjoy": "The Iron Islands",
    "Targaryen": "The Crownlands"
}

holds = []
hold_markers = []

# Load castle images with proper path handling
small_castle_image = pyglet.image.load(os.path.join(images_dir, 'Small_Castle_Icon.png'))
medium_castle_image = pyglet.image.load(os.path.join(images_dir, 'Medium_Castle_Icon.png'))
large_castle_image = pyglet.image.load(os.path.join(images_dir, 'Large_Castle_Icon.png'))

house_colours = {
    "Tyrell": [(150, 255, 150),(150, 255, 150), (0, 0, 0, 0), (0, 0, 0, 0)],
    "Stark": [(200, 200, 200),(240, 240, 240), (0, 0, 0, 0), (0, 0, 0, 0)],
    "Arryn": [(173, 150, 255),(173, 216, 255), (0, 0, 0, 0), (0, 0, 0, 0)],
    "Tully": [(170, 85, 230),(230, 85, 170), (0, 0, 0, 0), (0, 0, 0, 0)],
    "Baratheon": [(255, 255, 100),(255, 255, 100), (0, 0, 0, 0), (0, 0, 0, 0)],
    "Martell": [(255, 165, 50),(255, 165, 50), (0, 0, 0, 0), (0, 0, 0, 0)],
    "Lannister": [(255, 70, 70),(255, 70, 70), (0, 0, 0, 0), (0, 0, 0, 0)],
    "Greyjoy": [(50, 160, 160),(50, 160, 160), (0, 0, 0, 0), (0, 0, 0, 0)],
    "Targaryen": [(100, 100, 100),(00, 00, 00), (0, 0, 0, 0), (0, 0, 0, 0)]
}

def reset_resources():
    for house_idx, (house,colours) in enumerate(house_colours.items()):
        house_colours[house][2] = (0, 0, 0, 0)

def load_holds(turn_counter):
    global holds, hold_markers
    holds = []
    hold_markers = []

    reset_resources()
    csv_path = os.path.join(data_dir, 'holds.csv')
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            region_name = row.get("region", "")
            house_name = next((house for house, region in house_region.items() if region == region_name), "NA")
            resources_string = row.get("resources")
            resources = resources_string.split("|")
            size = row.get("size", "Small")
            if size == "Small":
                multiplier = 1
            elif size == "Medium":
                multiplier = 2
            elif size == "Large":
                multiplier = 4
            else:
                print("ERROR invalid castle size, exiting")
                exit(2)
                
            for i, resource in enumerate(resources):
                resources[i] = str(int(resources[i]) * multiplier)
            
            h = {
                "name": row.get("name", ""),
                "region": region_name,
                "x_cord": row.get("x_cord", "0"),
                "y_cord": row.get("y_cord", "0"),
                "defense_rating": row.get("defense_rating", "0"),
                "size": size,
                "house": house_name,
                "borders": row.get("borders", ".."),
                "food": resources[0],
                "wood": resources[1],
                "iron":resources[2],
                "gold": resources[3]
            }
            holds.append(h)

            for i, resource in enumerate(resources):
                increase_list = list(house_colours[house_name][2])
                increase_list[i] += int(resource)
                house_colours[house_name][2] = tuple(increase_list)
                
        for house, colours in house_colours.items():
            for i, resource in enumerate(resources):
                total_list = list(house_colours[house][3])
                increase_list = list(house_colours[house][2])
                total_list[i] += increase_list[i]
                house_colours[house][3] = tuple(total_list)

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
            sprite.color = house_colours[house][0]
            hold_markers.append({
                "world": (wx, wy),
                "sprite": sprite,
                "data": h,
                "size": size
            })

def show_titles(holds, world_to_screen, zoom, font_name, house_colours):
    for hold in holds:
        name = hold["name"]
        size = hold.get("size", "Small").lower()
        house = hold.get("house", "NA")

        try:
            wx = float(hold["x_cord"])
            wy = float(hold["y_cord"])
        except ValueError:
            continue

        sx, sy = world_to_screen(wx, wy)
        x_offset = 0
        if size == "large":
            y_offset = 65
            x_offset = 15
        elif size == "medium":
            y_offset = 35
        else:
            y_offset = 30

        colour = house_colours[house][1]

        label = pyglet.text.Label(
            name,
            font_name=font_name,
            font_size=int(30 * zoom),
            x=sx + x_offset,
            y=sy + y_offset,
            anchor_x='center',
            anchor_y='bottom',
            color=colour
        )
        label.draw()
        
def highlight_hold(window_width, window_height, camera_x, camera_y, zoom, mouse_x, mouse_y, tolerance, font_name):
    for hold in holds:
        x = int(hold["x_cord"])
        y = int(hold["y_cord"])
        dx = mouse_x - x
        dy = mouse_y - y
        distance = (dx**2 + dy**2)**0.5
        if (distance < tolerance):
            army.show_units(house_region, hold, window_width, window_height, camera_x, camera_y, zoom)
            
            
            icon_size = 40
            icons_width = icon_size * 8
            bg_width = icons_width + (icon_size / 2)
            bg_height = 50
            bg_x = x - (bg_width / 2)
            bg_y = y - (bg_height) - 5

            background_rect = shapes.RoundedRectangle(
                x=bg_x - (icon_size / 2), 
                y=bg_y, 
                width=bg_width, 
                height=bg_height, 
                color=menu_bg_color,
                radius=20
            )
            background_rect.draw()

            for i, (name, sprite_image) in enumerate(icons.items()):
                icon_x = x - (icons_width / 2) + (icons_width / (2 * len(icons))) + (i * (icons_width / len(icons))) - (icon_size / 2)
                text_x = icon_x - icon_size
                text_string = hold[name]
                
                sprite = pyglet.sprite.Sprite(sprite_image)
                scale = icon_size / max(sprite.image.width, sprite.image.height)
                sprite.scale = scale
                sprite.x = icon_x
                sprite.y = y - 50
                sprite.draw()
                
                pyglet.text.Label(
                    text_string,
                    font_name=font_name,
                    font_size=30,
                    x=text_x,
                    y=y - 50,
                    anchor_x="left",
                    anchor_y="bottom",
                    color=house_colours[hold["house"]][1]
                ).draw()