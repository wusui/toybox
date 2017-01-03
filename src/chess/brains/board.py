#!/usr/bin/python

class board(object):
    """
    Representation of the chessboard.

    self.board is a board layout to be intialized from that data.
    Pieces in the range 1-6 are white. Pieces in the range 11-16 are
    black.
        
    self.error_list is a list of errors found while trying to solve the
    problem
        
    self.msg_type either describes the error or indicates a solution.
    """
    def __init__(self, setup):
        """
        setup contains a board setup string as described in ../chess.py
        """
        self.board = []
        for _ in range(0, 8):
            self.board.append(8 * [0])
        self.rook_move = [[False, False], [False, False]]
        self.king_move = [False, False]
        self.past_move = []
        self.error_list = []
        self.msg_type = ''
        parts = setup.split("/")
        try:
            self.moves = int(parts[0])
        except ValueError:
            self.syntax_error('Number of moves is invalid')
        if not parts[1].startswith('W:'):
            self.syntax_error('White move list is invalid')
        if not parts[2].startswith('B:'):
            self.syntax_error('Black move list is invalid')
        if len(self.error_list) > 0:
            return
        elist = []
        elist.extend(self.validate(parts[1][2:],0))
        elist.extend(self.validate(parts[2][2:],10))
        if len(elist) > 0:
            etext = ', '.join(list(set(elist)))
            emsg = "The following positions are invalid: %s" % etext
            self.syntax_error(emsg)
            return
        kcount = [0, 0]
        self.kloc = {}
        bad_pawn = []
        for i in range(0,8):
            for j in range(0,8):
                cindx = self.board[i][j] // 10
                pindx = self.board[i][j] % 10
                if pindx == 6:
                    kcount[cindx] += 1
                    self.kloc[cindx] = (i, j)
                if pindx == 1:
                    if i == 0 or i == 7:
                        bad_pawn.append(self.square(i,j))
        if kcount[0] == 0:
            self.input_error('White king is missing')
        if kcount[1] == 0:
            self.input_error('Black king is missing')
        if kcount[0] > 1:
            self.input_error('Too many white kings')
        if kcount[1] > 1:
            self.input_error('Too many black kings')
        if 0 in self.kloc and 1 in self.kloc:
            if (abs(self.kloc[0][0] - self.kloc[1][0]) < 2 and
                abs(self.kloc[0][1] - self.kloc[1][1]) < 2):
                self.input_error('Kings should not be next to each other')
        if len(bad_pawn) > 0:
            self.input_error(
                "The following pawns are in invalid locations: %s" %
                ", ".join(bad_pawn))
        if len(self.error_list) > 0:
            return

    def validate(self, pstring, color):
        """
        set up the pieces for the color specified.  pstring should
        be a comma separate list of piece positions in algerbraic notation.
        """
        pieces = pstring.split(',')
        errors = []
        for txt in pieces:
            txt = txt.strip()
            if len(txt) < 2 or len(txt) > 3:
                if len(txt) != 0:
                    errors.append(txt)
            else:
                chrs = txt[::-1]
                try:
                    row = '12345678'.index(chrs[0])
                except ValueError:
                    errors.append(txt)
                    continue
                try:
                    col = 'abcdefgh'.index(chrs[1])
                except ValueError:
                    errors.append(txt)
                    continue
                if len(txt) == 3:
                    try:
                        pval = 'NBRQK'.index(chrs[2])
                    except ValueError:
                        errors.append(txt)
                        continue
                    pval += 2
                else:
                    pval = 1
                self.board[row][col] = pval + color
        return errors

    def square(self, i, j):
        """
        Given a row and column, return the algebraic square notation.
        """
        chr1 = 'abcdefgh'[j]
        chr2 = str(i+1)
        return chr1 + chr2

    def syntax_error(self, msg):
        """
        Handle a syntax error -- indicates the text sent is in error (probable
        software issue).
        """
        self.error_list.append(msg)
        self.msg_type = 'SYNTAX ERROR'

    def input_error(self, msg):
        """
        Handle an input error  -- probable user issue.
        """
        self.error_list.append(msg)
        self.msg_type = 'INPUT ERROR'
