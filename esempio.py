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

PLATFORM_SPEED = 3  # 🔥 stessa velocità per tutte

COIN_RESPAWN_TIME = 3

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
# PIATTAFORMA MOBILE
# ------------------
class MovingPlatform(arcade.SpriteSolidColor):
    def __init__(self, x, y):
        super().__init__(PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR)
        self.center_x = x
        self.center_y = y
        self.change_x = PLATFORM_SPEED

    def update(self, delta_time=0):
        self.center_x += self.change_x

        # 🔥 rimbalzo ai bordi dello schermo
        if self.left <= 0 or self.right >= SCREEN_WIDTH:
            self.change_x *= -1

# ------------------
# COIN
# ------------------
class Coin(arcade.Sprite):
    def __init__(self, piattaforma):
        super().__init__(
            "C:/Users/tahasin.mia/Desktop/gioco2d/immagini/coin.jpg",
            scale=0.05
        )
        self.piattaforma = piattaforma
        self.timer = 0
        self.update_position()

    def update_position(self):
        self.center_x = self.piattaforma.center_x
        self.center_y = self.piattaforma.top + self.height / 2

# ------------------
# GAME
# ------------------
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.coins_inattive = []

        self.player = Player()
        self.player_list.append(self.player)

        self.physics_engine = None

        self.score = 0
        self.level = 0
        self.level_text_timer = 0
        self.show_level_text = False

        self.platform_positions = [(300, 150), (500, 250), (650, 350),
                                   (850, 450), (1100, 550)]

    # ------------------
    def setup(self):

        self.background = arcade.load_texture(
            "C:/Users/tahasin.mia/Desktop/gioco2d/immagini/sfondo.webp"
        )

        # Terreno fisso
        ground = arcade.SpriteSolidColor(
            SCREEN_WIDTH, GROUND_HEIGHT, arcade.color.DARK_GREEN
        )
        ground.center_x = SCREEN_WIDTH // 2
        ground.center_y = GROUND_HEIGHT // 2
        self.platforms.append(ground)

        # 🔥 Piattaforme mobili
        for x, y in self.platform_positions:
            platform = MovingPlatform(x, y)
            self.platforms.append(platform)

        # Monete sopra ogni piattaforma mobile
        for p in self.platforms:
            if isinstance(p, MovingPlatform):
                coin = Coin(p)
                self.coins.append(coin)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platforms, gravity_constant=GRAVITY
        )

    # ------------------
    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.platforms.draw()
        self.coins.draw()
        self.player_list.draw()

        arcade.draw_text(
            f"Punteggio: {self.score}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            18
        )

        if self.show_level_text:
            arcade.draw_text(
                f"LEVEL {self.level}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.YELLOW,
                50,
                anchor_x="center",
                anchor_y="center"
            )

    # ------------------
    def on_update(self, delta_time):

        self.platforms.update()
        self.physics_engine.update()

        # Monete seguono le piattaforme
        for coin in self.coins:
            coin.update_position()

        # Collisione monete
        coins_hit = arcade.check_for_collision_with_list(
            self.player, self.coins
        )

        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            coin.timer = 0
            self.coins_inattive.append(coin)
            self.score += 10

            new_level = self.score // 100
            if new_level > self.level:
                self.level = new_level
                self.show_level_text = True
                self.level_text_timer = 0

        # Respawn monete
        for coin in list(self.coins_inattive):
            coin.timer += delta_time
            if coin.timer >= COIN_RESPAWN_TIME:
                coin.update_position()
                self.coins.append(coin)
                self.coins_inattive.remove(coin)

        # Timer testo livello
        if self.show_level_text:
            self.level_text_timer += delta_time
            if self.level_text_timer >= 2:
                self.show_level_text = False

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
def main():
    game = Game()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
