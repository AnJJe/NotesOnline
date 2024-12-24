#notes/urls.py
from django.urls import include, path
from . import views

app_name = 'notes'

urlpatterns = [
    path('input/', views.input, name='input'),
    # path('publicnotes/', views.publicnotes, name='publicnotes'),
    path('view/', views.view_notes, name='view_notes'),
    path('load_note/', views.load_note, name='load_note'),
    path('toggle_finished/<int:note_id>/', views.toggle_finished, name='toggle_finished'),
    path('update_note/<int:note_id>/', views.update_note, name='update_note'),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('load_more_notes/', views.load_more_notes, name='load_more_notes'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('board/', include('board.urls')),

]
