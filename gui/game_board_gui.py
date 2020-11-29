from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog
from logic.ludoGame import LudoGame


class MainWindow(QMainWindow):
    colors_style = {'RED': 'color: rgb(255, 0, 0)',
                    'GREEN': 'color: rgb(0, 170, 0)',
                    'BLUE': 'color: rgb(0, 0, 255)',
                    'YELLOW': 'color: rgb(255, 255, 0)'}
    home_fields = {'BLUE': (20, 500), 'RED': (20, 20), 'GREEN': (500, 20), 'YELLOW': (500, 500)}
    path_fields = [(180, 500), (180, 420), (180, 340), (100, 340), (20, 340), (20, 260), (20, 180), (100, 180),
                   (180, 180),
                   (180, 100), (180, 20), (260, 20), (340, 20), (340, 100), (340, 180), (420, 180), (500, 180),
                   (500, 260),
                   (500, 340), (420, 340), (340, 340), (340, 420),
                   (340, 500), (260, 500)]
    start_fields = {'RED': (20, 180), 'GREEN': (340, 20), 'BLUE': (180, 500), 'YELLOW': (500, 340)}
    goal_fields = {'BLUE': (260, 420), 'RED': (100, 260), 'GREEN': (260, 100), 'YELLOW': (420, 260)}
    colors = ['RED', 'GREEN', 'BLUE', 'YELLOW']
    pieces_in_goal_label = {}

    def __init__(self):
        super().__init__()
        self.setObjectName('MainWindow')
        self.setFixedSize(800, 620)
        self.central_widget = QtWidgets.QWidget(self)
        self.__init_menubar()
        self.__init_players_part()
        self.__init_turn_part()
        self.__init_board_part()
        self.translate_ui()
        self.setCentralWidget(self.central_widget)
        # *******************
        self.l_game = None
        self.players = []
        self.players_count = 0
        self.pieces = {'RED': [], 'GREEN': [], 'BLUE': [], 'YELLOW': []}
        self.players_label = []

    def __init_menubar(self):
        self.menubar = QtWidgets.QMenuBar(self.central_widget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menuGame = QtWidgets.QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.actionAdd_Player = QtWidgets.QAction(self)
        self.actionStart_Game = QtWidgets.QAction(self)
        self.actionStart_Game.setDisabled(True)
        self.actionNew_Game = QtWidgets.QAction(self)
        self.actionNew_Game.setDisabled(True)
        self.actionExit = QtWidgets.QAction(self)
        self.menuGame.addAction(self.actionAdd_Player)
        self.menuGame.addAction(self.actionStart_Game)
        self.menuGame.addAction(self.actionNew_Game)
        self.menuGame.addAction(self.actionExit)
        self.menubar.addAction(self.menuGame.menuAction())
        # events listener
        self.actionExit.triggered.connect(exit)
        self.actionAdd_Player.triggered.connect(self.show_add_player_dialog)
        self.actionStart_Game.triggered.connect(self.start_game)
        self.actionNew_Game.triggered.connect(self.new_game_btn)

    def __init_players_part(self):
        widget = QWidget(self.central_widget)
        widget.setGeometry(QtCore.QRect(10, 10, 201, 291))
        widget.setStyleSheet("background-color: rgb(85, 170, 255);\nborder-radius:10px;")
        # **************************************************************************
        player_text_label = QtWidgets.QLabel(widget)
        player_text_label.setText("Players")
        player_text_label.setGeometry(QtCore.QRect(60, 10, 81, 31))
        player_text_label.setFont(QtGui.QFont("Arial", 18, 50))
        player_text_label.setStyleSheet("background-color:rgba(255, 255, 255, 0);")
        player_text_label.setAlignment(QtCore.Qt.AlignCenter)
        # **************************************************************************
        self.verticalLayoutWidget = QtWidgets.QWidget(widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 50, 181, 231))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        # **************************************************************************
        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addSpacerItem(spacer_item)

    def __init_turn_part(self):
        widget = QtWidgets.QWidget(self.central_widget)
        widget.setGeometry(QtCore.QRect(10, 310, 201, 271))
        widget.setStyleSheet("background-color: rgb(85, 170, 255);\nborder-radius:10px;")
        self.turn_status_label = QtWidgets.QLabel(widget)
        self.turn_status_label.setText("TURN:  ...")
        self.turn_status_label.setGeometry(QtCore.QRect(0, 10, 201, 53))
        self.turn_status_label.setFont(QtGui.QFont("Arial", 14))
        self.turn_status_label.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.turn_status_label.setAlignment(QtCore.Qt.AlignCenter)

        self.roll_dice_btn = QtWidgets.QPushButton(widget)
        self.roll_dice_btn.setText("Roll Dice")
        self.roll_dice_btn.setGeometry(QtCore.QRect(40, 70, 131, 61))
        self.roll_dice_btn.setFont(QtGui.QFont("Arial", 15, 75))
        self.roll_dice_btn.setStyleSheet("border:1px solid black;\nbackground-color: rgba(255, 255, 255, 0);")
        self.roll_dice_btn.setDisabled(True)

        self.dice_number_label = QtWidgets.QLabel(widget)
        self.dice_number_label.setText(".")
        self.dice_number_label.setGeometry(QtCore.QRect(0, 150, 201, 121))
        self.dice_number_label.setFont(QtGui.QFont("Arial", 50, 75))
        self.dice_number_label.setAlignment(QtCore.Qt.AlignCenter)
        # event listener
        self.roll_dice_btn.clicked.connect(self.roll_dice)

    def __init_board_part(self):
        self.board_widget = QtWidgets.QWidget(self.central_widget)
        self.board_widget.setGeometry(QtCore.QRect(220, 10, 571, 571))
        self.board_widget.setStyleSheet("background-color: rgb(85, 170, 255);\nborder-radius:10px;")
        with open('gui/coordinates.txt') as openfile:
            for coordinate in openfile:
                coordinate = coordinate.strip().split(', ', 2)
                color = coordinate[-1]
                coordinate = [int(i) for i in coordinate[:-1]]
                label = QtWidgets.QLabel(self.board_widget)
                label.setGeometry(QtCore.QRect(*coordinate, 71, 71))
                label.setStyleSheet(f"border-radius:35px;\nbackground-color: rgb{color};")
        for color in self.goal_fields:
            piece_in_goal_label = QtWidgets.QLabel(self.board_widget)
            piece_in_goal_label.setText("0")
            piece_in_goal_label.setGeometry(QtCore.QRect(*self.goal_fields[color], 51, 51))
            piece_in_goal_label.setFont(QtGui.QFont("Arial", 30, 75))
            piece_in_goal_label.setAlignment(QtCore.Qt.AlignCenter)
            piece_in_goal_label.setStyleSheet("color: rgb(255, 255, 255);\nbackground-color: rgba(255, 255, 255, 0);")
            self.pieces_in_goal_label[color] = piece_in_goal_label

    def start_game(self):
        self.actionStart_Game.setDisabled(True)
        self.actionNew_Game.setDisabled(False)
        self.actionAdd_Player.setDisabled(True)
        self.roll_dice_btn.setDisabled(False)
        self.__start_logic()
        self.__init_start_ui()

    def __init_start_ui(self):
        for color, name in self.players:
            self.add_piece_to_home(color)
        self.update_turn()

    def __sort_players_list(self):
        sorted_key = lambda x: 1 if 'RED' in x else 2 if 'GREEN' in x else 3 \
            if 'BLUE' in x else 4 if 'YELLOW' in x else None
        self.players = sorted(self.players, key=sorted_key)

    def __start_logic(self):
        self.__sort_players_list()
        self.l_game = LudoGame(self.players)

    def update_turn(self):
        self.turn_status_label.setText(f"TURN:  {self.players[self.l_game.turn_n][1]}")
        self.turn_status_label.setStyleSheet(f'{self.colors_style[self.players[self.l_game.turn_n][0]]};')

    def roll_dice(self):
        self.l_game.dice()
        self.dice_number_label.setText(str(self.l_game.dice_n))
        if not self.l_game.piece_to_move:
            self.update_turn()
        elif self.l_game.over_roll:
            self.roll_dice_btn.setDisabled(True)
        # reset l_game fields
        self.l_game.over_roll = False

    def add_player(self, color_name, player_info):
        font = QtGui.QFont("Arial", 14)
        player = QtWidgets.QLabel(self.verticalLayoutWidget)
        player.setMaximumHeight(25)
        player.setFont(font)
        player.setText(player_info)
        player.setStyleSheet(f"{self.colors_style[color_name]};\nbackground-color: rgba(255, 255, 255, 0);")
        player.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.verticalLayout.insertWidget(self.players_count - 1, player)
        self.players_label.append(player)

    def add_piece_to_home(self, color):
        self.pieces_png = {
            'RED': 'red_pawn.png',
            'GREEN': 'green_pawn.png',
            'BLUE': 'blue_pawn.png',
            'YELLOW': 'yellow_pawn.png'
        }
        piece = QtWidgets.QPushButton(self.board_widget)
        piece.setGeometry(QtCore.QRect(*self.home_fields[color], 51, 51))
        piece.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f'resources/{self.pieces_png[color]}'))
        piece.setIcon(icon)
        piece.setIconSize(QtCore.QSize(51, 51))
        id = len(self.pieces[color]) + 1
        piece.clicked.connect(lambda x: self.change_piece_pos(piece, color, id))
        piece.show()
        self.pieces[color].append(piece)

    def change_piece_pos(self, piece, color, piece_id):
        pos_piece = (piece.x(), piece.y())
        if (self.l_game.player.color == color and self.l_game.dice_n) and (
                not (pos_piece in list(self.home_fields.values())) or (self.l_game.dice_n == 6)):
            self.l_game.start_game(piece_id)
            if not self.l_game.get_goal:
                pos = self.l_game.selected_piece.piece_pos
                piece.move(*self.path_fields[pos])
                if self.l_game.create_new_piece:
                    self.add_piece_to_home(self.l_game.selected_piece.color)
                if self.l_game.dest_overflow:
                    previous_piece = self.l_game.previous_piece
                    pp_color = previous_piece.color
                    self.pieces[pp_color][previous_piece.id - 1].move(*self.home_fields[pp_color])
            else:
                # piece.move(*self.goal_fields[color])
                # piece.setDisabled(True)
                piece.close()
                self.pieces_in_goal_label[color].setText(f"{self.l_game.pre_player.pieces_in_goal_label[1]}")
                if self.l_game.ranking:
                    self.show_ranking_dialog()
            self.update_turn()
            self.roll_dice_btn.setDisabled(False)

    def show_add_player_dialog(self):
        dlg = AddPlayerDialog(self)
        if dlg.exec_():
            print("Success!")
            self.players_count += 1
            self.players.append(dlg.player_info)
            self.add_player(dlg.player_info[0], str(self.players_count) + '. ' + dlg.player_info[1])
            if self.players_count == 2:
                self.actionStart_Game.setDisabled(False)
            if self.players_count == 4:
                self.actionAdd_Player.setDisabled(True)
        else:
            print("Cancel!")

    def show_ranking_dialog(self):
        dlg = RankingDialog(self, self.l_game.players)
        dlg.exec_()

    def new_game_btn(self):
        for color in self.pieces:
            for piece in self.pieces[color]:
                piece.close()
        for player in self.players_label:
            player.close()
        self.l_game = None
        self.players = []
        self.players_count = 0
        self.pieces = {'RED': [], 'GREEN': [], 'BLUE': [], 'YELLOW': []}
        self.roll_dice_btn.setDisabled(True)
        self.turn_status_label.setText("Turn: ...")
        self.turn_status_label.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.dice_number_label.setText('.')
        self.actionAdd_Player.setDisabled(False)
        self.actionNew_Game.setDisabled(True)

    def translate_ui(self):
        self.setWindowTitle("MainWindow")
        self.menuGame.setTitle("Game")
        self.actionAdd_Player.setText("Add Player")
        self.actionStart_Game.setText("Start Game")
        self.actionNew_Game.setText("New Game")
        self.actionExit.setText("Exit")

class AddPlayerDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.players = parent.players
        self.player_info = None
        self.setWindowTitle('hello')
        self.setFixedSize(294, 155)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(156, 110, 125, 42))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        font = QtGui.QFont('MS Shell Dlg 2', 10)
        self.username_textedit = QtWidgets.QLineEdit(self)
        self.username_textedit.setGeometry(QtCore.QRect(90, 20, 191, 20))
        self.username_textedit.setFont(font)
        self.pass_textedit = QtWidgets.QLineEdit(self)
        self.pass_textedit.setGeometry(QtCore.QRect(90, 50, 191, 20))
        self.pass_textedit.setFont(font)
        self.pass_textedit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.color = QtWidgets.QComboBox(self)
        self.color.setGeometry(QtCore.QRect(90, 82, 191, 22))
        self.color.addItem("RED")
        self.color.addItem("GREEN")
        self.color.addItem("BLUE")
        self.color.addItem("YELLOW")
        username_label = QtWidgets.QLabel(self)
        username_label.setText("Username:")
        username_label.setGeometry(QtCore.QRect(10, 19, 81, 21))
        username_label.setFont(font)
        pass_label = QtWidgets.QLabel(self)
        pass_label.setText("Password:")
        pass_label.setGeometry(QtCore.QRect(10, 50, 71, 21))
        pass_label.setFont(font)

        self.error_label = QtWidgets.QLabel(self)
        self.error_label.setGeometry(QtCore.QRect(10, 103, 152, 45))
        self.error_label.setWordWrap(True)
        font.setPointSize(8)
        self.error_label.setFont(font)
        self.error_label.setStyleSheet("color: rgb(255, 0, 0);")
        self.buttonBox.accepted.connect(self.check_user_info)
        self.buttonBox.rejected.connect(self.reject)

    def check_user_info(self):
        with open('resources/userandpass.txt') as fl:
            players = list(zip(*self.players)) if self.players else [(), ()]
            for line in fl:
                line = line.strip().split()
                if line[0] == self.username_textedit.text() and line[1] == self.pass_textedit.text():
                    if line[0] not in players[1]:
                        if (index := self.color.currentText()) not in players[0]:
                            self.player_info = (self.color.currentText(), line[0])
                            self.accept()
                        else:
                            self.error_label.setText(f'{self.color.currentText()} has already been selected!')
                    else:
                        self.error_label.setText('Player entered already!')
                    break
            else:
                self.error_label.setText("Username or pass is wrong!")


