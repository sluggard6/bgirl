//常规通用库
//全局日志函数，防止ie9以下异常
var log = function (o) {
    if (!!console && !!console.log) {
        console.log(o)
    }
};
var domi = {
    //通用基础方法
    common: {
        //通用服务端错误方法
        error: function (jqXHR, textStatus, errorThrown) {
//            jqXHR.responseText = jqXHR.responseText.substr(0, 100);
//            alert(JSON.stringify(jqXHR));
//            alert(JSON.stringify(textStatus));
//            alert(JSON.stringify(errorThrown));
            var data = null;
            try {
                data = $.parseJSON(jqXHR.responseText);
            }
            catch (ex) {

            }
            domi.flashMessage((!!data) ? data.message : jqXHR.statusText, 'warn');
        }
        //通用json类型ajax请求方法
        , jsonAjax: function (_options) {
            var success = _options.success || function () {
            };
            var error = _options.error || function () {
            };
            var settings = $.extend(_options, {
                contentType: 'application/json',
                dataType: 'json',
                success: function (_data) {
                    if (_data.success) {
                        if (success(_data) !== false) {
                            domi.flashMessage(_data.message || '操作成功！', 'ok');
                        }
                    }
                    else {
                        if (error(_data) !== false) {
                            domi.flashMessage(_data.message || '操作失败！', 'warn');
                        }
                    }
                },
                error: domi.common.error
            });
            $.ajax(settings);
        }

        //增加自动关闭pop元素的id到关闭队列 - 点击元素外部关闭
        , addAutoClosePopId: function (el_id) {
            var pop_ids = $(document).data('auto-close-pop-ids') || [];
            pop_ids.push(el_id);
            $(document).data('auto-close-pop-ids', pop_ids);
        }

        //点击元素外部自动关闭
        , autoClosePopId: function (e) {
            var pop_ids = $(document).data('auto-close-pop-ids');
            if (!!pop_ids) {
                var $tar = $(e.target);
                for (var i = 0; i < pop_ids.length; i++) {
                    var pop = $('#' + pop_ids[i]);
                    if (!($tar === pop || $tar.closest(pop).length > 0) && $tar.attr('auto-pop-ref') !== pop_ids[i]) {
                        pop.remove();
                        $(document).data('auto-close-pop-ids', _.without(pop_ids, pop_ids[i]));
                    }
                }
            }
        }
    },

    flashMessage: function (message, type) {
        if (arguments.length > 0) {
            $.showMessage(message, type);
            return;
        }
        if (typeof(window.flashMessage) !== 'undefined') {
            _.each(['success', 'info', 'warning', 'error'], function (el, idx, list) {
                if (window.flashMessage[el].length > 0) {
                    message = window.flashMessage[el];
                    type = el;
                }
            });
        }
        if(!!message && message.length)
            $.showMessage(message, type)
    }

    //在中央打开指定url窗口
    , openCenterWin: function (url, win, width, height) {
        var left, top;
        left = (window.screen.availWidth - width) / 2;
        top = (window.screen.availHeight - height) / 2;
        var per = 'width=' + width + ',height=' + height + ',left=' + left + ',top=' + top + ',screenX=' + left + ',screenY=' + top;
        window.open(url, win, per);
    }

};


/*
 * top slide message tips
 *
 * code by linnchord@gmail.com
 * 2011-12-12
 *
 * */
(function () {
    jQuery.showMessage = function (message, options) {
        //不同消息类型定义：背景,字体颜色,在页面上停留时间
        var mysettings = {
            'warning': {
                delay: 4000
            },
            'info': {
                delay: 3000
            },
            'success': {}
        };

        var settings = jQuery.extend({
            id: 'top_flash_message_box',
            delay: 1500,
            speed: 300
        }, mysettings[options]);

        var elem = $('#' + settings.id);

        //初始化消息显示元素
        var sub_elem = null;
        if (elem.length == 0) {
            elem = $('<div></div>').attr('id', settings.id);
            elem.css({
                'position': 'fixed',
                'top': '-30px',
                'left': 0,
                'width': '100%',
                'z-index': 9999,
                'display': 'none'
            });
            sub_elem = $('<span></span>');

            sub_elem.css({
                'padding': '10px',
                'margin': 'auto',
                'font-size': '14px',
                'line-height': '18px',
                'display': 'block',
                'width': '40%',
                'max-width': '400px',
                'min-width': '200px',
                'text-align': 'center'
            });
            elem.append(sub_elem);
            $('body').append(elem);
        }
        else {
            sub_elem = elem.find('span');
        }

        sub_elem.removeClass().addClass('alert').addClass('alert-' + options);

        sub_elem.html(message);

        if ($.browser.msie && parseInt($.browser.version) < 9) {
            elem.css({
                'top': $(document).scrollTop() + 5 + 'px',
                'position': 'absolute'
            }).show();
            setTimeout(function () {
                elem.remove();
            }, settings.delay);
        }
        else {
            elem.show();
            elem.animate({"top": 8}, 600, function () {
                setTimeout(function () {
                    elem.animate(
                        {"top": -60},
                        200,
                        function () {
                            elem.remove();
                        }
                    );
                }, settings.delay);
            });
        }
    }
})(jQuery);


