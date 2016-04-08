function ajaxRequest(){
    var activexmodes=["Msxml2.XMLHTTP", "Microsoft.XMLHTTP"] //activeX versions to check for in IE
    if (window.ActiveXObject){ //Test for support for ActiveXObject in IE first (as XMLHttpRequest in IE7 is broken)
        for (var i=0; i<activexmodes.length; i++){
            try{
                return new ActiveXObject(activexmodes[i])
            }
            catch(e){
                //suppress error
            }
        }
    }
    else if (window.XMLHttpRequest) // if Mozilla, Safari etc
        return new XMLHttpRequest()
    else
        return false
}

function request_user_delete(user_id){
    console.log("delete")
    var http = new ajaxRequest()
    var host = window.location.hostname
    if(host == '127.0.0.1'){
        host = host + ':8080';
    }


    var url = "http://"+ host +"/admin/user/delete";
    http.open("GET", url+'?id='+user_id, true);
    http.setRequestHeader("Content-Type", "application/json");
    http.onreadystatechange = function(){
        if(http.readyState == 4 && http.status == 200){
            alert("success");
        }
    }
    http.send();

}


function request_property_edit(id){
    var row = document.getElementById("user_"+id+"_property")
    var row_data = row.getElementsByTagName("td");
    var properties = new Object();
    properties.user_id = row_data.item(0).textContent;
    properties.nickname = row_data.item(1).textContent;
    properties.rune_stone = row_data.item(2).textContent;
    properties.gem = row_data.item(3).textContent;
    properties.ancient_coin = row_data.item(4).textContent;
    properties.honor_coin = row_data.item(5).textContent;
    properties.group_soul_stone_elf = row_data.item(6).textContent;
    properties.group_soul_stone_human = row_data.item(7).textContent;
    properties.group_soul_stone_orc = row_data.item(8).textContent;
    properties.group_soul_stone_furry = row_data.item(9).textContent;
    properties.adventure_slot = row_data.item(10).textContent;

    for(var property in properties){
        if (!isNaN(property)){
            alert("insert only number");
        }
    }

    properties_json = JSON.stringify(properties);

    var http = new ajaxRequest()
    var host = window.location.hostname
    if(host == '127.0.0.1'){
        host = host + ':8080';
    }


    var url = "http://"+ host +"/admin/user/edit";
    http.open("POST", url, true);
    http.setRequestHeader("Content-Type", "application/json");
    http.onreadystatechange = function(){
        if(http.readyState == 4 && http.status == 200){
            alert("success");
        }
    }
    http.send(properties_json);
}
