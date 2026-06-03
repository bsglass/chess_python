#Mappings for unicode piece symbols for more easily understood ones, for use in code.
piece_dict={
    'wk':'\u2654',
    'wq':'\u2655',
    'wr':'\u2656',
    'wb':'\u2657',
    'wn':'\u2658',
    'wp':'\u2659',
    'bk':'\u265A',
    'bq':'\u265B',
    'br':'\u265C',
    'bb':'\u265D',
    'bn':'\u265E',
    'bp':'\u265F',
    '':' '
}

file_list=['a','b','c','d','e','f','g','h']

def render_board_ascii(board:[[str]])->None:
    """Renders the board using ascii characters"""
    horizontal_line='--------------------------'
    rank=8
    print(horizontal_line)
    for row in board:
        generated_row=str(rank)+'|'
        generated_row+=(' |'.join([piece_dict[square] for square in row])+' |')
        print(generated_row)
        print(horizontal_line)
        rank-=1
    print(' |'+' |'.join(file_list)+' |')

def get_piece(board:[[str]],square:str)->str:
    """Returns the piece on the selected square."""
    if square[0] not in file_list or square[1] not in range(1,9):
        raise ValueError('Given square is not on the board')
    return board[8-int(square[1])][file_list.index(square[0])]

def legal_destinations(board:[[str]],origin:str,piece_type:str)->[str]:
    """Returns the legal destinations for a given piece_type on a certain square in the current board
    Open ended, to allow this to be used for checkmate code."""
    moves_dict={
        'r':[(0,1),(1,0),(0,-1),(-1,0)],
        'b':[(1,1),(1,-1),(-1,-1),(-1,1)],
        'n':[(1,2),(2,1),(2,-1),(1,-2),(-1,2),(-2,1),(-2,-1),(-1,-2)],
        'q':[(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1)],
        'k':[(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1)]
    }
    destinations=[]
    current_file,current_rank=origin[0],int(origin[1])

    if piece_type[1]=='p':
        forward=1 if piece_type[0]=='w' else -1
        candidate_square=current_file+str(current_rank+forward)
        if get_piece(candidate_square)=='':
            destinations.append(candidate_square)
    if piece_type[1] in ['r','b','q']:
        pass
    if piece_type[1] in ['n','k']:
        pass

    return desinations

if __name__=="__main__":
    board=[['br','bn','bb','bq','bk','bb','bn','br'],['bp']*8,['']*8,['']*8,['']*8,['']*8,['wp']*8,['wr','wn','wb','wq','wk','wb','wn','wr']]
    #render_board_ascii(board)
    print(get_piece(board,'e1'))