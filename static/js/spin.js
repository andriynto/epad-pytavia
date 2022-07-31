var Rats = {};
		
Rats.UI = {};

Rats.UI.LoadAnimation = {
    "start" : function() {
        $('#spinner-preview').css('display','inline');
        $('#spinner-preview').height('100%');
        $('#spinner-preview').width('100%');
        var top = $(window).height() / 2;
        var left = $(window).width() / 2;
        
        var opts = {
                lines:13,
                length:28,
                width:14,
                radius:42,
                scale:0.2,
                corners:1,
                color:'#FFFFFF',
                opacity:0.25,
                rotate:0,
                direction:1,
                speed:1,
                trail:60,
                fps:20,
                zIndex:2e9,
                className:'spinner',
                top:top + 'px',
                left:left + 'px',
                shadow:false,
                hwaccel:false,
                position:'fixed'};
        
        var target = document.getElementById('spinner-preview');
        return new Spinner(opts).spin(target);
    },
    "stop" : function(spinner) {
        spinner.stop();
        $('#spinner-preview').fadeOut(200);
    }
};