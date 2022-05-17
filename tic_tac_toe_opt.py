import operator, pprint, numpy, copy

BOARD_SIZE = 3

WINNER_DICT = {  'x' : 1, 'o' : -1  }


def generate_board():
    board = numpy.array([
        [ ' ', ' ', ' ' ],  
        [ ' ', ' ', ' ' ],    
        [ ' ', ' ', ' ' ]  
    ])
    return board


def find_available_moves(board):
    moves = [  (i, j) for (i, j) in zip(*numpy.where(board == ' '))  ]
    return moves 


def determine_score(winner):
    return WINNER_DICT.get(winner, 0)


def is_terminal(board):
    
    def check_array_terminal(array):
        for checker in (  'x', 'o'  ):
            if (numpy.count_nonzero(array == checker) == BOARD_SIZE):
                return True, checker 
        return False, None
    
    for i in range(BOARD_SIZE):
        for array in (  board[ i , : ], board[ : , i ]  ):
            terminal, winner = check_array_terminal(array)
            if (terminal):
                return terminal, winner 
            
    for array in (  numpy.diag(board_type) for board_type in (  board, numpy.rot90(board)  )  ):
        terminal, winner = check_array_terminal(array)
        if (terminal):
            return terminal, winner
        
    return False, None


def get_player(maximizing = True):
    return (('x') if (maximizing) else ('o'))


def make_move(board, i, j, player = 'x'):
    board = copy.deepcopy(board);  board[i][j] = player
    return board


def minimax(board, maximizing = True):
    
    terminal, winner = is_terminal(board)
    if (terminal):
        return determine_score(winner), None
    
    moves = find_available_moves(board)
    if (moves.__len__() == 0):
        return determine_score(None), None
    
    best_score     = 2 - (4 * maximizing)
    best_move      = None
    function       = ((operator.gt) if (maximizing) else (operator.lt))
    current_player = get_player(maximizing)
    
    for i, j in moves:
        
        score = minimax(make_move(board, i, j, current_player), not maximizing)[0]
        
        if (function(score, best_score)):
            best_score = score;  best_move = (i, j)
            
    return best_score, best_move


def print_board(board):
    board = board.tolist()
    for i in range(3):
        pprint.pprint(board[i])
    print()
        
def input_board(board):
    position = eval(input("> "))
    return make_move(board, *position, 'o')

def main():
    
    board = generate_board()
    print_board(board)
    
    board = input_board(board)
    print_board(board)
    
    turn = 1
    
    while ((is_terminal(board)[0] == False) and (find_available_moves(board).__len__())):
        if (turn):
            best_move = minimax(board)[1]
            board = make_move(board, *best_move, player = get_player(turn))
        else:
            board = input_board(board)
        turn = not turn
        print_board(board)
        
    print("Winner: ", is_terminal(board)[1])
    
if (__name__ == "__main__"):
    main()
    