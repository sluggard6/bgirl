/**
 * Created with PyCharm.
 * User: liubo
 * Date: 13-5-5
 * Time: 上午9:32
 * To change this template use File | Settings | File Templates.
 */

var LuhuAdmin = {
    upload: function (selector, media_type, success_callback, options) {
        var sizelimt = 5120000000
        var setting = $.extend({
            'swf': '/static/js/lib/uploadify-v3.2.1/uploadify.swf',
            'uploader': '/api/upload/' + media_type,
            'cancelImg': '/static/js/lib/uploadify-v3.2.1/uploadify-cancel.png',
            'auto': true,
            'width': 123,
            'height': 30,
            'buttonText': '选择图片',
            'fileDataName': 'file_uploader',
            'fileExt': '*',
            'sizeLimit': sizelimt,
            'onUploadSuccess': function (file, data, response) {
                // alert('id: ' + file.id
                //     + ' - 索引: ' + file.index
                //     + ' - 文件名: ' + file.name
                //     + ' - 文件大小: ' + file.size
                //     + ' - 类型: ' + file.type
                //     + ' - 创建日期: ' + file.creationdate
                //     + ' - 修改日期: ' + file.modificationdate
                //     + ' - 文件状态: ' + file.filestatus
                //     + ' - 服务器端消息: ' + data
                //     + ' - 是否上传成功: ' + response);
                var json = jQuery.parseJSON(data);
                if (json.success) {
                    success_callback(json);
                }
            },
            'onUploadError': function (file, errorCode, erorMsg, errorString) {
                $.showMessage('错误码: ' + errorCode
                    + ' - 错误信息: ' + erorMsg
                    + ' - 错误信息详细: ' + errorString, 'warning');
            }
        }, options);
        console.log(setting);
        $(selector).uploadify(setting);
    },
    uploadQbox: function (selector, success_callback, options) {

        var setting = $.extend({
            'swf': '/static/js/lib/uploadify-v3.2.1/uploadify.swf',
            'uploader': '/api/upload',
            'cancelImg': '/static/js/lib/uploadify-v3.2.1/uploadify-cancel.png',
            'auto': true,
            'width': 123,
            'height': 30,
            'buttonText': '选择图片',
            'fileDataName': 'file_uploader',
            'fileExt': '*',
            'sizeLimit': 5120000000,
            'onComplete': function (event, ID, fileObj, response, data) {
                var json = jQuery.parseJSON(response);
                if (json.success) {
                    success_callback(json);
                }
                else {
                    $.showMessage(json.errorMsg, 'warning');
                }
            }
        }, options);
        $(selector).uploadify(setting);
    },
    /**
     * 替换url中的参数值，比如将当前url：http://mige365.com/essence?p=1 中的p替换成2，变成http://mige365.com/essence?p=2
     * 如果参数不存在，会增加这个参数
     * @param url
     * @param param
     * @param value
     */
    replaceOrAddUrlParam: function (url, param, value) {
        var need_parsed_str = null;
        var param_length = param.length;
        var url_part_begin = null;  //存储“http://mige365.com/essence?p=” 这一部分
        var part_begin_index = 0;
        var url_part_end = "";    //存储url尾部，这里只提取value部分做替换
        var part_end_index = 0;
        if (url.indexOf("&" + param) != -1) {
            part_begin_index = url.indexOf("&" + param) + param.length + 2; //+2 包含了"&“和"="
            need_parsed_str = url.substr(part_begin_index);

        } else if (url.indexOf("?" + param) != -1) {
            part_begin_index = url.indexOf("?" + param) + param.length + 2;
            need_parsed_str = url.substr(part_begin_index);
        } else {
            var kv_str = param + "=" + value;
            if (url.indexOf("?") != -1) {
                url += "&" + kv_str;
            } else {
                url += "?" + kv_str;
            }
            return url;
        }
        url_part_begin = url.substr(0, part_begin_index);

        if (need_parsed_str.indexOf("&") != -1) {
            part_end_index = need_parsed_str.indexOf("&");
            url_part_end = need_parsed_str.substr(part_end_index);
        }
        return url_part_begin + value + url_part_end;
    },
    /**
     * 从url中删除某个参数值
     * @param url
     * @param param
     */
    removeUrlParam: function (url, param) {
        var patten = "(^|\\?|&)" + param + "=\\d*(?=(&|$))";
        console.log(patten);
        //(^|\?|&)courseid=\d*(&|$)
        var param_reg = new RegExp(patten);
        var param_value_reg = new RegExp();
        var matched = param_reg.exec(url);
        if (matched != null) {
            var match_value = matched[0];
            console.log(match_value)
            if (new RegExp("^\\?").test(match_value)) {
                url = url.replace(param_reg, "?")
            } else {
                url = url.replace(param_reg, "")
            }
        }
        return url
    },
    upload_sys: function (selector, script, success_callback, options) {
        var setting = $.extend({
            'swf': '/static/js/lib/uploadify-v3.2.1/uploadify.swf',
            'uploader': script,
            'cancelImg': '/static/js/lib/uploadify-v3.2.1/uploadifyy-cancel.png',
            'auto': true,
            'width': 123,
            'height': 30,
            'buttonText': '选择图片',
            'fileDataName': 'file_uploader',
            'fileExt': '*',
            'sizeLimit': 5120000000,
            'onComplete': function (event, ID, fileObj, response, data) {
                var json = jQuery.parseJSON(response);
                if (json.success) {
                    success_callback(json);
                }
                else {
                    $.showMessage(json.errorMsg, 'warning');
                }
            }
        }, options);
        $(selector).uploadify(setting);
    },
    get: function (url, success_callback, error_callback) {
        $.ajax({
            type: 'GET',
            dataType: 'json',
            url: url,
            success: function (ret) {
                if (ret.success) {
                    if (success_callback) {
                        success_callback(ret);
                    } else {
                        $.showMessage("操作成功", "ok");
                    }
                }
                else {
                    if (error_callback) {
                        error_callback(ret);
                    } else {
                        $.showMessage(ret.message, "warning");
                    }
                }
            },
            error: function (resp) {
                $.showMessage("操作失败，请稍后再试。", "warning");
            }
        });
    },
    post: function (url, data, success_callback, error_callback) {
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: url,
            data: data,
            success: function (ret) {
                if (ret.success) {
                    if (success_callback) {
                        success_callback(ret);
                    } else {
                        $.showMessage("操作成功", "ok");
                    }
                }
                else {
                    if (error_callback) {
                        error_callback(ret);
                    } else {
                        $.showMessage(ret.message, "warning");
                    }
                }
            },
            error: function (resp) {
                $.showMessage("操作失败，请稍后再试。", "warning");
            }
        });
    }, del: function (url, data, success_callback, error_callback) {
        $.ajax({
            type: 'DELETE',
            dataType: 'json',
            url: url,
            data: data,
            success: function (ret) {
                if (ret.success) {
                    if (success_callback) {
                        success_callback(ret);
                    } else {
                        $.showMessage("操作成功", "ok");
                    }
                }
                else {
                    if (error_callback) {
                        error_callback(ret);
                    } else {
                        $.showMessage(ret.message, "warning");
                    }
                }
            },
            error: function (resp) {
                $.showMessage("操作失败，请稍后再试。", "warning");
            }
        });
    }, reload: function () {
        window.location.reload();
    }, loadUrl: function (url) {
        window.location = url;
    }
};

$(function () {
    $('[data-toggle=tooltip]').tooltip();
    $('[data-auto-light-menu]').each(function () {
        var deep = $(this).data('auto-light-menu'), current = null;
        var path = $.url('path');
        if (!!deep) {
            _.each($(this).find('a'), function (el) {
                for (var i = deep; i > 0; i--) {
                    current = $.url(i, $(el).attr('href'));
                    if (current === $.url(i)) {
                        if (!!current && path.split(current)[0] === $(el).attr('href').split(current)[0]) {
                            //当前path分段有值且之前的路径一致
                            $(el).parent().addClass('active');
                        }
                        else {
                            continue;
                        }

                    }
                    break;
                }
            });
        }
    });
});

function validateField(id, message) {
    var selector = "#" + id;
    var val = $(selector).val();
    if ($.isBlankStr(val)) {
        $.showMessage(message, "warn");
        $(selector).focus();
        return false;
    }
    return true;
}

