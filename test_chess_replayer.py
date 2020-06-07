from game import ChessPiece, NewGame

game_text = '''
1. c4 e6 2. Nf3 d5 3. d4 Nf6 4. Nc3 Be7 5. Bg5 O-O 6. e3 h6
7. Bh4 b6 8. cxd5 Nxd5 9. Bxe7 Qxe7 10. Nxd5 exd5 11. Rc1 Be6
12. Qa4 c5 13. Qa3 Rc8 14. Bb5 a6 15. dxc5 bxc5 16. O-O Ra7
17. Be2 Nd7 18. Nd4 Qf8 19. Nxe6 fxe6 20. e4 d4 21. f4 Qe7
22. e5 Rb8 23. Bc4 Kh8 24. Qh3 Nf8 25. b3 a5 26. f5 exf5
27. Rxf5 Nh7 28. Rcf1 Qd8 29. Qg3 Re7 30. h4 Rbb7 31. e6 Rbc7
32. Qe5 Qe8 33. a4 Qd8 34. R1f2 Qe8 35. R2f3 Qd8 36. Bd3 Qe8
37. Qe4 Nf6 38. Rxf6 gxf6 39. Rxf6 Kg8 40. Bc4 Kh8 41. Qf4 1-0
'''

test_game = '1. a4 Nc6 2. Ra3 Rb8 3. Rh3'

two_rooks_game = '1. h4 h5 2. Rh3 a6 3. a3 b6 4. a4 d5 5. Raa3 d4 6. g4 d3 7. Rhxd3'

two_knights_game = '1. Nf3 e5 2. Nc3 c5 3. Nxe5 f6 4. Nc4 d6 5. Ne4 g6 6. Nexd6+'

new_game = NewGame(game_text)
new_game_2 = NewGame(game_text)
new_game_3 = NewGame(two_rooks_game)
new_game_4 = NewGame(two_knights_game)


def test_setting_pieces_for_new_game():
    assert len(new_game.pieces) == 32


def test_white_pieces_quantity():
    white_pieces = []
    for piece in new_game.pieces:
        if piece.color == 'white':
            white_pieces.append(piece)

    assert len(white_pieces) == 16


def test_black_pieces_quantity():
    black_pieces = []
    for piece in new_game.pieces:
        if piece.color == 'black':
            black_pieces.append(piece)

    assert len(black_pieces) == 16


def test_pawns_quantity():
    black_pawns = []
    white_pawns = []
    pawns = []

    for piece in new_game.pieces:
        if piece.piece_type == 'pawn':
            pawns.append(piece)
            if piece.color == 'black':
                black_pawns.append(piece)
            elif piece.color == 'white':
                white_pawns.append(piece)

    assert len(pawns) == 16 and len(white_pawns) == 8 and len(black_pawns) == 8


def test_piece_notation_position():
    piece_1 = ChessPiece('pawn', 1)
    piece_2 = ChessPiece('pawn', 16)
    piece_3 = ChessPiece('king', 37)
    assert piece_1.piece_notation_position() == 'a1' and piece_2.piece_notation_position() == 'h2' and \
           piece_3.piece_notation_position() == 'e5'


def test_possible_black_pawns_moves():
    black_pawn_1 = ChessPiece('pawn', 50, 'black')
    black_pawn_2 = ChessPiece('pawn', 20, 'black')

    assert sorted(black_pawn_1.possible_moves) == [34, 41, 42, 43] and sorted(black_pawn_2.possible_moves) == [11, 12,
                                                                                                               13]

def test_piece_capture():
    before = len(new_game.pieces)
    new_game.piece_capture(1, 2)
    after = len(new_game.pieces)
    assert before - 1 == after


def test_rook_blocked_lines():
    rooks = []
    for piece in new_game_2.pieces:
        rook = piece if piece.piece_type == 'rook' else None
        if rook:
            rooks.append(piece)
    assert len(rooks) == 4


'''def test_two_rooks_capture():
    for i in range(0, 13):
        new_game_3.move(i)
    assert new_game_3.move(12) == 'two pieces capture'


def test_two_knights_capture():
    for i in range(0, 11):
        new_game_4.move(i)
    assert new_game_4.move(10) == 'two pieces capture'
    '''
