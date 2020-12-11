from logic.ludoHandler import LudoHandler


class LudoGame:
    def __init__(self, players_info):
        self.players_info = players_info
        self.players = []
        self.pre_player = None
        self.players_n = 0
        self.lg_handler = LudoHandler()
        for color, name in players_info:
            player = self.lg_handler.add_player(name, color)
            self.players.append(player)
            self.players_n += 1
            player.add_piece()
        self.turn_n = 0
        self.player = self.players[self.turn_n]
        self.board = [None for _ in range(24)]
        self.roll_c = 0
        self.dice_n = 0
        self.selected_piece = None
        self.previous_piece = None
        self.dest_overflow = False
        self.get_goal = False
        self.create_new_piece = False
        self.over_roll = False
        self.ranking = None

    def reset_instance_fields(self):
        self.selected_piece = None
        self.previous_piece = None
        self.dest_overflow = False
        self.get_goal = False
        self.create_new_piece = False

    def change_turn(self):
        if self.players_n:
            self.turn_n = (self.turn_n + 1) % self.players_n
            self.player = self.players[self.turn_n]

    def start_game(self, piece_id):
        self.reset_instance_fields()
        print(self.board)
        self.selected_piece = self.player.get_piece(piece_id)
        if not self.player.pieces_in_path[1]:
            self.put_in_start(self.selected_piece)
            if self.dice_n == 6 or self.over_roll:
                self.change_turn()
        else:
            if self.selected_piece in self.player.pieces_in_path[0]:
                print(f'{self.player}: {self.dice_n}')
                if not self.player.move_piece(self.selected_piece, self.dice_n):
                    self.move_in_board(self.selected_piece, self.dice_n)
                else:
                    self.get_goal = True
                    self.remove_piece(self.selected_piece, self.dice_n)
                    if self.player.pieces_in_goal[1] == 4:
                        self.update_ranking()
                    print(self.player.pieces_in_goal)
            elif self.selected_piece in self.player.pieces_in_home[0]:
                self.put_in_start(self.selected_piece)
            self.change_turn()
        self.dice_n = 0
        print(self.board)

    def put_in_start(self, piece):
        print(f'{self.player}: {self.dice_n}')
        if self.dice_n == 6:
            if self.player.pieces_count < 4:
                self.create_new_piece = True
            self.player.get_to_start_pos(piece)
            self.put_to_board_start(piece)

    def move_in_board(self, piece, dice_n):
        if not self.board[piece.piece_pos]:
            self.board[piece.piece_pos - dice_n] = None
            self.board[piece.piece_pos] = piece
        elif self.board[piece.piece_pos] == piece:
            pass
        else:
            self.dest_overflow = True
            self.previous_piece = self.board[piece.piece_pos]
            self.previous_piece.player.back_to_home(self.previous_piece)
            self.board[piece.piece_pos] = piece
            self.board[piece.piece_pos - dice_n] = None

    def put_to_board_start(self, piece):
        if not self.board[piece.piece_pos]:
            self.board[piece.piece_pos] = piece
        else:
            self.dest_overflow = True
            self.previous_piece = self.board[piece.piece_pos]
            self.previous_piece.player.back_to_home(self.previous_piece)
            self.board[piece.piece_pos] = piece

    def remove_piece(self, piece, dice_n):
        self.board[piece.piece_pos - dice_n] = None
        self.pre_player = self.player

    def update_ranking(self):
        self.ranking = sorted(self.players, key=lambda x: x.pieces_in_goal_label[1], reverse=True)

    def dice(self):
        self.dice_n = randint(1, 6)
        self.roll_c += 1
        if not self.player.pieces_in_path[0] and (self.roll_c == 3 or self.dice_n == 6):
                self.roll_c = 0
                self.over_roll = True
        elif self.player.pieces_in_path[0] and self.roll_c == 1:
            self.roll_c = 0
            self.over_roll = True

    @property
    def piece_to_move(self):
        if not self.player.pieces_in_path[0] and self.over_roll and self.dice_n != 6:
            self.change_turn()
            return False
        return True