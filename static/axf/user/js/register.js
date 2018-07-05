// 用户注册表单提交是否满足要求,返回True或者False
function check_input() {
    let username_color = $('#usernameinfo').find('span').css('color');
    // console.log(username_color);
    if(username_color==='rgb(255, 0, 0)'){
        return false
    }
    let $password = $('#exampleInputPassword');
    let password = $password.val();
    let password_confirm = $('#exampleInputPasswordConfirm').val();
    if (password.length > 5) {
        if(password===password_confirm){
            $password.val(md5(password));
            return true
        }else {
            return false
        }
    } else {
        return false
    }
}


$(function () {
    $('#exampleInputUsername').change(function () {
        let username = $(this).val();
        $.getJSON('/axf/checkuser/', {'username': username}, function (data) {
            console.log(data);
            if(data['status']==='200'){
                $('#usernameinfo').html(data['msg']);
            }else if(data['status']==='901'){
                $('#usernameinfo').html(data['msg']);
            }
        })
    })
});