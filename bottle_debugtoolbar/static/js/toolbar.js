(function($) {
    $.cookie = function(name, value, options) { if (typeof value != 'undefined') { options = options || {}; if (value === null) { value = ''; options.expires = -1; } var expires = ''; if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) { var date; if (typeof options.expires == 'number') { date = new Date(); date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000)); } else { date = options.expires; } expires = '; expires=' + date.toUTCString(); } var path = options.path ? '; path=' + (options.path) : ''; var domain = options.domain ? '; domain=' + (options.domain) : ''; var secure = options.secure ? '; secure' : ''; document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join(''); } else { var cookieValue = null; if (document.cookie && document.cookie != '') { var cookies = document.cookie.split(';'); for (var i = 0; i < cookies.length; i++) { var cookie = $.trim(cookies[i]); if (cookie.substring(0, name.length + 1) == (name + '=')) { cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); break; } } } return cookieValue; } };
    $('head').append('<link rel="stylesheet" href="'+DEBUG_TOOLBAR_STATIC_PATH+'css/toolbar.css?'+ Math.random() +'" type="text/css" />');
    var COOKIE_NAME = 'fldt';
    var COOKIE_NAME_ACTIVE = COOKIE_NAME +'_active';
    var fldt = {
        init: function() {
            $('#flDebug').show();
            var current = null;
            $('#flDebugPanelList li a').click(function() {
                if (!this.className) {
                    return false;
                }
                current = $('#flDebug #' + this.className + '-content');
                if (current.is(':visible')) {
                    $(document).trigger('close.flDebug');
                    $(this).parent().removeClass('active');
                } else {
                    $('.panelContent').hide(); // Hide any that are already open
                    current.show();
                    $('#flDebugToolbar li').removeClass('active');
                    $(this).parent().addClass('active');
                }
                return false;
            });
            $('#flDebugPanelList li .switch').click(function() {
                var $panel = $(this).parent();
                var $this = $(this);
                var dom_id = $panel.attr('id');

                // Turn cookie content into an array of active panels
                var active_str = $.cookie(COOKIE_NAME_ACTIVE);
                var active = (active_str) ? active_str.split(';') : [];
                active = $.grep(active, function(n,i) { return n != dom_id; });

                if ($this.hasClass('active')) {
                    $this.removeClass('active');
                    $this.addClass('inactive');
                }
                else {
                    active.push(dom_id);
                    $this.removeClass('inactive');
                    $this.addClass('active');
                }

                if (active.length > 0) {
                    $.cookie(COOKIE_NAME_ACTIVE, active.join(';'), {
                        path: '/', expires: 10
                    });
                }
                else {
                    $.cookie(COOKIE_NAME_ACTIVE, null, {
                        path: '/', expires: -1
                    });
                }
            });
            $('#flDebug a.flDebugClose').click(function() {
                $(document).trigger('close.flDebug');
                $('#flDebugToolbar li').removeClass('active');
                return false;
            });
            $('#flDebug a.remoteCall').click(function() {
                $('#flDebugWindow').load(this.href, {}, function() {
                    $('#flDebugWindow a.flDebugBack').click(function() {
                        $(this).parent().parent().hide();
                        return false;
                    });
                });
                $('#flDebugWindow').show();
                return false;
            });
            $('#flDebugTemplatePanel a.flTemplateShowContext').click(function() {
                fldt.toggle_arrow($(this).children('.toggleArrow'))
                fldt.toggle_content($(this).parent().next());
                return false;
            });
            $('#flDebugSQLPanel a.flSQLShowStacktrace').click(function() {
                fldt.toggle_content($('.flSQLHideStacktraceDiv', $(this).parents('tr')));
                return false;
            });
            $('#flHideToolBarButton').click(function() {
                fldt.hide_toolbar(true);
                return false;
            });
            $('#flShowToolBarButton').click(function() {
                fldt.show_toolbar();
                return false;
            });
            $(document).bind('close.flDebug', function() {
                // If a sub-panel is open, close that
                if ($('#flDebugWindow').is(':visible')) {
                    $('#flDebugWindow').hide();
                    return;
                }
                // If a panel is open, close that
                if ($('.panelContent').is(':visible')) {
                    $('.panelContent').hide();
                    return;
                }
                // Otherwise, just minimize the toolbar
                if ($('#flDebugToolbar').is(':visible')) {
                    fldt.hide_toolbar(true);
                    return;
                }
            });
            if ($.cookie(COOKIE_NAME)) {
                fldt.hide_toolbar(false);
            } else {
                fldt.show_toolbar(false);
            }
            $('#flDebug table.tablesorter')
                .tablesorter()
                .bind('sortStart', function() {
                    $(this).find('tbody tr')
                        .removeClass('flDebugEven')
                        .removeClass('flDebugOdd');
                })
                .bind('sortEnd', function() {
                    $(this).find('tbody tr').each(function(idx, elem) {
                        var even = idx % 2 == 0;
                        $(elem)
                            .toggleClass('flDebugEven', even)
                            .toggleClass('flDebugOdd', !even);
                    });
                });
        },
        toggle_content: function(elem) {
            if (elem.is(':visible')) {
                elem.hide();
            } else {
                elem.show();
            }
        },
        close: function() {
            $(document).trigger('close.flDebug');
            return false;
        },
        hide_toolbar: function(setCookie) {
            // close any sub panels
            $('#flDebugWindow').hide();
            // close all panels
            $('.panelContent').hide();
            $('#flDebugToolbar li').removeClass('active');
            // finally close toolbar
            $('#flDebugToolbar').hide('fast');
            $('#flDebugToolbarHandle').show();
            // Unbind keydown
            $(document).unbind('keydown.flDebug');
            if (setCookie) {
                $.cookie(COOKIE_NAME, 'hide', {
                    path: '/',
                    expires: 10
                });
            }
        },
        show_toolbar: function(animate) {
            // Set up keybindings
            $(document).bind('keydown.flDebug', function(e) {
                if (e.keyCode == 27) {
                    fldt.close();
                }
            });
            $('#flDebugToolbarHandle').hide();
            if (animate) {
                $('#flDebugToolbar').show('fast');
            } else {
                $('#flDebugToolbar').show();
            }
            $.cookie(COOKIE_NAME, null, {
                path: '/',
                expires: -1
            });
        },
        toggle_arrow: function(elem) {
            var uarr = String.fromCharCode(0x25b6);
            var darr = String.fromCharCode(0x25bc);
            elem.html(elem.html() == uarr ? darr : uarr);
        },
        load_href: function(href) {
          $.get(href, function(data, status, xhr) {
            document.open();
            document.write(xhr.responseText);
            document.close();
          });
          return false;
        }
    };
    $(document).ready(function() {
        fldt.init();
    });
    window.fldt = fldt;

})(jQuery.noConflict(true));



