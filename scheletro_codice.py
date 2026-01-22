import arcade

# ======================
# COSTANTI
# ======================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Gioco 2D Base"

PLAYER_SPEED = 5
PLAYER_JUMP_SPEED = 12
GRAVITY = 0.6

# ======================
# CLASSE PLAYER
# ======================
class Player(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(40, 60, arcade.color.BLUE)
        self.center_x = 100
        self.center_y = 150

# ======================
# CLASSE PIATTAFORMA
# ======================
class Platform(arcade.SpriteSolidColor):
    def __init__(self, width, height, x, y):
        super().__init__(width, height, arcade.color.BROWN)
        self.center_x = x
        self.center_y = y

# ======================
# CLASSE MONETA
# ======================
class Coin(arcade.SpriteSolidColor):
    def __init__(self, x, y):
        super().__init__(20, 20, arcade.color.GOLD)
        self.center_x = x
        self.center_y = y

# ======================
# FINESTRA DI GIOCO
# ======================
class GameWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Sprite
        self.player = None
        self.platforms = arcade.SpriteList()
        self.coins = arcade.SpriteList()

        # Motore fisico
        self.physics_engine = None

        # Punteggio
        self.score = 0

    # ----------------------
    # SETUP
    # ----------------------
    def setup(self):
        # Player
        self.player = Player()

        # Terreno
        ground = Platform(800, 40, 400, 20)
        self.platforms.append(ground)

        # Piattaforma esempio
        platform = Platform(120, 30, 400, 200)
        self.platforms.append(platform)

        # Moneta esempio
        coin = Coin(400, 250)
        self.coins.append(coin)

        # Fisica
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.platforms,
            gravity_constant=GRAVITY
        )

    # ----------------------
    # DISEGNO
    # ----------------------
    def on_draw(self):
        arcade.start_render()

        self.platforms.draw()
        self.coins.draw()
        self.player.draw()

        arcade.draw_text(
            f"Punti: {self.score}",
            20, SCREEN_HEIGHT - 40,
            arcade.color.BLACK,
            20
        )

    # ----------------------
    # AGGIORNAMENTO
    # ----------------------
    def on_update(self, delta_time):
        self.physics_engine.update()

        # Collisione monete
        coins_hit = arcade.check_for_collision_with_list(
            self.player, self.coins
        )
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1

    # ----------------------
    # INPUT TASTIERA
    # ----------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED
        elif key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0


# ======================
# MAIN
# ======================
def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()