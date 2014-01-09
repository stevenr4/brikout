










///////////////////////////////////////









////////////////////////////////////////////         'event_id' IS BEING PASSED AS A VARIABLE











//////////////////////////////



$(document).ready(function(){

    $("#input_invite_buddies_wrapper").hide();




    // Get the data to populate friends, games, and systems
    $.ajax({
        type: "GET",
        url: '/api01/event/?event_id=' + event_id,
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
    

    $("#input_attend").on('click',function(){

        $('#input_attend').prop('disabled', true);
        

        $.ajax({
            type: "POST",
            url: '/api01/event/attend/',
            dataType: 'json',
            data: {
                'event_id': event_id
            },
            success: function(data){
                $("#user_status").html("You are now attending this event.");
                location.reload();
            },
            error: function(xhr, text, errorScript){
                console.log("Failure attempting to attend event.");
                console.log(text);
                console.log(errorScript);
                $("#output_message").text("Something went wrong, notify server admin and try again.");
                $("#input_attend").prop('disabled',false);
            }
        });
    });


    $("#input_leave").on('click',function(){

        $('#input_leave').prop('disabled', true);
        

        $.ajax({
            type: "POST",
            url: '/api01/event/attend/',
            dataType: 'json',
            data: {
                'event_id': event_id,
                'leave': true
            },
            success: function(data){
                $("#user_status").html("You have now left this event.");
                location.reload();
            },
            error: function(xhr, text, errorScript){
                console.log("Failure attempting to leave event.");
                console.log(text);
                console.log(errorScript);
                $("#output_message").text("Something went wrong, notify server admin and try again.");
                $("#input_leave").prop('disabled',false);
            }
        });
    });

    var invite_buddies_showing = false


    $("#input_invite_buddies").on('click',function(){

        if(invite_buddies_showing==false){
            invite_buddies_showing = true;

            $("#input_invite_buddies_wrapper").show(300);
            
            $("#input_invite_buddies").prop('disabled', true);

            $.ajax({
                type:"GET",
                url: '/api01/event/attend/?event_id=' + event_id + "&buddies_not_attending=true",
                dataType: 'json',
                success: function(data){
                    if(data['success'] == true){
                        if(data['list_of_users'].length == 0){
                            $("#input_invite_buddies_wrapper").html("<br>All of your buddies are invited or already going!")
                        }else{
                            console.log(data);
                            console.log(data['list_of_users'][0])
                            var output_string = "<br>";
                            //Go through the users and add their data to the data string
                            for(var index = 0; index < data['list_of_users'].length; index++){
                                console.log(data['list_of_users'][index]['id'] + " > " + data['list_of_users'][index]['username'] );
                                output_string += "<input type='checkbox' class='input_invite_buddy_checkbox' id='" + 
                                    data['list_of_users'][index]['id'] + "'>" + data['list_of_users'][index]['username'] + "<br>";
                            }
                            $("#input_invite_buddies_wrapper").html(output_string);
                            $("#input_invite_buddies").prop('disabled', false);
                            $("#input_invite_buddies").text('Send Invites.');
                        }
                    }else{
                        $("#input_invite_buddies_wrapper").text("Something went wrong, notify server admin and try again.");
                        $("#input_invite_buddies").prop('disabled',false);
                        invite_buddies_showing = false;
                    }


                },
                error: function(xhr, text, errorScript){
                    console.log("Failure pulling friend data.");
                    console.log(text);
                    console.log(errorScript);
                    $("#input_invite_buddies_wrapper").text("Something went wrong, notify server admin and try again.");
                    $("#input_invite_buddies").prop('disabled',false);
                    invite_buddies_showing = false;
                }
            });
        }else{
            console.log("ELSE");


            // Go through all of the checkboxes that have the class tag and make a call to invite that person
            $(".input_invite_buddy_checkbox:checked").each(function(){
                console.log("Inviting " + this.id);
                console.log(this.checked);
                $.ajax({
                    type:"POST",
                    url: '/api01/event/invite/',
                    dataType: 'json',
                    data: {
                        'event_id': event_id,
                        'buddy_id': this.id
                    },
                    success: function(data){
                        if(data['success'] == true){
                            $("#input_invite_buddies").text('Invite More Buddies');
                            $("#input_invite_buddies_wrapper").html("<br>Invites sent!")
                            invite_buddies_showing = false;
                        }else{
                            $("#input_invite_buddies_wrapper").text("Something went wrong, notify server admin and try again.");
                            $("#input_invite_buddies").prop('disabled',false);
                            invite_buddies_showing = false;

                        }
                    },
                    error: function(xhr, text, errorScript){
                        console.log("Failure sending friend data.");
                        console.log(text);
                        console.log(errorScript);
                        $("#input_invite_buddies_wrapper").text("Something went wrong, notify server admin and try again.");
                        $("#input_invite_buddies").prop('disabled',false);
                        invite_buddies_showing = false;
                    }
                });
            });
        }

    });


});








