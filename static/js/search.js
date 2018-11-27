$("#search_page_form").submit(function(e){
    e.preventDefault();
    var $name = $("#search_page_form_name").val();
    window.location.href = "/search/"+$name;
});

$("#search_group").submit(function(e){
    e.preventDefault();
    var $name = $("#group_search_name").val();
    console.log($name);
    window.location.href = "/search/"+$name;
});

$(".group_request").click(function(){
    var $id=$(this).attr("key");
    form = {id: $id}
    $.post("/api/add_group",
    form,
    function(data, status){
        console.log(data)
        var result=JSON.parse(data);
        if(result['status']=="true"){
            $("#group-modal").modal('toggle');
        }
    });

});