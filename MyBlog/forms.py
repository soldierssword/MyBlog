#coding:utf-8
from wtforms import (
    Form,
    StringField,
    TextAreaField,
    validators,
    HiddenField,
    PasswordField
)
strip_filter=lambda x:x.strip() if x else None

class BlogCreateForm(Form):
    title=StringField(u'标题',[validators.Length(min=1, max=255)],filters=[strip_filter])
    body = TextAreaField(u'内容', [validators.Length(min=1)],filters=[strip_filter])


class BlogUpdateForm(BlogCreateForm):
    uid = HiddenField()

class LoginForm(Form):
    username = StringField (u'用户名',[validators.Length(min=1, max=255)],filters=[strip_filter])
    password = PasswordField(u'密码',[validators.Length(min=1, max=255)],filters=[strip_filter])