//
// HTML Validator panel
//
(function(window, document, version, callback) {
    var j, d;
    var loaded = false;
    if (!(j = window.jQuery) || version > j.fn.jquery || callback(j)) {
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = DEBUG_TOOLBAR_MEDIA_URL + "js/jquery.js";
        script.onload = script.onreadystatechange = function() {
            if (!loaded && (!(d = this.readyState) || d == "loaded" || d == "complete")) {
                callback((j = window.jQuery).noConflict(1), loaded = true);
                j(script).remove();
            }
        };
        document.documentElement.childNodes[0].appendChild(script)
    }
})(window, document, "1.3", function($, jquery_loaded){
    $(document).ready(function() {
        var prevBackToTopElem = null;
        $('#djDebug-htmlvalidator .handle-position').click(function(){
            $('#djDebug-htmlvalidator .repr-info-sel').removeClass('repr-info-sel');
            $(this).parent().parent().addClass('repr-info-sel');
            var text = $(this).text();
            var re = new RegExp('line\\s+([0-9]+)');
            var result = text.match(re);

            try{
                var lineno = result[1];
            }catch(e){return;}
            //
            var prevPos = $(document).data('reprlineselpos') || null;
            if(prevPos){
                prevPos.removeClass('repr-line-sel');
            }
            var reprLineElem = $('#djDebug-htmlvalidator .repr-line-' + lineno + ':first');
            reprLineElem.addClass('repr-line-sel');
            $(document).data('reprlineselpos', $('.repr-line-' + lineno));
            // skip pervious link and add new one

            var locationPrefix = location;
            if(location.href.indexOf('#') > -1){
                var newLocation = location.href.substring(0, location.href.indexOf('#'));
                locationPrefix = newLocation;
            }
            location = locationPrefix + '#' + 'repr-line-' + lineno;

            // add `back to top` functionality
            if(prevBackToTopElem){
              prevBackToTopElem.remove();
            }
            var backToTopElem = $('#repr-line-backtotop').fadeOut('fast');

            var reprLineElemOffset = reprLineElem.offset();
            backToTopElem.css({
              'top': reprLineElemOffset.top + 'px',
              'left': (reprLineElemOffset.left - 17) + 'px'
            }).fadeIn('fast');
        });
        $('#djDebug-htmlvalidator .tidy-msg').click(function(e){
            $('.handle-position:first', $(this).prev()).click();
        });
    });
});
