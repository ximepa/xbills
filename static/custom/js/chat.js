$(document).ready(function($) {
    var ws4redis1 = WS4Redis({
		uri: 'ws://' + document.location.host + '/ws/global_chat?subscribe-broadcast&publish-broadcast&echo',
		receive_message: receiveMessage,
		heartbeat_msg: '--heartbeat--'
	});
	var billboard = $('#billboard');

	// send message though the Websocket to the server
	$("#text_message").keydown(function(event) {
		if (event.keyCode === 13) {
			event.preventDefault();
			ws4redis1.send_message($('#text_message').val());
			$('#text_message').val("")
		}
	});

	$('#send_message').click(function() {
		ws4redis1.send_message($('#text_message').val());
		$('#text_message').val("")
	});

	// receive a message though the Websocket from the server
	function receiveMessage(msg) {
		billboard.append('&#13;&#10;' + msg);
		billboard.scrollTop(billboard.scrollTop() + 25);
	}
});