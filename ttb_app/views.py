from django.shortcuts import render, render_to_response
from django.template import RequestContext
from ttb_app.tictactoe import UltimateTicTacToe

def index(request):
    board = request.session.get('board', UltimateTicTacToe())
    request.session['board'] = repr(board) # TODO need to make the board actually serializable to maintain state over sess
    return render_to_response('board.html', {'board':request.session['board']})