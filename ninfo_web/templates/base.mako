<!DOCTYPE html>
<html>
<head>
<style type="text/css">
h1 a{
    text-decoration: none;
}
legend {
    color: #2C4762;
    font-weight: bold;
    border: 1px solid #2C4762;
}
input {
    border: 2px solid #2C4762;
    padding: 2px;
}
input:focus {
    border: 2px solid green;
}
input[type=submit]:hover {
    background: #2C4762;
    color: #f0f4f8;
}

body {
    background: #2C4762;
}

#content {
    width: 700px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 20px;
    background: #f0f4f8;
    padding: 20px;
}


h1, h2, h3 {
    color: #2C4762;
}
div.plugin_result {
    max-height: 400px;
    overflow: auto;
}
ul#nav li {
    list-style-type: none;
    display: inline;
}
.button {
    padding: 5px 10px;
    display: inline;
    background: #2C4762;
    border: none;
    color: #fff;
    cursor: pointer;
    font-weight: bold;
    border-radius: 5px;
    -moz-border-radius: 5px;
    -webkit-border-radius: 5px;
    text-decoration: none;
}
.button:hover {
    background: #fff;
    color: #2C4762;
}

</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>
<title>
nInfo
%if arg:
- ${arg}
%endif
</title>
</head>
<body>
<div id="content">

<h1> <a href="/">nInfo</a> </h1>

<ul id="nav">
<li> <a class="button" href="/">Single address</a> </li>
<li> <a class="button" href="/multiple">Multiple addreses</a> </li>
</ul>

${self.body()}

</div>
</body>
</html>
