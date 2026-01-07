import chess

piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
}

def evaluate_piece_values(board, player):
    score = 0
    for _,piece in board.piece_map().items():
        value = piece_values[piece.piece_type]
        if piece.color == player:
            score += value
        else:
            score -= value
    
    return(score)

def evaluate_pawn_ranks(board, player):
    score = 0
    for pawn in board.pieces(chess.PAWN, player):
        rank = chess.square_rank(pawn)
        if player == chess.BLACK:
            rank = 7 - rank
        score += 0.1 * rank

    return(score)

def evaluate_piece_attacks(board, player):
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.color == player:
            attackers = board.attackers(not player, square)
            defenders = board.attackers(player, square)
            score -= (0.05 * len(attackers) * piece_values[piece.piece_type]) - (0.05 * len(defenders) * piece_values[piece.piece_type])
        if piece and piece.color != player:
            attackers = board.attackers(not player, square)
            defenders = board.attackers(player, square)
            score += (0.05 * len(attackers) * piece_values[piece.piece_type]) - (0.05 * len(defenders) * piece_values[piece.piece_type])
    return(score)


def evaluate(board, player):
    
    score = 0

    temp_score = evaluate_piece_values(board,player)
    score += temp_score

    print("Piece value score: ", temp_score)

    temp_score = evaluate_pawn_ranks(board,player)
    score += temp_score

    print("Pawn rank score: ", temp_score)

    temp_score = evaluate_piece_attacks(board,player)
    score += temp_score

    print("Piece attacks score: ", temp_score)

    return(score)

def minimax(board, depth, maximizing_player, player_color):
    if depth == 0 or board.is_game_over():
        return None, evaluate(board, player_color)

    if maximizing_player:
        max_eval = -float('inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            _, eval = minimax(board, depth - 1, False, player_color)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move, max_eval
    else:
        min_eval = float('inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            _, eval = minimax(board, depth - 1, True, player_color)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return best_move, min_eval

while True:
    input_text = input("Enter board state (FEN notation), your move (san notation), or 'exit' to quit: ")
    if input_text.lower() == 'exit':
        break

    try:
        board = chess.Board(input_text)
    except ValueError:
        try:
            board.push_san(input_text)
            print("Board after your move:")
            print(board)
        except ValueError:
            print("Invalid input.")
            continue

    player = chess.WHITE if board.turn == chess.WHITE else chess.BLACK

    best_move, _ = minimax(board, 2, True, player)

    print("\n\nChosen move: ", best_move)
    print("Board: ")
    board.push(best_move)
    print(board)