$(document).ready(function(){
    $('#email').keyup(function(){
        var data = $("#regForm").serialize() // capture all data in the variable data
        $.ajax({
            method:"POST", // we are using a post request here, but this could also be done with a get
            url:"/useremail",
            data: data
        })
        .done(function(res){
            $('#useremailMsg').html(res) // manipulate the dom when the response comes back
        })
    })
})