import arcade
import random

class MyGame(arcade.Window):
    
    def __init__(self, width, height, title):
        # Ignorare per il momento
        super().__init__(width, height, title)
        
        # ATTRIBUTI -> lo stato del nostro gioco
        self.rect_x = width // 2  #  X  (centro)
        self.rect_y = height // 2  # Y  (centro)
        self.rect_size = 50  # Dimensione iniziale
        self.rect_color = arcade.color.RED  # Colore iniziale
        
        # Lista di colori
        self.color_list = [
            arcade.color.RED,
            arcade.color.BLUE,
            arcade.color.GREEN,
            arcade.color.YELLOW,
            arcade.color.PURPLE,
            arcade.color.ORANGE,
            arcade.color.PINK,
            arcade.color.TURQUOISE
        ]
        
        # Imposta lo sfondo
        arcade.set_background_color(arcade.color.DARK_BLUE)
    
    # Chiamato ad ogni frame. delta_time di solito è 1/60 di secondo. 
    # In questo metodo qui "ridisegnamo" lo schermo
    def on_draw(self):
        # Pulisci lo schermo
        self.clear()
        
        # Disegna un rettangolo
        arcade.draw_rect_filled(
            arcade.XYWH( 
                self.rect_x, 
                self.rect_y,
                self.rect_size,  # width
                self.rect_size,  # height
            ),
            self.rect_color
        )
        
        # Disegna le scritte
        arcade.draw_text(
            "Premi SPAZIO!",
            10, self.height - 30,
            arcade.color.WHITE, 14
        )
        
        arcade.draw_text(
            f"Dim: {self.rect_size}",
            10, self.height - 55,
            arcade.color.WHITE, 14
        )

    # Chiamato ad ogni frame. delta_time di solito è 1/60 di secondo  
    # In questa sezione mettiamo la LOGICA del gioco  
    def on_update(self, delta_time):
        # Aumenta la dimensione del rettangolo
        self.rect_size += 0.5
        
        # Resetta la dimensione se è troppo grande
        if self.rect_size > 400:
            self.rect_size = 50

    # Chiamato automaticamente quando un tasto viene premuto.
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.rect_color = random.choice(self.color_list)
            print(f"Colore cambiato! Nuovo colore: {self.rect_color}")


def run_game():
    # Crea un'istanza di un oggetto "MyGame", la dimensione della finestra è 
    game = MyGame(800, 900, "Disco rettangolo")
    # Avvia il gioco    
    arcade.run()

if __name__ == "__main__":
    run_game()

