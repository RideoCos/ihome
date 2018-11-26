function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
// 加载用户头像
 $(document).ready(function(){
        $.get("/user/my_info/", function(data){
        if (data.code == 200){
            $("#user-avatar").attr("src", "/static/media/"+data.avatar);
        }
        });
    });

$(document).ready(function(){
    // 显示上传的图片
    $('#to_up').on('change',function(){
        var filePath = $(this).val(), //获取到input的value，里面是文件的路径
            fileFormat = filePath.substring(filePath.lastIndexOf(".")).toLowerCase(),
            src = window.URL.createObjectURL(this.files[0]); //转成可以在本地预览的格式
            $('#up_img').attr('src',src);
    });
    // 上传图片验证
    $("#form-avatar").submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/user/profile_info/',
            type: 'POST',
            dataType: 'json',
            success: function(data){
                if(data.code == 200){
                    $.get("/user/my_info/", function(data){
                        if (data.code == 200){
                            $("#user-avatar").attr("src", "/static/media/"+data.avatar);
                            location.href = '/user/my/';
                        }
                    })
                }
                if(data.code == 2001){
                    alert('图片格式错误!')
                }
            },
            error: function(data){
                alert('上传失败')
            }
        });
    });

})

$("#form-name").submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url: '/user/profile_info/',
        type: 'POST',
        dataType: 'json',
        success: function(data){
            if(data.code==200){
                location.href = '/user/my/';
            }
            if(data.code == 2002){
                $(".error-msg").html("用户名已存在")
                $(".error-msg").show();
            }
        },
        error: function(data){
            alert('修改失败')
        }
    });
});