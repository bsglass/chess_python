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

def render_board_ascii(board:[[str]])->[None]:
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


if __name__=="__main__":
    board=[['br','bn','bb','bq','bk','bb','bn','br'],['bp']*8,['']*8,['']*8,['']*8,['']*8,['wp']*8,['wr','wn','wb','wq','wk','wb','wn','wr']]
    render_board_ascii(board)