class RankingDialog(QDialog):
    def __init__(self, parent, ranking):
        super().__init__(parent)
        self.setWindowTitle("Ranking")
        self.setFixedSize(393, 300)
        layout = QtWidgets.QWidget(self)
        layout.setGeometry(QtCore.QRect(9, 90, 371, 191))
        self.verticalLayout = QtWidgets.QVBoxLayout(layout)
        self.t_font = QtGui.QFont()
        self.t_font.setPointSize(15)
        self.ranking_dialog_title = QtWidgets.QLabel(self)
        self.ranking_dialog_title.setGeometry(QtCore.QRect(20, 10, 349, 71))
        self.ranking_dialog_title.setMaximumHeight(100)
        self.ranking_dialog_title.setFont(self.t_font)
        self.ranking_dialog_title.setAlignment(QtCore.Qt.AlignCenter)
        self.ranking_dialog_title.setText("<html><head/><body><p>Game Finished!</p><p>ranking:</p></body></html>")
        self.update_ranking(ranking)

    def update_ranking(self, ranking):
        colors_style = {'RED': 'color: rgb(255, 0, 0)',
                        'GREEN': 'color: rgb(0, 170, 0)',
                        'BLUE': 'color: rgb(0, 0, 255)',
                        'YELLOW': 'color: rgb(255, 255, 0)'}
        for index, player in enumerate(ranking, 1):
            player_name_label = QtWidgets.QLabel(self)
            player_name_label.setText(f'{index}. {player.name}')
            player_name_label.setMaximumHeight(18)
            player_name_label.setFont(self.t_font)
            player_name_label.setAlignment(QtCore.Qt.AlignCenter)
            player_name_label.setStyleSheet(colors_style[player.color])
            self.verticalLayout.addWidget(player_name_label)
        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item)