//获取url指定参数
$.getUrlParam = function (name) {
    var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (!results) {
        return null;
    }
    return results[1] || 0;
};

var gourl = function (url) {
    location.href = url;
};


$(function () {
    $(document).on('click', domi.autoClosePopId);
    domi.flashMessage();
});


/**
 * 根据event返回对应的element
 * @param event
 */
function get_target_element(event) {
    var targetElement;
    if (typeof event.target != 'undefined') {
        targetElement = event.target;
    }
    else {
        targetElement = event.srcElement;
    }
    return $(targetElement);
}
function load_url(url) {
    if (url.indexOf("http") == -1) {
        url = "http://" + window.location.host + url
    }
    window.location.href = url;
}
function reload() {
    window.location.reload();
}
/**
 * 判断是否为空字符串
 * @param str
 */
$.isBlankStr = function (str) {
    return !str || !$.trim(str)
};

/**
 * 判断字符串是否不为空
 * @param str
 */
$.isNotBlankStr = function (str) {
    return !($.isBlankStr(str));
};

function validate_field(id, message) {
    var selector = "#" + id;
    var val = $(selector).val();
    if ($.isBlankStr(val)) {
        //TODO 改成提示
        domi.flashMessage(message, "warn");

        $(selector).focus();
        return false;
    }
    return true;
}

/**
 * 是否整数
 * @param n
 */
function is_int(n) {
    try {
        n = parseFloat(n);
    } catch (e) {
        return false;
    }
    return typeof n === 'number' && n % 1 == 0;
}
/**
 * 元素是否存在
 * @param selector
 */
function is_exist(selector) {
    if ($(selector).length > 0) {
        return true
    } else {
        return false;
    }
}
/**
 * 元素是否可见
 * @param selector
 */
function is_visible(selector) {
    if ($(selector).is(":visible")) {
        return true;
    } else {
        return false;
    }
}
/**
 * 获取属性数量
 * @param o
 */
function get_property_count(o) {
    var n, count = 0;
    for (n in o) {
        if (o.hasOwnProperty(n)) {
            count++;
        }
    }
    return count;
}

$.fn.isOnScreen = function () {

    var win = $(window);

    var viewport = {
        top: win.scrollTop(),
        left: win.scrollLeft()
    };
    viewport.right = viewport.left + win.width();
    viewport.bottom = viewport.top + win.height();

    var bounds = this.offset();
    bounds.right = bounds.left + this.outerWidth();
    bounds.bottom = bounds.top + this.outerHeight();

    return (!(viewport.right < bounds.left || viewport.left > bounds.right || viewport.bottom < bounds.top || viewport.top > bounds.bottom));

};

/**
 * 是否整个元素都可见
 * @returns {boolean}
 */
$.fn.isFullOnScreen = function () {

    var win = $(window);

    var viewport = {
        top: win.scrollTop(),
        left: win.scrollLeft()
    };
    viewport.right = viewport.left + win.width();
    viewport.bottom = viewport.top + win.height();

    var bounds = this.offset();
    bounds.right = bounds.left + this.outerWidth();
    bounds.bottom = bounds.top + this.outerHeight();

    return (viewport.right >= bounds.right && viewport.left <= bounds.left && viewport.bottom >= bounds.bottom && viewport.top <= bounds.top);

};

$.fn.isMobile = function (val) {
    var mobileReg = /^1\d{10}$/;
    if (!mobileReg.test(val)) {
        return false;
    } else {
        return true;
    }
};

$.fn.isEmail = function (val) {
    var reg = /^([a-z\d\._-]+)@([\da-z\._-]+)\.([a-z]{2,6})$/;
    if (!reg.test(val)) {
        return false;
    } else {
        return true;
    }
};

$.fn.isTel = function (val) {
    return (/^(([0\+]\d{2,3}-)?(0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$/.test(val));
};

$.fn.isPhone = function (val) {
    return $.fn.isMobile(val) || $.fn.isTel(val);
};
