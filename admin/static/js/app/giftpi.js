; var refreshCaptcha = function(){
    var $captcha = $('img.captcha');
    $captcha.attr('src', $captcha.attr('src').split('?')[0] + '?' + Math.random());
};