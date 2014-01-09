



///////////////////////////////////////









////////////////         'game_id' IS BEING PASSED AS A VARIABLE











//////////////////////////////



$(document).ready(function(){


    $("#input_claim").on('click',function(){
        // alert("CLICKED!");

        $('#input_claim').prop('disabled', true);
        

        $.ajax({
            type: "POST",
            url: '/api01/user/game/',
            dataType: 'json',
            data: {
                'game_id': game_id
            },
            success: function(data){
                $("#user_status").html("You have claimed you own this game.");
            },
            error: function(xhr, text, errorScript){
                console.log("Failure attempting to claim game.");
                console.log(text);
                console.log(errorScript);
                $("#output_message").text("Something went wrong, notify server admin and try again.");
                $("#input_claim").prop('disabled',false);
            }
        });
    });


    $("#input_disown").on('click',function(){
        // alert("DISOWNED!");

        $('#input_disown').prop('disabled', true);
        

        $.ajax({
            type: "POST",
            url: '/api01/user/game/',
            dataType: 'json',
            data: {
                'game_id': game_id,
                'disown': true
            },
            success: function(data){
                $("#user_status").html("You have now disowned this game.");
            },
            error: function(xhr, text, errorScript){
                console.log("Failure attempting to disown game.");
                console.log(text);
                console.log(errorScript);
                $("#output_message").text("Something went wrong, notify server admin and try again.");
                $("#input_disown").prop('disabled',false);
            }
        });
    });
});