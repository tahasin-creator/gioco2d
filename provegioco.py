import arcade
import random

# ------------------------
# COSTANTI GIOCO
# ------------------------
LARGHEZZA = 800
ALTEZZA = 600
TITOLO = "Flappy Bird Livelli"

GRAVITA = 0.3        # uccellino più lento
SALTO = 4            # salto ridotto

VELOCITA_TUBI = 2.5  # ostacoli più lenti
SPAZIO = 180
TUBO_LARGHEZZA = 50  # ostacoli più stretti

OSTACOLI_PER_LIVELLO = 10

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
        self.paused = False  # variabile pausa
        self.ostacoli_passati = 0

    # ------------------------
    # SETUP INIZIALE
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

        for i in range(3):
            self.crea_tubi(LARGHEZZA + i * 300)

    # ------------------------
    # CREA TUBI
    # ------------------------
    def crea_tubi(self, x):
        y_spazio = random.randint(200, 400)

        altezza_basso = y_spazio - SPAZIO // 2
        tubo_basso = arcade.SpriteSolidColor(TUBO_LARGHEZZA, altezza_basso, arcade.color.GREEN)
        tubo_basso.center_x = x
        tubo_basso.center_y = altezza_basso / 2

        altezza_alto = ALTEZZA - (y_spazio + SPAZIO // 2)
        tubo_alto = arcade.SpriteSolidColor(TUBO_LARGHEZZA, altezza_alto, arcade.color.GREEN)
        tubo_alto.center_x = x
        tubo_alto.center_y = y_spazio + SPAZIO // 2 + altezza_alto / 2

        self.tubi.append(tubo_basso)
        self.tubi.append(tubo_alto)

    # ------------------------
    # DISEGNO
    # ------------------------
    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.tubi.draw()

        arcade.draw_text(
            f"Punteggio: {self.punteggio}",
            20,
            ALTEZZA - 40,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            f"Livello: {self.livello}",
            700,
            ALTEZZA - 40,
            arcade.color.YELLOW,
            20
        )

        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                LARGHEZZA / 2,
                ALTEZZA / 2 + 40,
                arcade.color.RED,
                40,
                anchor_x="center"
            )
            arcade.draw_text(
                "Premi R per ricominciare",
                LARGHEZZA / 2,
                ALTEZZA / 2,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

        if self.paused and not self.game_over:
            arcade.draw_text(
                "PAUSA",
                LARGHEZZA / 2,
                ALTEZZA / 2 + 20,
                arcade.color.YELLOW,
                40,
                anchor_x="center"
            )
            arcade.draw_text(
                "Premi P per riprendere",
                LARGHEZZA / 2,
                ALTEZZA / 2 - 20,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

    # ------------------------
    # LOGICA
    # ------------------------
    def on_update(self, delta_time):
        if self.game_over or self.paused:
            return  # ferma tutto se game over o in pausa

        # gravità
        self.velocita_y -= GRAVITA
        self.uccello.center_y += self.velocita_y

        # movimento ostacoli
        for tubo in self.tubi:
            tubo.center_x -= VELOCITA_TUBI

        # rimuovi ostacoli fuori schermo e aggiorna punteggio
        for tubo in list(self.tubi):
            if tubo.right < 0:
                tubo.remove_from_sprite_lists()
                if tubo.center_y < ALTEZZA / 2:
                    self.ostacoli_passati += 1
                    self.punteggio += 1
                    if self.ostacoli_passati % OSTACOLI_PER_LIVELLO == 0:
                        self.livello += 1

        # crea nuovi tubi se necessario
        if len(self.tubi) < 6:
            self.crea_tubi(LARGHEZZA + 200)

        # collisioni
        colpito = arcade.check_for_collision_with_list(self.uccello, self.tubi)
        if len(colpito) > 0 or self.uccello.bottom <= 0 or self.uccello.top >= ALTEZZA:
            self.game_over = True

    # ------------------------
    # CONTROLLI
    # ------------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and not self.game_over and not self.paused:
            self.velocita_y = SALTO
        if key == arcade.key.R and self.game_over:
            self.setup()
        if key == arcade.key.P and not self.game_over:
            self.paused = not self.paused  # toggle pausa


# ------------------------
# MAIN
# ------------------------
def main():
    gioco = Gioco()
    gioco.setup()
    arcade.run()


main()