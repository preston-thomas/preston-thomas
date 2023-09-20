# -*- coding: utf-8 -*-
"""new project 4

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C6q1ZXCDYpEw9w3NbY6eLDdfIFoXBaAs
"""

import abc
import random
from _ast import List
from typing import Tuple

import pygame
from pygame import color
from pygame.examples.textinput import Game

from images import *
from enum import Enum
import pygame as pg
import pygame_gui as gui
from game import *


class Color(Enum):
    """This class will hold enumerated values for WHITE & BLACK pieces.
    """
    BLACK = 0
    WHITE = 1


class Piece(abc.ABC):
    """This class will handle data related to the pieces.
    """
    SPRITESHEET = pg.image.load("pieces.png")
    _game = None

    def set_game(game):
        """This method sets the game.
        """
        if not isinstance(game, Game):
            raise ValueError("You must provide a valid Game instance.")
        Piece._game = game

    def __init__(self, _color: Color):
        """This is the constructor for the Piece class.

        Parameters: color(Color)
        """
        self._color = _color
        self._image = pygame.Surface((105, 105), pg.SRCALPHA)

    @property
    def color(self):
        return self._color

    def set_image(self, x: int, y: int):
        """This method will set the image of the Chess piece.

        Parameters: x(int), y(int)
        Return: None
        """
        self._image.blit(Piece.SPRITESHEET, (0, 0), pygame.rect.Rect(x, y, 105, 105))

    def _diagonal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> List(Tuple[int, int]):
        """Given a starting position (y, x) on the board and a diagonal direction vector (y_d, x_d),
        returns a list of valid moves in that direction up to the given distance.

        Args:
            y (int): The starting row position.
            x (int): The starting column position.
            y_d (int): The direction vector for rows. -1 for up, 1 for down.
            x_d (int): The direction vector for columns. -1 for left, 1 for right.
            distance (int): The maximum number of spaces to check in the given direction.

        Returns:
            List[Tuple[int, int]]: A list of valid moves in the diagonal direction.
        """

        # Can't really test this method's functionality until the Game class is implemented.
        moves = []
        y += y_d
        x += x_d
        count = 0
        while count < distance:
            count += 1
            if y < 0 or y > 7 or x < 0 or x > 7:
                # check if we've gone off the edge of the board
                break
            if Piece._game.get(y, x) is None:
                # if the square is empty, it's a valid move
                moves.append((y, x))
                x += x_d
                y += y_d
            else:
                # if there is a piece on the square, check if we can capture it
                if self._color != Piece._game.get(y, x).color:
                    moves.append((y, x))
                break  # stop checking in this direction
        return moves

    def _horizontal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> List(Tuple[int, int]):
        """
        Finds all valid moves horizontally from a given position up to a certain distance.

        Args:
            y (int): The y position on the board to start from.
            x (int): The x position on the board to start from.
            y_d (int): The direction to check vertically. Should be either -1 or 1.
            x_d (int): The direction to check horizontally. Should be either -1 or 1.
            distance (int): The maximum number of spaces to check from the starting position.

        Returns:
            List[Tuple[int, int]]: A list of all valid moves in the horizontal direction.
        """
        moves = []
        x += x_d
        count = 0
        while count < distance:
            count += 1
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            if Piece._game.get(y, x) is None:
                moves.append((y, x))
                x += x_d
            else:
                if Piece._game.get(y, x).color != self._color:
                    moves.append((y, x))
                    x += x_d

        return moves

    def _vertical_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> List(Tuple[int, int]):
        """
        Finds all valid moves vertically from a given position up to a certain distance.

        Parameters:
            y (int): The y position on the board to start from.
            x (int): The x position on the board to start from.
            y_d (int): The direction to check vertically. Should be either -1 or 1.
            x_d (int): The direction to check horizontally. Should be either -1 or 1.
            distance (int): The maximum number of spaces to check from the starting position.

        Returns:
            List[Tuple[int, int]]: A list of all valid moves in the vertical direction.
        """

        moves = []
        y += y_d
        count = 0
        while count < distance:
            count += 1
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            if Piece._game.get(y, x) is None:
                moves.append((y, x))
                y += y_d
            else:
                if Piece._game.get(y, x).color != self._color:
                    moves.append((y, x))
                break
        return moves

    def get_diagonal_moves(self, y: int, x: int, distance: int) -> List(Tuple[int, int]):
        """This method will get the possible diagonal moves

        Parameters:
            y(int): y-coordinate
            x(int): x-coordinate
            distance(int): number of spaces to check from starting position
        """
        moves = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                list1 = self._diagonal_moves(y, x, i, j, distance)
                for move in list1:
                    moves.append(move)
        return moves

    def get_horizontal_moves(self, y: int, x: int, distance: int) -> List(Tuple[int, int]):
        """This method will get the possible horizontal moves

        Parameters:
            y(int): y-coordinate
            x(int): x-coordinate
            distance(int): number of spaces to check from starting position
        """
        moves = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                list1 = self._horizontal_moves(y, x, i, j, distance)
                for move in list1:
                    moves.append(move)
        return moves

    def get_vertical_moves(self, y: int, x: int, distance: int) -> List(Tuple[int, int]):
        """This method will get the possible vertical moves

        Parameters:
            y(int): y-coordinate
            x(int): x-coordinate
            distance(int): number of spaces to check from starting position
        """
        moves = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                list1 = self._vertical_moves(y, x, i, j, distance)
                for move in list1:
                    moves.append(move)
        return moves


