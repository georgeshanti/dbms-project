$('#login-form').submit(function(){
  var form = {user: $('#login_username').val(), pass: $('#login_password').val()};
  $.post("/api/login",
  form,
  function(data, status){
    console.log(status+" "+data)
  });
});
