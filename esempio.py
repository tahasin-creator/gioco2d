import arcade

# Costanti che non cambiano mai
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My First Arcade Window"

def main():
    # Apri la finestra
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    # Imposta lo sfondo
    arcade.set_background_color(arcade.color.SKY_BLUE)
    
    # Inizia a renderizzare
    arcade.start_render()
    
    # Scrivi qualcosa
    arcade.draw_text("Hello, Arcade!", 
                     SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                     arcade.color.WHITE, 40, anchor_x="center")
    
    # Finisci di renderizzare
    arcade.finish_render()
    
    # Fai partire il tutto e mantieni la finestra aperta
    arcade.run()

if __name__ == "__main__":
    main()