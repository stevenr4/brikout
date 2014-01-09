



var monthNames = [ "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December" ];

$(document).ready(function(){

    function read_hour(){
        hour_int = $("#input_hour").val() // 0-95 (0 - ((24 * 4) -1)
        //for(x = 0; x < 96; x++){console.log((Math.floor(x/4) + ":" + ("0" + ((x % 4) * 15)).slice(-2));}
        ampm = ""
        if(hour_int < 48){
            ampm = "am";
        }else{
            ampm = "pm";
        }
        hour_string = "  " + ("0" + (((Math.floor(hour_int/4) + 11) % 12) + 1)).slice(-2) + ":" + ("0" + ((hour_int % 4) * 15)).slice(-2) + ampm;
        $("#output_hour").text(hour_string);
    }


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

    function hide_where(){
        $('#input_where_wrapper').hide(300);
    }

    function show_where(){
        $('#input_where_wrapper').show(300);
    }

    function populate_lists(){

        // Get the date so we can highlight today
        var d = new Date();
        // Populate the date time lists
        var output_string = "";
        // The day of the month  *1-31
        for(var index = 1; index <= 31; index++){
            output_string += "<option value='" + index + "'>" + index + "</option>";
        }
        $("#input_day").html(output_string);
        $("#input_day").val(String(d.getDate()))
        // The months *0-11
        output_string = "";
        for(var index = 0; index < 12; index++){
            output_string += "<option value='" + index + "'>" + monthNames[index] + "</option>";
        }
        $("#input_month").html(output_string);
        $("#input_month").val(String(d.getMonth()));
        // The year (from this year onwards 2 years, to total 3)
        output_string = "";
        for(var index = d.getFullYear(); index < (d.getFullYear() + 4); index++){
            output_string += "<option value='" + index + "'>" + index + "</option>";
        }
        $("#input_year").html(output_string);
        $("#input_year").val(String(d.getFullYear()));

        //Finally, The hours
        output_string = "";
        for(var index = 0; index < 24; index++){
            output_string += "<option>" + (index * 4) + "</option>";
        }
        $("#input_hour_data").html(output_string);
        $("#input_hour").val(60);
        read_hour();

        // // DOING A RANGE |-----x------| 12:00pm






        // Get the data to populate friends, games, and systems
        $.ajax({
            type: "GET",
            url: '/api01/user/',
            dataType: 'json',
            success: function(data){
                console.log(data);


                // Populate the list of buddies
                array_of_buddies = data['buddies'];
                var output_string;
                if(array_of_buddies.length <= 0){
                    output_string = "<br>You currently don't have any buddies to add. <br>You can invite buddies after you've created the event.";
                }else{
                    output_string = "<ul>";
                    var index = 0
                    for(index = 0; (index < array_of_buddies.length) && (index < 5); index++){
                        var tmp_string = 
                        "<li><input type='checkbox' value='" + 
                        array_of_buddies[index].user_id +
                        "' class='input_friend_checkbox'> " + array_of_buddies[index].username +
                        "</li>";

                        output_string += tmp_string;
                    }
                    if(index >= 5){
                        output_string += "<li>[ You can add more buddies after the event is created ]</li>";
                    }
                    output_string += "</ul>";
                }
                $("#input_buddies_wrapper").html(output_string);

                // Populate the list of games
                array_of_games = data['games'];
                var output_string = "";
                output_string = "<option value='any'>Any Game</option>";
                for(index = 0; index < array_of_games.length; index++){
                    output_string += "<option value='" + 
                    array_of_games[index].id + 
                    "'>" + array_of_games[index].name +
                    "</option>";
                }
                $("#input_game").html(output_string);

                // // Populate the list of systems
                // array_of_systems = data['systems'];
                // var output_string = "";
                // output_string = "<option value='any'>Any System</option>";
                // for(index = 0; index < array_of_systems.length; index++){
                //     output_string += "<option value='" + 
                //     array_of_systems[index].id + 
                //     "'>" + array_of_systems[index].name +
                //     "</option>";
                // }
                // $("#input_system").html(output_string);

            },
            error: function(xhr, text, errorScript){
                console.log("Failure attempting to populate event data.");
                console.log(text);
                console.log(errorScript);
                $("#form_error_message").text("Something went wrong, notify server admin and try again.");
            }
        });
    }

    populate_lists();
    $('#input_where_wrapper').hide();
    $("#input_hour").on("change",read_hour);













    $("#input_in_person").on("change",function(){

        in_person = $(this).prop('checked');

        console.log(in_person);

        if(in_person){
            show_where();
        }else{
            hide_where();
        }
    });















    $("#input_submit").on("click",function(){

        var title = $("#input_title").val()
        var game_id = $("#input_game").val();
        var system_id = $("#input_system").val();
        var month = $("#input_month").val();
        var day = $("#input_day").val();
        var year = $("#input_year").val();
        var hour = $("#input_hour").val();
        var is_private = $("#input_private").val();
        var invite_only = $("#input_invite_only").val();
        var in_person = $("#input_in_person").val();
        var where = $("#input_where").val();
        var description = $("#input_description").val();



        if(title == ""){
            $("#output_message").text("You need to create a title for your event!");
            return;
        }


        d = new Date(0);


        d.setDate(day);
        d.setMonth(month);
        d.setFullYear(year);
        d.setHours(hour);

        var millisecs = d.getTime();

        console.log(millisecs);
        console.log(game_id);
        console.log(system_id);


        invite_array = [];

        $(".input_friend_checkbox").each(function(){
            if(this.checked){
                invite_array.push(this.value);
            }
        });

        data_to_send = {
            'title': title,
            'game_id': game_id,
            'system_id': system_id,
            'millisecs': millisecs,
            'private': is_private,
            'invite_only': invite_only,
            'in_person': in_person,
            'where': where,
            'invites': invite_array,
            'description': description
        }



        deactivate_all();


        
        $.ajax({
            type: "POST",
            url: '/api01/event/',
            dataType: 'json',
            data:data_to_send,
            success: function(g){
                console.log(g);
                console.log("SUCCESS!!!");
                if(g['success'] == true){
                    document.location = g['url'];
                }else{
                    activate_all();
                    $("#output_message").text("Event failed to create.");
                }
                activate_all();
            },
            error: function(xhr, text, errorScript){
                console.log("Failure attempting to log in.");
                console.log(text);
                console.log(errorScript);
                $("#output_message").text("Something went wrong, notify server admin and try again.");
            }
        });
    });
});