$(document).ready(function($) {
	function formatBytes(bytes,decimals) {
	   if(bytes == 0) return '0 Byte';
	   var k = 1024; // or 1024 for binary
	   var dm = decimals + 1 || 3;
	   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
	   var i = Math.floor(Math.log(bytes) / Math.log(k));
	   return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
	}

	var ws4redis = WS4Redis({
		uri: 'ws://' + document.location.host + '/ws/dashboard?subscribe-broadcast&publish-broadcast&echo',
		receive_message: receive_get_pc_info,
		heartbeat_msg: '--heartbeat--'});

	function receive_get_pc_info(msg) {
        var data = jQuery.parseJSON(msg);
        $('#uptime').text(data.uptime);
        $.each(data.cpu, function(index, value) {
            var cores = index +1;
            $('#core' + cores).progress({percent: value.core});
        });
        $.each(data.memory, function(index, value) {
			$('#getMemory').progress({percent: value.cur});
        	$('#getSwap').progress({percent: value.swap});
			$('#getMemoryTotal').text(formatBytes(value.total));
			$('#getMemoryUsed').text(formatBytes(value.used));
			$('#getMemoryFree').text(formatBytes(value.free));
			$('#getMemoryCached').text(formatBytes(value.cached));
			$('#getSwapTotal').text(formatBytes(value.stotal));
			$('#getSwapUsed').text(formatBytes(value.sused));
			$('#getSwapFree').text(formatBytes(value.sfree));
        });
	}
});