// static/notes/main.js
$(document).ready(function () {
    $('#load-note').click(function () {
        let noteId = $('#note_id').val();

        $.ajax({
            url: "/notes/load_note/",
            type: "GET",
            data: {note_id: noteId},
            dataType: "json",
            success: function (data) {
                $('#note-title').text(data.title);
                $('#note-text').text(data.text);
                $('#divinvis, #toggle-finished').show();
            },
            error: function () {
                alert("Error loading note");
            }
        });
    });

    $('#toggle-finished').click(function () {
        let noteId = $('#note_id').val();

        $.ajax({
            url: `/notes/toggle_finished/${noteId}/`,
            type: "POST",
            headers: {'X-CSRFToken': '{{ csrf_token }}'},
            success: function () {
                $('#note-title, #note-text').text('');
                $('#divinvis, #toggle-finished').hide();
                location.reload();
            },
            error: function () {
                alert("Error updating note status");
            }
        });
    });

    $('#load-more').click(function () {
        const offset = $(this).data('offset');
        $.ajax({
            url: "/notes/load_more_notes/",
            type: 'GET',
            data: {
                offset: offset
            },
            success: function (data) {
                $('#notes-container').append(data.notes_html);
                if (!data.has_more) {
                    $('#load-more').hide();
                }
                $('#load-more').data('offset', offset + 20);
            },
            error: function () {
                alert("Error loading more notes");
            }
        });
    });

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});


const csrftoken = getCookie('csrftoken'); //Получение CSRF токена


