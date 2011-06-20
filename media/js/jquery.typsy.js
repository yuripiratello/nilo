(function($) {
    $.fn.tipsy = function(opts) {

        opts = $.extend({fade: false, gravity: 'n'}, opts || {});
        // ...Added by andy@twitter.com 20090717
        if(!opts['offsetTop']) { opts['offsetTop'] = 0; }
        if(!opts['offsetLeft']) { opts['offsetLeft'] = 0; }
        if(!opts['header']) { opts['header'] = ''; }
        if(!opts['footer']) { opts['footer'] = ''; }
        if(!opts['hideTimeout']) { opts['hideTimeout'] = 100; }
        if(!opts['showTimeout']) { opts['hideTimeout'] = 0; }
        if(!opts['additionalCSSClass']) { opts['additionalCSSClass'] = ''; }
        var showTimeoutKey = false;
        // ...Added by andy@twitter.com 20090717
        var tip = null, cancelHide = false;
        this.hover(function() {

            // ...Added by andy@twitter.com 20090717
            var linkText = $(this).text();
            var header = opts['header'].replace('%{link}', linkText);
            var footer = opts['footer'].replace('%{link}', linkText);
            // ...Added by andy@twitter.com 20090717

            $.data(this, 'cancel.tipsy', true);

            var tip = $.data(this, 'active.tipsy');
            if (!tip) {
                $('.tipsy').hide();
                tip = $('<div class="tipsy '+ opts['additionalCSSClass'] +'"><div class="tipsy-inner">' + header + $(this).attr('title') + footer + '</div></div>');
                tip.css({position: 'absolute', zIndex: 100000});
                $(this).attr('title', '');
                $.data(this, 'active.tipsy', tip);
            // Added by rael@twitter.com 20090628...
            } else if ($(this).attr('title') != '') {
              tip.find('.tipsy-inner').html($(this).attr('title'));
              $(this).attr('title', '');
            // ...Added by rael@twitter.com 20090628
            }

            var pos = $.extend({}, $(this).offset(), {width: this.offsetWidth, height: this.offsetHeight});
            // ...Added by andy@twitter.com 20090717
            pos.top = pos.top + opts['offsetTop'];
            pos.left = pos.left + opts['offsetLeft'];

            // remove open tips if timeout to fade
            $('.tipsy').hide();
            // ...Added by andy@twitter.com 20090717
            tip.remove().css({top: 0, left: 0, visibility: 'hidden', display: 'block'}).appendTo(document.body);
            var actualWidth = tip[0].offsetWidth, actualHeight = tip[0].offsetHeight;

            switch (opts.gravity.charAt(0)) {
                case 'n':
                    tip.css({top: pos.top + pos.height, left: pos.left + pos.width / 2 - actualWidth / 2}).addClass('tipsy-north');
                    break;
                case 'l':
                    //left north align
                    tip.css({top: pos.top + pos.height, left: pos.left + pos.width / 2 - 18}).addClass('tipsy-north');
                    break;
                case 's':
                    tip.css({top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2}).addClass('tipsy-south');
                    break;
                case 'e':
                    tip.css({top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth}).addClass('tipsy-east');
                    break;
                case 'w':
                    tip.css({top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width}).addClass('tipsy-west');
                    break;
            }
            // ...Added by andy@twitter.com 20090717
            function show() {
              if (opts.fade) {
                  tip.css({opacity: 0, display: 'block', visibility: 'visible'}).animate({opacity: 1});
              } else {
                  tip.css({visibility: 'visible'});
              }
            }
            if(opts['showTimeout']) {
              showTimeoutKey = setTimeout(show, opts['showTimeout']);
            } else {
              show();
            }
        }, function() {
            clearTimeout(showTimeoutKey);
            // ...Added by andy@twitter.com 20090717
            $.data(this, 'cancel.tipsy', false);
            var self = this;
            setTimeout(function() {
                if ($.data(this, 'cancel.tipsy')) return;
                var tip = $.data(self, 'active.tipsy');
                if (opts.fade) {
                    tip.stop().fadeOut(function() { $(this).remove(); });
                } else {
                    tip.remove();
                }
            }, opts['hideTimeout']);
        });

    };
})(jQuery);

