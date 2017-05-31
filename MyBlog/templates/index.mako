<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>个人博客</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
	<script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>

<div class="container">
	<h2>文章列表</h2>
    %if userid:
        <h3>
            ${userid},欢迎回来
            <a href="${request.route_url('blog_action',action='create')}">
                <button class="btn btn-default" >
                    添加
                </button>
            </a>
            <a href='${request.route_url('admin')}?do=out'>
                <button class="btn btn-default" >
                    退出登录
                </button>
            </a>
        </h3>
    %endif
    %if not userid:
        <a href='${request.route_url('admin')}'>
                <button class="btn btn-default" >
                    管理员登录
                </button>
            </a>
    %endif
	<table class="table table-striped table-bordered table-hover table-condensed">
		<thead>
			<tr>
				<th>编号</th>
				<th>标题</th>
				<th>发表时间</th>
                % if userid:
                    <th>操作</th>
                % endif

			</tr>
		</thead>
		<tbody>

            % for row in rows:
                <tr>
				    <td>${row.uid}</td>
				    <td><a href="${request.route_url('blog_view')}?uid=${row.uid}">${row.title}</a></td>
				    <td>${row.date}</td>
                    %if userid:
                        <td>
                            <a href="${request.route_url('blog_action',action='delete')}?uid=${row.uid}"><button class="btn btn-danger">删除</button></a>
                            <a href="${request.route_url('blog_action',action='update')}?uid=${row.uid}"><button class="btn btn-warning">修改</button></a>
                        </td>
                    %endif
                </tr>
			% endfor

		</tbody>
	</table>
</div>

</body>
</html>