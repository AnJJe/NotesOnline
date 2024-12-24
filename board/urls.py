from django.urls import path
from . import views
from notes import views as notes_views

app_name = 'board'

urlpatterns = [
    path('list/', views.boards, name='boards'),
    path('join/', views.join_board, name='join_board'),
    path('get_notes/<int:board_id>/', views.get_notes, name='get_notes'),
    path('create/', views.create_board, name='create_board'),
    path('load_more_notes/', views.load_more_notes, name='load_more_notes'),
    path('<pk>/', views.view_board, name='view_board'),
    path('generate/<int:board_id>/', views.generate_code_ajax, name='generate_code'),
    path('notes/<pk>/edit/', views.edit_note, name='edit_note'),
    path('notes/<pk>/delete/', views.delete_note, name='delete_note'),
    path('<pk>/notes/create/', views.create_note, name='create_note'),
    path('notes/<int:note_id>/toggle_finished/', views.toggle_finished, name='toggle_finished'),
    path('<pk>/delete/', views.delete_board, name='delete_board'),
    path('<int:board_id>/exclude/<int:user_id>/', views.exclude_member, name='exclude_member'),

]
