<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>编辑</title>
	<link rel="stylesheet" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
	<script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>
<div  style="width:800px; margin-left:auto; margin-right:auto; background-color:White; color:black; height:400px">
<form class="form-horizontal" role="form" action="${request.route_url('blog_action',action=action)}" method="post">
    % if action=='update':
        ${form.uid()}
    % endif

    % for error in form.title.errors:
        <div class="error">${error}</div>
    % endfor
    <div class="form-group">
            <label for="title">${form.title.label}</label>
            ${form.title(class_='form-control')}
    </div>
    % for error in form.body.errors:
        <div class="error">${error}</div>
    % endfor
    <div class="form-group">
            <label for="title">${form.body.label}</label>
            ${form.body(class_='form-control')}
    </div>
    <div class="form-group">
            <label></label>
            <button type="submit" class="btn btn-default">提交</button>
    </div>
</form>
</div>
</body>
</html>