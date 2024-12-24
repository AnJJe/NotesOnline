// static/board/main.js

$(document).ready(function () {

    $('#gen-code').click(function () {
        const boardID = this.getAttribute('data-board-id')
        $.ajax({
            url: `/board/generate/${boardID}/`,
            type: 'POST',
            headers: {'X-CSRFToken': '{{ csrf_token }}'},
            success: function () {
                location.reload();
            },
            error: function () {
                alert("Error of generation");
            }
        });
    });
    $('#load-more').click(function () {
        const offset = $(this).data('offset');
        const boardId = $('#board-id').val();

        $.ajax({
            url: "/board/load_more_notes/",
            method: "GET",
            data: {
                offset: offset,
                board_id: boardId
            },
            success: function (data) {
                $('.lsr-nt').append(data.notes_html);

                $('#load-more').data('offset', offset + 20);

                if (!data.has_more) {
                    $('#load-more').hide();
                }
            },
            error: function (xhr, status, error) {
                console.error('Error while loading', error);
            }
        });
    });
    $('#refresh').click(function () {
            location.reload()
        }
    )
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    // Аналог WebSocket на AJAX
    // setInterval(function () {
    //     let boardId = $('#board-id').val();
    //     let maxOffset = $('#load-more').data('offset');
    //
    //     // AJAX-запрос для получения списка заметок
    //     $.ajax({
    //         url: `/board/get_notes/${boardId}/`,
    //         type: 'GET',
    //         data: {'offset': maxOffset},
    //         dataType: 'json',
    //         success: function (response) {
    //             let notes = JSON.parse(response.notes);
    //
    //             // Проверка первой заметки
    //             let firstNoteIdOnPage = $('.lst-note').first().attr('id');
    //             console.log($('.lst-note').first().attr('id'))
    //             let firstNoteIdFromServer = notes.length > 0 ? `note-${notes[0].pk}` : null;
    //             console.log(firstNoteIdFromServer)
    //
    //             // if (firstNoteIdOnPage !== firstNoteIdFromServer) {
    //                 $('#list_notes').empty();  // Очищаем список заметок
    //                 notes.forEach(note => {
    //                     let noteHtml = `
    //                         <li class="list-group-item lst-note" id="note-${note.pk}">
    //                             <div>
    //                                 <h3>${note.fields.title}</h3>
    //                                 <small style="color: slategray">by ${note.fields.user}
    //                                     on ${note.fields.created_at}</small>
    //                                 <p>${note.fields.text}</p>
    //                             </div>
    //                             <div style="width:30vh">
    //                                 <a href="/edit_note/${note.pk}/"
    //                                    class="btn btn-sm btn-outline-secondary">Edit</a>
    //                                 <a href="/toggle_finished/${note.pk}/"
    //                                    class="btn btn-sm btn-${note.fields.finished ? 'info' : 'warning'}"
    //                                    style="min-width: 100px"
    //                                    data-finished-state="${note.fields.finished}">
    //                                     ${note.fields.finished ? '<span class="finished-text">Mark as Unfinished</span>' : '<span class="unfinished-text">Mark as Finished</span>'}
    //                                 </a>
    //                             </div>
    //                         </li>`;
    //                     $('#list_notes').append(noteHtml);
    //                 });
    //
    //             }
    //         // }
    //     });
    // }, 5000);
});

const csrftoken = getCookie('csrftoken'); //Получение CSRF токена


function toggleFinished(noteId) {
    fetch(`/board/toggle_finished/${noteId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`finished-checkbox-${noteId}`).checked = !document.getElementById(`finished-checkbox-${noteId}`).checked;
                document.getElementById(`finished-status-${noteId}`).textContent = data.status;
            } else {
                alert('Ошибка при обновлении статуса заметки');
            }
        });
}

// На удаление
// document.addEventListener('DOMContentLoaded', function () {
//     const boardIds = Array.from(document.querySelectorAll('[data-board-id]')).map(el => el.dataset.boardId);
//
//     boardIds.forEach(boardId => {
//         updateBoardCode(boardId);
//
//
//         const finishedCheckbox = document.querySelector(`#finished-checkbox-${boardId}`);
//         if (finishedCheckbox) {
//             finishedCheckbox.addEventListener('change', function () {
//                 toggleFinished(boardId);
//             });
//         }
//
//     });
// });



