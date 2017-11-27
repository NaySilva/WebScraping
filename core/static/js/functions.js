console.log('page3');

function loaderData(id){
    var loading = $('#loading');
    var content = $('#content');
    content.hide();
    loading.show();
    $.ajax({
        url: '/save/'+id,
        dataType:'json',
        success: function(data){
            console.log('ok');
            if (data.done){
                location.reload();
            };
        }
    });
}