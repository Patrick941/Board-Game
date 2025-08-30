import pyglet

scoreboard_bg_colour = (228, 213, 183, 225)

def open_scoreboard(holds, house_region, window_width, window_height, font_name):
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
    
    for house,region in house_region.items():
        print(house)
        