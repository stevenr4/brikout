





console.log(name);
console.log("LDSJFKLHSDF");


















$(document).ready(function(){


    // n/a KILLER
    $.tablesorter.addParser({ 
        // set a unique id 
        id: 'my_na_killer', 
        is: function(s) { 
            return false
        }, 
        format: function(s) { 
            // format your data for normalization 
            if(s.indexOf("n/a") != -1){
                return null;
            }

            //  console.log(s);
            return s;

        }, 
        // set type, either numeric or text 
        type: 'text' 
    }); 


    $('#output_systems_table').tablesorter({ 
        headers: { 
            2: {
                sorter:'my_na_killer'
            },
            3: {
                sorter:'my_na_killer'
            },
            4: {
                sorter:'my_na_killer'
            }
        } 
    }); 










////////////////////////////////////////

    // var total_users = {{total_games}};
    // var name={{name}};

///////////////////////////////////////



    function setSearchParameters(){
        $('#input_name').val(name);

    }

    setSearchParameters();


    function getURLWithParams(){

        name = $('#input_name').val();

        //The page that we're gonna send to
        url_string = document.location.origin;
        url_string += document.location.pathname;

        url_string += '?'

        //Now we start attaching things to the string
        if(name != ''){
            url_string += "name=" + name;
        }
        return url_string;

    }






    $("#input_submit").on("click",function(){

        // Now we direct the user to this version of the page
        document.location = getURLWithParams();
    });


});










