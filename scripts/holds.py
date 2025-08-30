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
    "NA": "The Crownlands"
}

holds = []
hold_markers = []

# Load castle images with proper path handling
small_castle_image = pyglet.image.load(os.path.join(images_dir, 'Small_Castle_Icon.png'))
medium_castle_image = pyglet.image.load(os.path.join(images_dir, 'Medium_Castle_Icon.png'))
large_castle_image = pyglet.image.load(os.path.join(images_dir, 'Large_Castle_Icon.png'))

house_colours = {
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

def load_holds(dt=None):
    global holds, hold_markers
    holds = []
    hold_markers = []

    csv_path = os.path.join(data_dir, 'holds.csv')
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            region_name = row.get("region", "")
            house_name = next((house for house, region in house_region.items() if region == region_name), "NA")
            
            h = {
                "name": row.get("name", ""),
                "region": region_name,
                "x_cord": row.get("x_cord", "0"),
                "y_cord": row.get("y_cord", "0"),
                "defense_rating": row.get("defense_rating", "0"),
                "size": row.get("size", "Small"),
                "house": house_name,
                "borders": row.get("borders", ".."),
                "resources": row.get("resources", ".")
            }
            holds.append(h)

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
            sprite.color = house_colours.get(house, (255, 255, 255)) 
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

        colour = house_colours.get(house, (255, 255, 255))

        label = pyglet.text.Label(
            name,
            font_name=font_name,
            font_size=int(30 * zoom),
            x=sx + x_offset,
            y=sy + y_offset,
            anchor_x='center',
            anchor_y='bottom',
            color=(colour[0], colour[1], colour[2], 255)
        )
        label.draw()