class King(Piece):
    """ The King class will hold data for the King pieces.

    Attributes:
        color(Color): Piece's color.
    """

    def __init__(self, color: Color):
        """Constructor for the King class.

        Parameters:
            color(Color): color of the piece
        """
        super().__init__(color)
        if color == Color.BLACK:
            self.set_image(0, 105)
        if color == Color.WHITE:
            self.set_image(0, 0)

    def valid_moves(self, y: int, x: int) -> List(Tuple[int, int]):
        """Returns valid moves.

        Parameters:
            y(int): y-coordinate
            x(int): x-coordinate

        Return:
            List[Tuple[int, int]]: Valid moves
        """
        # return self.get_diagonal_moves(y, x, 1), self.get_vertical_moves(y, x, 1), self.get_horizontal_moves(y, x, 1)
        moves = []
        diagmoves = self.get_diagonal_moves(y, x, 1)
        for i in diagmoves:
            moves.append(i)
        vertmoves = self.get_vertical_moves(y, x, 1)
        for i in vertmoves:
            moves.append(i)
        horizmoves = self.get_horizontal_moves(y, x, 1)
        for i in horizmoves:
            moves.append(i)
        return moves

    def copy(self):
        """Returns a new piece of the same color.

        Return:
            new_king(King): Piece of the same color.
        """
        new_king = King(self.color)
        return new_king


class Queen(Piece):
    """This class stores data about the Queen piece.

    Attributes:
        color(Color): Piece's color
    """

    def __init__(self, color: Color):
        """Constructor for the Queen class.

        Parameters:
            color(Color): color of the piece
        """
        super().__init__(color)
        if color == Color.BLACK:
            self.set_image(105, 105)
        if color == Color.WHITE:
            self.set_image(105, 0)

    def valid_moves(self, y: int, x: int) -> List(Tuple[int, int]):
        """Returns valid moves.

        Parameters:
            y(int): y-coordinate
            x(int): x-coordinate

        Return:
            List[Tuple[int, int]]: Valid moves
        """
        # return self.get_diagonal_moves(y, x, 8), self.get_vertical_moves(y, x, 8), self.get_horizontal_moves(y, x, 8)
        moves = []
        diagmoves = self.get_diagonal_moves(y, x, 8)
        for i in diagmoves:
            moves.append(i)
        vertmoves = self.get_vertical_moves(y, x, 8)
        for i in vertmoves:
            moves.append(i)
        horizmoves = self.get_horizontal_moves(y, x, 8)
        for i in horizmoves:
            moves.append(i)
        return moves

    def copy(self):
        """Returns a new piece of the same color.

        Return:
            new_queen(Queen): Piece of the same color.
        """
        new_queen = Queen(self.color)
        return new_queen


class Bishop(Piece):
    """This class stores data about the Bishop piece.

    Attributes:
        color(Color): Piece's color
    """

    def __init__(self, color: Color):
        """Constructor for the Bishop class.

        Parameters:
            color(Color): color of the piece
        """
        super().__init__(color)
        if color == Color.BLACK:
            self.set_image(210, 105)
        if color == Color.WHITE:
            self.set_image(210, 0)

    def valid_moves(self, y: int, x: int) -> List(Tuple[int, int]):
        """Returns valid moves.

        Parameters:
            y(int): y-coordinate
            x(int): x-coordinate

        Return:
            List[Tuple[int, int]]: Valid moves
        """
        return self.get_diagonal_moves(y, x, 8)

    def copy(self):
        """Returns a new piece of the same color.

        Return:
            new_bishop(Bishop): Piece of the same color.
        """
        new_bishop = Bishop(self.color)
        return new_bishop


