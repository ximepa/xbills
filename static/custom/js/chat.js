$(document).ready(function($) {
    var ws4redis1 = WS4Redis({
		uri: 'ws://' + document.location.host + '/ws/global_chat?subscribe-broadcast&publish-broadcast&echo',
		receive_message: receiveMessage,
		heartbeat_msg: '--heartbeat--'
	});
    var ws4redis2 = WS4Redis({
		uri: 'ws://' + document.location.host + '/ws/global_chat?subscribe-user',
		receive_message: receiveMessage,
		heartbeat_msg: '--heartbeat--'
	});
	var billboard = $('#billboard');

	$("#text_message").keydown(function(event) {
		if (event.keyCode === 13) {
			event.preventDefault();
            var pm_user = $('#pm_user')[0].innerText;
            get_pc_info(pm_user);
			//ws4redis1.send_message($('#text_message').val());
			$('#text_message').val("")
		}
	});

	function get_pc_info(user) {
        $.post('/admin/chat/', {
            room: 'global_chat',
            user: user,
            action: 'send_msg',
            message: $('#text_message').val()
        });
    }

	$('#send_message').click(function(e) {
	    var pm_user = $('#pm_user')[0].innerText;
		get_pc_info(pm_user);
		//ws4redis1.send_message($('#text_message').val());
		$('#text_message').val("")
	});

	function receiveMessage(msg) {
		var data = jQuery.parseJSON(msg);

		if (billboard.length == 0) {
			noty({
				login: data.login,
				text: data.message,
				input: 'ui mini fluid input',
				type: 'warning',
				dismissQueue: true,
				layout: 'bottomRight',
				theme: 'semantic_ui',
				buttons: [
					{
						addClass: 'mini positive ui button', text: 'Ok', onClick: function ($noty) {
						$.post('/admin/chat/', {
							room: 'global_chat',
							user: $noty.$message[0].textContent,
							action: 'send_msg',
							message: $noty.$input.val()
						});
						$noty.close();
					}
					},
					{
						addClass: 'mini negative ui button', text: 'Cancel', onClick: function ($noty) {
						$noty.close();
					}
					}
				]
			});
		} else {
			var comments = $('<div/>').addClass('ui comments'),
				metadata = $('<div/>').addClass('metadata').append($('<div/>').addClass('date').text(data.date)),
				comment = $('<div/>').addClass('comment').append($('<a/>').addClass('avatar').append($('<img/>').attr('src', 'http://semantic-ui.com/images/avatar/small/stevie.jpg'))),
				content = $('<div/>').addClass('content').append($('<div/>').addClass('ui inline dropdown').text(data.login), metadata, $('<div/>').addClass('text').text(data.message));
			billboard.append(comments.append(comment.append(content)));
			billboard.scrollTop(billboard.scrollTop() + comments.height() + comments.height());
		}
	}

});

function pMessage(e) {
    var user = $('#text_message');
    user.val('');
    user.val(e + ':');
}