from random import choice


class LudoHandler:
    __colors = ['RED', 'GREEN', 'BLUE', 'YELLOW']

    def __init__(self):
        self.__players_count = 0
        self.__players = []
        self.__players_name = []

    def add_player(self, player_name):
        if self.__players_count < 4:
            chosen_color = self.__set_color()
            player = self.Player(player_name, chosen_color, self.__players_count)
            self.__players_count += 1
            self.__players_name.append(f'{player_name}: {chosen_color}')
            self.__players.append(player)
            sorted_key = lambda x: 1 if 'RED' in x else 2 if 'GREEN' in x else 3 \
                if 'BLUE' in x else 4 if 'YELLOW' in x else None
            self.__players_name = sorted(self.__players_name, key=sorted_key)
            return player
        else:
            print('Error: players count must be between 0 and 5')

    def __set_color(self):
        if self.__colors:
            player_color = choice(self.__colors)
            self.__colors.remove(player_color)
            return player_color

    @property
    def players_count(self):
        return self.__players_count

    class Player:
        def __init__(self, name, color, players_count):
            self.__id = players_count + 1
            self.__player_name = name
            self.__pieces_count = 0
            self.__pieces_color = color
            self.pieces_in_home = [[], 4]
            self.pieces_in_path = [[], 0]
            self.pieces_in_goal = [[], 0]

        def add_piece(self):
            if self.pieces_count < 4:
                piece = self.Piece(self)
                self.pieces_in_home[0].append(piece)
                self.__pieces_count += 1
                return piece
            else:
                print('Error: piece count must be between 0 and 5')

        def move_piece(self, piece, dice_number):
            if piece.move(dice_number):
                self.pieces_in_path[0].remove(piece)
                self.pieces_in_path[1] -= 1
                self.pieces_in_goal[0].append(piece)
                self.pieces_in_goal[1] += 1
                return True
            else:
                return False

        def get_piece(self, piece_id):
            pieces = self.pieces_in_path[0] + self.pieces_in_home[0]
            for piece in pieces:
                if piece.piece_id == piece_id:
                    return piece

        def get_to_start_pos(self, piece=None):
            if not piece:
                piece = self.pieces_in_home[0][-1]
                del self.pieces_in_home[0][-1]
                self.pieces_in_path[0].append(piece)
            else:
                self.pieces_in_home[0].remove(piece)
                self.pieces_in_path[0].append(piece)
            piece.get_start()
            self.pieces_in_home[1] -= 1
            self.add_piece()
            self.pieces_in_path[1] += 1
            return piece

        def back_to_home(self, piece):
            piece.drop_to_home()
            self.pieces_in_home[0].append(piece)
            self.pieces_in_home[1] += 1
            self.pieces_in_path[0].remove(piece)
            self.pieces_in_path[1] -= 1

        @property
        def pieces_count(self):
            return self.__pieces_count

        @property
        def color(self):
            return self.__pieces_color

        @property
        def player_id(self):
            return self.__id

        @property
        def name(self):
            return self.__player_name

        def __repr__(self):
            return f'Player{self.__id}'

        class Piece:
            START_POS = {
                'RED': 0,
                'GREEN': 6,
                'BLUE': 12,
                'YELLOW': 18,
            }

            def __init__(self, player):
                self.__id = player.pieces_count + 1
                self.__pos = ...
                self.player_id = player.player_id
                self.__color = player.color
                self.player = player

            @property
            def piece_pos(self):
                return (self.__pos + self.START_POS[self.__color]) % 24

            def move(self, dice_n):
                if (self.__pos + dice_n) < 24:
                    self.__pos += dice_n
                elif self.__pos + dice_n == 24:
                    self.__pos += dice_n
                    return True
                else:
                    print(f'Warning: invalid dice number to move piece{self.__id}')
                return False

            def get_start(self):
                self.__pos = 0

            def drop_to_home(self):
                self.__pos = ...

            @property
            def piece_id(self):
                return self.__id

            def __repr__(self):
                return f'Player{self.player_id}.Piece{self.__id}'

