import pyglet
from scripts.holds import hold_manager
from typing import List, Dict, Any

class Scoreboard:
    def __init__(self):
        self.scoreboard_bg_colour = (228, 213, 183, 225)
        self.categories = ["House", "Food", "Wood", "Iron", "Gold", "Total"]
    
    def open_scoreboard(self, holds_arr: List[Dict[str, Any]], houses: Dict[str, Any],
                        window_width: int, window_height: int, font_name: str) -> None:
        menu_width, menu_height, menu_x, menu_y = self._calculate_menu_dimensions(window_width, window_height)
        
        self._draw_background(menu_x, menu_y, menu_width, menu_height)
        self._draw_scoreboard_content(menu_x, menu_y, menu_width, menu_height, houses, font_name)
    
    def _calculate_menu_dimensions(self, window_width: int, window_height: int) -> tuple:
        menu_width = int(window_width * 0.8)
        menu_height = int(window_height * 0.8)
        menu_x = (window_width - menu_width) // 2
        menu_y = (window_height - menu_height) // 2
        return menu_width, menu_height, menu_x, menu_y
    
    def _draw_background(self, menu_x: int, menu_y: int, menu_width: int, menu_height: int) -> None:
        pyglet.shapes.RoundedRectangle(
            menu_x, menu_y, menu_width, menu_height,
            color=self.scoreboard_bg_colour,
            batch=None,
            radius=50
        ).draw()
    
    def _draw_scoreboard_content(self, menu_x: int, menu_y: int, menu_width: int,
                                 menu_height: int, houses: Dict[str, Any], font_name: str) -> None:
        self._draw_category_headers(menu_x, menu_y, menu_width, menu_height, font_name, houses)
        self._draw_house_data(menu_x, menu_y, menu_width, menu_height, houses, font_name)
    
    def _draw_category_headers(self, menu_x: int, menu_y: int, menu_width: int,
                               menu_height: int, font_name: str, houses: Dict[str, Any]) -> None:
        padding = menu_width * ((1) / (len(self.categories))) / 4
        zoom = 1
        
        for cat_idx, category in enumerate(self.categories):
            label_x = menu_x + padding + (menu_width * ((cat_idx) / (len(self.categories))))
            label_y = menu_y + (menu_height * ((len(houses) - 1) / len(houses)))
            
            self._draw_text_label(
                category, font_name, int(60 * zoom),
                label_x, label_y, (255, 255, 255, 255), 'bottom'
            )
    
    def _draw_house_data(self, menu_x: int, menu_y: int, menu_width: int,
                         menu_height: int, houses: Dict[str, Any], font_name: str) -> None:
        padding = menu_width * ((1) / (len(self.categories))) / 4
        zoom = 1
        
        for cat_idx, category in enumerate(self.categories):
            label_x = menu_x + padding + (menu_width * ((cat_idx) / (len(self.categories))))
            
            for house_idx, house in enumerate(houses):
                label_y = menu_y + (menu_height * ((house_idx) / (len(houses) + 1)))
                text = self._get_house_data_text(category, house, houses)
                color = houses[house]['colours'][1]
                
                self._draw_text_label(
                    text, font_name, int(60 * zoom),
                    label_x, label_y, color, 'bottom'
                )
    
    def _get_house_data_text(self, category: str, house: str, houses: Dict[str, Any]) -> str:
        total_list = hold_manager.get_total_resources(house)
        increase_list = hold_manager.get_total_increase(house)
        
        if category == "House":
            return house
        elif category == "Total":
            total = str(sum(total_list))
            increase = str(sum(increase_list))
            return f"{total}/{increase}"
        else:
            category_to_index = {"Food": 0, "Wood": 1, "Iron": 2, "Gold": 3}
            index = category_to_index[category]
            return f"{total_list[index]}/{increase_list[index]}"
    
    def _draw_text_label(self, text: str, font_name: str, font_size: int,
                         x: int, y: int, color: tuple, anchor_y: str = 'center') -> None:
        label = pyglet.text.Label(
            text,
            font_name=font_name,
            font_size=font_size,
            x=x,
            y=y,
            anchor_y=anchor_y,
            color=color
        )
        label.draw()

scoreboard = Scoreboard()