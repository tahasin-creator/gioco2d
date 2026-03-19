import arcade
import random

# ------------------------
# COSTANTI GIOCO
# ------------------------
LARGHEZZA = 800
ALTEZZA = 600
TITOLO = "Flappy Bird Livelli"

GRAVITA = 0.3
SALTO = 4

VELOCITA_TUBI = 2.5
SPAZIO = 180
TUBO_LARGHEZZA = 50

OSTACOLI_PER_LIVELLO = 10

VERDE_TUBI = arcade.color.DARK_GREEN

# ------------------------
# CLASSE GIOCO
# ------------------------
class Gioco(arcade.Window):

    def __init__(self):
        super().__init__(LARGHEZZA, ALTEZZA, TITOLO)

        self.player_list = None
        self.tubi = None
        self.uccello = None

        self.velocita_y = 0
        self.punteggio = 0
        self.livello = 1
        self.game_over = False
        self.paused = False
        self.start_screen = True

        self.ostacoli_passati = 0

        # vite ❤️
        self.vite = 3

        # invincibilità ✨
        self.invincibile = False
        self.invincibile_timer = 0

        # stato gioco
        self.game_started = False

        self.velocita_tubi = VELOCITA_TUBI
        self.spazio = SPAZIO
        self.tubo_larghezza = TUBO_LARGHEZZA

        self.colore_sfondo = arcade.color.SKY_BLUE

    # ------------------------
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.tubi = arcade.SpriteList()

        self.uccello = arcade.SpriteSolidColor(30, 30, arcade.color.YELLOW)
        self.uccello.center_x = 200
        self.uccello.center_y = 300
        self.player_list.append(self.uccello)

        self.punteggio = 0
        self.livello = 1
        self.game_over = False
        self.paused = False
        self.ostacoli_passati = 0

        self.vite = 3

        self.invincibile = False
        self.invincibile_timer = 0

        self.game_started = False

        self.velocita_tubi = VELOCITA_TUBI
        self.spazio = SPAZIO
        self.tubo_larghezza = TUBO_LARGHEZZA

        self.start_screen = False

        for i in range(3):
            self.crea_tubi(LARGHEZZA + i * 300)

    # ------------------------
    def crea_tubi(self, x):
        y_spazio = random.randint(200, 400)

        altezza_basso = max(20, y_spazio - self.spazio // 2)
        tubo_basso = arcade.SpriteSolidColor(
            self.tubo_larghezza,
            altezza_basso,
            VERDE_TUBI
        )
        tubo_basso.center_x = x
        tubo_basso.center_y = altezza_basso / 2

        altezza_alto = max(20, ALTEZZA - (y_spazio + self.spazio // 2))
        tubo_alto = arcade.SpriteSolidColor(
            self.tubo_larghezza,
            altezza_alto,
            VERDE_TUBI
        )
        tubo_alto.center_x = x
        tubo_alto.center_y = ALTEZZA - (altezza_alto / 2)

        self.tubi.append(tubo_basso)
        self.tubi.append(tubo_alto)

    # ------------------------
    def on_draw(self):
        arcade.set_background_color(self.colore_sfondo)
        self.clear()

        # schermata iniziale
        if self.start_screen:
            arcade.draw_text(
                "FLAPPY BIRD 2.0",
                LARGHEZZA / 2,
                ALTEZZA / 2 + 50,
                arcade.color.WHITE,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                "Premi INVIO per iniziare",
                LARGHEZZA / 2,
                ALTEZZA / 2,
                arcade.color.YELLOW,
                20,
                anchor_x="center"
            )
            return

        # gioco
        self.tubi.draw()

        # vite ❤️
        for i in range(self.vite):
            arcade.draw_text(
                "❤️",
                20 + i * 30,
                ALTEZZA - 80,
                arcade.color.RED,
                20
            )

        arcade.draw_text(f"Punteggio: {self.punteggio}", 20, ALTEZZA - 40, arcade.color.WHITE, 20)
        arcade.draw_text(f"Livello: {self.livello}", 650, ALTEZZA - 40, arcade.color.YELLOW, 20)

        # lampeggio uccellino
        if not self.invincibile or int(self.invincibile_timer * 10) % 2 == 0:
            self.player_list.draw()

        if self.game_over:
            arcade.draw_text("GAME OVER", LARGHEZZA / 2, ALTEZZA / 2 + 40,
                             arcade.color.RED, 40, anchor_x="center")
            arcade.draw_text("Premi R per ricominciare", LARGHEZZA / 2, ALTEZZA / 2,
                             arcade.color.WHITE, 20, anchor_x="center")

        if self.paused and not self.game_over:
            arcade.draw_text("PAUSA", LARGHEZZA / 2, ALTEZZA / 2 + 20,
                             arcade.color.YELLOW, 40, anchor_x="center")

    # ------------------------
    def on_update(self, delta_time):
        if self.start_screen or self.game_over or self.paused or not self.game_started:
            return

        # invincibilità
        if self.invincibile:
            self.invincibile_timer -= delta_time
            if self.invincibile_timer <= 0:
                self.invincibile = False

        # fisica
        self.velocita_y -= GRAVITA
        self.uccello.center_y += self.velocita_y

        # movimento tubi
        for tubo in self.tubi:
            tubo.center_x -= self.velocita_tubi

        # rimozione tubi
        for tubo in list(self.tubi):
            if tubo.right < 0:
                tubo.remove_from_sprite_lists()
                if tubo.center_y < ALTEZZA / 2:
                    self.ostacoli_passati += 1
                    self.punteggio += 1

                    if self.ostacoli_passati % OSTACOLI_PER_LIVELLO == 0:
                        self.livello += 1
                        self.velocita_tubi += 0.3
                        self.spazio = max(100, self.spazio - 10)
                        self.tubo_larghezza = min(120, self.tubo_larghezza + 2)

        if len(self.tubi) < 6:
            self.crea_tubi(LARGHEZZA + 200)

        # collisioni
        colpito = arcade.check_for_collision_with_list(self.uccello, self.tubi)

        if (len(colpito) > 0 or self.uccello.bottom <= 0 or self.uccello.top >= ALTEZZA) and not self.invincibile:
            self.vite -= 1

            if self.vite > 0:
                self.uccello.center_x = 200
                self.uccello.center_y = 300
                self.velocita_y = 0

                self.invincibile = True
                self.invincibile_timer = 2.0
            else:
                self.game_over = True

    # ------------------------
    def on_key_press(self, key, modifiers):

        # start screen
        if self.start_screen and key == arcade.key.ENTER:
            self.setup()
            return

        # avvio gioco con SPAZIO
        if not self.start_screen and not self.game_started and key == arcade.key.SPACE:
            self.game_started = True
            self.velocita_y = SALTO
            return

        # salto
        if key == arcade.key.SPACE and self.game_started and not self.game_over and not self.paused:
            self.velocita_y = SALTO

        # restart
        if key == arcade.key.R and self.game_over:
            self.setup()

        # pausa
        if key == arcade.key.P and not self.game_over and not self.start_screen:
            self.paused = not self.paused


# ------------------------
# MAIN
# ------------------------
def main():
    gioco = Gioco()
    arcade.run()

main()