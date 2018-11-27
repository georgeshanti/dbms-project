$("#create_reminder").submit(function(e){
    e.preventDefault();
    var $name = $("#reminderName").val();
    var $date = $("#reminderDate").val();
    var $desc = $("#reminderDescription").val();
    var $grp_t = $("#reminderGroup").val();
    var $grp = $($("#groups").find("[value="+$grp_t+"]")).attr("key");
    console.log($grp);
    form = {name: $name, date: $date, desc: $desc, group: $grp}
    $.post("/api/new_reminder",
    form,
    function(data, status){
        console.log(data)
        var result=JSON.parse(data);
        if(result['status']=="true"){
            $("#reminder-modal").modal('toggle');
        }
    });
});

$("#create_group").submit(function(e){
    e.preventDefault();
    var $name = $("#groupName").val();
    var $desc = $("#groupDesc").val();
    form = {name: $name, desc: $desc}
    $.post("/api/new_group",
    form,
    function(data, status){
        console.log(data)
        var result=JSON.parse(data);
        if(result['status']=="true"){
            $("#group-modal").modal('toggle');
        }
    });
});

$("#search_group").submit(function(e){
    e.preventDefault();
    var $name = $("#group_search_name").val();
    console.log($name);
    window.location.href = "/search/"+$name;
});