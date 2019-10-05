from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core import serializers
from ttb_app.tictactoe import UltimateTicTacToe
from ttb_app.models import DjangoBoard

def index(request):
    if request.method == "GET":
        #django_board = next(serializers.deserialize("json", request.session.get('board')))
        django_board = request.session.get('board')
        if django_board is None:
            django_board = DjangoBoard()
        uttt = django_board.get_utt_from_state()
        uttt.random_move()
        db = DjangoBoard()
        db.set_state_from_uttt(uttt)
        #request.session['board'] = serializers.serialize("json", db)
        return render_to_response('board.html', {'board':uttt.get_board_tuples(), 'needs_board': True})
    elif request.method == "PUT":
        # pretty much passes right now
        x = request
        x.method == "GET"
        return index(x)