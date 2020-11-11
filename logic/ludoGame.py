from random import randint
from ludoHandler import LudoHandler


class LudoGame:
    def __init__(self):
        players_name = ['Shahin', 'Saeid']
        self.players = []
        self.players_n = 0
        self.lg_handler = LudoHandler()
        for name in players_name:
            player = self.lg_handler.add_player(name)
            self.players.append(player)
            self.players_n += 1
            player.add_piece()
        self.turn_n = 0
        self.player = self.players[self.turn_n]
        self.board = [None for _ in range(24)]

    def change_turn(self):
        if self.players_n:
            self.turn_n = (self.turn_n + 1) % self.players_n
            self.player = self.players[self.turn_n]

    def start_game(self):
        while self.players_n:
            print(self.board)
            if not self.player.pieces_in_path[1]:
                self.first_start()
            else:
                piece_id = int(
                    input(f'{self.player}: select your piece by id (number of pieces = {self.player.pieces_count}): '))
                piece = self.player.get_piece(piece_id)
                if piece in self.player.pieces_in_path[0]:
                    dice_n = self.dice()
                    print(f'{self.player}: {dice_n}')
                    if not self.player.move_piece(piece, dice_n):
                        self.move_in_board(piece, dice_n)
                    else:
                        self.remove_piece(piece, dice_n)
                        print(self.player.pieces_in_goal)
                elif piece in self.player.pieces_in_home[0]:
                    self.put_in_start(piece)
            self.change_turn()
        print(self.board)

    def first_start(self):
        for _ in range(3):
            if self.put_in_start():
                break

    def put_in_start(self, piece=None):
        dice_n = self.dice()
        print(f'{self.player}: {dice_n}')
        if dice_n == 6:
            if piece:
                self.player.get_to_start_pos(piece)
            else:
                piece = self.player.get_to_start_pos()
            self.put_to_board_start(piece)
            return True
        return False

    def move_in_board(self, piece, dice_n):
        if not self.board[piece.piece_pos]:
            self.board[piece.piece_pos - dice_n] = None
            self.board[piece.piece_pos] = piece
        elif self.board[piece.piece_pos] == piece:
            pass
        else:
            piece_in_pos = self.board[piece.piece_pos]
            piece_in_pos.player.back_to_home(piece_in_pos)
            self.board[piece.piece_pos] = piece
            self.board[piece.piece_pos - dice_n] = None

    def put_to_board_start(self, piece):
        if not self.board[piece.piece_pos]:
            self.board[piece.piece_pos] = piece
        else:
            piece_in_path = self.board[piece.piece_pos]
            piece_in_path.player.back_to_home(piece_in_path)
            self.board[piece.piece_pos] = piece

    def remove_piece(self, piece, dice_n):
        self.board[piece.piece_pos - dice_n] = None
        self.players_n -= 1
        self.players.remove(self.player)

    @staticmethod
    def dice(n=1):
        if n > 1:
            temp_list = []
            for _ in range(n):
                temp_list.append(randint(1, 6))
            return temp_list
        elif n == 1:
            return randint(1, 6)


mygame = LudoGame()
mygame.start_game()
