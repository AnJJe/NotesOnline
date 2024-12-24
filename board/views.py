from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from django.template.loader import render_to_string

import board
from .models import Board, BoardCode
from notes.models import ListNote
from .forms import BoardForm
from notes.forms import NoteForm
from django.utils import timezone
import random

@login_required
def boards(request):
    owned_boards = request.user.owned_boards.all()
    member_boards = request.user.member_boards.all()
    return render(request, 'board/boards.html', {'owned_boards': owned_boards, 'member_boards': member_boards})

@login_required
def create_board(request):
    if not request.user.userprofile.is_admin:
        messages.error(request, "Only admins can create boards.")
        return redirect('board:boards')
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            board.members.add(request.user)
            messages.success(request, f"Board '{board.name}' created successfully!")
            return redirect('board:boards')
    else:
        form = BoardForm()
    return render(request, 'board/create_board.html', {'form': form})

@login_required
def view_board(request, pk):
    board = get_object_or_404(Board, pk=pk, deleted=False)
    if request.user not in board.members.all():
        messages.error(request, "You don't have access to this board now.")
        return redirect('board:boards')
    notes = ListNote.objects.filter(board_id=board.pk, deleted=False).order_by('-created_at')[:20]
    count_notes = ListNote.objects.filter(board_id=board.pk, deleted=False).count()
    code = get_object_or_404(BoardCode, board_id=board.pk)

    return render(request, 'board/view_board.html', {'board': board, 'notes': notes, 'code': code, 'count_notes': count_notes})



@login_required
def create_note(request, pk):
    board_par = Board.objects.get(pk=pk).name
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.board = Board.objects.get(pk=pk)
            note.save()
            messages.success(request, 'Added note successfully!')
            return redirect('board:view_board', pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteForm()
    return render(request, 'board/create_note.html', {'form': form, 'pk': pk, 'board_par': board_par})

@login_required
def edit_note(request, pk):
    note = get_object_or_404(ListNote, pk=pk, deleted=False)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.updated_at = timezone.now()
            note.public_note = False  # Публичная заметка по умолчанию выключена
            note.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('board:view_board', pk=note.board.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteForm(instance=note)
    return render(request, 'board/edit_note.html', {'form': form, 'note': note})

@login_required
def toggle_finished(request, note_id):
    note = get_object_or_404(ListNote, pk=note_id)
    note.finished = not note.finished
    note.updated_at = timezone.now()
    note.save()
    return redirect('board:view_board', pk=note.board.pk)

@login_required
def delete_note(request, pk):
    note = get_object_or_404(ListNote, pk=pk)
    if note.user != request.user:
        messages.error(request, "You can't delete this note.")
        return redirect('board:view_board', pk=note.board.pk)
    board_id = note.board.pk
    note.board = None
    note.updated_at = timezone.now()
    note.save()
    messages.success(request, "Note deleted successfully!")
    return redirect('board:view_board', pk=board_id)

@login_required
def join_board(request):
    if request.method == 'POST':
        code_value = request.POST.get('code')
        try:
            board_code = BoardCode.objects.get(code=code_value)
            board = board_code.board
            if request.user in board.members.all():
                messages.warning(request, "You're already a member of this board.")
            elif request.user == board.owner:
                messages.warning(request, "You can't join your own board.")
            else:
                board.members.add(request.user)
                messages.success(request, f"You've joined '{board.name}' board!")
        except BoardCode.DoesNotExist:
            messages.error(request, "Invalid code.")
    member_boards = request.user.member_boards.all()
    return render(request, 'board/boards.html', {'member_boards': member_boards})

def generate_code(board):
    code = ''.join(random.choices('0123456789', k=16))
    BoardCode.objects.update(board=board, code=code, generated_at=timezone.now())

def generate_code_ajax(request, board_id):
    if request.method == 'POST':
        code = ''.join(random.choices('0123456789', k=16))
        board = get_object_or_404(Board, pk=board_id)
        BoardCode.objects.update(board=board, code=code, generated_at=timezone.now())
        return JsonResponse({'status': 'success'})

# Попытка на реализацию самообновления кода для доступа к доске
# def check_and_generate_code():
#     boards = Board.objects.all()
#     now = timezone.now()
#     for board in boards:
#         last_code = get_object_or_404(BoardCode, board_id=board.pk)
#         if not last_code or (now - last_code.generated_at).total_seconds() > 900:  # 15 минут
#             generate_code(board)

@login_required
def delete_board(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.user != board.owner:
        messages.warning(request, "You're not allowed to change this board.")
        return redirect('board:view_board', pk=board.pk)
    else:
        board.deleted = True
        return redirect('board:boards')

@login_required
def exclude_member(request, board_id, user_id):
    board = get_object_or_404(Board, pk=board_id)
    board.members.remove(user_id)
    return redirect('board:view_board', pk=board_id)

@login_required
def load_more_notes(request):
    offset = int(request.GET.get('offset', 0))
    limit = 20  # Число заметок, которое подгружается
    board_id = request.GET.get('board_id')
    notes = ListNote.objects.filter(board_id=board_id, deleted=False).order_by('-created_at')[offset:offset + limit]
    has_more = ListNote.objects.filter(board_id=board_id, deleted=False).count() > offset + limit

    notes_html = render_to_string('board/partials/notes_list.html', {'notes': notes})
    return JsonResponse({'notes_html': notes_html, 'has_more': has_more})

@login_required
def get_notes(request, board_id):
    board = get_object_or_404(Board, pk=board_id, deleted=False)
    offset = int(request.GET.get('offset'))
    print(offset)
    notes = ListNote.objects.filter(board_id=board.pk, deleted=False).order_by('-created_at')[:offset]
    notes_data = serializers.serialize('json', notes)
    return JsonResponse({'notes': notes_data})
