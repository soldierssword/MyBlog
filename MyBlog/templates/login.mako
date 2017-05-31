<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>管理员登录</title>
	<link rel="stylesheet" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
	<script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>
<div  style="width:800px; margin-left:auto; margin-right:auto; background-color:White; color:black; height:400px">
<form class="form-horizontal" role="form" action="${request.route_url('admin')}" method="post">
    % for error in form.username.errors:
        <div class="error">{{ error }}</div>
    % endfor
    <div class="form-group">
            <label for="title">${form.username.label}</label>
            ${form.username(class_='form-control')}
    </div>
    % for error in form.password.errors:
        <div class="error">{{ error }}</div>
    % endfor
    <div class="form-group">
            <label for="title">${form.password.label}</label>
            ${form.password(class_='form-control')}
    </div>
    <div class="form-group">
            <label></label>
            <button type="submit" class="btn btn-default">提交</button>
    </div>
</form>
</div>
</body>
</html>