class Knight(Piece):
    """This class stores data associated with the Knight piece.

    Attributes:
        color(str): Piece's color
    """

    def __init__(self, color: Color):
        """Constructor for the Knight class.

        Parameters:
            color(Color): color of the piece
        """
        super().__init__(color)
        if color == Color.BLACK:
            self.set_image(315, 105)
        if color == Color.WHITE:
            self.set_image(315, 0)

    def valid_moves(self, y: int, x: int) -> List(Tuple[int, int]):
        """Returns valid moves.

        Parameters:
            y(int): y-coordinate
            x(int): x-coordinate

        Return:
            List[Tuple[int, int]]: Valid moves
        """
        moves = [(y - 1, x - 2), (y - 2, x - 1), (y - 2, x + 1), (y - 1, x + 2),
                 (y + 2, x + 1), (y + 1, x + 2), (y + 2, x - 1), (y + 1, x - 2)]
        valid_moves = []
        for move in moves:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:  # Check if move is within the board
                piece = Piece._game.get(move[0], move[1])  # Get the piece at the move position
                if not piece or piece.color != self.color:  # Check if move is valid (i.e., not taking your own piece)
                    valid_moves.append(move)
        return valid_moves

    def copy(self):
        """Returns a new piece of the same color.

        Return:
            new_knight(Knight): Piece of the same color.
        """
        new_knight = Knight(self.color)
        return new_knight


class Rook(Piece):
    """This class will store data associated with the Rook piece.

    Attributes:
        color(Color): Piece's color.
    """

    def __init__(self, color: Color):
        """Constructor for the Rook class.

        Parameters:
            color(Color): color of the piece
        """
        super().__init__(color)
        if color == Color.BLACK:
            self.set_image(420, 105)
        if color == Color.WHITE:
            self.set_image(420, 0)

    def valid_moves(self, y: int, x: int) -> List(Tuple[int, int]):
        """Returns valid moves.

        Parameters:
            y(int): y-coordinate
            x(int): x-coordinate

        Return:
            List[Tuple[int, int]]: Valid moves
        """
        moves = []
        vertmoves = self.get_vertical_moves(y, x, 8)
        for i in vertmoves:
            moves.append(i)
        horizmoves = self.get_horizontal_moves(y, x, 8)
        for j in horizmoves:
            moves.append(j)
        return moves

    def copy(self):
        """Returns a new piece of the same color.

        Return:
            new_rook(Rook): Piece of the same color.
        """
        new_rook = Rook(self.color)
        return new_rook


class Pawn(Piece):
    """This class stores data associated with the Pawn piece.

    Attributes:
        color(Color): Piece's color
    """

    def __init__(self, color: Color):
        """Constructor for the Pawn class.

        Parameters:
            color(Color): color of the piece
        """
        super().__init__(color)
        self.pawn_color = color
        if color == Color.BLACK:
            self.set_image(525, 105)
        if color == Color.WHITE:
            self.set_image(525, 0)
        self.first_move = True

    def valid_moves(self, y: int, x: int) -> List(Tuple[int, int]):
        """Returns valid moves.

        Parameters:
            y(int): y-coordinate
            x(int): x-coordinate

        Return:
            List[Tuple[int, int]]: Valid moves
        """
        moves = []
        if self.first_move:  # checks if it's the first move
            if self.color == Color.BLACK:
                if Piece._game.get(y - 2, x) is None:
                    moves += self.get_vertical_moves(y, x, 2)
            if self.color == Color.WHITE:
                if Piece._game.get(y + 2, x) is None:
                    moves += self.get_vertical_moves(y, x, 2)
        else:
            if self.color == Color.BLACK:
                if Piece._game.get(y + 1, x) is None:
                    moves += [(y + 1, x)]
            if self.color == Color.WHITE:
                if Piece._game.get(y - 1, x) is None:
                    moves += [(y - 1, x)]
        if self.color == Color.BLACK:
            diagonal = [(y + 1, x - 1), (y + 1, x + 1)]
            for k in diagonal:
                if k[0] < 0 or k[0] > 7 or k[1] < 0 or k[1] > 7:
                    continue
                if Piece._game.get(k[0], k[1]) is not None and Piece._game.get(k[0], k[1]).color != self.color:
                    moves.append(k)
        if self.color == Color.WHITE:
            diagonal = [(y - 1, x - 1), (y - 1, x + 1)]
            for k in diagonal:
                if k[0] < 0 or k[0] > 7 or k[1] < 0 or k[1] > 7:
                    continue
                if Piece._game.get(k[0], k[1]) is not None and Piece._game.get(k[0], k[1]).color != self.color:
                    moves.append(k)
        return moves



    def copy(self):
        """Returns a new piece of the same color.

        Return:
            new_pawn(Pawn): Piece of the same color.
        """
        new_pawn = Pawn(self.color)
        return new_pawn


