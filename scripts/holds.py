import pyglet
import csv
import os

# Get the directory of this file to handle relative paths correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, '..', 'Images')
data_dir = os.path.join(current_dir, '..', 'data')

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
    "Tyrell": [(150, 255, 150),(150, 255, 150), (0, 0, 0, 0)],
    "Stark": [(200, 200, 200),(240, 240, 240), (0, 0, 0, 0)],
    "Arryn": [(173, 150, 255),(173, 216, 255), (0, 0, 0, 0)],
    "Tully": [(170, 85, 230),(230, 85, 170), (0, 0, 0, 0)],
    "Baratheon": [(255, 255, 100),(255, 255, 100), (0, 0, 0, 0)],
    "Martell": [(255, 165, 50),(255, 165, 50), (0, 0, 0, 0)],
    "Lannister": [(255, 70, 70),(255, 70, 70), (0, 0, 0, 0)],
    "Greyjoy": [(50, 160, 160),(50, 160, 160), (0, 0, 0, 0)],
    "Targaryen": [(100, 100, 100),(00, 00, 00), (0, 0, 0, 0)]
}

def reset_resources():
    for house_idx, (house,colours) in enumerate(house_colours.items()):
        house_colours[house][2] = (0, 0, 0, 0)

def load_holds(dt=None):
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
            
            h = {
                "name": row.get("name", ""),
                "region": region_name,
                "x_cord": row.get("x_cord", "0"),
                "y_cord": row.get("y_cord", "0"),
                "defense_rating": row.get("defense_rating", "0"),
                "size": row.get("size", "Small"),
                "house": house_name,
                "borders": row.get("borders", ".."),
                "food": resources[0],
                "wood": resources[1],
                "iron":resources[2],
                "gold": resources[3]
            }
            holds.append(h)

            for i, resource in enumerate(resources):
                colour_list = list(house_colours[house_name][2])
                colour_list[i] += int(resource)
                house_colours[house_name][2] = tuple(colour_list)

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