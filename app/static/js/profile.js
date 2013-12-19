

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
        $("#input_edit_name_wrapper").hide();
        $("#input_edit_email_wrapper").hide();
        $("#input_edit_bio_wrapper").hide();
        $("#input_edit_user_xbox_wrapper").hide();
        $("#input_edit_user_steam_wrapper").hide();
    }

    hide_all_editables();

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


    $("#input_remove_buddy").on('click',function(){

        $("input_remove_buddy").prop('disabled',true);

        $.ajax({
            type: "POST",
            url: '/api01/user/buddies/',
            dataType: 'json',
            data: {
                'user_id': user_id,
                'buddy_id': profile_id,
                'unbuddy': true
            },
            success: function(data){
                console.log(data);
                if(data.success == true){
                    $("#input_remove_buddy").text("You have successfully un-buddied");
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


    // $("input").on('keydown',function(){
    //     $("#input_save_changes").text("Save Changes");
    //     $("#input_save_changes").prop('disabled',false);
    //     $("#input_save_changes").show(300);
    // });
    // $("textarea").on('keydown', function(){
    //     $("#input_save_changes").text("Save Changes");
    //     $("#input_save_changes").prop('disabled',false);
    //     $("#input_save_changes").show(300);
    // });
    var name_editing = false;
    $("#input_edit_name_cancel").on("click",function(){
        name_editing = false;
        $("#output_edit_name_wrapper").show(300);
        $("#input_edit_name_wrapper").hide(300);
        $("#input_edit_name").text("Edit Name");
    });
    $("#input_edit_name").on("click",function(){
        if(name_editing == false){
            name_editing = true;
            $("#output_edit_name_wrapper").prop('disabled',false);
            $("#input_edit_name_wrapper").prop('disabled',false);
            $("#output_edit_name_wrapper").hide(300);
            $("#input_edit_name_wrapper").show(300);
            $("#input_edit_name").text("Save Changes");

        }else{
            $("#output_edit_name_wrapper").prop('disabled',true);
            $("#input_edit_name_wrapper").prop('disabled',true);
            $("#input_edit_name").text("Saving...");
            $("#input_edit_name").prop('disabled',true);

            var first_name = $("#input_first_name").val()
            var last_name = $("#input_last_name").val();

            data_to_send = {
                'user_id':user_id, ///////////////// PASSED THROUGH BY TEMPLATE
                'first_name': first_name,
                'last_name': last_name
            }

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
                        $("#input_edit_name").text("Changes Saved, Edit Again");
                        $("#input_edit_name").prop('disabled',false);

                        $("#output_edit_name_wrapper").text(first_name + " " + last_name);

                        $("#output_edit_name_wrapper").show(300);
                        $("#input_edit_name_wrapper").hide(300);
                        name_editing = false;
                    }else{
                        $("#input_edit_name").text("Failed to Save");
                        $("#input_edit_name").prop('disabled',false);
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
        }

    });


    var email_editing = false;
    $("#input_edit_email_cancel").on("click",function(){
        email_editing = false;
        $("#output_edit_email_wrapper").show(300);
        $("#input_edit_email_wrapper").hide(300);
        $("#input_edit_email").text("Edit Email");
    });

    $("#input_edit_email").on("click",function(){
        if(email_editing == false){
            email_editing = true;
            $("#output_edit_email_wrapper").prop('disabled',false);
            $("#input_edit_email_wrapper").prop('disabled',false);
            $("#output_edit_email_wrapper").hide(300);
            $("#input_edit_email_wrapper").show(300);
            $("#input_edit_email").text("Save Changes");

        }else{
            $("#output_edit_email_wrapper").prop('disabled',true);
            $("#input_edit_email_wrapper").prop('disabled',true);
            $("#input_edit_email").text("Saving...");
            $("#input_edit_email").prop('disabled',true);

            var email = $("#input_email").val()

            data_to_send = {
                'user_id':user_id, ///////////////// PASSED THROUGH BY TEMPLATE
                'email': email
            }

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
                        $("#input_edit_email").text("Changes Saved, Edit Again");
                        $("#input_edit_email").prop('disabled',false);

                        $("#output_edit_email_wrapper").text(email);

                        $("#output_edit_email_wrapper").show(300);
                        $("#input_edit_email_wrapper").hide(300);
                        email_editing = false;
                    }else{
                        $("#input_edit_email").text("Failed to Save");
                        $("#input_edit_email").prop('disabled',false);
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
        }

    });


    var bio_editing = false;
    $("#input_edit_bio_cancel").on("click",function(){
        bio_editing = false;
        $("#output_edit_bio_wrapper").show(300);
        $("#input_edit_bio_wrapper").hide(300);
        $("#input_edit_bio").text("Edit Bio");
    });

    $("#input_edit_bio").on("click",function(){
        if(bio_editing == false){
            bio_editing = true;
            $("#output_edit_bio_wrapper").prop('disabled',false);
            $("#input_edit_bio_wrapper").prop('disabled',false);
            $("#output_edit_bio_wrapper").hide(300);
            $("#input_edit_bio_wrapper").show(300);
            $("#input_edit_bio").text("Save Changes");

        }else{
            $("#output_edit_bio_wrapper").prop('disabled',true);
            $("#input_edit_bio_wrapper").prop('disabled',true);
            $("#input_edit_bio").text("Saving...");
            $("#input_edit_bio").prop('disabled',true);

            var bio = $("#input_bio").val()

            data_to_send = {
                'user_id':user_id, ///////////////// PASSED THROUGH BY TEMPLATE
                'bio': bio
            }

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
                        $("#input_edit_bio").text("Changes Saved, Edit Again");
                        $("#input_edit_bio").prop('disabled',false);

                        $("#output_edit_bio_wrapper").text(bio);

                        $("#output_edit_bio_wrapper").show(300);
                        $("#input_edit_bio_wrapper").hide(300);
                        bio_editing = false;
                    }else{
                        $("#input_edit_bio").text("Failed to Save");
                        $("#input_edit_bio").prop('disabled',false);
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
        }

    });

    var user_xbox_editing = false;
    $("#input_edit_user_xbox_cancel").on("click",function(){
        user_xbox_editing = false;
        $("#output_edit_user_xbox_wrapper").show(300);
        $("#input_edit_user_xbox_wrapper").hide(300);
        $("#input_edit_user_xbox").text("Edit Xbox Live Account");
    });

    $("#input_edit_user_xbox").on("click",function(){
        if(user_xbox_editing == false){
            user_xbox_editing = true;
            $("#output_edit_user_xbox_wrapper").prop('disabled',false);
            $("#input_edit_user_xbox_wrapper").prop('disabled',false);
            $("#output_edit_user_xbox_wrapper").hide(300);
            $("#input_edit_user_xbox_wrapper").show(300);
            $("#input_edit_user_xbox").text("Save Changes");

        }else{
            $("#output_edit_user_xbox_wrapper").prop('disabled',true);
            $("#input_edit_user_xbox_wrapper").prop('disabled',true);
            $("#input_edit_user_xbox").text("Saving...");
            $("#input_edit_user_xbox").prop('disabled',true);

            var user_xbox = $("#input_user_xbox").val()

            data_to_send = {
                'user_id':user_id, ///////////////// PASSED THROUGH BY TEMPLATE
                'user_xbox': user_xbox
            }

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
                        $("#input_edit_user_xbox").text("Changes Saved, Edit Again");
                        $("#input_edit_user_xbox").prop('disabled',false);

                        $("#output_edit_user_xbox_wrapper").text(user_xbox);

                        $("#output_edit_user_xbox_wrapper").show(300);
                        $("#input_edit_user_xbox_wrapper").hide(300);
                        user_xbox_editing = false;
                    }else{
                        $("#input_edit_user_xbox").text("Failed to Save");
                        $("#input_edit_user_xbox").prop('disabled',false);
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
        }

    });


    var user_steam_editing = false;
    $("#input_edit_user_steam_cancel").on("click",function(){
        user_steam_editing = false;
        $("#output_edit_user_steam_wrapper").show(300);
        $("#input_edit_user_steam_wrapper").hide(300);
        $("#input_edit_user_steam").text("Edit Steam Account");
    });

    $("#input_edit_user_steam").on("click",function(){
        if(user_steam_editing == false){
            user_steam_editing = true;
            $("#output_edit_user_steam_wrapper").prop('disabled',false);
            $("#input_edit_user_steam_wrapper").prop('disabled',false);
            $("#output_edit_user_steam_wrapper").hide(300);
            $("#input_edit_user_steam_wrapper").show(300);
            $("#input_edit_user_steam").text("Save Changes");

        }else{
            $("#output_edit_user_steam_wrapper").prop('disabled',true);
            $("#input_edit_user_steam_wrapper").prop('disabled',true);
            $("#input_edit_user_steam").text("Saving...");
            $("#input_edit_user_steam").prop('disabled',true);

            var user_steam = $("#input_user_steam").val()

            data_to_send = {
                'user_id':user_id, ///////////////// PASSED THROUGH BY TEMPLATE
                'user_steam': user_steam
            }

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
                        $("#input_edit_user_steam").text("Changes Saved, Edit Again");
                        $("#input_edit_user_steam").prop('disabled',false);

                        $("#output_edit_user_steam_wrapper").text(user_steam);

                        $("#output_edit_user_steam_wrapper").show(300);
                        $("#input_edit_user_steam_wrapper").hide(300);
                        user_steam_editing = false;
                    }else{
                        $("#input_edit_user_steam").text("Failed to Save");
                        $("#input_edit_user_steam").prop('disabled',false);
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
        }

    });


    // $("#input_save_changes").on("click",function(){

    //     var first_name = $("#input_first_name").val()
    //     var last_name = $("#input_last_name").val();
    //     var email = $("#input_email").val();
    //     var bio = $("#input_bio").val();

    //     // VALIDATE EMAIL

    //     data_to_send = {
    //         'user_id':user_id, ///////////////// PASSED THROUGH BY TEMPLATE
    //         'first_name': first_name,
    //         'last_name': last_name,
    //         'email': email,
    //         'bio': bio
    //     }



    //     deactivate_all();


        
    //     $.ajax({
    //         type: "POST",
    //         url: '/api01/user/',
    //         dataType: 'json',
    //         data:data_to_send,
    //         success: function(g){
    //             console.log(g);
    //             console.log("SUCCESS!!!");
    //             if(g['success'] == true){
    //                 activate_all();
    //                 $("#input_save_changes").text("Changes Saved");
    //                 $("#input_save_changes").prop('disabled',true);

    //             }else{
    //                 activate_all();
    //                 $("#input_save_changes").text("Failed to Save");
    //             }
    //         },
    //         error: function(xhr, text, errorScript){
    //             console.log("Failure attempting to save changes.");
    //             console.log(text);
    //             console.log(errorScript);
    //             activate_all();
    //             $("#input_save_changes").text("Error");
    //         }
    //     });
    // });
});