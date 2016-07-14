$(document).ready(function() {

    function updateInfo() {

        $.ajax({
            url: window.location.protocol + "//" + window.location.host + '/info',
            type: 'get',

            beforeSend: function() {},
            success: function(info) {

                var label = info.playing ? "pause" : "play";
                $("#togglePlay").css('background-image', 'url("/static/icons/' + label + '.svg")');

                $("#info #name").html(info.name);

                var fullscreen = info.fullscreen ? "restore" : "fullscreen";
                $("#toggleFullscreen").css('background-image', 'url("/static/icons/' + fullscreen + '.svg")');

                var mute = info.volume ? 'speaker' : 'mute';
                $("#toggleMute").css('background-image', 'url("/static/icons/' + mute + '.svg")');

                $("#progress").attr('max', info.length);
                $("#progress").val(info.time);
                $("#progress").attr('title', Math.round((info.time / info.length * 100 * 100) / 100) + "%");

                $("#volume").val(Math.round(info.volume * 100) / 100);
                $("#volume").attr('title', Math.round(info.volume / 1 * 100) + "%");

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


    // Time Change
    $("#progress").change(function() {

        $.ajax({
            url: window.location.protocol + "//" + window.location.host + '/seekTime/' + $(this).val(),
            type: 'get'
        });

    });


    // Buttons Click event
    $("#togglePlay, #toggleFullscreen, #toggleMute, #volumeDown, #volumeUp, #next, #previous, #exit, #seekBWD, #seekFWD").on("click", function() {

        var eventID = $(this).attr('id');

        $.ajax({
            url: window.location.protocol + "//" + window.location.host + '/' + eventID,
            type: 'get',
            success: function(response) {

                switch (eventID) {
                    case 'togglePlay':
                        var label = response.playing ? "pause" : "play";
                        $("#togglePlay").css('background-image', 'url("/static/icons/' + label + '.svg")');
                        break;
                    case 'toggleFullscreen':
                        var fullscreen = response.fullscreen ? "restore" : "fullscreen";
                        $("#toggleFullscreen").css('background-image', 'url("/static/icons/' + fullscreen + '.svg")');
                        break;
                    case 'toggleMute':
                        var mute = response.sound ? 'speaker' : 'mute';
                        $("#toggleMute").css('background-image', 'url("/static/icons/' + mute + '.svg")');
                        break;
                    case 'volumeDown':
                    case 'volumeUp':
                        $("#volume").val(Math.round(response.volume * 100) / 100);
                        $("#volume").attr('title', Math.round(response.volume / 1 * 100) + "%");
                        break;
                    case 'seekBWD':
                    case 'seekFWD':
                        $("#progress").attr('max', response.length);
                        $("#progress").val(response.time);
                        $("#progress").attr('title', Math.round((response.time / response.length * 100 * 100) / 100) + "%");
                        break;
                    default:
                        break;
                }
            }
        });

    });

    updateInfo();
    setInterval(updateInfo, 3000);

});