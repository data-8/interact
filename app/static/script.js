
// Launches a socket connection with server-side, receiving status updates and
// updating the page accordingly.
function openStatusSocket(username, callback) {
    url = 'ws://' + window.location.hostname + ':' + window.location.port +
        '/socket/' + username +
        window.location.search;

    var socket = new WebSocket(url);

    socket.onopen = function() {
        console.log('[Client] Connected to url: ' + url);
    };

    socket.onmessage = function(message) {
        data = JSON.parse(message.data);
        console.log(data);
    };

    return;

    /*
    * EVENT HANDLERS
    * These receive data from server and update pages client-side.
    */

    socket.on('status update', function(msg) {
        $('.status').html(msg.status);
    });

    socket.on('process redirect', function(msg) {
        console.log(msg);
        $('.status').html('Redirecting you to ' + msg.url);
        window.location.href = msg.url;
    });

    socket.on('log update', function(msg) {
        console.log('received update');
        $('.log').html(msg.log);
    });

    // Event handler for new connections
    socket.on('connect', function() {
        callback();
    });
}

$(document).ready(function() {
    $('.console_log').on('click', function() {
        if ($('.log-container').is(':visible')) {
            $('.log-container').hide();
            $('.console_log').html('Show Console Log');
        } else {
            $('.log-container').show();
            $('.console_log').html('Hide Console Log');
        }
        return false;
    });

    $('.server-field').on('input', function() {
        value = $(this).val();
        $('.server-display').each(function() {
            if (value == '') {
                $(this).html('ds8.berkeley.edu');
            } else {
                $(this).html(value);
            }
        });
        $('.server-button').attr('href', 'http://' + value +
            $('.server-input .reversed').contents()[2].textContent);
    });
});
