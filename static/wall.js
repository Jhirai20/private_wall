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
    $('#search').keyup(function(){
        var data = $('#searchForm').serialize()
        $.ajax({
            method:"GET",
            url:"/emailsearch",
            data: data
        })
        .done(function(res){
            $('#searchMsg').html(res)
        })
    })
    $('.trash').click(function(){
        
        var id=$(this).attr('id')
        console.log(id);
        $.ajax({
            method:"post",
            url:'/destroy/'+id,
        })
        .done(function(){
            console.log("***clicke", id)
            $('#message'+id).css("display", "none");
        })
    })
    $('#message2').submit(function(event){
        event.preventDefault();
        $.ajax({
            method: "POST",
            url: $(this).attr('message'),
            data: $(this).serialize()
        })
    
        return false;
    })
})
