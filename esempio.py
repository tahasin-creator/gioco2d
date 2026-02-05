import arcade

# ------------------
# COSTANTI DI GIOCO
# ------------------
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_COLOR = arcade.color.BLUE
PLAYER_SPEED = 5
PLAYER_JUMP_SPEED = 15

GRAVITY = 0.6

PLATFORM_COLOR = arcade.color.BROWN
PLATFORM_WIDTH = 120
PLATFORM_HEIGHT = 30
GROUND_HEIGHT = 40

COIN_SIZE = 20
COIN_COLOR = arcade.color.GOLD
COIN_RESPAWN_TIME = 3  # secondi

BACKGROUND_COLOR = arcade.color.SKY_BLUE
SCORE_TEXT_COLOR = arcade.color.WHITE
SCORE_TEXT_SIZE = 18

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platformer 2D - Semplice"

# ------------------
# PLAYER
# ------------------
class Player(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)
        self.center_x = 100
        self.center_y = 150

# ------------------
# COIN
# ------------------
class Coin(arcade.Sprite):
    def __init__(self, piattaforma):
        # Usa l'immagine "moneta.png" e scala 1.0 (puoi modificare se troppo grande o piccola)
        super().__init__("C:/Users/tahasin.mia/Desktop/gioco2d/immagini/coin.jpg", scale=0.05)
        
        self.piattaforma = piattaforma
        self.reset_position()
        self.timer = 0
        self.da_respawnare = False

    def reset_position(self):
        # Posiziona la moneta sopra la piattaforma
        self.center_x = self.piattaforma.center_x
        self.center_y = self.piattaforma.top + self.height / 2  # usa l'altezza della sprite

# ------------------
# GAME
# ------------------
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite Lists
        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.coins_inattive = []

        # Player
        self.player = Player()
        self.player_list.append(self.player)

        # Physics
        self.physics_engine = None

        # Score
        self.score = 0

        # Piattaforme
        self.platform_positions = [(300, 150), (500, 250), (650, 350),
                                   (850, 450), (1100, 550), (1400, 650)]

    # ------------------
    # SETUP
    # ------------------
    def setup(self):
        
        self.background = arcade.load_texture("C:/Users/tahasin.mia/Desktop/gioco2d/immagini/sfondo.webp")

        # Terreno
        ground = arcade.SpriteSolidColor(SCREEN_WIDTH, GROUND_HEIGHT, arcade.color.DARK_GREEN)
        ground.center_x = SCREEN_WIDTH // 2
        ground.center_y = GROUND_HEIGHT // 2
        self.platforms.append(ground)

        # Piattaforme
        for x, y in self.platform_positions:
            box = arcade.SpriteSolidColor(PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR)
            box.center_x = x
            box.center_y = y
            self.platforms.append(box)

        # Monete
        for p in self.platforms:
            if p.width < SCREEN_WIDTH:  # esclude il terreno
                coin = Coin(p)
                self.coins.append(coin)

        # Physics Engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platforms, gravity_constant=GRAVITY
        )

    # ------------------
    # DRAW
    # ------------------
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0,0,1280,720)
        )
        self.platforms.draw()
        self.coins.draw()
        self.player_list.draw()

        

        # Punteggio
        arcade.draw_text(f"Punteggio: {self.score}", 20, SCREEN_HEIGHT - 40,
                         SCORE_TEXT_COLOR, SCORE_TEXT_SIZE)

    # ------------------
    # UPDATE
    # ------------------
    def on_update(self, delta_time):
        self.physics_engine.update()

        # Blocca player dentro lo schermo
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.top > SCREEN_HEIGHT:
            self.player.top = SCREEN_HEIGHT

        # Collisione con monete
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coins)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            coin.da_respawnare = True
            coin.timer = 0
            self.coins_inattive.append(coin)
            self.score += 10

        # Respawn monete
        for coin in list(self.coins_inattive):
            coin.timer += delta_time
            if coin.timer >= COIN_RESPAWN_TIME:
                coin.reset_position()
                coin.da_respawnare = False
                coin.timer = 0
                self.coins.append(coin)
                self.coins_inattive.remove(coin)

    # ------------------
    # INPUT
    # ------------------
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

# ------------------
# MAIN
# ------------------
def main():
    game = Game()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
