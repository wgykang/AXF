// 用户注册表单提交是否满足要求,返回True或者False
function check_input() {
    let $password = $('#exampleInputPassword');
    let password = $password.val();
    if(password){
        $password.val(md5(password));
        return true
    }else {
        return false
    }
}