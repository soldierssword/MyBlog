<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>${entry.title}</title>
	<link rel="stylesheet" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
	<script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>
<div  style="width:800px; margin-left:auto; margin-right:auto; background-color:White; color:black; height:400px">
    <h1>${ entry.title }</h1>
    <p class="text-muted">修改时间:${entry.date}</p>
    <p class="text-primary">${entry.body}</p>
    <p><a href="${request.route_url('index')}"><button class="btn-default">返回</button></a></p>
</div>
</body>
</html>