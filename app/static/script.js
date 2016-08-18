
// Launches a socket connection with server-side, receiving status updates and
// updating the page accordingly.
function openStatusSocket(username, callback) {

    // Socket.io documentation recommends sending an explicit package upon
    // connection. This is especially important when using the global namespace
    url = 'http://' + document.domain + ':' + location.port + '/' + username
    var socket = io.connect(url);
    console.log('Connected to "' + url + '"');

    /*
    * EVENT HANDLERS
    * These receive data from server and update pages client-side.
    */

    socket.on('status update', function(msg) {
        $('.status').html(msg.status);
    });

    socket.on('process complete', function(msg) {
        $('.status').html('Redirecting you to ' + msg.url);
        window.location.href = msg.url;
    });

    socket.on('log update', function(msg) {
        if ($('.log').is(':visible')) {
            $('.log').html(msg.log);
        }
    });

    // Event handler for new connections
    socket.on('connect', function() {
        callback();
    });

    // Global socket
    var global = io.connect('http://' + document.domain + ':' + location.port
     + '/global');

    global.on('estimate update', function(msg) {
        $('.time').html(msg.estimate + ' seconds');
    });
}

$(document).ready(function() {
    $('.log').hide();

    $('.console_log').on('click', function() {
        if ($('.log').is(':visible')) {
            $('.log').hide();
            $('.console_log').html('Show Console Log');
        } else {
            $('.log').show();
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