class Stack:
    """
    This class is a stack for storing states of the board.
    """

    def __init__(self):
        self._data = []

    def empty(self):
        return len(self._data) == 0

    def push(self, object) -> None:
        self._data.append(object)

    def peek(self) -> object:
        return self._data[len(self._data) - 1]

    def pop(self) -> object:
        data = self.peek()
        del (self._data[len(self._data) - 1])
        return data


class Game:
    """This class stores data associated with the game.

    Attributes:
        _board[List[List[None]]: Game's board
        current_player: Current player
    """

    def __init__(self):
        self._board = [[None for i in range(8)] for i in range(8)]
        self.current_player = Color.WHITE  ###this isnt right but idk what to say
        Piece.set_game(self)
        self.stack = Stack()
        self.reset()

    def reset(self):
        """Resets the board, player and prior states data to default.
        """
        self._board = [[None for i in range(8)] for i in range(8)]
        self._setup_pieces()

    def _setup_pieces(self):
        """Sets up the pieces on the board.
        """
        bqueen = Queen(Color.BLACK)
        self._board[0][3] = bqueen
        bking = King(Color.BLACK)
        self._board[0][4] = bking
        bbishop1 = Bishop(Color.BLACK)
        self._board[0][2] = bbishop1
        bbishop2 = Bishop(Color.BLACK)
        self._board[0][5] = bbishop2
        brook1 = Rook(Color.BLACK)
        self._board[0][0] = brook1
        brook2 = Rook(Color.BLACK)
        self._board[0][7] = brook2
        bknight1 = Knight(Color.BLACK)
        self._board[0][1] = bknight1
        bknight2 = Knight(Color.BLACK)
        self._board[0][6] = bknight2
        bpawn1 = Pawn(Color.BLACK)
        self._board[1][0] = bpawn1
        bpawn2 = Pawn(Color.BLACK)
        self._board[1][1] = bpawn2
        bpawn3 = Pawn(Color.BLACK)
        self._board[1][2] = bpawn3
        bpawn4 = Pawn(Color.BLACK)
        self._board[1][3] = bpawn4
        bpawn5 = Pawn(Color.BLACK)
        self._board[1][4] = bpawn5
        bpawn6 = Pawn(Color.BLACK)
        self._board[1][5] = bpawn6
        bpawn7 = Pawn(Color.BLACK)
        self._board[1][6] = bpawn7
        bpawn8 = Pawn(Color.BLACK)
        self._board[1][7] = bpawn8
        ##
        wqueen = Queen(Color.WHITE)
        self._board[7][3] = wqueen
        wking = King(Color.WHITE)
        self._board[7][4] = wking
        wbishop1 = Bishop(Color.WHITE)
        self._board[7][2] = wbishop1
        wbishop2 = Bishop(Color.WHITE)
        self._board[7][5] = wbishop2
        wrook1 = Rook(Color.WHITE)
        self._board[7][0] = wrook1
        wrook2 = Rook(Color.WHITE)
        self._board[7][7] = wrook2
        wknight1 = Knight(Color.WHITE)
        self._board[7][1] = wknight1
        wknight2 = Knight(Color.WHITE)
        self._board[7][6] = wknight2
        wpawn1 = Pawn(Color.WHITE)
        self._board[6][0] = wpawn1
        wpawn2 = Pawn(Color.WHITE)
        self._board[6][1] = wpawn2
        wpawn3 = Pawn(Color.WHITE)
        self._board[6][2] = wpawn3
        wpawn4 = Pawn(Color.WHITE)
        self._board[6][3] = wpawn4
        wpawn5 = Pawn(Color.WHITE)
        self._board[6][4] = wpawn5
        wpawn6 = Pawn(Color.WHITE)
        self._board[6][5] = wpawn6
        wpawn7 = Pawn(Color.WHITE)
        self._board[6][6] = wpawn7
        wpawn8 = Pawn(Color.WHITE)
        self._board[6][7] = wpawn8

    def get(self, y: int, x: int):  # -> Optional[Piece]:
        """Returns the piece at the given position, otherwise returns None.

        Parameters:
            y(int): y-coordinate
            x(int): x-coordinate

        Return:
            Optional[Piece]: returns the piece if it is in the position.
        """
        if y in range(8) and x in range(8):
            return self._board[y][x]
        else:
            return None

    def switch_player(self):
        """Switches the current player to opposing player.
        """
        if self.current_player == Color.BLACK:
            self.current_player = Color.WHITE
        else:
            self.current_player = Color.BLACK

    def undo(self):
        """Pops the last board state off of the stack & sets the current board to it.

        Return:
            bool: True if there is a prior state, False otherwise.
        """
        if not self.stack.empty():
            self._board = self.stack.pop()
            self._board = self.stack.pop()
            return True
        return False

    def copy_board(self):  ##i have no clue if this will work
        """Copies the board.
        """
        new_board = []
        for i in range(len(self._board)):
            new_board.append([])
            for j in range(len(self._board[i])):
                new_board[i].append(self._board[i][j])
        self.stack.push(self._board)
        self._board = new_board
        return new_board

    def move(self, piece: Piece, y: int, x: int, y2: int, x2: int) -> bool:
        """This method performs the moves on the board.

        Parameters:
            piece(Piece): piece being moved
            y(int): y-coordinate
            x(int): x-coordinate
            y2(int): new y-coordinate
            x2(int): new x-coordinate

        Return:
            bool: Returns true to indicate a successful move occurred, false otherwise.
        """
        copy = self.copy_board()
        self.stack.push(copy)
        color1 = self._board[y][x].color
        other = None
        if color1 == Color.BLACK:
            other = Color.WHITE
        else:
            other = Color.BLACK
        self._board[y2][x2] = self._board[y][x]
        self._board[y][x] = None
        if color1 == Color.WHITE:
            print('checking white', self.check(Color.WHITE))
            if self.check(Color.WHITE):
                self.undo()
                return False
        if color1 == Color.BLACK:
            if self.check(Color.BLACK):
                self.undo()
                return False
        if isinstance(self._board[y2][x2], Pawn):
            self._board[y2][x2].first_move = False
            if (y2 == 0) and self._board[y2][x2].color == Color.WHITE:
                new_queen = Queen(color1)
                self._board[y2][x2] = new_queen
            if (y2 == 7) and self._board[y2][x2].color == Color.BLACK:
                new_queen = Queen(color1)
                self._board[y2][x2] = new_queen
        return True

    def get_piece_locations(self, color1: Color) -> List(Tuple[int, int]):
        """Returns locations of all pieces on the board for the given color.

        Parameters:
            color1(Color): Piece color

        Return:
            List[Tuple[int, int]]: (y, x) locations for all pieces of the color.
        """
        locations = []
        colora: Color
        if color1 == Color.BLACK:
            colora = Color.BLACK
        else:
            colora = Color.WHITE
        #  for element in self._board:
        #     print(element)
        for y in range(len(self._board)):
            for x in range(len(self._board[y])):
                if self._board[y][x] is None:
                    continue
                if self._board[y][x] is not None and self._board[y][x].color == colora:
                    locations.append((y, x))
        return locations

    def find_king(self, color1: Color) -> Tuple[int, int]:
        """Finds the King piece of the given color.

        Parameters:
            color1(Color): Piece color

        Return: Tuple[int, int]: King's position on the board.
        """
        colora: Color
        if color1 == Color.BLACK:
            colora = Color.BLACK
        else:
            colora = Color.WHITE
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if isinstance(self._board[i][j], King) and self._board[i][j].color == colora:
                    return (i, j)

    def check(self, _color: Color) -> bool:
        """Check if the given color's king is in check.

        Parameters:
            _color(Color): Color of the king to check for.

        Return:
            bool: True if the king is in check, False otherwise.
        """
        other_color = Color.WHITE if _color == Color.BLACK else Color.BLACK
        king_location = self.find_king(_color)
        pieces = self.get_piece_locations(other_color)
        for y, x in pieces:
            moves = self._board[y][x].valid_moves(y, x)
            if king_location in moves:
                return True
        return False


    def mate(self, my_color: Color) -> bool:
        """Verifies if the king is in a checkmate.

        Parameters:
            my_color(Color): Piece's color

        Return:
            bool: Returns True if in a checkmate, False otherwise
        """
        # other: Color
        # _color: Color
        if my_color == Color.BLACK:
            _color = Color.BLACK
            other = Color.WHITE
        else:
            _color = Color.WHITE
            other = Color.BLACK
        if not self.check(_color):
            return False
        pieces = self.get_piece_locations(_color)
        moves = []
        for y, x in pieces:
            each_move = self._board[y][x].valid_moves(y, x)
            for a, b in each_move:
                self.move(self._board[y][x], y, x, a,b)
                if not self.check(_color):
                    #self.undo()
                    return False
                #self.undo()
        return True

    def get_threat(self):
        """
        this function returns the white piece that is in attack position of the black king.
        :return: Piece
        """
        if self.check(Color.BLACK):
            kloc = self.find_king(Color.BLACK)
            pieces = self.get_piece_locations(Color.WHITE)
            for y, x in pieces:
                if kloc in self._board[y][x].valid_moves(y, x):
                    return self._board[y][x]
        return None

    def _computer_move(self):  # this one just returns the best move, would need another function to work properly
        # i dont think we need it, im just afraid to delete it
        checkmates = []
        checks = []
        queen_captures = []
        bishop_captures = []
        knight_captures = []
        rook_captures = []
        pawn_captures = []
        pieces = self.get_piece_locations(Color.BLACK)
        if self.check(Color.BLACK) and self.get_threat() is not None:
            threat = self.get_threat()
            print(threat)
            pieces = self.get_piece_locations(Color.BLACK)
            for y, x in pieces:
                moves = self._board[y][x].valid_moves(y, x)
                for p, q in moves:
                    if self._board[p][q] == threat:
                        self.move(self._board[y][x], y, x, p, q)
                        break
        else:
            #
            #
            #
            #
            pieces = self.get_piece_locations(Color.BLACK)
            for y, x in pieces:
                moves = self._board[y][x].valid_moves(y, x)
                for a, b in moves:
                    ##
                    self.move(self._board[y][x], y, x, a, b)
                    if self.mate(Color.WHITE):
                        checkmates.append((self._board[y][x], y, x, a, b))
                    if self.check(Color.WHITE):
                        checks.append((self._board[y][x], y, x, a, b))
                    self.undo()
                    ##
                    if isinstance(self._board[a][b], Queen):
                        queen_captures.append((self._board[y][x], y, x, a, b))
                    if isinstance(self._board[a][b], Bishop):
                        bishop_captures.append((self._board[y][x], y, x, a, b))
                    if isinstance(self._board[a][b], Knight):
                        knight_captures.append((self._board[y][x], y, x, a, b))
                    if isinstance(self._board[a][b], Rook):
                        rook_captures.append((self._board[y][x], y, x, a, b))
                    if isinstance(self._board[a][b], Pawn):
                        pawn_captures.append((self._board[y][x], y, x, a, b))
            if len(checkmates) != 0:
                self.move(checkmates[0][0], checkmates[0][1], checkmates[0][2], checkmates[0][3], checkmates[0][4])
            if len(checks) != 0:
                self.move(checks[0][0], checks[0][1], checks[0][2], checks[0][3], checks[0][4])
            if len(queen_captures) != 0:
                self.move(queen_captures[0][0], queen_captures[0][1], queen_captures[0][2], queen_captures[0][3], queen_captures[0][4])
            elif len(bishop_captures) != 0:
                self.move(bishop_captures[0][0], bishop_captures[0][1], bishop_captures[0][2], bishop_captures[0][3], bishop_captures[0][4])
            elif len(knight_captures) != 0:
                self.move(knight_captures[0][0], knight_captures[0][1], knight_captures[0][2], knight_captures[0][3], knight_captures[0][4])
            elif len(rook_captures) != 0:
                self.move(rook_captures[0][0], rook_captures[0][1], rook_captures[0][2], rook_captures[0][3], rook_captures[0][4])
            elif len(pawn_captures) != 0:
                self.move(pawn_captures[0][0], pawn_captures[0][1], pawn_captures[0][2], pawn_captures[0][3], pawn_captures[0][4])
            else:
                #
                #
                #
                moves = []
                index = 0
                while len(moves) == 0:
                    pieces = self.get_piece_locations(Color.BLACK)
                    print('pieces', pieces)
                    piece = pieces[random.randint(0, len(pieces)-1)]
                    a, b = piece
                    print(self._board[a][b])
                    moves = self._board[a][b].valid_moves(a, b)
                    print(moves)
                move = moves[random.randint(0, len(moves)-1)]
                c, d = move
                self.move(self._board[a][b], a, b, c, d)