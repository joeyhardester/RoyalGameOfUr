"""
File:        royal_game_of_ur.py
Author:      Joey Hardester
Date:        11/10/2020
Section:     31
E-mail:      josephh5@umbc.edu
Description: This file is a copy of the Royal Game of Ur, using classes and objects
             in order to complete the goal of moving all pieces of the board.
"""

from sys import argv
from random import choice
from board_square import BoardSquare, UrPiece


class RoyalGameOfUr:
    STARTING_PIECES = 7
    BLACK = "Black"
    WHITE = "White"

    def __init__(self, board_file_name):
        self.board = None
        self.load_board(board_file_name)

    def load_board(self, board_file_name):
        """
        This function takes a file name and loads the map, creating BoardSquare objects in a grid.

        :param board_file_name: the board file name
        :return: sets the self.board object within the class
        """

        import json
        try:
            with open(board_file_name) as board_file:
                board_json = json.loads(board_file.read())
                self.num_pieces = self.STARTING_PIECES
                self.board = []
                for x, row in enumerate(board_json):
                    self.board.append([])
                    for y, square in enumerate(row):
                        self.board[x].append(BoardSquare(x, y, entrance=square['entrance'], _exit=square['exit'],
                                                         rosette=square['rosette'], forbidden=square['forbidden']))

                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if board_json[i][j]['next_white']:
                            x, y = board_json[i][j]['next_white']
                            self.board[i][j].next_white = self.board[x][y]
                        if board_json[i][j]['next_black']:
                            x, y = board_json[i][j]['next_black']
                            self.board[i][j].next_black = self.board[x][y]
        except OSError:
            print('The file was unable to be opened. ')

    def draw_block(self, output, i, j, square):
        """
        Helper function for the display_board method
        :param output: the 2d output list of strings
        :param i: grid position row = i
        :param j: grid position col = j
        :param square: square information, should be a BoardSquare object
        """
        MAX_X = 8
        MAX_Y = 5
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if x == 0 or y == 0 or x == MAX_X - 1 or y == MAX_Y - 1:
                    output[MAX_Y * i + y][MAX_X * j + x] = '+'
                if square.rosette and (y, x) in [(1, 1), (1, MAX_X - 2), (MAX_Y - 2, 1), (MAX_Y - 2, MAX_X - 2)]:
                    output[MAX_Y * i + y][MAX_X * j + x] = '*'
                if square.piece:
                    # print(square.piece.symbol)
                    output[MAX_Y * i + 2][MAX_X * j + 3: MAX_X * j + 5] = square.piece.symbol

    def display_board(self):
        """
        Draws the board contained in the self.board object

        """
        if self.board:
            output = [[' ' for _ in range(8 * len(self.board[i // 5]))] for i in range(5 * len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if not self.board[i][j].forbidden:
                        self.draw_block(output, i, j, self.board[i][j])

            print('\n'.join(''.join(output[i]) for i in range(5 * len(self.board))))

    def roll_d4_dice(self, n=4):
        """
        Keep this function as is.  It ensures that we'll have the same runs with different random seeds for rolls.
        :param n: the number of tetrahedral d4 to roll, each with one dot on
        :return: the result of the four rolls.
        """
        dots = 0
        for _ in range(n):
            dots += choice([0, 1])
        return dots

    def play_game(self):
        player_one = input("Enter name: ")
        print(player_one, "will play as white.")
        player_two = input("Enter name: ")
        print(player_two, "will play as black.")
        self.display_board()
        """
            all these variables will be used as fillers since there are different boards
            white_start - used to get the position of where the starting position for the white pieces is
            black_start - same as white_start but for the black pieces
            rosette_list - used to get all the pieces that have a rosette
            white_rosette_list - used to keep track of the pieces that are currently on the rosette, if
                                 they were not previously in the list, the user is allowed to go again
            black_rosette_list - same as before but for the black pieces
        """
        white_start = None
        black_start = None
        rosette_list = []
        white_rosette_list = []
        black_rosette_list = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].entrance == self.WHITE:
                    white_start = self.board[i][j]
                if self.board[i][j].entrance == self.BLACK:
                    black_start = self.board[i][j]
                if self.board[i][j].rosette:
                    rosette_list.append(self.board[i][j])
        # white pieces are created here using a helper function
        player_one_pieces = self.create_white_pieces(white_start)
        # black pieces are created here using a helper function
        player_two_pieces = self.create_black_pieces(black_start)
        # will be used to monitor whose turn it is, 0 for player 1, 1 for player 2
        turn_check = 0
        # a variable that determines when the game ends by checking when all the pieces are complete
        game_end = self.check_complete(player_one_pieces, player_one)
        while not game_end:
            # player 1 goes
            if turn_check == 0:
                roll = self.roll_d4_dice()
                print("You rolled a", roll)
                # call to display_options which displays which pieces are allowed to move
                self.display_options(player_one_pieces, roll, white_start, black_start, turn_check)
                # call to check_capture to see if any of the white pieces landed on a spot that isn't a
                # rosette with a black piece
                self.check_capture(player_one_pieces, white_start, player_two_pieces, black_start, turn_check)
                # this function is to check if the piece has moved off the rosette in order to prevent an infinite
                # loop of pieces because the piece is on a rosette
                white_rosette_list = self.check_rosette_move(player_one_pieces, white_rosette_list)
                # this function checks if the piece has landed on a rosette that wasn't previously on it,
                # if the function returns true, the player goes again
                rosette_check = self.another_turn(player_one_pieces, white_rosette_list)
                # this function is to make sure that the new piece is added to the rosette_list in order to prevent
                # the infinite loop
                white_rosette_list = self.check_rosette(player_one_pieces, white_rosette_list)
                game_end = self.check_complete(player_one_pieces, player_one)
                if rosette_check:
                    print("You landed on a rosette, you get another turn")
                    turn_check = 0
                else:
                    turn_check = 1
            # player 2 goes
            elif turn_check == 1:
                # all functions are same as before but instead it is player 2
                roll = self.roll_d4_dice()
                print("You rolled a", roll)
                self.display_options(player_two_pieces, roll, white_start, black_start, turn_check)
                self.check_capture(player_one_pieces, white_start, player_two_pieces, black_start, turn_check)
                black_rosette_list = self.check_rosette_move(player_two_pieces, black_rosette_list)
                rosette_check = self.another_turn(player_two_pieces, black_rosette_list)
                black_rosette_list = self.check_rosette(player_two_pieces, black_rosette_list)
                game_end = self.check_complete(player_two_pieces, player_two)
                if rosette_check:
                    print("You landed on a rosette, you get another turn")
                    turn_check = 1
                else:
                    turn_check = 0

    # helper function that creates all 7 pieces for the white side
    def create_white_pieces(self, white_start):
        white_pieces = []
        for i in range(self.STARTING_PIECES):
            white_pieces.append(UrPiece(self.WHITE, "W" + str(i)))
            white_pieces[i].position = white_start
        return white_pieces

    # helper function that creates 7 pieces for the black side
    def create_black_pieces(self, black_start):
        black_pieces = []
        for i in range(self.STARTING_PIECES):
            black_pieces.append(UrPiece(self.BLACK, "B" + str(i)))
            black_pieces[i].position = black_start
        return black_pieces

    # this function is where most of the display takes place
    def display_options(self, player_pieces, num_moves, white_start, black_start, player_turn):
        # used to check which pieces are allowed to move using the can_move function within the board_square program
        move_list = []
        for i in range(len(player_pieces)):
            move_check = player_pieces[i].can_move(num_moves)
            if move_check:
                move_list.append(player_pieces[i])

        # used to check which pieces have completed the race
        complete_list = []
        for i in range(len(player_pieces)):
            if player_pieces[i].complete:
                complete_list.append(player_pieces[i])

        # used to print the options out on the board
        for i in range(len(move_list)):
            if player_turn == 0:
                # if the position of the piece is at the start but not on the board,
                # it is technically off the board
                if move_list[i].position == white_start:
                    if not white_start.piece:
                        print(i + 1, move_list[i].symbol, "currently off the board.")
                    elif white_start.piece != move_list[i]:
                        print(i + 1, move_list[i].symbol, "currently off the board.")
                    # if the piece is on the board, it's position is printed
                    else:
                        print(i + 1, move_list[i].symbol, move_list[i].position.position)
                else:
                    print(i + 1, move_list[i].symbol, move_list[i].position.position)
            elif player_turn == 1:
                # same as before but for the black pieces
                if move_list[i].position == black_start:
                    if not black_start.piece:
                        print(i + 1, move_list[i].symbol, "currently off the board.")
                    elif black_start.piece != move_list[i]:
                        print(i + 1, move_list[i].symbol, "currently off the board.")
                    else:
                        print(i + 1, move_list[i].symbol, move_list[i].position.position)
                else:
                    print(i + 1, move_list[i].symbol, move_list[i].position.position)
        # if there are no possible moves, the next turn is taken
        if len(move_list) == 0:
            print("No moves are possible")
            self.display_board()
        else:
            for i in range(len(complete_list)):
                print(complete_list[i].symbol, "has completed the race")
            user_turn = int(input("What would you like to do? "))
            invalid_selection = True
            # makes sure the user makes a valid selection in order to move a certain piece
            while invalid_selection:
                for i in range(len(move_list)):
                    if user_turn == i + 1:
                        self.move_piece(move_list[i], num_moves)
                        invalid_selection = False
                if invalid_selection:
                    user_turn = int(input("Sorry, that wasn't a valid selection, which move do you wish to make? "))

    # this helper function also does a lot as well, it moves the pieces, and makes sure that the previous position
    # does not have that same piece
    def move_piece(self, piece, num_moves):
        if piece.color == self.WHITE:
            # every move has the same setup, just different locations
            if num_moves == 1:
                # if the piece is at the entrance
                if piece.position.entrance == self.WHITE:
                    # if the first position does not have a piece, piece isn't on the board
                    if not piece.position.piece:
                        self.board[piece.position.position[0]][piece.position.position[1]].piece = piece
                    # if the piece is already on the board
                    else:
                        self.board[piece.position.next_white.position[0]][
                            piece.position.next_white.position[1]].piece = piece
                        self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                        piece.position = self.board[piece.position.next_white.position[0]][
                            piece.position.next_white.position[1]]
                elif piece.position.exit == self.WHITE:
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.complete = True
                # for every other spot on the board except the exit and the entrance, moves the piece
                else:
                    self.board[piece.position.next_white.position[0]][
                        piece.position.next_white.position[1]].piece = piece
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = self.board[piece.position.next_white.position[0]][
                        piece.position.next_white.position[1]]
            # same as before but if it is a white piece with 2 moves
            elif num_moves == 2:
                if piece.position.entrance == self.WHITE:
                    if piece.position.piece == piece:
                        self.board[piece.position.next_white.next_white.position[0]][
                            piece.position.next_white.next_white.position[1]].piece = piece
                        self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                        piece.position = self.board[piece.position.next_white.next_white.position[0]][
                            piece.position.next_white.next_white.position[1]]
                    else:
                        self.board[piece.position.next_white.position[0]][
                            piece.position.next_white.position[1]].piece = piece
                        piece.position = self.board[piece.position.next_white.position[0]][
                            piece.position.next_white.position[1]]
                elif piece.position.next_white.exit == self.WHITE:
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = piece.position.next_white
                    piece.complete = True
                else:
                    self.board[piece.position.next_white.next_white.position[0]][
                        piece.position.next_white.next_white.position[1]].piece = piece
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = self.board[piece.position.next_white.next_white.position[0]][
                        piece.position.next_white.next_white.position[1]]
            # same as before but if it is a white piece with 3 moves
            elif num_moves == 3:
                if piece.position.entrance == self.WHITE:
                    if piece.position.piece == piece:
                        self.board[piece.position.next_white.next_white.next_white.position[0]][
                            piece.position.next_white.next_white.next_white.position[1]].piece = piece
                        self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                        piece.position = self.board[piece.position.next_white.next_white.next_white.position[0]][
                            piece.position.next_white.next_white.next_white.position[1]]
                    else:
                        self.board[piece.position.next_white.next_white.position[0]][
                            piece.position.next_white.next_white.position[1]].piece = piece
                        piece.position = self.board[piece.position.next_white.next_white.position[0]][
                            piece.position.next_white.next_white.position[1]]
                elif piece.position.next_white.next_white.exit == self.WHITE:
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = piece.position.next_white.next_white
                    piece.complete = True
                else:
                    self.board[piece.position.next_white.next_white.next_white.position[0]][
                        piece.position.next_white.next_white.next_white.position[1]].piece = piece
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = self.board[piece.position.next_white.next_white.next_white.position[0]][
                        piece.position.next_white.next_white.next_white.position[1]]
            # same as before but if the piece is white with 4 moves
            elif num_moves == 4:
                if piece.position.entrance == self.WHITE:
                    if piece.position.piece == piece:
                        self.board[piece.position.next_white.next_white.next_white.next_white.position[0]][
                            piece.position.next_white.next_white.next_white.next_white.position[1]].piece = piece
                        self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                        piece.position = \
                        self.board[piece.position.next_white.next_white.next_white.next_white.position[0]][
                            piece.position.next_white.next_white.next_white.next_white.position[1]]
                    else:
                        self.board[piece.position.next_white.next_white.next_white.position[0]][
                            piece.position.next_white.next_white.next_white.position[1]].piece = piece
                        piece.position = self.board[piece.position.next_white.next_white.next_white.position[0]][
                            piece.position.next_white.next_white.next_white.position[1]]
                elif piece.position.next_white.next_white.next_white.exit == self.WHITE:
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = piece.position.next_white.next_white.next_white
                    piece.complete = True
                else:
                    self.board[piece.position.next_white.next_white.next_white.next_white.position[0]][
                        piece.position.next_white.next_white.next_white.next_white.position[1]].piece = piece
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = self.board[piece.position.next_white.next_white.next_white.next_white.position[0]][
                        piece.position.next_white.next_white.next_white.next_white.position[1]]
        elif piece.color == self.BLACK:
            # same as before and continued for if the piece color is black
            if num_moves == 1:
                if piece.position.entrance == self.BLACK:
                    if not piece.position.piece:
                        self.board[piece.position.position[0]][piece.position.position[1]].piece = piece
                    else:
                        self.board[piece.position.next_black.position[0]][
                            piece.position.next_black.position[1]].piece = piece
                        self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                        piece.position = self.board[piece.position.next_black.position[0]][
                            piece.position.next_black.position[1]]
                elif piece.position.exit == self.BLACK:
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.complete = True
                else:
                    self.board[piece.position.next_black.position[0]][
                        piece.position.next_black.position[1]].piece = piece
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = self.board[piece.position.next_black.position[0]][
                        piece.position.next_black.position[1]]
            elif num_moves == 2:
                if piece.position.entrance == self.BLACK:
                    if piece.position.piece == piece:
                        self.board[piece.position.next_black.next_black.position[0]][
                            piece.position.next_black.next_black.position[1]].piece = piece
                        self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                        piece.position = self.board[piece.position.next_black.next_black.position[0]][
                            piece.position.next_black.next_black.position[1]]
                    else:
                        self.board[piece.position.next_black.position[0]][
                            piece.position.next_black.position[1]].piece = piece
                        piece.position = self.board[piece.position.next_black.position[0]][
                            piece.position.next_black.position[1]]
                elif piece.position.next_black.exit == self.BLACK:
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = piece.position.next_black
                    piece.complete = True
                else:
                    self.board[piece.position.next_black.next_black.position[0]][
                        piece.position.next_black.next_black.position[1]].piece = piece
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = self.board[piece.position.next_black.next_black.position[0]][
                        piece.position.next_black.next_black.position[1]]
            elif num_moves == 3:
                if piece.position.entrance == self.BLACK:
                    if piece.position.piece == piece:
                        self.board[piece.position.next_black.next_black.next_black.position[0]][
                            piece.position.next_black.next_black.next_black.position[1]].piece = piece
                        self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                        piece.position = self.board[piece.position.next_black.next_black.next_black.position[0]][
                            piece.position.next_black.next_black.next_black.position[1]]
                    else:
                        self.board[piece.position.next_black.next_black.position[0]][
                            piece.position.next_black.next_black.position[1]].piece = piece
                        piece.position = self.board[piece.position.next_black.next_black.position[0]][
                            piece.position.next_black.next_black.position[1]]
                elif piece.position.next_black.next_black.exit == self.BLACK:
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = piece.position.next_black.next_black
                    piece.complete = True
                else:
                    self.board[piece.position.next_black.next_black.next_black.position[0]][
                        piece.position.next_black.next_black.next_black.position[1]].piece = piece
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = self.board[piece.position.next_black.next_black.next_black.position[0]][
                        piece.position.next_black.next_black.next_black.position[1]]
            elif num_moves == 4:
                if piece.position.entrance == self.BLACK:
                    if piece.position.piece == piece:
                        self.board[piece.position.next_black.next_black.next_black.next_black.position[0]][
                            piece.position.next_black.next_black.next_black.next_black.position[1]].piece = piece
                        self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                        piece.position = \
                        self.board[piece.position.next_black.next_black.next_black.next_black.position[0]][
                            piece.position.next_black.next_black.next_black.next_black.position[1]]
                    else:
                        self.board[piece.position.next_black.next_black.next_black.position[0]][
                            piece.position.next_black.next_black.next_black.position[1]].piece = piece
                        piece.position = self.board[piece.position.next_black.next_black.next_black.position[0]][
                            piece.position.next_black.next_black.next_black.position[1]]
                elif piece.position.next_black.next_black.next_black.exit == self.BLACK:
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = piece.position.next_black.next_black.next_black
                    piece.complete = True
                else:
                    self.board[piece.position.next_black.next_black.next_black.next_black.position[0]][
                        piece.position.next_black.next_black.next_black.next_black.position[1]].piece = piece
                    self.board[piece.position.position[0]][piece.position.position[1]].piece = None
                    piece.position = self.board[piece.position.next_black.next_black.next_black.next_black.position[0]][
                        piece.position.next_black.next_black.next_black.next_black.position[1]]
        self.display_board()

    # this helper function is used to see if all 7 pieces have completed the race
    # if so, the player has won the game
    def check_complete(self, pieces, player):
        complete_list = []
        for i in range(len(pieces)):
            if pieces[i].complete:
                complete_list.append(pieces[i])
        if len(complete_list) == self.STARTING_PIECES:
            print(player, "has won the game.")
            return True
        else:
            return False

    # this helper function checks to see if any of the pieces have been captured(or knocked off)
    def check_capture(self, white_pieces, white_start, black_pieces, black_start, player_turn):
        # for the player with the white pieces
        if player_turn == 0:
            # checks through all the white pieces
            for i in range(len(white_pieces)):
                # checks to see if a black piece is on the same position with the i white piece
                for j in range(len(black_pieces)):
                    if white_pieces[i].position == black_pieces[j].position:
                        print(black_pieces[j].symbol, "has been knocked off the board.")
                        black_pieces[j].position = black_start
        # for the player with the black pieces, same as before but reversed
        elif player_turn == 1:
            for i in range(len(black_pieces)):
                for j in range(len(white_pieces)):
                    if black_pieces[i].position == white_pieces[j].position:
                        print(white_pieces[j].symbol, "has been knocked off the board.")
                        white_pieces[j].position = white_start

    # this helper function is used to keep track of which pieces are on the rosettes
    def check_rosette(self, pieces, rosette_list):
        for i in range(len(pieces)):
            if pieces[i].position.rosette:
                if not pieces[i] in rosette_list:
                    rosette_list.append(pieces[i])
        return rosette_list

    # this helper function is used to determine if the player can take another turn
    # if the player is on the rosette and not in the list, they are allowed to take another turn
    def another_turn(self, pieces, rosette_list):
        for i in range(len(pieces)):
            if pieces[i].position.rosette and pieces[i] not in rosette_list:
                return True
        return False

    # this helper function is used to check if a piece that was previously on a rosette has moved off
    # it does this by removing it from the rosette list itself
    def check_rosette_move(self, pieces, rosette_list):
        for i in range(len(pieces)):
            if not pieces[i].position.rosette and pieces[i] in rosette_list:
                rosette_list.remove(pieces[i])
        return rosette_list


if __name__ == '__main__':
    file_name = input('What is the file name of the board json? ') if len(argv) < 2 else argv[1]
    rgu = RoyalGameOfUr(file_name)
    rgu.play_game()
