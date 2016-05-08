$(document).ready(function() {

	function updateInfo() {

		$.ajax({
            url: window.location.protocol + "//" + window.location.host + '/info',
            type:  'get',

            beforeSend: function () {},
            success: function (info) {

        		// console.log(info);

        		var label = info.playing ? "pause" : "play";
        		$("#play").css('background-image', 'url("/static/icons/'+label+'.svg")');

        		$("#info #name").html(info.name);

        		var fullscreen = info.fullscreen ? "restore" : "fullscreen";
        		$("#toggleFullscreen").css('background-image', 'url("/static/icons/'+fullscreen+'.svg")');
        		
        		var mute = info.volume ? 'speaker' : 'mute';
        		$("#toggleMute").css('background-image', 'url("/static/icons/'+mute+'.svg")');

        		$("#progress").val(info.time);
        		$("#progress").attr('max', info.length);
        		$("#progress").attr('title', Math.round((info.time/info.length*100 * 100) / 100) + "%");
        		
        		$("#volume").val(Math.round(info.volume * 100) / 100);
        		// $("#volume").attr('title', Math.round(info.volume * 100) / 100);
        		$("#volume").attr('title', Math.round(info.volume/1*100) + "%");

        		$("#current").html(formatTime(info.time));
        		$("#remaining").html(formatTime(info.length));
        		
            },
           	error: function(err) {
           		$("#info #name").html("Connection Error");
            }
    	});
	}

	function formatTime(date) {

		var date = new Date(date);
		var str = '';

		// str += date.getUTCDate()-1 + " days, ";
		str += date.getUTCHours() + ":";
		// str += pad_with_zeroes(date.getUTCMinutes(), 2) + ":";
		str += pad_with_zeroes(date.getUTCMinutes(), 2);
		// str += pad_with_zeroes(date.getUTCSeconds(), 2) + "";
		// str += date.getUTCMilliseconds() + " millis";
		return str

	}


	function pad_with_zeroes(number, length) {

	    var my_string = '' + number;
	    while (my_string.length < length) {
	        my_string = '0' + my_string;
	    }
	    return my_string;
        
	}

	// Play
	$("#play").on("click", function() {

		$.ajax({
            url: window.location.protocol + "//" + window.location.host + '/togglePlay',
            type:  'get',
            success: function (response) {

                var label = response.playing ? "pause" : "play";
                $("#play").css('background-image', 'url("/static/icons/'+label+'.svg")');

                // console.log(response);
            }
    	});

	});

	// Next,Prev, exit
	$("#next, #previous, #exit, #toggleFullscreen, #toggleMute, #volumeDown, #volumeUp, #seekBWD, #seekFWD").on("click", function() {

		$.ajax({
            url: window.location.protocol + "//" + window.location.host + '/' + $(this).attr('id'),
            type:  'get',
            success: function (response) {
            	// console.log(response);                		
            }
    	});

	});

	// Time Change
	$("#progress").change(function() {

		$.ajax({
            url: window.location.protocol + "//" + window.location.host + '/seekTime/' + $(this).val(),
            type:  'get',
            success: function (response) {
            	// console.log(response);
            }
    	});

	});

	updateInfo();
	setInterval(updateInfo, 3000);

});