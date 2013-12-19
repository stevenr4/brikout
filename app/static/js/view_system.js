










///////////////////////////////////////









////////////////         'system_id' IS BEING PASSED AS A VARIABLE











//////////////////////////////



$(document).ready(function(){

    



    /*
    // Get the data for the system (May need this)
    $.ajax({
        type: "GET",
        url: '/api01/system/?system_id=' + event_id,
        dataType: 'json',
        success: function(data){
            console.log(data);
        },
        error: function(xhr, text, errorScript){
            console.log("Failure attempting get data.");
            console.log(text);
            console.log(errorScript);
            $("#output_message").text("Something went wrong, notify server admin and try again.");
        }
    });
    */


    $("#input_claim").on('click',function(){
        //alert("CLICKED!");

        $('#input_claim').prop('disabled', true);
        

        $.ajax({
            type: "POST",
            url: '/api01/user/system/',
            dataType: 'json',
            data: {
                'system_id': system_id
            },
            success: function(data){
                $("#user_status").html("You have claimed you own this system.");
            },
            error: function(xhr, text, errorScript){
                console.log("Failure attempting to claim system.");
                console.log(text);
                console.log(errorScript);
                $("#output_message").text("Something went wrong, notify server admin and try again.");
                $("#input_claim").prop('disabled',false);
            }
        });
    });


    $("#input_disown").on('click',function(){
        //alert("DISOWNED!");

        $('#input_disown').prop('disabled', true);
        

        $.ajax({
            type: "POST",
            url: '/api01/user/system/',
            dataType: 'json',
            data: {
                'system_id': system_id,
                'disown': true
            },
            success: function(data){
                $("#user_status").html("You have now disowned this system.");
            },
            error: function(xhr, text, errorScript){
                console.log("Failure attempting to disown system.");
                console.log(text);
                console.log(errorScript);
                $("#output_message").text("Something went wrong, notify server admin and try again.");
                $("#input_disown").prop('disabled',false);
            }
        });
    });
});