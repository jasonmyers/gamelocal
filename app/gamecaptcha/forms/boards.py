# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools
from collections import namedtuple
import random


class Position(namedtuple('Position', 'x y')):

    def __add__(self, other):
        return Position(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        return Position(self.x + other[0], self.y + other[1])

    def __neg__(self):
        return Position(-self.x, -self.y)


class GamePiece(object):
    def __init__(self, glyph, x, y):
        self.glyph = glyph
        self.position = Position(x, y)

    def __getitem__(self, key):
        return self.position[key]

    def __unicode__(self):
        return "{self.glyph} ({self.x}, {self.y})".format(self=self)

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y


class ChessPiece(GamePiece):
    @staticmethod
    def horizontal(old, new, limit=None):
        """ True if the old and new positions are horizontal from
        each other

        Positions must not be further apart than `limit`
        """
        dx = abs(new.x - old.x)
        if limit is not None and dx > limit:
            return False
        return old.y == new.y and old.x != new.x

    @staticmethod
    def vertical(old, new, limit=None):
        """ True if the old and new positions are vertical from
        each other

        Positions must not be further apart than `limit`
        """
        dy = abs(new.y - old.y)
        if limit is not None and dy > limit:
            return False
        return old.x == new.x and old.y != new.y

    @staticmethod
    def diagonal(old, new, limit=None):
        """ True if the old and new position are diagonal from
        each other

        Positions must not be further apart than `limit`
        """
        dx, dy = abs(new.x - old.x), abs(new.y - old.y)
        if limit is not None and (dx > limit or dy > limit):
            return False
        return dx == dy

    @staticmethod
    def knights(old, new, limit=None):
        """ True if the old and new position are a knight's
        jump apart

        `limit` argument is ignored
        """
        return {abs(new.x - old.x), abs(new.y - old.y)} == {1, 2}

    @classmethod
    def make_checkable_position(cls, target, board):
        """ Given a target on the board, generate a position that is one
        move away from giving check
        """
        assert board.size.x > 1
        assert board.size.y > 1
        position = None
        while position is None or position == target:
            position = Position(
                random.randint(0, board.size.x - 1),
                random.randint(0, board.size.y - 1),
            )
        return position


class King(ChessPiece):
    def can_move(self, new):
        return (
            self.horizontal(self.position, new, limit=1) or
            self.vertical(self.position, new, limit=1) or
            self.diagonal(self.position, new, limit=1)
        )


class Queen(ChessPiece):
    def can_move(self, new):
        return (
            self.horizontal(self.position, new) or
            self.vertical(self.position, new) or
            self.diagonal(self.position, new)
        )


class Rook(ChessPiece):
    def can_move(self, new):
        return (
            self.horizontal(self.position, new) or
            self.vertical(self.position, new)
        )


class Bishop(ChessPiece):
    def can_move(self, new):
        return self.diagonal(self.position, new)

    @classmethod
    def make_checkable_position(cls, target, board):
        position = super(Bishop, cls).make_checkable_position(
            target, board)

        # Make sure we're on same color square as the target
        if (
            board.square_color(position)
            != board.square_color(target)
        ):
            # Move one right and wrap if needed
            position = position + (1, 0)
            if position.x >= board.size.x:
                position = Position(0, position.y)

        return position


class Knight(ChessPiece):
    # (2, 1), (1, 2), etc.
    JUMPS = [
        Position(*p) for p in
        filter(sum, itertools.permutations([-2, -1, 1, 2], 2))
    ]

    def can_move(self, new):
        return self.knights(self.position, new)

    @classmethod
    def make_checkable_position(cls, target, board):
        """ Jump twice away from the target, if we're on the board then
        that's a valid knight position
        """
        position = None
        while position is None or not board.on_board(position):
            first_jump = random.choice(Knight.JUMPS)
            first_position = target + first_jump

            second_jump = random.choice([
                jump for jump in Knight.JUMPS
                if jump != -first_jump
            ])
            position = first_position + second_jump

        return position


class GoPiece(GamePiece):
    pass


class Board(object):
    EMPTY = '_'
    DELIM = '|'
    NONPIECE = EMPTY + DELIM

    PIECES = {}

    TARGET = ''
    MOVERS = ()

    DEFAULT_SIZE = 8

    def __init__(self, board_code):
        self._code = board_code
        self.board = [list(row) for row in board_code.split(self.DELIM)]
        self.size = Position(len(self.board[0]), len(self.board))
        self.pieces = [
            self.PIECES[glyph](glyph, x, y)
            for y, row in enumerate(self.board)
            for x, glyph in enumerate(row)
            if glyph not in self.NONPIECE
        ]

    def __getitem__(self, key):
        return self.board[key[1]][key[0]]

    def __setitem__(self, key, value):
        self.board[key[1]][key[0]] = value
        self.pieces.append(
            self.PIECES[value](value, key[0], key[1])
        )

    def __delitem__(self, key):
        if self.board[key[1]][key[0]] == self.EMPTY:
            return
        self.board[key[1]][key[0]] = self.EMPTY
        delete = self.find_piece(key=lambda p: p.position == key)
        self.pieces.remove(delete)

    def __unicode__(self):
        return self.DELIM.join(''.join(row) for row in self.board)

    def pretty(self):
        return '\n'.join('|'.join(row) for row in self.board)

    def find_piece(self, key=None):
        """ Returns the first piece on the board
        that matches the `key` func
        """
        if key is None:
            key = lambda p: True
        return next(p for p in self.pieces if key(p))

    def on_board(self, position):
        """ Returns True if the given position is within the board """
        if not (0 <= position.x < self.size.x):
            return False
        if not (0 <= position.y < self.size.y):
            return False
        return True

    @classmethod
    def empty_board(cls, size=None):
        """ Constructs a empty Board """
        if size is None:
            size = cls.DEFAULT_SIZE
        return cls(cls.DELIM.join(cls.EMPTY * size for _ in xrange(size)))


class ChessBoard(Board):
    PIECES = {
        '♔': King,
        '♛': Queen,
        '♜': Rook,
        '♝': Bishop,
        '♞': Knight,
    }

    TARGET = '♔'
    MOVERS = tuple(
        piece for piece, cls in PIECES.iteritems()
        if cls != King
    )

    DEFAULT_SIZE = 8

    @staticmethod
    def square_color(position):
        return ['light', 'dark'][position.y % 2 ^ position.x % 2]

    @classmethod
    def generate_board(cls):
        board = cls.empty_board()

        target = board.PIECES[board.TARGET](
            board.TARGET,
            random.randint(0, board.DEFAULT_SIZE - 1),
            random.randint(0, board.DEFAULT_SIZE - 1),
        )
        mover = None
        count = 0
        mover_glyph = random.choice(board.MOVERS)
        MoverClass = board.PIECES[mover_glyph]

        while not board.valid_problem(target, mover):
            count += 1
            mover_position = MoverClass.make_checkable_position(
                target, board,
            )

            mover = MoverClass(
                mover_glyph, mover_position.x, mover_position.y
            )

        board[target] = target.glyph
        board[mover] = mover.glyph

        print "Generated board in {} tries:\n\n{}".format(
            count,
            '\n'.join(board.DELIM.join(row) for row in board.board)
        )
        return board

    def valid_problem(self, target, mover):
        """ Checks that a board is valid for solving (i.e. king not in check,
        piece is able to move into check) """
        if not target or not mover:
            return False

        if target == mover.position:
            return False

        if mover.can_move(target):
            # King in check
            return False

        return True


class GoBoard(Board):
    PIECES = {
        '○': GoPiece,
        '●': GoPiece,
    }

    TARGET = '○'
    MOVERS = ('●',)

    DEFAULT_SIZE = 9

    LIBERTIES = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def liberties(self, position):
        return [
            neighbor for neighbor in (
                position + delta for delta in self.LIBERTIES
            )
            if self.on_board(neighbor)
            and self[neighbor] == self.EMPTY
        ]

    @classmethod
    def generate_board(cls):
        board = cls.empty_board()

        # Initial stone
        target = board.PIECES[board.TARGET](
            board.TARGET,
            random.randint(0, board.DEFAULT_SIZE - 1),
            random.randint(0, board.DEFAULT_SIZE - 1),
        )

        board[target] = target.glyph

        # Recursively add a few more stones
        board.add_stones(target.position)

        # Surround with black stones
        for target in (
            piece for piece in board.pieces
            if piece.glyph == board.TARGET
        ):
            for liberty in board.liberties(target.position):
                if board.on_board(liberty):
                    board[liberty] = board.MOVERS[0]

        # Remove just one black stone

        black_stones = [
            piece for piece in board.pieces if piece.glyph == board.MOVERS[0]
        ]
        if not black_stones:
            black_stones = board.pieces
        answer = random.choice(black_stones)

        del board[answer.position]

        count = 1
        print "Generated board in {} tries:\n\n{}".format(
            count,
            '\n'.join(board.DELIM.join(row) for row in board.board)
        )
        return board

    def add_stones(self, position):
        for liberty in self.LIBERTIES:
            if random.random() > .30:
                continue
            new_position = position + liberty
            if (
                self.on_board(new_position) and
                self[new_position] == self.EMPTY
            ):
                target = self.PIECES[self.TARGET](
                    self.TARGET,
                    new_position.x,
                    new_position.y,
                )

                self[target] = target.glyph

                self.add_stones(target.position)


GAMECAPTCHA_BOARDS = {
    'go': GoBoard,
    'chess': ChessBoard,
}
