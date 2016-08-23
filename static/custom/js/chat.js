$(document).ready(function($) {
    var ws4redis1 = WS4Redis({
		uri: 'ws://' + document.location.host + '/ws/global_chat?subscribe-broadcast&publish-broadcast&echo',
		receive_message: receiveMessage,
		heartbeat_msg: '--heartbeat--'
	});
	var billboard = $('#billboard');

	$("#text_message").keydown(function(event) {
		if (event.keyCode === 13) {
			event.preventDefault();
			ws4redis1.send_message($('#text_message').val());
			$('#text_message').val("")
		}
	});

	function get_pc_info() {
        $.post('/admin/chat/', {
            room: 'global_chat',
            action: 'send_msg',
            message: $('#text_message').val()
        });
    }

	$('#send_message').click(function() {
		get_pc_info();
		//ws4redis1.send_message($('#text_message').val());
		$('#text_message').val("")
	});

	// receive a message though the Websocket from the server
	function receiveMessage(msg) {
		console.log(msg)
		billboard.append('<br/>' + msg);
		billboard.scrollTop(billboard.scrollTop() + 25);
	}
});