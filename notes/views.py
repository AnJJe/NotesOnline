# notes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.middleware import csrf

from .models import ListNote
from board.models import Board
from .forms import NoteForm

User = get_user_model()


@login_required
def input(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Added note successfully!')
            return redirect('notes:input')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteForm()
    return render(request, 'notes/input.html', {'form': form})


@login_required
def view_notes(request):
    user_notes = ListNote.objects.filter(user=request.user, finished=False, deleted=False).order_by('-created_at')[:20]
    finished_notes = ListNote.objects.filter(user=request.user, finished=True, deleted=False).order_by('-created_at')
    count_notes = ListNote.objects.filter(user=request.user, finished=False, deleted=False).count()
    boards = Board.objects.all()
    context = {
        'user_notes': user_notes,
        'finished_notes': finished_notes,
        'count_notes': count_notes,
        'boards': boards
    }
    return render(request, 'notes/view.html', context)


@login_required
def load_more_notes(request):
    offset = int(request.GET.get('offset', 0))
    limit = 20  # Число заметок, которое подгружается
    notes = ListNote.objects.filter(user=request.user, finished=False, deleted=False).order_by('-created_at')[
            offset:offset + limit]

    # Добавляем CSRF-токен в контекст вручную
    notes_html = render_to_string('notes/partials/notes_list.html', {
        'notes': notes,
        'csrf_token': csrf.get_token(request)
    })
    has_more = ListNote.objects.filter(user=request.user, finished=False, deleted=False).count() > offset + limit
    return JsonResponse({'notes_html': notes_html, 'has_more': has_more})


# Для загрузки завершенной заметки
@login_required
def load_note(request):
    if request.method == "GET":
        note_id = request.GET.get('note_id')
        note = get_object_or_404(ListNote, id=note_id, user=request.user, deleted=False)
        return JsonResponse({'title': note.title, 'text': note.text})


@login_required
def toggle_finished(request, note_id):
    note = get_object_or_404(ListNote, id=note_id, user=request.user, deleted=False)
    note.finished = not note.finished
    note.updated_at = timezone.now()
    note.save()
    return JsonResponse({'status': 'success'})


@login_required
def update_note(request, note_id):
    note = get_object_or_404(ListNote, id=note_id, user=request.user, deleted=False)
    if request.method == 'POST':
        finished = request.POST.get('finished') == '1'
        note.finished = finished
        note.save()
        return redirect('notes:view_notes')
    return redirect('notes:view_notes')


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(ListNote, id=note_id, user=request.user, deleted=False)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.updated_at = timezone.now()
            note.save()
            messages.success(request, 'Work with note ended successfully!')
            return redirect('notes:view_notes')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(ListNote, id=note_id, user=request.user)
    note.deleted = True
    note.updated_at = timezone.now()
    note.save()
    messages.success(request, 'Note deleted successfully.')
    return redirect('notes:view_notes')
