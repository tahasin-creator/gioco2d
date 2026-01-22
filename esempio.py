import arcade

# Costanti
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Platformer 2D - Scatole e Monete"

PLAYER_SPEED = 5
JUMP_SPEED = 12
GRAVITY = 0.6

class Player(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(40, 60, arcade.color.BLUE)
        self.center_x = 100
        self.center_y = 150
        self.change_y = 0

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player = Player()
        self.platforms = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.playerSpriteList = arcade.SpriteList()

        self.score = 0
        self.physics_engine = None
        self.score_text = None  # Testo del punteggio

    def setup(self):
        # Terreno
        ground = arcade.SpriteSolidColor(800, 40, arcade.color.DARK_GREEN)
        ground.center_x = 400
        ground.center_y = 20
        self.platforms.append(ground)

        # Scatole / piattaforme
        positions = [(300, 150), (500, 250), (650, 350)]
        for x, y in positions:
            box = arcade.SpriteSolidColor(120, 30, arcade.color.BROWN)
            box.center_x = x
            box.center_y = y
            self.platforms.append(box)

        # Monete
        for x, y in positions:
            coin = arcade.SpriteSolidColor(20, 20, arcade.color.GOLD)
            coin.center_x = x
            coin.center_y = y + 40
            self.coins.append(coin)

        # Motore fisico
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platforms, gravity_constant=GRAVITY
        )

        # Aggiungiamo player alla SpriteList
        self.playerSpriteList.append(self.player)

        # Testo del punteggio
        self.score_text = arcade.Text(
            text=f"Punteggio: {self.score}",
            x=20,
            y=SCREEN_HEIGHT - 40,
        )

    def on_draw(self):
        self.clear()
        self.platforms.draw()
        self.coins.draw()
        self.playerSpriteList.draw()

        # Aggiorniamo il punteggio e lo disegniamo
        self.score_text.text = f"Punteggio: {self.score}"
        self.score_text.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()

        # Collisione con monete
        coins_hit = arcade.check_for_collision_with_list(
            self.player, self.coins
        )
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 10

    # ----------------------------
    # MOVIMENTO A DESTRA/SINISTRA
    # ----------------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED
        elif key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0

def main():
    game = Game()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
