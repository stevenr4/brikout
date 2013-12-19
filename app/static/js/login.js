function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^(("[\w-+\s]+")|([\w-+]+(?:\.[\w-+]+)*)|("[\w-+\s]+")([\w-+]+(?:\.[\w-+]+)*))(@((?:[\w-+]+\.)*\w[\w-+]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][\d]\.|1[\d]{2}\.|[\d]{1,2}\.))((25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\.){2}(25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\]?$)/i);
    return pattern.test(emailAddress);
};

$(document).ready(function(){





    is_extra_showing = false;

    function deactivate_all(){
        $('input').prop('disabled', true);
    }

    function activate_all(){
        $('input').prop('disabled', false);
    }

    function hide_extra(){
        $('#input_signup_extra').hide();
        is_extra_showing = false;
        $("#input_login").val("Login");
    }

    function show_extra(){
        $('#input_signup_extra').show();
        is_extra_showing = true;
        $("#input_login").val("Switch To Login");
    }


    hide_extra();




    function login(){

        if(is_extra_showing){
            hide_extra();
        }else{

            username = $("#input_username").val();
            password = $("#input_password").val();
            deactivate_all();
            $.ajax({
                type: "POST",
                url: '/api01/user/auth/',
                dataType: 'json',
                data:{
                    'login': true,
                    'username': username,
                    'password': password
                },
                success: function(g){
                    console.log(g);
                    console.log("SUCCESS!!!");
                    if(g['success'] == true){
                        document.location = g['url'];
                    }else{
                        activate_all();
                        $("#form_error_message").text("Login Unsuccessful.");
                    }
                },
                error: function(xhr, text, errorScript){
                    console.log("Failure attempting to log in.");
                    console.log(text);
                    console.log(errorScript);
                    $("#form_error_message").text("Something went wrong, notify server admin and try again.");
                }
            });
        }
    }

    function signup(){

        username = $("#input_username").val();
        password = $("#input_password").val();
        password_confirm = $("#input_password_confirm").val();
        email = $("#input_email").val();

        if((email.length < 1) || (password_confirm.length < 1)){
            show_extra();
            $("#form_error_message").text("Please fill out an email and confirm password to create an account.");
        }else{

            if(!isValidEmailAddress(email)){
                $("#form_error_message").text("The email address you entered is invalid.");
            }else if(password != password_confirm){
                $("#form_error_message").text("The passwords you entered did not match up.");
            }else{

                deactivate_all();
                //PRINT OUT THAT WE ARE TRYING TO CREATE A USER AND LOGIN

                // First we try to create a user
                $.ajax({
                    type: "POST",
                    url: '/api01/user/',
                    dataType: 'json',
                    data:{
                        'username': username,
                        'password': password
                    },
                    success: function(g){
                        console.log(g);
                        console.log("SUCCESS!!!");
                        if(g['success'] == true){

                            // We successfully created a user, now let's log into that user.
                            $.ajax({
                                type: "POST",
                                url: '/api01/user/auth/',
                                dataType: 'json',
                                data:{
                                    'login': true,
                                    'username': username,
                                    'password': password
                                },
                                success: function(g){
                                    console.log(g);
                                    console.log("SUCCESS!!!");
                                    if(g['success'] == true){
                                        document.location = g['url'];
                                    }else{
                                        activate_all();
                                        $("#form_error_message").text("Login Unsuccessful.");
                                    }
                                },
                                error: function(xhr, text, errorScript){
                                    console.log("Failure attempting to log in.");
                                    console.log(text);
                                    console.log(errorScript);
                                    $("#form_error_message").text("Something went wrong, notify server admin and try again.");
                                }
                            });


                        }else{
                            activate_all();
                            $("#form_error_message").text("Login Unsuccessful.");
                        }
                    },
                    error: function(xhr, text, errorScript){
                        console.log("Failure attempting to log in.");
                        console.log(text);
                        console.log(errorScript);
                        $("#form_error_message").text("Something went wrong, notify server admin and try again.");
                    }
                });
            }
        }
    }






    $('input').keypress(function (e) {
        if (e.which == 13) {
            if (is_extra_showing){
                signup();
            }else{
                login();
            }
        }
    });

    $("#input_login").on("click",login);

    $("#input_signup").on("click",signup);


});