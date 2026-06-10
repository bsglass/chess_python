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

def turn_manager(board:[[str]])->None:
    """Manages turns"""
    while True:
        render_board_ascii(board)
        selected_origin=str(input('Select the square of the piece which you want to move (e.g d4)'))
        if get_piece(board,selected_origin)=='':
            print('Selected square is not valid, try again')
            continue

        available_moves=legal_destinations(board,selected_origin,get_piece(board,selected_origin))
        if len(available_moves)==0:
            print('Piece on selected square has no available moves, try again')
            continue

        selected_destination=str(input('Select which destination out of these choices: '+', '.join(available_moves)))
        if selected_destination not in available_moves:
            print('Selected square is not valid, try again')
            continue
        
        board=make_move(board,selected_origin,selected_destination)

def get_piece(board:[[str]],square:str)->str:
    """Returns the piece on the selected square."""
    if square[0] not in file_list or int(square[1:]) not in range(1,9):
        return '-1' #indicates that the square is not on the board
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
    opponent_colour='w' if piece_type[0]=='b' else 'b'

    if piece_type[1]=='p':
        forward=1 if piece_type[0]=='w' else -1
        candidate_square=current_file+str(current_rank+forward)
        if get_piece(board,candidate_square)=='':
            destinations.append(candidate_square)
        candidate_square=[chr(ord(current_file)-1)+str(current_rank+forward),chr(ord(current_file)+1)+str(current_rank+forward)]
        destinations.extend([square for square in candidate_square if get_piece(board,square)!='' if get_piece(board,square)[0]==opponent_colour])

    if piece_type[1] in ['r','b','q']:
        move_vectors=moves_dict[piece_type[1]]
        for x,y in move_vectors:
            looping=True
            i=0
            while looping:
                i+=1
                candidate_square=chr(ord(current_file)+x*i)+str(current_rank+y*i)
                if get_piece(board,candidate_square)=='':
                    destinations.append(candidate_square)
                    continue
                if get_piece(board,candidate_square)[0]==opponent_colour:
                    destinations.append(candidate_square)
                looping=False

    if piece_type[1] in ['n','k']:
        move_vectors=moves_dict[piece_type[1]]
        for x,y in move_vectors:
            candidate_square=chr(ord(current_file)+x)+str(current_rank+y)
            if get_piece(board,candidate_square)=='' or get_piece(board,candidate_square)[0]==opponent_colour:
                destinations.append(candidate_square)

    return destinations

def make_move(board:[[str]],origin:str,des:str)->[[str]]:
    """Moves something from origin to destination on the board"""
    board[8-int(des[1])][file_list.index(des[0])]=get_piece(board,origin)
    board[8-int(origin[1])][file_list.index(origin[0])]=''
    return board

if __name__=="__main__":
    board=[['br','bn','bb','bq','bk','bb','bn','br'],['bp']*8,['']*8,['']*8,['']*8,['']*8,['wp']*8,['wr','wn','wb','wq','wk','wb','wn','wr']]
    #render_board_ascii(board)
    turn_manager(board)