"""
File:        board_square.py
Author:      Joey Hardester
Date:        11/5/2020
Section:     31
E-mail:      josephh5@umbc.edu
Description: This file is to help determine if a piece can move to a certain spot for
             Project2.
"""


class UrPiece:
    WhiteStarts = []
    WhiteEnds = []
    BlackStarts = []
    BlackEnds = []

    def __init__(self, color, symbol):
        self.color = color
        self.position = None
        self.complete = False
        self.symbol = symbol

    def can_move(self, num_moves):
        # for all white pieces since they use a different attribute called next_white
        if self.color == "White":
            if num_moves == 1:
                # if the piece has already completed the race, it cannot move
                if self.complete:
                    return False
                # if the piece is on the exit position, since they rolled a 1, they are allowed to move
                # forward in order to complete the race
                if self.position.exit == "White":
                    return True
                else:
                    # if the piece is at the entrance but not on the board, it is moved to the first spot
                    if self.position.entrance == "White":
                        if not self.position.piece:
                            return True
                        else:
                            # if the piece is already on the entrance block, it can move to the next_white space
                            if self.position.piece == self:
                                if self.position.next_white:
                                    if self.position.next_white.piece:
                                        return False
                                    else:
                                        return True
                                else:
                                    return True
                            else:
                                return False
                    else:
                        # the remaining code is for if the piece is off the entrance and can move ahead
                        if self.position.next_white:
                            # if there is no piece in the next spot, it can move
                            if not self.position.next_white.piece:
                                return True
                            # if the piece on the next block is a black piece, unless it is a rosette,
                            # the piece can move and knock the black piece off the board
                            elif self.position.next_white.piece.color == "Black":
                                if self.position.next_white.rosette:
                                    return False
                                else:
                                    return True
                            else:
                                return False
                        else:
                            return False
            elif num_moves == 2:
                # same steps as before, but instead checks 2 spaces ahead since the player rolled a 2
                if self.complete:
                    return False
                if self.position.exit == "White":
                    return False
                else:
                    if self.position.next_white.exit == "White":
                        return True
                    else:
                        if self.position.entrance == "White":
                            if self.position.piece == self:
                                if not self.position.next_white.next_white.piece:
                                    return True
                                else:
                                    return False
                            else:
                                if not self.position.next_white.piece:
                                    return True
                                else:
                                    return False
                        else:
                            if self.position.next_white.next_white:
                                if not self.position.next_white.next_white.piece:
                                    return True
                                elif self.position.next_white.next_white.piece.color == "Black":
                                    if self.position.next_white.next_white.rosette:
                                        return False
                                    else:
                                        return True
                                else:
                                    return False
                            else:
                                return False
            elif num_moves == 3:
                # same as the first move set, but checks 3 spaces ahead since the player rolled a 3
                if self.complete:
                    return False
                if self.position.exit == "White":
                    return False
                else:
                    if self.position.next_white.exit == "White":
                        return False
                    else:
                        if self.position.next_white.next_white.exit == "White":
                            return True
                        else:
                            if self.position.entrance == "White":
                                if self.position.piece == self:
                                    if not self.position.next_white.next_white.next_white.piece:
                                        return True
                                    else:
                                        return False
                                else:
                                    if not self.position.next_white.next_white.piece:
                                        return True
                                    else:
                                        return False
                            else:
                                if self.position.next_white.next_white.next_white:
                                    if not self.position.next_white.next_white.next_white.piece:
                                        return True
                                    elif self.position.next_white.next_white.next_white.piece.color == "Black":
                                        if self.position.next_white.next_white.next_white.rosette:
                                            return False
                                        else:
                                            return True
                                    else:
                                        return False
                                else:
                                    return False
            elif num_moves == 4:
                # same as before but if the player rolled a 4
                if self.complete:
                    return False
                if self.position.exit == "White":
                    return False
                else:
                    if self.position.next_white.exit == "White":
                        return False
                    else:
                        if self.position.next_white.next_white.exit == "White":
                            return False
                        else:
                            if self.position.next_white.next_white.next_white.exit == "White":
                                return True
                            else:
                                if self.position.entrance == "White":
                                    if self.position.piece == self:
                                        if not self.position.next_white.next_white.next_white.next_white.piece:
                                            return True
                                        else:
                                            return False
                                    else:
                                        if not self.position.next_white.next_white.next_white.piece:
                                            return True
                                        else:
                                            return False
                                else:
                                    if self.position.next_white.next_white.next_white.next_white:
                                        if not self.position.next_white.next_white.next_white.next_white.piece:
                                            return True
                                        elif self.position.next_white.next_white.next_white.next_white.piece.color == "Black":
                                            if self.position.next_white.next_white.next_white.next_white.rosette:
                                                return False
                                            else:
                                                return True
                                        else:
                                            return False
                                    else:
                                        return False
        # same as before but if the colors were switched
        elif self.color == "Black":
            if num_moves == 1:
                if self.complete:
                    return False
                if self.position.exit == "Black":
                    return True
                else:
                    if self.position.entrance == "Black":
                        if not self.position.piece:
                            return True
                        else:
                            if self.position.piece == self:
                                if self.position.next_black:
                                    if self.position.next_black.piece:
                                        return False
                                    else:
                                        return True
                                else:
                                    return True
                            else:
                                return False
                    else:
                        if self.position.next_black:
                            if not self.position.next_black.piece:
                                return True
                            elif self.position.next_black.piece.color == "White":
                                if self.position.next_black.rosette:
                                    return False
                                else:
                                    return True
                            else:
                                return False
                        else:
                            return False
            elif num_moves == 2:
                if self.complete:
                    return False
                if self.position.exit == "Black":
                    return False
                else:
                    if self.position.next_black.exit == "Black":
                        return True
                    else:
                        if self.position.entrance == "Black":
                            if self.position.piece == self:
                                if not self.position.next_black.next_black.piece:
                                    return True
                                else:
                                    return False
                            else:
                                if not self.position.next_black.piece:
                                    return True
                                else:
                                    return False
                        else:
                            if self.position.next_black.next_black:
                                if not self.position.next_black.next_black.piece:
                                    return True
                                elif self.position.next_black.next_black.piece.color == "White":
                                    if self.position.next_black.next_black.rosette:
                                        return False
                                    else:
                                        return True
                                else:
                                    return False
                            else:
                                return False
            elif num_moves == 3:
                if self.complete:
                    return False
                if self.position.exit == "Black":
                    return False
                else:
                    if self.position.next_black.exit == "Black":
                        return False
                    else:
                        if self.position.next_black.next_black.exit == "Black":
                            return True
                        else:
                            if self.position.entrance == "Black":
                                if self.position.piece == self:
                                    if not self.position.next_black.next_black.next_black.piece:
                                        return True
                                    else:
                                        return False
                                else:
                                    if not self.position.next_black.next_black.piece:
                                        return True
                                    else:
                                        return False
                            else:
                                if self.position.next_black.next_black.next_black:
                                    if not self.position.next_black.next_black.next_black.piece:
                                        return True
                                    elif self.position.next_black.next_black.next_black.piece.color == "White":
                                        if self.position.next_black.next_black.next_black.rosette:
                                            return False
                                        else:
                                            return True
                                    else:
                                        return False
                                else:
                                    return False
            elif num_moves == 4:
                if self.complete:
                    return False
                if self.position.exit == "Black":
                    return False
                else:
                    if self.position.next_black.exit == "Black":
                        return False
                    else:
                        if self.position.next_black.next_black.exit == "Black":
                            return False
                        else:
                            if self.position.next_black.next_black.next_black.exit == "Black":
                                return True
                            else:
                                if self.position.entrance == "Black":
                                    if self.position.piece == self:
                                        if not self.position.next_black.next_black.next_black.next_black.piece:
                                            return True
                                        else:
                                            return False
                                    else:
                                        if not self.position.next_black.next_black.next_black.piece:
                                            return True
                                        else:
                                            return False
                                else:
                                    if self.position.next_black.next_black.next_black.next_black:
                                        if not self.position.next_black.next_black.next_black.next_black.piece:
                                            return True
                                        elif self.position.next_black.next_black.next_black.next_black.piece.color == "White":
                                            if self.position.next_black.next_black.next_black.next_black.rosette:
                                                return False
                                            else:
                                                return True
                                        else:
                                            return False
                                    else:
                                        return False


class BoardSquare:
    def __init__(self, x, y, entrance=False, _exit=False, rosette=False, forbidden=False):
        self.piece = None
        self.position = (x, y)
        self.next_white = None
        self.next_black = None
        self.exit = _exit
        self.entrance = entrance
        self.rosette = rosette
        self.forbidden = forbidden

    def load_from_json(self, json_string):
        import json
        loaded_position = json.loads(json_string)
        self.piece = None
        self.position = loaded_position['position']
        self.next_white = loaded_position['next_white']
        self.next_black = loaded_position['next_black']
        self.exit = loaded_position['exit']
        self.entrance = loaded_position['entrance']
        self.rosette = loaded_position['rosette']
        self.forbidden = loaded_position['forbidden']

    def jsonify(self):
        next_white = self.next_white.position if self.next_white else None
        next_black = self.next_black.position if self.next_black else None
        return {'position': self.position, 'next_white': next_white, 'next_black': next_black, 'exit': self.exit,
                'entrance': self.entrance, 'rosette': self.rosette, 'forbidden': self.forbidden}
