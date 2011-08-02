<%inherit file="base.mako"/>

%if nodes:
%for idx,node in enumerate(nodes):
<h2> ${ node } </h2>
<div class="host">

%for p in enabled_plugins:
    <h3> ${ p } </h3>
    <div id="${idx}_${p}_result" class="plugin_result">
    Loading...
    </div>
%endfor
</div>

%endfor
%endif

<p>
<form method="POST">
<b>Which plugins to run?</b> </br>
%for p in plugins:
<label>
%if p.name in enabled_plugins:
    <input type="checkbox" name="plugins" value="${p.name}" checked="checked">
%else:
    <input type="checkbox" name="plugins" value="${p.name}">
%endif
${ p.title }  </br>
</label>
%endfor
<button id="select_inside">Select inside plugins</button>
<button id="select_outside">Select outside plugins</button>
</br>
<label for="q"><b>Paste in any text containing IPs and MAC Addresses:</b> </label><br/>
<textarea name="q" rows="10" cols="80">${q}</textarea> <br>
<input id="find" name="find" type="submit" value="find">
</form>
</p>

<script>
selectonly = function(boxes)
{
    $("input[name=plugins]").each(function(){
        this.checked = boxes.indexOf(this.value) !=-1;
    })
    return false;
}
$(function(){
    $("#select_outside").click(function(){
        var outside = ['cymruwhois', 'geoip','ipblocker','passivedns','whois', 'cif','siteadvisor'];
        return selectonly(outside);
    });
    $("#select_inside").click(function(){
        var inside = ['djf','netreg','pinginventory','radius','snort','uanet'];
        return selectonly(inside);
    });
%if nodes:

    var nodes = ${nodes_js | n};
    var plugins = ${plugins_js | n};
    $(nodes).each(function(nx,n){
        $(plugins).each(function(px, p){
            var elem = "#" + nx + "_" + p + "_result"
            $.get("/info/html/" + p + "/" + n, function(data){
                $(elem).html(data);
            });
        });
    });

%endif
})
</script>
