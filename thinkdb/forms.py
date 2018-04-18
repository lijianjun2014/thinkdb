from flask_wtf import Form,FlaskForm
from wtforms import StringField,BooleanField,PasswordField,IntegerField,RadioField,SelectField,ValidationError,TextField,DateTimeField,TextAreaField
from wtforms.validators import DataRequired,Email
from thinkdb.models import User,User_Group

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])

class ChangeUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "用户名"})
    password = StringField('Password',validators=[DataRequired(message="请输入密码")])
    group_id = SelectField('User_group',coerce=int,validators=[DataRequired()])
    real_name = StringField('RealName',validators=[DataRequired(message="请输入完整信息")])
    email = StringField('Email',validators=[Email(u'请输入正确的邮件信息')])
    status =  SelectField('Status',choices=[('正常','正常'),('过期','过期'),('锁定','锁定')],validators=[DataRequired()])

class NewUserForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()],render_kw={"placeholder": "用户名"})
    password = StringField('Password',validators=[DataRequired()],render_kw={"placeholder": "密码"})
    group_id = SelectField(coerce=int)
    real_name = StringField('RealName',validators=[DataRequired()])
    email = StringField('Email',validators=[Email()])
    status =  SelectField('Status',choices=[('normal','正常'),('expired','过期'),('hold','锁定')],validators=[DataRequired()])

#用户组表单
class UserGroupForm(FlaskForm):
    group_name = StringField('Username',validators=[DataRequired()],render_kw={"placeholder": "用户名称"})
    introduction = StringField('Introduction',validators=[DataRequired()],render_kw={"placeholder": "用户组说明"})
#数据中心表单
class DataCenterForm(FlaskForm):
    name = StringField('DbTypeName',validators=[DataRequired()],render_kw={"placeholder": "数据中心名称"})
    introduction = StringField('Introduction',validators=[DataRequired()],render_kw={"placeholder": "数据中心说明"})
#数据库集群表单
class DbClusterForm(FlaskForm):
    name = StringField('cluster tag',validators=[DataRequired()],render_kw={"placeholder": "集群名称(标识)"})
    introduction = StringField('Introduction',validators=[DataRequired()],render_kw={"placeholder": "集群说明"})
    status = SelectField("是否在线",choices=[("online","Online"),("down","Down")],validators=[DataRequired()],render_kw={"placeholder": "集群是否在线"})
    applicant = StringField("application_user",validators=[DataRequired()],render_kw={"placeholder": "申请人"})
#数据库表单
class DbForm(FlaskForm):
    name = StringField('name',validators=[DataRequired()],render_kw={"placeholder": "数据库名称(标识)"})
    datacenter_id = SelectField(coerce=int)
    cluster_id = SelectField(coerce=int)
    version = StringField('version',validators=[DataRequired()],render_kw={"placeholder":"软件版本"})
    ip = StringField('IP',validators=[DataRequired()],render_kw={"placeholder":"IP Address"})
    port = IntegerField('Port',validators=[DataRequired()],render_kw={"placeholder":"Port"})
    applicant = StringField("application_user",validators=[DataRequired()],render_kw={"placeholder": "数据库申请人"})
    introduction = StringField('Introduction',validators=[DataRequired()],render_kw={"placeholder": "数据库用途简介"})

#SQL and DDL目标数据库表单
class TargetDbForm(FlaskForm):
    #cluster_id = SelectField(coerce=int)
    db_id = SelectField(coerce=int)
    ticket_introduction = StringField('Tickets Introduction',validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"8个字内的工单说明"})
    sqlarea = TextAreaField('Text Erea',validators=[DataRequired()],render_kw={"class":"form-control","rows":"8","placeholder":"请输入你的SQL语句，多条语句用;分割"})

#Tickets FORM
class TicketsForm(FlaskForm):
    tickets_num = IntegerField('工单编号',validators=[DataRequired()])
    applicant = StringField('申请人',validators=[DataRequired()])
    auditor = StringField('审核人',validators=[DataRequired()])
    status = StringField('工单状态',validators=[DataRequired()])
    is_execute = IntegerField('是否执行过')
    sqlcontent = TextAreaField('待审核sql内容',validators=[DataRequired()],render_kw={"class":"form-control-self","rows":"8","placeholder":"请输入你的SQL语句，多条语句用;分割"})
    add_time = StringField('申请时间',validators=[DataRequired()])
    db_id = IntegerField('目标数据库ID',validators=[DataRequired()],render_kw={"placeholder":"目标数据库ID"})
    audit_advise = TextAreaField('审核意见',validators=[DataRequired()],render_kw={"class":"form-control","rows":"8","placeholder":"审核意见"})

#Slowquery Search FORM
class SlowSearchForm(FlaskForm):
    start_time = DateTimeField('开始时间')
    end_time = DateTimeField('结束时间')




