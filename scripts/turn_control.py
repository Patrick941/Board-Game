import pyglet
import os
import math
from scripts.holds import hold_manager
from typing import List, Dict, Any, Tuple, Optional

class TurnControl:
    def __init__(self):
        self.bar_height = 40
        self.circle_button: Optional[Tuple[float, float, float]] = None
        
        self.bar_color = (200, 180, 150)
        self.circle_color = (180, 150, 120)
        self.circle_hover_color = (200, 170, 140)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(current_dir, '../Images')
        
        self.icons = self._load_icons(images_dir)
    
    def _load_icons(self, images_dir: str) -> Dict[str, Any]:
        icon_files = {
            "food": 'Food.png',
            "wood": 'Wood.png',
            "iron": 'Iron.png',
            "gold": 'Gold.png'
        }
        
        icons = {}
        for name, filename in icon_files.items():
            try:
                path = os.path.join(images_dir, filename)
                icons[name] = pyglet.image.load(path)
            except FileNotFoundError:
                print(f"Warning: Could not load icon {filename}")
                icons[name] = pyglet.image.SolidColorImagePattern((255, 0, 0, 255)).create_image(32, 32)
        
        return icons
    
    def draw_menu_bar(self, window_width: int, window_height: int, font_name: str,
                      turn_counter_ref: List[int], houses: Dict[str, Any],
                      player_house: str, right_selected_hold: Optional[Any]) -> None:
        if right_selected_hold is not None:
            return
            
        self._draw_bar_background(window_width, window_height, houses, player_house)
        self._draw_turn_counter(window_width, window_height, font_name, turn_counter_ref)
        self._draw_resource_icons(window_width, window_height, font_name, player_house)
    
    def _draw_bar_background(self, window_width: int, window_height: int,
                             houses: Dict[str, Any], player_house: str) -> None:
        pyglet.shapes.Rectangle(
            0, window_height - self.bar_height,
            window_width, self.bar_height,
            color=houses[player_house]['colours'][0]
        ).draw()
    
    def _draw_turn_counter(self, window_width: int, window_height: int, font_name: str,
                           turn_counter_ref: List[int]) -> None:
        x_base = window_width * 0.02
        pyglet.text.Label(
            f"Turn: {turn_counter_ref[0]}",
            font_name=font_name,
            font_size=20,
            x=x_base,
            y=window_height - self.bar_height // 2,
            anchor_x="left",
            anchor_y="center",
            color=(0, 0, 0, 255)
        ).draw()
    
    def _draw_resource_icons(self, window_width: int, window_height: int,
                             font_name: str, player_house: str) -> None:
        icons_width = 400
        icons_x_base = window_width * 0.02 + window_width * 0.05
        icon_size = 35
        padding = 10
        
        total_list = hold_manager.get_total_resources(player_house)
        
        for i, (name, sprite_image) in enumerate(self.icons.items()):
            icon_x = icons_x_base + (icons_width / (2 * len(self.icons))) + (i * (icons_width / len(self.icons))) - (icon_size / 2)
            text_x = icon_x - icon_size - padding
            
            self._draw_resource_text(text_x, window_height, font_name, str(total_list[i]))
            self._draw_resource_icon(icon_x, window_height, sprite_image, icon_size)
    
    def _draw_resource_text(self, x: float, window_height: int, font_name: str, text: str) -> None:
        pyglet.text.Label(
            text,
            font_name=font_name,
            font_size=20,
            x=x,
            y=window_height - self.bar_height // 2,
            anchor_x="left",
            anchor_y="center",
            color=(0, 0, 0, 255)
        ).draw()
    
    def _draw_resource_icon(self, x: float, window_height: int,
                            sprite_image: Any, icon_size: int) -> None:
        sprite = pyglet.sprite.Sprite(sprite_image)
        scale = icon_size / max(sprite.image.width, sprite.image.height)
        sprite.scale = scale
        sprite.x = x
        sprite.y = window_height - (self.bar_height * 0.95)
        sprite.draw()
    
    def display_UI(self, window_width: int, window_height: int, font_name: str,
                   is_hovering: bool, turn_counter_ref: List[int], menu_only: bool,
                   houses: Dict[str, Any], player_house: str,
                   right_selected_hold: Optional[Any]) -> None:
        self.draw_menu_bar(window_width, window_height, font_name, turn_counter_ref,
                           houses, player_house, right_selected_hold)
        
        if menu_only:
            return
            
        self._draw_next_turn_button(window_width, window_height, font_name,
                                    is_hovering, houses, player_house)
    
    def _draw_next_turn_button(self, window_width: int, window_height: int,
                               font_name: str, is_hovering: bool,
                               houses: Dict[str, Any], player_house: str) -> None:
        radius = window_width * 0.06
        bx = window_width - radius - 20
        by = radius + 20
        self.circle_button = (bx, by, radius)
        
        circle_col = houses[player_house]['colours'][1] if is_hovering else houses[player_house]['colours'][0]
        circle = pyglet.shapes.Circle(bx, by, radius, color=circle_col)
        circle.draw()
        
        self._draw_button_text(bx, by, font_name)
    
    def _draw_button_text(self, x: float, y: float, font_name: str) -> None:
        pyglet.text.Label(
            "Next Turn",
            font_name=font_name,
            font_size=50,
            x=x,
            y=y,
            anchor_x="center",
            anchor_y="center",
            color=(0, 0, 0)
        ).draw()
    
    def handle_mouse_press(self, x: float, y: float, button: int,
                           modifiers: int, turn_counter_ref: List[int]) -> bool:
        if self.circle_button is None:
            return False
            
        bx, by, radius = self.circle_button
        dist = math.hypot(x - bx, y - by)
        
        if dist <= radius:
            turn_counter_ref[0] += 1
            return True
            
        return False
    
turn_control = TurnControl()