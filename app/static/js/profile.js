

$(document).ready(function(){



    $("#input_save_changes").hide(0);

    function deactivate_all(){
        $('input').prop('disabled', true);
        $('select').prop('disabled', true);
        $("textarea").prop('disabled', true);
        $('button').prop('disabled', true);
    }

    function activate_all(){
        $('input').prop('disabled', false);
        $('select').prop('disabled', false);
        $('textarea').prop('disabled', false);
        $('button').prop('disabled', false);
    }

    function hide_all_editables(){
        $("#output_edit_name_wrapper").show();
        $("#input_edit_name_wrapper").hide();
    }

    $(".input_remove_game").on('click',function(){
        

        var game_id = parseInt(this.id.match(/\d+/g)); // Get the id

        $.ajax({
            type: "POST",
            url: '/api01/user/game/',
            dataType: 'json',
            data: {
                'game_id': game_id,
                'disown': true
            },
            success: function(data){
                if(data['success'] == true){
                    $("#span_remove_game_id" + game_id).html("[disowned]");
                }else{
                    $("#span_remove_game_id" + game_id).html("[failed-to-disown]");
                    alert("Remove failed.");
                }
            },
            error: function(xhr, text, errorScript){
                console.log("Failure attempting to disown game.");
                console.log(text);
                console.log(errorScript);
                alert("Remove game failed.");
            }
        });
    });


// ADDING AND REMOVIN BUDDIES

    $("#input_add_buddy").on('click',function(){

        $("input_add_buddy").prop('disabled',true);

        $.ajax({
            type: "POST",
            url: '/api01/user/buddies/',
            dataType: 'json',
            data: {
                'user_id': user_id,
                'buddy_id': profile_id
            },
            success: function(data){
                if(data.success == true){
                    $("#input_add_buddy").text("You have sent a buddy invite!");
                }
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


    $("input").on('keydown',function(){
        $("#input_save_changes").text("Save Changes");
        $("#input_save_changes").prop('disabled',false);
        $("#input_save_changes").show(300);
    });
    $("textarea").on('keydown', function(){
        $("#input_save_changes").text("Save Changes");
        $("#input_save_changes").prop('disabled',false);
        $("#input_save_changes").show(300);
    });




    $("#input_save_changes").on("click",function(){

        var first_name = $("#input_first_name").val()
        var last_name = $("#input_last_name").val();
        var email = $("#input_email").val();
        var bio = $("#input_bio").val();

        // VALIDATE EMAIL

        data_to_send = {
            'user_id':user_id, ///////////////// PASSED THROUGH BY TEMPLATE
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'bio': bio
        }



        deactivate_all();


        
        $.ajax({
            type: "POST",
            url: '/api01/user/',
            dataType: 'json',
            data:data_to_send,
            success: function(g){
                console.log(g);
                console.log("SUCCESS!!!");
                if(g['success'] == true){
                    activate_all();
                    $("#input_save_changes").text("Changes Saved");
                    $("#input_save_changes").prop('disabled',true);

                }else{
                    activate_all();
                    $("#input_save_changes").text("Failed to Save");
                }
            },
            error: function(xhr, text, errorScript){
                console.log("Failure attempting to save changes.");
                console.log(text);
                console.log(errorScript);
                activate_all();
                $("#input_save_changes").text("Error");
            }
        });
    });
});