<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>
<title>
Info
%if arg:
- ${arg}
%endif
</title>
<style type="text/css">
div.plugin_result {
    max-height: 400px;
    overflow: auto;
}
</style>
</head>

<body>

<h1>nInfo</h1>

<form method="GET" action="/">

<fieldset>
    <legend> Information Lookup </legend>
    <label for="arg">Query:</label>
    <input type="search" name="arg" id="arg" required autofocus value="${arg}">
    <input type="submit" value="Lookup">
</fieldset>
</form>

%if arg:

Jump to:
%for p in plugins:
<a href="#${p.name}" class="jumper", data-rdiv="#${p.name}" id="${p.name}_link">${p.title}</a>
%endfor

%for p in plugins:
    <div id="${p.name}">
        <h2> ${p.title} <a href="aboutplugin/${p.name}" class="about_link">(?)</a></h2>
        <div id="${p.name}_explanation"></div>
        <div id="${p.name}_result" class="plugin_result">
            Loading...
        </div>
    </div>
    <br>

%endfor

<script>
function scrollTo(selector) {
    var targetOffset = $(selector).offset().top;
    $('html,body').animate({scrollTop: targetOffset}, 500);
}

$(function(){
    //$('a[rel*=facebox]').facebox();

    var q = "${arg}";
    var plugins = ${[p.name for p in plugins]};
    $(plugins).each(function(i){
        var p = plugins[i];
        $.get("/info/html/" + p + "/" + q, function(data){
            if (data!=""){
                $("#" + p + "_result").html(data);
            } else {
                $("#" + p).hide("slow");
                $("#" + p + "_link").hide();
            }
            //$('a[rel*=facebox]').unbind('click');
            //$('a[rel*=facebox]').facebox();
        }).error(function(){
            $("#" + p + "_result").html("Error :-(");
        });
    });

    $(".jumper").click(function(){
        var d = $(this).data("rdiv");
        scrollTo(d);
        $(d).effect("highlight", {}, 2000);
        return false;
    });
});
</script>
%endif
</body>
