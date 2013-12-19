



















var short_month_names = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ];

$(document).ready(function(){

    // add parser through the tablesorter addParser method 
    $.tablesorter.addParser({ 
        // set a unique id 
        id: 'my_dates', 
        is: function(s) { 
            return false
        }, 
        format: function(s) {

            // format your data for normalization 
            for(var i = 0; i < short_month_names.length; i++){
                s = s.replace(short_month_names[i], i);
            }
            var list = s.match(/\d+/g); // Get a list of all integers
            // console.log(list);
            if((list == null) || (list.length != 3)){
                return null
            }
            // console.log((list[2] * 365))
            // console.log(list[0] * 31)
            // console.log((list[2] * 365) + (list[0] * 31) + list[1]);
            return ((list[2] * 365) + (list[0] * 31) + list[1]); 
        }, 
        // set type, either numeric or text 
        type: 'numeric' 
    }); 

    // $.tablesorter.formatInt = function (s) {
    //     var i = parseInt(s);
    //     return (isNaN(i)) ? null : i;
    // };
    // $.tablesorter.formatFloat = function (s) {
    //     var i = parseFloat(s);
    //     return (isNaN(i)) ? null : i;
    // };
    $.tablesorter.formatStr = function (s) {
        return (s.indexOf('n/a') == -1) ? s : null;
    }


    // ESRB
    $.tablesorter.addParser({ 
        // set a unique id 
        id: 'my_esrb', 
        is: function(s) { 
            return false
        }, 
        format: function(s) { 
            // format your data for normalization 
            if(s.indexOf("n/a") != -1){
                return null;
            }


            // An array of all the possible ratings from least to violent
            ratings_arr = ['EC','E','E10+','T','M','RP'];

            s = $.trim(s);
            // console.log(s);
            var found = $.inArray(s, ratings_arr);
            // console.log(found);
            if(found > -1){
                return found;
            }else{
                return null
            }

        }, 
        // set type, either numeric or text 
        type: 'numeric' 
    }); 

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
            1: {
                sorter:'my_esrb'
            },
            2: {
                sorter:'my_na_killer'
            },
            3: {
                sorter:'my_na_killer'
            },
            4: {
                sorter:'my_na_killer'
            },
            5: {
                sorter:'my_na_killer'
            },
            6: { 
                sorter:'my_dates' 
            } 
        } 
    }); 










////////////////////////////////////////

    // var advanced_search = {{advanced_search}}
    // var page_number = {{page_number}};
    // var page_size = {{page_size}};
    // var page_total = {{page_total}};
    // var total_games = {{total_games}};
    // var name={{name}};
    // var system_id={{system_id}};
    // var genre={{genre}};
    // var esrb={{esrb}};
    // var coop={{coop}};
    // var sort_by={{sort_by}};

///////////////////////////////////////



    function setSearchParameters(){
        // Check if we're doing an advanced search
        if(advanced_search){
            $("#input_advanced").prop('checked',true);
            $("#input_advanced_wrapper").show(0);
            $("#input_system").val(system_id);
            $("#input_genre").val(genre);
            $("#input_esrb").val(esrb);
            $("#input_coop").val(coop);
            $("#input_sort").val(sort_by);
        }
        $('#input_name').val(name);
        $("#input_page_size").val(page_size);
        //alert(page_size);

    }







    $("#input_advanced_wrapper").hide();

    $("#input_advanced").on('change',function(){
        if(this.checked){
            $("#input_advanced_wrapper").show(300);
        }else{
            $("#input_advanced_wrapper").hide(300);
        }
    });

    setSearchParameters();

    function getURLWithParams(){

        advanced_search = $("#input_advanced").is(':checked')?true:false;

        //alert(advanced_search);
        name = $('#input_name').val();
        system_id = $("#input_system").val();
        genre = $("#input_genre").val();
        esrb = $("#input_esrb").val();
        coop = $("#input_coop").val();
        
        sort_by = $("#input_sort").val();
        page_size = $("#input_page_size").val();

        //The page that we're gonna send to
        url_string = document.location.origin;
        url_string += document.location.pathname;

        url_string += '?'

        //Now we start attaching things to the string
        if(name != ''){
            url_string += "name=" + name + "&";
        }
        if(advanced_search == true){
            url_string += "advanced=true&";
            if(parseInt(system_id) != 0){
                url_string += "system_id=" + system_id + "&";
            }
            if(genre != 'any'){
                url_string += "genre=" + genre + '&';
            }
            if(esrb != 'any'){
                url_string += "esrb=" + esrb + '&';
            }
            if(coop != 'either'){
                url_string += "coop=" + coop + '&';
            }
            if(sort_by != 'title'){
                url_string += "sort_by=" + sort_by + '&';
            }
        }
        url_string += "page_size=" + page_size;

        return url_string;

    }






    // The submit for the data for another search
    console.log(document.location);

    $("#input_submit").on("click",function(){

        // Now we direct the user to this version of the page
        document.location = getURLWithParams();
    });


    /*
    ============================================
    == This section is for the page switching ==
    ============================================

    */

    // First page
    $("#input_first_page").on('click',function(){
        document.location = getURLWithParams();
    });

    $("#input_prev_page").on('click',function(){
        if(page_number > 1){
            document.location = getURLWithParams() + "&page_number=" + (page_number - 1);
        }
    });

    $("#input_next_page").on('click',function(){
        if(page_number < page_total){
            document.location = getURLWithParams() + "&page_number=" + (page_number + 1);
        }
    });

    $("#input_last_page").on('click',function(){
        document.location = getURLWithParams() + "&page_number=" + page_total;
    });


});










