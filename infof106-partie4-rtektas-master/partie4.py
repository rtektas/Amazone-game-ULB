
"""
projet Jeu des amazones : partie4:
La quatrième partie de ce projet consiste à réaliser une interface (PyQt5) et
améliorer l’IA grâce à une ou plusieurs fonctions heuristiques.
matricule:000495364
Auteur: Tektas Resul
Date: 07-04-21
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pygame
from pygame import mixer
from amazons import *
from action import Action
from pos2d import Pos2D
from players import HumanPlayer, AIPlayer
from const import PLAYER_1, PLAYER_2, EMPTY, ARROW

pygame.init()
global musique
musique ='menu.wav'
try:
    mixer.music.load(musique)
    mixer.music.play(-1)
except Exception:
    # fichier audio manquant ou erreur d'initialisation audio -> ignorer
    pass
try:
    click = mixer.Sound('click.wav')
except Exception:
    class _DummySound:
        def play(self, *a, **k):
            return
    click = _DummySound()
global image
image = 'choix3.png'


def play():
    """
    cette fonction permet de jouer de la musique
    """
    click.play()
    mixer.music.load(musique)
    mixer.music.play(-1)

def pause():
    """
    cette fonction permet de mettre en pause la musique
    """
    click.play()
    mixer.music.pause()


class fenetreMenu(QWidget):
    """
    cette clase est la fenêtre du menu
    """

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
            super().__init__()
            # taille de la fenetre
            self.setFixedSize(1400, 886)
            self.form = QFormLayout()
            # image d'origine
            self.pic = QImage('amazone.jpg')
            self.setWindowTitle("Game of the amazons: settler vs native")

            pic = self.pic
            # affiche l'image de fond
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(pic))
            self.setPalette(palette)


            # bouton 1
            self.button = QPushButton('JOUER', self)
            self.button.setToolTip('Clickez ici')
            self.button.setStyleSheet('background-color: #C13A1C')
            self.button.setGeometry(500, 200, 200, 50)
            self.button.setFont(QFont("arial", 20, QFont.Bold))
            self.button.clicked.connect(self.test)

            # bouton 2
            self.button2 = QPushButton('QUITTER', self)
            self.button2.setToolTip('Clickez ici')
            self.button2.setStyleSheet('background-color: #DEB116')
            self.button2.setGeometry(500, 400, 200, 50)
            self.button2.setFont(QFont("arial", 20, QFont.Bold))
            self.button2.clicked.connect(QApplication.instance().quit)

            # bouton 3
            self.button3 = QPushButton('THÈME', self)
            self.button3.setToolTip('Clickez ici')
            self.button3.setStyleSheet('background-color: #FF9400')
            self.button3.setGeometry(500, 300, 200, 50)
            self.button3.setFont(QFont("arial", 20, QFont.Bold))
            self.button3.clicked.connect(self.theme)

            #groupbox de musique
            self.widget = QWidget(self)
            self.main_vbox = QVBoxLayout()
            self.settings_groupbox = QGroupBox('musique :')
            self.settings_groupbox.setFont(QFont("arial", 15, QFont.Bold))
            self.settings_groupbox.setStyleSheet('color: #C13A1C')
            self.settings_grid = QGridLayout()
            self.settings_groupbox.setLayout(self.settings_grid)

            #play
            label = QLabel('play:')
            label.setFont(QFont("arial", 15, QFont.Bold))
            self.settings_grid.addWidget(label, 0, 0, alignment=Qt.AlignRight)
            self.playbutton = QPushButton()
            self.playbutton.setIcon(QIcon("play.png"))
            self.playbutton.setStyleSheet('background-color: #DEB116')
            self.playbutton.setMaximumWidth(45)
            self.playbutton.setMaximumHeight(30)
            self.playbutton.clicked.connect(play)
            self.settings_grid.addWidget(self.playbutton, 0, 1)

            #pause
            label = QLabel('pause:')
            label.setFont(QFont("arial", 15, QFont.Bold))
            self.settings_grid.addWidget(label, 1, 0, alignment=Qt.AlignRight)
            self.pausebutton = QPushButton()
            self.pausebutton.setIcon(QIcon("pause.png"))
            self.pausebutton.setStyleSheet('background-color: #DEB116')
            self.pausebutton.setMaximumWidth(45)
            self.pausebutton.setMaximumHeight(30)
            self.pausebutton.clicked.connect(pause)
            self.settings_grid.addWidget(self.pausebutton, 1, 1)

            self.main_vbox.addWidget(self.settings_groupbox)
            self.widget.setLayout(self.main_vbox)

            # groupbox de thème

            self.choix = QWidget(self)
            self.box = QVBoxLayout()

            self.parametre = QGroupBox('choix 1 :')
            self.parametre.setFont(QFont("arial", 30, QFont.Bold))
            self.parametre.setStyleSheet('color: #C13A1C')
            self.settings = QGridLayout()
            self.parametre.setLayout(self.settings)
            self.choix.move(50, 300)

            self.choix1 = QLabel('1 :')
            self.choix1.setStyleSheet("border-top: 1px solid #DEB116; \
                                            border-left: 1px solid #DEB116; \
                                            border-right: 1px solid #DEB116;\
                                            border-bottom: 2px solid #DEB116;")
            self.choix1.setFont(QFont("arial", 15, QFont.Bold))
            self.pixmap = QPixmap('choix1.png').scaledToWidth(300)
            self.choix1.setPixmap(self.pixmap)

            self.settings.addWidget(self.choix1, 1, 0, alignment=Qt.AlignRight)
            self.bouton_choix = QPushButton()
            self.bouton_choix.setIcon(QIcon("coche.svg"))
            self.bouton_choix.setStyleSheet('background-color: #DEB116')
            self.bouton_choix.setMaximumWidth(45)
            self.bouton_choix.setMaximumHeight(30)
            self.bouton_choix.clicked.connect(self.revenir_theme)
            self.settings.addWidget(self.bouton_choix, 1, 1)
            self.box.addWidget(self.parametre)
            self.choix.setLayout(self.box)
            self.choix.setVisible(False)

            # groupbox de thème 2

            self.choix2 = QWidget(self)
            self.box2 = QVBoxLayout()

            self.parametre2 = QGroupBox('choix 2 :')
            self.parametre2.setFont(QFont("arial", 30, QFont.Bold))
            self.parametre2.setStyleSheet('color: #C13A1C')
            self.settings2 = QGridLayout()
            self.parametre2.setLayout(self.settings2)
            self.choix2.move(500, 300)

            self.choix_label = QLabel('1 :')
            self.choix2.setFont(QFont("arial", 15, QFont.Bold))
            self.pixmap2 = QPixmap('choix2.png').scaledToWidth(300)
            self.choix_label.setPixmap(self.pixmap2)
            self.choix_label.setStyleSheet("border-top: 1px solid #DEB116; \
                                                            border-left: 1px solid #DEB116; \
                                                            border-right: 1px solid #DEB116;\
                                                            border-bottom: 2px solid #DEB116;")

            self.settings2.addWidget(self.choix_label, 1, 0, alignment=Qt.AlignRight)
            self.bouton_choix2 = QPushButton()
            self.bouton_choix2.setIcon(QIcon("coche.svg"))
            self.bouton_choix2.setStyleSheet('background-color: #DEB116')
            self.bouton_choix2.setMaximumWidth(45)
            self.bouton_choix2.setMaximumHeight(30)
            self.bouton_choix2.clicked.connect(self.revenir_theme2)

            self.settings2.addWidget(self.bouton_choix2, 1, 1)
            self.box2.addWidget(self.parametre2)
            self.choix2.setLayout(self.box2)
            self.choix2.setVisible(False)

            # groupbox de thème 3

            self.choix3 = QWidget(self)
            self.box3 = QVBoxLayout()

            self.parametre3 = QGroupBox('choix 3 :')
            self.parametre3.setFont(QFont("arial", 30, QFont.Bold))
            self.parametre3.setStyleSheet('color: #C13A1C')
            self.settings3 = QGridLayout()
            self.parametre3.setLayout(self.settings3)
            self.choix3.move(950, 300)

            self.choix_label2 = QLabel('1 :')
            self.choix3.setFont(QFont("arial", 15, QFont.Bold))
            self.pixmap3 = QPixmap('choix3.png').scaledToWidth(300)
            self.choix_label2.setPixmap(self.pixmap3)
            self.choix_label2.setStyleSheet("border-top: 1px solid #DEB116; \
                                                                    border-left: 1px solid #DEB116; \
                                                                    border-right: 1px solid #DEB116;\
                                                                    border-bottom: 2px solid #DEB116;")
            self.settings3.addWidget(self.choix_label2, 1, 0, alignment=Qt.AlignBottom)
            self.bouton_choix3 = QPushButton()
            self.bouton_choix3.setIcon(QIcon("coche.svg"))
            self.bouton_choix3.setStyleSheet('background-color: #DEB116')
            self.bouton_choix3.setMaximumWidth(45)
            self.bouton_choix3.setMaximumHeight(30)
            self.bouton_choix3.clicked.connect(self.revenir_theme3)

            self.settings3.addWidget(self.bouton_choix3, 1, 1)
            self.box3.addWidget(self.parametre3)
            self.choix3.setLayout(self.box3)
            self.choix3.setVisible(False)

    def test(self):
        """
        cette fonction permet d'apeller deux autres fonctions
        """
        click.play()
        self.a = fenetreJeu()
        mixer.music.stop()
        self.close()
        mixer.music.load('fond.wav')
        mixer.music.play(-1)


    def theme(self):
        """
        cette fonction permet de cacher le menu quand on appuye sur le bouton "theme" pour faire apparaître les
        thèmes
        """
        click.play()
        self.button.setVisible(False)
        self.button2.setVisible(False)
        self.button3.setVisible(False)
        self.choix.setVisible(True)
        self.choix2.setVisible(True)
        self.choix3.setVisible(True)


    def revenir_theme(self):
        """
        cette fonction permet de remettre le menu et enregistrer le choix du thème 1
        """
        global image
        image = 'choix1.png'
        print(image)
        click.play()
        self.button.setVisible(True)
        self.button2.setVisible(True)
        self.button3.setVisible(True)
        self.choix.setVisible(False)
        self.choix2.setVisible(False)
        self.choix3.setVisible(False)
        return image

    def revenir_theme2(self):
        """
        cette fonction permet de remettre le menu et enregistrer le choix du thème 2
        """
        global image
        image= 'choix2.png'
        click.play()
        self.button.setVisible(True)
        self.button2.setVisible(True)
        self.button3.setVisible(True)
        self.choix.setVisible(False)
        self.choix2.setVisible(False)
        self.choix3.setVisible(False)
        return image

    def revenir_theme3(self):
        """
        cette fonction permet de remettre le menu et enregistrer le choix du thème 2
        """
        global image
        image= 'choix3.png'
        click.play()
        self.button.setVisible(True)
        self.button2.setVisible(True)
        self.button3.setVisible(True)
        self.choix.setVisible(False)
        self.choix2.setVisible(False)
        self.choix3.setVisible(False)
        return image




class fenetreJeu(QWidget):
    """
    cette clase est la fenêtre du jeu
    """

    def __init__(self):
        super().__init__()
        self.initUI()
        global musique
        musique = 'fond.wav'

    def initUI(self):
        self.flag = 0
        # taille de la fenetre
        self.setFixedSize(1400, 886)
        self.form = QFormLayout()
        self.move(200, 50)
        # image d'origine
        self.photo = QImage(image)
        self.setWindowTitle("Game of the amazons: settler vs native")
        photo = self.photo
        # affiche l'image de fond
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(photo))
        self.setPalette(palette)

        self.m,self.matrice,self.position  = [],[],[]

        # groupbox de musique
        self.widget = QWidget(self)
        self.main_vbox = QVBoxLayout()
        self.settings_groupbox = QGroupBox('musique :')
        self.settings_groupbox.setFont(QFont("arial", 15, QFont.Bold))
        self.settings_groupbox.setStyleSheet('color: #C13A1C')
        self.settings_grid = QGridLayout()
        self.settings_groupbox.setLayout(self.settings_grid)

        # play
        label = QLabel('play:')
        label.setFont(QFont("arial", 15, QFont.Bold))
        self.settings_grid.addWidget(label, 0, 0, alignment=Qt.AlignRight)
        self.playbutton = QPushButton()
        self.playbutton.setIcon(QIcon("play.png"))
        self.playbutton.setStyleSheet('background-color: #DEB116')
        self.playbutton.setMaximumWidth(45)
        self.playbutton.setMaximumHeight(30)
        self.playbutton.clicked.connect(play)
        self.settings_grid.addWidget(self.playbutton, 0, 1)

        # pause
        label = QLabel('pause:')
        label.setFont(QFont("arial", 15, QFont.Bold))
        self.settings_grid.addWidget(label, 1, 0, alignment=Qt.AlignRight)
        self.pausebutton = QPushButton()
        self.pausebutton.setIcon(QIcon("pause.png"))
        self.pausebutton.setStyleSheet('background-color: #DEB116')
        self.pausebutton.setMaximumWidth(45)
        self.pausebutton.setMaximumHeight(30)
        self.pausebutton.clicked.connect(pause)
        self.settings_grid.addWidget(self.pausebutton, 1, 1)

        self.main_vbox.addWidget(self.settings_groupbox)
        self.widget.setLayout(self.main_vbox)



        self.centre = QWidget(self)
        self.vbox_1 = QVBoxLayout()
        self.centre.move(0, 300)

        #groupbox des paramètres
        self.box_ensemble = QGroupBox('paramètres')
        self.grilles = QGridLayout()
        self.box_ensemble.setLayout(self.grilles)
        self.box_ensemble.setStyleSheet('color: #C13A1C')
        self.box_ensemble.setStyleSheet('background-color: #DEB116')
        self.box_ensemble.setFont(QFont("arial", 15, QFont.Bold))
        label_jeux = QLabel('Joueur 1:')
        self.grilles.addWidget(label_jeux, 0, 0, alignment=Qt.AlignRight)

        self.cb_player1 = QComboBox()
        self.cb_player1.addItems(['Minimax', 'Humain'])
        self.grilles.addWidget(self.cb_player1, 0, 1)
        # Par défaut, rendre le joueur 1 humain pour permettre les clics immédiatement
        self.cb_player1.setCurrentText('Humain')
        label_jeux = QLabel('Joueur 2:')
        self.grilles.addWidget(label_jeux, 1, 0, alignment=Qt.AlignRight)

        self.cb_player2 = QComboBox()
        self.cb_player2.addItems(['Minimax', 'Humain'])
        self.grilles.addWidget(self.cb_player2, 1, 1)
        label_jeux = QLabel("Delai de l'IA :")
        self.grilles.addWidget(label_jeux, 2, 0, alignment=Qt.AlignRight)
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setTickPosition(QSlider.TicksBelow)
        self.time_slider.setTickInterval(10)
        self.time_slider.setValue(1)
        self.grilles.addWidget(self.time_slider, 2, 1)

        self.charger = QPushButton()
        self.charger.setText('charger')
        self.charger.setStyleSheet('background-color: #DEB116')
        self.charger.setMaximumWidth(60)
        self.charger.setMaximumHeight(30)
        self.charger.clicked.connect(self.ouvrir_fichier)
        # bouton de test rapide: charger le plateau_1.txt s'il existe
        self.charger_test = QPushButton('charger demo', self)
        self.charger_test.setStyleSheet('background-color: #DEB116')
        self.charger_test.setMaximumWidth(100)
        self.charger_test.setMaximumHeight(30)
        # ajout du bouton de test dans la grille des paramètres
        self.grilles.addWidget(self.charger_test, 3, 2)
        self.charger_test.clicked.connect(lambda: self.load_plateau_from_path('plateau_1.txt'))

        label_jeux = QLabel("charger un plateau :")
        self.grilles.addWidget(label_jeux, 3, 0)
        self.grilles.addWidget(self.charger, 3, 1)

        self.vbox_1.addWidget(self.box_ensemble)
        self.centre.setLayout(self.vbox_1)

        # label d'état du joueur courant
        self.status_label = QLabel('Aucun plateau chargé')
        self.status_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.status_label.setStyleSheet('color: #C13A1C')
        self.status_label.move(10, 560)
        self.status_label.setParent(self)

        # bouton Jouer
        self.boutton_jouer = QPushButton('JOUER', self)
        self.boutton_jouer.setToolTip('Clickez ici')
        self.boutton_jouer.setStyleSheet('background-color: #C13A1C')
        self.boutton_jouer.setGeometry(10, 500, 200, 50)
        self.boutton_jouer.setFont(QFont("arial", 20, QFont.Bold))
        self.boutton_jouer.clicked.connect(self.theme)
        self.show()


    def enleve_icon(self):
        """
        cette classe permet d'enlever le pion quand on clique dessus
        """
        nom = self.sender()
        nom.setIcon(QIcon(""))





    def ouvrir_fichier(self):
        """
        cette classe permet d'ouvrir le fichier et faire un plateau à partir d'un fichier
        """
        # Récupère le chemin complet du fichier sélectionné
        fichier = QFileDialog.getOpenFileName(self)
        path = fichier[0]
        if not path:
            return
        self.load_plateau_from_path(path)

    def load_plateau_from_path(self, path):
        """Charge un plateau depuis un chemin donné (factored pour tests)"""
        try:
            self.game = Amazons(path)
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f"Impossible de charger le plateau: {e}")
            return
        # Ajuste les types de joueurs selon les cases de sélection
        p1_type = self.cb_player1.currentText()
        p2_type = self.cb_player2.currentText()
        p1 = HumanPlayer(self.game.board, PLAYER_1) if p1_type == 'Humain' else AIPlayer(self.game.board, PLAYER_1)
        p2 = HumanPlayer(self.game.board, PLAYER_2) if p2_type == 'Humain' else AIPlayer(self.game.board, PLAYER_2)
        self.game.players = (p1, p2)
        self.game.current_player_idx = 0
        # Construire l'affichage du plateau
        b = self.game.board
        # nettoie plateau précédent si besoin
        try:
            for row in getattr(self, 'buttons', []):
                for btn in row:
                    btn.setParent(None)
        except Exception:
            pass
        self.buttons = []
        try:
            self.plateau_boutton(b.size)
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f"Erreur en construisant l'interface du plateau: {e}")


    def plateau_boutton(self, a):
        """
        cette fonction permet de creer les boutons du plateau
        prend en paramètre la taille du plateau `a`
        """
        # Nouvelle version: construit la grille depuis self.game.board
        board = getattr(self, 'game', None).board if hasattr(self, 'game') else None
        if board is None:
            return
        x0, y0 = 500, 120
        size = 70
        for i in range(a):
            row_buttons = []
            y = y0 + i*size
            for j in range(a):
                x = x0 + j*size
                btn = QPushButton(self)
                btn.setGeometry(x, y, size, size)
                pos = Pos2D(a - i - 1, j)  # convertir index de l'UI en coordonnées du board
                btn._pos = pos
                cell = board.at(pos)
                if cell == PLAYER_1:
                    btn.setIcon(QIcon("pion1.png"))
                    btn.setIconSize(QSize(50, 50))
                elif cell == PLAYER_2:
                    btn.setIcon(QIcon("pion2.png"))
                    btn.setIconSize(QSize(50, 50))
                elif cell == ARROW:
                    btn.setIcon(QIcon("fleche.png"))
                    btn.setIconSize(QSize(50, 50))
                btn.setVisible(True)
                btn.clicked.connect(self.cell_clicked)
                # coloration damier
                if (i + j) % 2 == 0:
                    btn.setStyleSheet('background-color: #C13A1C')
                else:
                    btn.setStyleSheet('background-color: #DEB116')
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        # if both players are AI, start the AI loop (non-blocking)
        try:
            p0 = self.game.players[0]
            p1 = self.game.players[1]
            if isinstance(p0, AIPlayer) and isinstance(p1, AIPlayer):
                QTimer.singleShot(200, self._play_ai_turn)
        except Exception:
            pass


    def _clear_selection_styles(self):
        """Enlève les bordures de sélection sur tous les boutons"""
        # Remet le style damier d'origine pour chaque bouton
        a = len(self.buttons)
        for row in getattr(self, 'buttons', []):
            for btn in row:
                pos = getattr(btn, '_pos', None)
                if pos is None or a == 0:
                    btn.setStyleSheet('')
                    continue
                # calculer l'indice i,j utilisés lors de la construction
                i = a - 1 - pos.row
                j = pos.col
                if (i + j) % 2 == 0:
                    btn.setStyleSheet('background-color: #C13A1C')
                else:
                    btn.setStyleSheet('background-color: #DEB116')

    def refresh_board(self):
        """Met à jour les icônes des boutons depuis l'état du board"""
        if not hasattr(self, 'game'):
            return
        board = self.game.board
        for row in self.buttons:
            for btn in row:
                pos = btn._pos
                cell = board.at(pos)
                btn.setIcon(QIcon(""))
                if cell == PLAYER_1:
                    btn.setIcon(QIcon("pion1.png"))
                    btn.setIconSize(QSize(50, 50))
                elif cell == PLAYER_2:
                    btn.setIcon(QIcon("pion2.png"))
                    btn.setIconSize(QSize(50, 50))
                elif cell == ARROW:
                    btn.setIcon(QIcon("fleche.png"))
                    btn.setIconSize(QSize(50, 50))
        # Mettre à jour le label d'état
        if hasattr(self, 'game'):
            cur = self.game.current_player_idx
            player_char = '1' if self.game.players[cur].player_id == PLAYER_1 else '2'
            self.status_label.setText(f"Tour du joueur {player_char}")

    def cell_clicked(self):
        """Gère la logique de sélection/clic pour jouer un coup via la GUI"""
        if not hasattr(self, 'game'):
            return
        btn = self.sender()
        pos = getattr(btn, '_pos', None)
        if pos is None:
            return
        player_idx = self.game.current_player_idx
        player = self.game.players[player_idx]
        player_id = player.player_id
        # si c'est au tour d'une IA, on ignore les clics
        if isinstance(player, AIPlayer):
            return

        # initialise les sélections si nécessaire
        if not hasattr(self, 'sel_old'):
            self.sel_old = None
            self.sel_new = None

        # étape 1: choisir la reine
        if self.sel_old is None:
            if self.game.board.at(pos) != player_id:
                QMessageBox.information(self, 'Erreur', "Pas de reine du joueur à cet emplacement")
                return
            self.sel_old = pos
            btn.setStyleSheet(btn.styleSheet() + '; border: 3px solid blue')
            return

        # étape 2: choisir la position d'arrivée
        if self.sel_new is None:
            if self.game.board.at(pos) != EMPTY:
                QMessageBox.information(self, 'Erreur', "Case d'arrivée invalide")
                return
            if not self.game.board.is_accessible(self.sel_old, pos):
                QMessageBox.information(self, 'Erreur', "Déplacement non accessible")
                return
            self.sel_new = pos
            btn.setStyleSheet(btn.styleSheet() + '; border: 3px solid green')
            return

        # étape 3: choisir la case de la flèche et jouer l'action
        try:
            action = Action(self.sel_old, self.sel_new, pos, player_id)
            if not self.game.board.is_valid_action(action):
                QMessageBox.information(self, 'Erreur', 'Action invalide')
                self._clear_selection_styles()
                self.sel_old = None
                self.sel_new = None
                return
            self.game.board.act(action)
        except Exception as e:
            QMessageBox.information(self, 'Erreur', str(e))
            self._clear_selection_styles()
            self.sel_old = None
            self.sel_new = None
            return

        # reset visuel et rafraîchir
        self._clear_selection_styles()
        self.sel_old = None
        self.sel_new = None
        self.refresh_board()

        # passe au joueur suivant
        self.game.current_player_idx = 1 - self.game.current_player_idx

        # si le suivant est une IA, on programme son coup via QTimer (non bloquant)
        next_player = self.game.players[self.game.current_player_idx]
        if isinstance(next_player, AIPlayer):
            delay_ms = max(50, int(self.time_slider.value() * 300))
            QTimer.singleShot(delay_ms, self._play_ai_turn)

        # vérifier fin de partie
        if self.game.is_over():
            QMessageBox.information(self, 'Fin', f"Player {('1' if self.game.status.winner==PLAYER_1 else '2')} won: {self.game.status.winner_score} vs {self.game.status.loser_score}!")


    def theme(self):
        self.boutton_jouer.setText('REJOUER')


    def _play_ai_turn(self):
        """Execute one AI move for the current player, refresh UI and reschedule if next is also AI."""
        if not hasattr(self, 'game'):
            return
        if self.game.is_over():
            QMessageBox.information(self, 'Fin', f"Player {('1' if self.game.status.winner==PLAYER_1 else '2')} won: {self.game.status.winner_score} vs {self.game.status.loser_score}!")
            return
        player = self.game.players[self.game.current_player_idx]
        if not isinstance(player, AIPlayer):
            return
        try:
            action = player._play()
            if action is None:
                return
            self.game.board.act(action)
        except Exception as e:
            QMessageBox.information(self, 'Erreur IA', str(e))
            return
        # refresh and advance
        self.refresh_board()
        self.game.current_player_idx = 1 - self.game.current_player_idx
        # if next is AI, schedule next move
        next_player = self.game.players[self.game.current_player_idx]
        if isinstance(next_player, AIPlayer) and not self.game.is_over():
            delay_ms = max(50, int(self.time_slider.value() * 300))
            QTimer.singleShot(delay_ms, self._play_ai_turn)
        else:
            # update status label if human to indicate turn
            self.refresh_board()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = fenetreMenu()
    fenetre.show()
    sys.exit(app.exec_())


