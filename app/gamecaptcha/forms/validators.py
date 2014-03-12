# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

try:
    import urllib2 as http
except ImportError:
    # Python 3
    from urllib import request as http

from flask import request, current_app
from wtforms import ValidationError

from .boards import Board, ChessBoard, GoBoard

__all__ = ["ChessCaptcha", "GoCaptcha"]


class GameCaptcha(object):
    """ A captcha expecting a certain move in a game """

    _error_codes = {
        'invalid-board': 'The board provided for GameCaptcha is invalid',
        'invalid-move': 'The move provided for GameCaptcha is invalid',
    }

    _board_field_name = 'gameCaptchaChallenge'
    _move_field_name = 'gameCaptchaResponse'

    game = 'game'
    Board = Board

    def __init__(self, message="Invalid move.  Please try again."):
        self.message = message

    def __call__(self, form, field):
        self.field = field
        #if current_app.testing:
        #    return True

        if request.json:
            entry = request.json
        else:
            entry = request.form

        board_code = entry.get(self._board_field_name.format(self.game), '')
        move_code = entry.get(self._move_field_name.format(self.game), '')

        # Validate that the board and move are in the correct format
        try:
            board = self.parse_board(board_code)
            move = self.parse_move(move_code)
        except:
            raise ValidationError(self.field.gettext(self.message))

        if (
            not self.validate_board_input(board) or
            not self.validate_move_input(board, move)
        ):
            raise ValidationError(self.field.gettext(self.message))

        # Check for a correct answer
        if not self.validate_captcha(board, move):
            field.captcha_error = 'incorrect-captcha-sol'
            raise ValidationError(self.field.gettext(self.message))

    def parse_board(self, board_code):
        if not board_code:
            raise ValueError('Incorrect board format')
        return self.Board(board_code)

    def parse_move(self, move_code):
        try:
            glyph, x, y = move_code.split()
            return self.Board.PIECES[glyph](glyph, int(x), int(y))
        except:
            raise ValueError('Incorrect move format')

    def validate_board_input(self, board):
        """ A valid board is `_board_size` in dimension,
        is not empty, and contains appropriate pieces
        """
        try:
            if board.size != (
                board.DEFAULT_SIZE,
                board.DEFAULT_SIZE
            ):
                return False

            if any(
                piece for piece in board.pieces
                if piece.glyph not in board.NONPIECE
                and piece.glyph not in board.PIECES
            ):
                return False

            if board.TARGET not in board._code:
                return False

            return True

        except:
            current_app.logger.debug("Invalid board {}".format(board._code))
            return False

    def validate_move_input(self, board, move):
        """ A Valid move consists of a piece and a coordinate within
         the board boundaries

            >>> ChessCaptcha().validate_move_input("♛ 1 1")
            True
            >>> GoCaptcha().validate_move_input("○ 5 6")
            True
            >>> ChessCaptcha().validate_move_input("")
            False
            >>> ChessCaptcha().validate_move_input("♛ 0 0")
            False
            >>> ChessCaptcha().validate_move_input("♛ 10 5")
            False
        """
        try:
            if not move:
                return False

            if move.glyph not in board.PIECES:
                return False

            if not board.on_board(move):
                return False

            return True

        except:
            current_app.logger.debug("Invalid move {}".format(move))
            return False

    def validate_captcha(self, board, move):
        """ Given a validated board and a validated move, check if correct """
        return self.can_move(board, move) \
            and self.solves(board, move)

    def can_move(self, board, move):
        raise NotImplementedError

    def solves(self, board, move):
        raise NotImplementedError


class ChessCaptcha(GameCaptcha):
    """ Validates a Chess GameCaptcha """

    game = "chess"

    Board = ChessBoard

    def can_move(self, board, move):
        """ Validates that the given move is allowed in this game """
        # No other pieces at new position
        if board[move] != board.EMPTY:
            return False

        # TODO: No pieces blocking movement

        # Piece can move in this manner
        old_position = board.find_piece(lambda p: p.glyph == move.glyph)
        if not old_position.can_move(move):
            return False
        return True

    def solves(self, board, move):
        """ Validates that the given move puts the king in check """
        target = board.find_piece(lambda p: p.glyph == board.TARGET)

        return move.can_move(target)


class GoCaptcha(GameCaptcha):
    """ Validates a Go GameCaptcha """

    game = "go"

    Board = GoBoard

    def can_move(self, board, move):
        """ Validates that the given move is allowed in this game """
        # No other pieces at new position
        if board[move] != board.EMPTY:
            return False

        return True

    def solves(self, board, move):
        """ Validates that the given move captures the target """

        # Find the white stone that only has one liberty
        answer = next(
            liberties[0] for liberties in (
                board.liberties(piece.position) for piece in board.pieces
                if piece.glyph == board.TARGET
            ) if len(liberties) == 1
        )

        return (move.x, move.y) == (answer.x, answer.y)
