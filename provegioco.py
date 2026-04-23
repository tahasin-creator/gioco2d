import arcade
import random

# info del gioco

LARGHEZZA = 800      # larghezza finestra
ALTEZZA = 600        # altezza finestra
TITOLO = "Flappy Bird Livelli"

GRAVITA = 0.3        # forza che tira giù l'uccello
SALTO = 4            # forza del salto

VELOCITA_TUBI = 2.5  # velocità dei tubi
SPAZIO = 180         # spazio tra tubo sopra e sotto
TUBO_LARGHEZZA = 50  # larghezza dei tubi

OSTACOLI_PER_LIVELLO = 10  # ogni quanti ostacoli si sale di livello

VERDE_TUBI = arcade.color.DARK_GREEN

# CLASSE PRINCIPALE

class Gioco(arcade.Window):

    # funzione che parte all'inizio del gioco
    def __init__(self):
        super().__init__(LARGHEZZA, ALTEZZA, TITOLO)

        self.colore_sfondo = arcade.color.SKY_BLUE
        self.start_screen = True  # schermata iniziale 

        self.setup_variabili()

   # imposta le variabili
    def setup_variabili(self):
        self.player_list = arcade.SpriteList()  # lista giocatore
        self.tubi = arcade.SpriteList()         # lista tubi

        # creazione uccellino
        self.uccello = arcade.SpriteSolidColor(30, 30, arcade.color.YELLOW)
        self.uccello.center_x = 200
        self.uccello.center_y = 300
        self.player_list.append(self.uccello)

        # variabili di gioco
        self.velocita_y = 0
        self.punteggio = 0
        self.livello = 1
        self.vite = 3
        self.ostacoli_passati = 0

        # condizioni del gioco (pausa, game over, ecc.)
        self.game_over = False
        self.paused = False
        self.invincibile = False
        self.game_started = False

        self.invincibile_timer = 0

       # valori che possono cambiare
        self.velocita_tubi = VELOCITA_TUBI
        self.spazio = SPAZIO
        self.tubo_larghezza = TUBO_LARGHEZZA

    # avvia una nuova partita
    def setup(self):
        self.setup_variabili()
        self.start_screen = False

        # crea i primi tubi
        for i in range(3):
            x = LARGHEZZA + i * 300
            self.crea_tubi(x)

    # crea una coppia di tubi (sopra e sotto)
    def crea_tubi(self, x):
        y = random.randint(200, 400)  # posizione casuale del buco

        # tubo basso
        altezza_basso = max(20, y - self.spazio // 2)
        tubo_basso = arcade.SpriteSolidColor(self.tubo_larghezza, altezza_basso, VERDE_TUBI)
        tubo_basso.center_x = x
        tubo_basso.center_y = altezza_basso / 2

        # tubo alto
        altezza_alto = max(20, ALTEZZA - (y + self.spazio // 2))
        tubo_alto = arcade.SpriteSolidColor(self.tubo_larghezza, altezza_alto, VERDE_TUBI)
        tubo_alto.center_x = x
        tubo_alto.center_y = ALTEZZA - (altezza_alto / 2)

        # aggiungo i tubi alla lista
        self.tubi.append(tubo_basso)
        self.tubi.append(tubo_alto)

    # disegna tutto a schermo
    def on_draw(self):
        arcade.set_background_color(self.colore_sfondo)
        self.clear()

        # schermata iniziale
        if self.start_screen:
            arcade.draw_text("FLAPPY BIRD 2.0", 400, 350, arcade.color.WHITE, 40, anchor_x="center")
            arcade.draw_text("Premi INVIO per iniziare", 400, 300, arcade.color.YELLOW, 20, anchor_x="center")
            return

        # disegna tubi
        self.tubi.draw()

        # disegna vite
        for i in range(self.vite):
            arcade.draw_text("❤️", 20 + i * 30, ALTEZZA - 80, arcade.color.RED, 20)

        # punteggio e livello
        arcade.draw_text("Punteggio: " + str(self.punteggio), 20, ALTEZZA - 40, arcade.color.WHITE, 20)
        arcade.draw_text("Livello: " + str(self.livello), 650, ALTEZZA - 40, arcade.color.YELLOW, 20)

        # effetto lampeggio
        if not self.invincibile or int(self.invincibile_timer * 10) % 2 == 0:
            self.player_list.draw()

        # schermata game over
        if self.game_over:
            arcade.draw_text("GAME OVER", 400, 340, arcade.color.RED, 40, anchor_x="center")
            arcade.draw_text("Premi R per ricominciare", 400, 300, arcade.color.WHITE, 20, anchor_x="center")

        # pausa
        if self.paused and not self.game_over:
            arcade.draw_text("PAUSA", 400, 320, arcade.color.YELLOW, 40, anchor_x="center")

    # aggiornamento continuo del gioco
    def on_update(self, dt):

        # se il gioco non è attivo, non fare nulla
        if self.start_screen or self.game_over or self.paused or not self.game_started:
            return

        # gestione invincibilità
        if self.invincibile:
            self.invincibile_timer -= dt
            if self.invincibile_timer <= 0:
                self.invincibile = False

        # gravità
        self.velocita_y = self.velocita_y - GRAVITA
        self.uccello.center_y = self.uccello.center_y + self.velocita_y

        # movimento tubi
        for tubo in self.tubi:
            tubo.center_x = tubo.center_x - self.velocita_tubi

        # rimuove tubi usciti dallo schermo
        for tubo in list(self.tubi):
            if tubo.right < 0:
                tubo.remove_from_sprite_lists()

                # se è un tubo basso, aumenta punteggio
                if tubo.center_y < ALTEZZA / 2:
                    self.ostacoli_passati += 1
                    self.punteggio += 1

                    # aumento difficoltà
                    if self.ostacoli_passati % OSTACOLI_PER_LIVELLO == 0:
                        self.livello += 1
                        self.velocita_tubi += 0.3
                        self.spazio = max(100, self.spazio - 10)
                        self.tubo_larghezza = min(120, self.tubo_larghezza + 2)

        # crea nuovi tubi
        if len(self.tubi) < 6:
            self.crea_tubi(LARGHEZZA + 200)

        # controlla collisioni
        colpito = arcade.check_for_collision_with_list(self.uccello, self.tubi)

        if (len(colpito) > 0 or self.uccello.bottom <= 0 or self.uccello.top >= ALTEZZA) and not self.invincibile:
            self.vite -= 1

            if self.vite > 0:
                # reset posizione
                self.uccello.center_x = 200
                self.uccello.center_y = 300
                self.velocita_y = 0

                # attiva invincibilità temporanea
                self.invincibile = True
                self.invincibile_timer = 2.0
            else:
                self.game_over = True

    # gestione tasti
    def on_key_press(self, key, mod):

        # start
        if self.start_screen and key == arcade.key.ENTER:
            self.setup()

        # primo salto per iniziare
        elif not self.game_started and key == arcade.key.SPACE:
            self.game_started = True
            self.velocita_y = SALTO

        # salto normale
        elif key == arcade.key.SPACE and not self.game_over and not self.paused:
            self.velocita_y = SALTO

        # restart
        elif key == arcade.key.R and self.game_over:
            self.setup()

        # pausa
        elif key == arcade.key.P and not self.game_over and not self.start_screen:
            self.paused = not self.paused


# funzione principale
def main():
    gioco = Gioco()
    arcade.run


main()