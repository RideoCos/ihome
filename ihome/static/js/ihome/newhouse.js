function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    $.get('/house/area_info/', function(data){
        var area_str = '';
        for(var i=0;i<data[0].length;i++){
            area_str += "<option value='"+ data[0][i]["id"] +"'>"+ data[0][i]["name"] + "</option>";
            $("#area-id").html(area_str);
        }
    });
    $.get('/house/area_info/', function(data){
        var facility_str = '';
        for(var i=0;i<data[1].length;i++){
            facility_str += "<li><div class='checkbox'><label><input type='checkbox' name='facility' value='"+ data[1][i]["id"] +"'>"+ data[1][i]["name"] +"</label></div></li>"
            $(".house-facility-list").html(facility_str);
        }
    });
    $('#form-house-info').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/house/up_house/',
            type: 'POST',
            dataType: 'json',
            success: function(data){
                 if(data.code == 200){
                    $('#form-house-info').hide();
                    $("#form-house-image").css("display", "block");
                    $("#house-id").val(data.house_id);
                 }
            },
            error: function(data){
                alert("发布失败")
            }
        })
    });

    $('#house-image').on('change',function(){
        var filePath = $(this).val(), //获取到input的value，里面是文件的路径
        fileFormat = filePath.substring(filePath.lastIndexOf(".")).toLowerCase(),
        src = window.URL.createObjectURL(this.files[0]); //转成可以在本地预览的格式
        $('#up_img').attr('src',src);
     });

    $('#form-house-image').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/house/up_house_image/',
            type: 'POST',
            dataType: 'json',
            success: function(data){
                if(data.code == 200){
                    alert('发布成功！')
                    location.href = '/house/my_house/';
                }
                if(data.code == 2001){
                    alert("图片格式错误！")
                }
            },
            error: function(data){

            }
        })
    })

})