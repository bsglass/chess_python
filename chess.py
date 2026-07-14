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
board=[['br','bn','bb','bq','bk','bb','bn','br'],['bp']*8,['']*8,['']*8,['']*8,['']*8,['wp']*8,['wr','wn','wb','wq','wk','wb','wn','wr']]

def render_board_ascii()->None:
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

def turn_manager()->None:
    """Manages turns"""
    players=['White','Black']
    move_no=0
    while not (is_checkmate('w') or is_checkmate('b')):
        player=players[move_no%2]

        render_board_ascii()
        print(player+' to move.')
        if is_check(player[0].lower()):
            print('You are in check!')
        selected_origin=str(input('Select the square of the piece which you want to move (e.g d4)'))
        if get_piece(selected_origin)=='' or get_piece(selected_origin)[0]!=player[0].lower():
            print('Selected square is not valid, try again')
            continue

        available_moves=legal_destinations(selected_origin,get_piece(selected_origin))
        if len(available_moves['moves']+available_moves['takes'])==0:
            print('Piece on selected square has no available moves, try again')
            continue

        selected_destination=input(f'Select which destination out of these choices:\nMoves: {', '.join(available_moves['moves'])}\nTakes: {', '.join(available_moves['takes'])}')
        if selected_destination not in available_moves['moves']+available_moves['takes']:
            print('Selected square is not valid, try again')
            continue
        
        board=make_move(selected_origin,selected_destination)

        move_no+=1

    winner='White' if is_checkmate('b') else 'Black'
    print(winner+' wins!')

def get_piece(square:str)->str:
    """Returns the piece on the selected square."""
    if square[0] not in file_list or int(square[1:]) not in range(1,9):
        return '-1' #indicates that the square is not on the board
    return board[8-int(square[1])][file_list.index(square[0])]

def legal_destinations(origin:str,piece_type:str,board=board)->{str:[str]}:
    """Returns the legal destinations for a given piece_type on a certain square in the current board
    Open ended, to allow this to be used for checkmate code."""
    moves_dict={
        'r':[(0,1),(1,0),(0,-1),(-1,0)],
        'b':[(1,1),(1,-1),(-1,-1),(-1,1)],
        'n':[(1,2),(2,1),(2,-1),(1,-2),(-1,2),(-2,1),(-2,-1),(-1,-2)],
        'q':[(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1)],
        'k':[(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1)]
    }
    destinations={
        'moves':[],
        'takes':[]
    }
    current_file,current_rank=origin[0],int(origin[1])
    opponent_colour='w' if piece_type[0]=='b' else 'b'

    if piece_type[1]=='p':
        forward=1 if piece_type[0]=='w' else -1
        candidate_square=current_file+str(current_rank+forward)
        if get_piece(candidate_square)=='':
            destinations['moves'].append(candidate_square)
            if (current_rank==2 and piece_type[0]=='w') or (current_rank==7 and piece_type[0]=='b'):
                candidate_square=current_file+str(current_rank+forward*2)
                if get_piece(candidate_square)=='':
                    destinations['moves'].append(candidate_square)
        candidate_square=[chr(ord(current_file)-1)+str(current_rank+forward),chr(ord(current_file)+1)+str(current_rank+forward)]
        destinations['takes'].extend([square for square in candidate_square if get_piece(square)!='' if get_piece(square)[0]==opponent_colour])

    if piece_type[1] in ['r','b','q']:
        move_vectors=moves_dict[piece_type[1]]
        for x,y in move_vectors:
            looping=True
            i=0
            while looping:
                i+=1
                candidate_square=chr(ord(current_file)+x*i)+str(current_rank+y*i)
                if get_piece(candidate_square)=='':
                    destinations['moves'].append(candidate_square)
                    continue
                if get_piece(candidate_square)[0]==opponent_colour:
                    destinations['takes'].append(candidate_square)
                looping=False

    if piece_type[1] in ['n','k']:
        move_vectors=moves_dict[piece_type[1]]
        for x,y in move_vectors:
            candidate_square=chr(ord(current_file)+x)+str(current_rank+y)
            if get_piece(candidate_square)=='':
                destinations['moves'].append(candidate_square)
            elif get_piece(candidate_square)[0]==opponent_colour:
                destinations['takes'].append(candidate_square)

    # all_moves=[x for xs in destinations.values() for x in xs]
    # print(all_moves)
    # if len(all_moves):
    #     destinations=[x for x in all_moves if not is_check(piece_type[0],make_move(origin,x,board))]
        
    return destinations

def make_move(origin:str,des:str,board=board):
    """Moves something from origin to destination on the board"""
    board[8-int(des[1])][file_list.index(des[0])]=get_piece(origin)
    board[8-int(origin[1])][file_list.index(origin[0])]=''

def find_piece(piece_type:str)->[str]:
    """Returns a list of the squares which have a specified piece on."""
    valid_squares=[]
    for row in range(1,9):
        for file in file_list:
            if get_piece(file+str(row))==piece_type:
                valid_squares.append(file+str(row))
    return valid_squares

def is_check(colour:str,board=board)->bool:
    """Returns True if the selected colour ('w' or 'b') is in check, else False"""
    opponent_colour='w' if colour=='b' else 'b'
    king_square=find_piece(colour+'k')[0]

    for piece in ['p','r','n','b','q','k']:
        for square in legal_destinations(king_square,colour+piece)['takes']:
            if get_piece(square)==opponent_colour+piece:
                return True
    return False

def is_checkmate(colour:str)->bool:
    """Returns True if the selected colour ('w' or 'b') is in checkmate, else False"""
    if not is_check(colour):
        return False
    for piece in ['p','r','n','b','q','k']:
        if len([x for xs in legal_destinations(find_piece(colour+'k')[0],colour+piece,board).values() for x in xs]):
            return False
    print('CHECKMATE')
    return True

def is_stalemate(colour:str)->bool:
    """Returns True if the selected colour ('w' or 'b') is in stalemate, else False"""
    return False

if __name__=="__main__":
    board=[['br','bn','bb','bq','bk','bb','bn','br'],['bp']*8,['']*8,['']*8,['']*8,['']*8,['wp']*8,['wr','wn','wb','wq','wk','wb','wn','wr']]
    turn_manager()