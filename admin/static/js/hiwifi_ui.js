var HiwifiUI = {
    /**
     * 将select跟某些字段的显示与否绑定在一起，只在form中有效
     * @param 选择器
     * @param 配置 {'1': ['phones'],'2': ['score_low_bound', 'score_high_bound', 'area']}) key为selector的值，val为要显示的selector列表
     * @param value
     */
    selectTrigger: function (selector, config) {
        var f = function () {
            var selectedVal = $(selector).val();
            for (var val in config) {
                if (val == selectedVal) {
                    continue;
                }
                for (var i in config[val]) {
                    var field = config[val][i];
                    $('#' + field).parent().parent().hide();
                }
            }
            for (var i in config[selectedVal]) {
                var field = config[selectedVal][i];
                $('#' + field).parent().parent().show();
            }
        }
        $(selector).bind('change', f);
        f();
    }
}

