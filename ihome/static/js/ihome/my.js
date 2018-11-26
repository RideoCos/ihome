function logout() {
   $.ajax({
        url: '/user/logout/',
        dataType: 'json',
        type: 'GET',
        success: function(data){
            if (data.code == 200){
                location.href = '/user/login/'
            }
        },
        error: function(){
            alert('退出失败')
        }
    })
}

$(document).ready(function(){
    $.get("/user/my_info/", function(data){
        if(data.code == 200){
             $("#user-name").html(data.name);
             $("#user-mobile").html(data.phone);
             $("#user-avatar").attr("src", "/static/media/"+data.avatar)
        }
    });
})