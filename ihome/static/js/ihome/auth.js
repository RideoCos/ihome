function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
};


$.get('/user/auth_success/', function(data){
    if(data.code == 200){
        $("#real-name").val(data.id_name);
        $("#id-card").val(data.id_card);
        $("#real-name").attr("disabled", true);
        $("#id-card").attr("disabled", true);
        $(".btn-success").hide();

    }
});

$('#form-auth').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url: '/user/auth_info/',
        dataType: 'json',
        type: 'POST',
        success: function(data){
            if(data.code == 200){
                location.href = '/user/my/';
            }
            if(data.code == 3000){
                $(".error-msg").html("身份证号格式不对！")
                $(".error-msg").show();
            }
            if(data.code == 3001){
                $(".error-msg").html("姓名格式不对！")
                $(".error-msg").show();
            }
            if(data.code == 2000){
                alert("认证失败")
            }
        },
        error: function(){
            alert("认证失败")
        }
    })
});
