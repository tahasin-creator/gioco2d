import arcade

# ----------------------
# COSTANTI
# ----------------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Mini Mario Style"

WORLD_WIDTH = 3000

PLAYER_SPEED = 5
PLAYER_JUMP = 15
GRAVITY = 0.7


# ----------------------
# PLAYER
# ----------------------
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        image = arcade.make_soft_square_texture(40, arcade.color.BLUE, 255, 255)
        self.texture = image
        self.width = 40
        self.height = 60
        self.center_x = 200
        self.center_y = 150


# ----------------------
# NEMICO
# ----------------------
class Enemy(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = arcade.make_soft_square_texture(40, arcade.color.RED, 255, 255)
        self.texture = image
        self.width = 40
        self.height = 40
        self.center_x = x
        self.center_y = y
        self.change_x = 2

    def update(self, delta_time=0):
        self.center_x += self.change_x
        if self.center_x <= 20 or self.center_x >= WORLD_WIDTH - 20:
            self.change_x *= -1


# ----------------------
# MONETA
# ----------------------
class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = arcade.make_soft_square_texture(20, arcade.color.YELLOW, 255, 255)
        self.texture = image
        self.width = 20
        self.height = 20
        self.center_x = x
        self.center_y = y


# ----------------------
# GIOCO
# ----------------------
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.coins = arcade.SpriteList()

        # Player
        self.player = Player()
        self.player_list.append(self.player)

        self.physics_engine = None

        # Stato gioco
        self.score = 0
        self.game_over = False
        self.win = False

    # ----------------------
    def setup(self):
        # Terreno
        ground = arcade.SpriteSolidColor(WORLD_WIDTH, 40, arcade.color.DARK_GREEN)
        ground.center_x = WORLD_WIDTH // 2
        ground.center_y = 20
        self.platforms.append(ground)

        # Piattaforme
        for i in range(5):
            platform = arcade.SpriteSolidColor(200, 20, arcade.color.BROWN)
            platform.center_x = 600 + i * 400
            platform.center_y = 200 + i * 50
            self.platforms.append(platform)

        # Nemici
        for i in range(5):
            enemy = Enemy(800 + i * 400, 80)
            self.enemies.append(enemy)

        # Monete sopra piattaforme (evita il terreno)
        for platform in self.platforms:
            if platform.height > 40:  # piattaforme vere
                coin = Coin(platform.center_x, platform.top + 10)
                self.coins.append(coin)

        # Fisica
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.platforms,
            gravity_constant=GRAVITY
        )

    # ----------------------
    def on_draw(self):
        self.clear()

        self.platforms.draw()
        self.coins.draw()
        self.enemies.draw()
        self.player_list.draw()

        arcade.draw_text(
            f"Punteggio: {self.score}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            18
        )

        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.RED,
                40,
                anchor_x="center"
            )

        if self.win:
            arcade.draw_text(
                "HAI VINTO!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.YELLOW,
                40,
                anchor_x="center"
            )

    # ----------------------
    def on_update(self, delta_time):
        if self.game_over or self.win:
            return

        self.physics_engine.update()
        self.enemies.update(delta_time)
        self.player_list.update()

        # Scroll semplice
        if self.player.center_x > SCREEN_WIDTH // 2:
            shift = self.player.center_x - SCREEN_WIDTH // 2
            self.player.center_x = SCREEN_WIDTH // 2
            for sprite_list in [self.platforms, self.enemies, self.coins]:
                for sprite in sprite_list:
                    sprite.center_x -= shift

        # Collisioni monete
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coins)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 10

        # Collisioni nemici
        enemies_hit = arcade.check_for_collision_with_list(self.player, self.enemies)
        for enemy in enemies_hit:
            if self.player.change_y < 0 and self.player.bottom > enemy.center_y:
                enemy.remove_from_sprite_lists()
                self.player.change_y = PLAYER_JUMP
                self.score += 20
            else:
                self.game_over = True

        # Caduta
        if self.player.center_y < 0:
            self.game_over = True

        # Vittoria
        if len(self.enemies) == 0:
            self.win = True

    # ----------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED
        elif key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0


# ----------------------
def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

