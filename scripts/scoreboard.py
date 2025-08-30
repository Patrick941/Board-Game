import pyglet

scoreboard_bg_colour = (228, 213, 183, 225)

def open_scoreboard(holds, house_colours, window_width, window_height, font_name):
    menu_width = int(window_width * 0.8)
    menu_height = int(window_height * 0.8)
    menu_x = (window_width - menu_width) // 2
    menu_y = (window_height - menu_height) // 2
    
    pyglet.shapes.RoundedRectangle(
        menu_x, menu_y, menu_width, menu_height,
        color=scoreboard_bg_colour,
        batch=None,
        radius=50
    ).draw()
    
    categories = ["House", "Food", "Wood", "Iron", "Gold", "Total"]

    padding = menu_width * ((1) / (len(categories))) / 4
    zoom = 1
    for cat_idx, category in enumerate(categories):
        label_x = menu_x + padding + (menu_width * ((cat_idx) / (len(categories))))
        label_y = menu_y + (menu_height * ((len(house_colours) - 1) / len(house_colours)))
        label = pyglet.text.Label(
            category,
            font_name=font_name,
            font_size=int(60 * zoom),
            x=label_x,
            y=label_y,
            anchor_y='bottom',
            color=(255, 255, 255, 255)
        )
        label.draw()
    
        for house_idx, (house,colours) in enumerate(house_colours.items()):
            label_y = menu_y + (menu_height * ((house_idx) / (len(house_colours) + 1)) )
            if category == "House": text = house
            elif category == "Total": text = str(house_colours[house][2][0] + house_colours[house][2][1] + house_colours[house][2][2] + house_colours[house][2][3])
            else:  text = str(house_colours[house][2][cat_idx - 1])
            label = pyglet.text.Label(
                text,
                font_name=font_name,
                font_size=int(60 * zoom),
                x=label_x,
                y=label_y,
                anchor_y='bottom',
                color=colours[1]
            )
            label.draw()
        