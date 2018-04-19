from sqlalchemy.sql import or_,and_
from flask import render_template,request,url_for,redirect,session,flash,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user
from thinkdb import app,login_manager,db
from thinkdb.models import *
from thinkdb.forms import *
import datetime,random,time,asyncio
import json
# 数据库连接信息
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'thinkdb',
    'password': '123456',
    'db': 'fthinkdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    }
#Inception数据库连接配置
inception_config = {
    'host': '192.168.79.128',
    'port': 6669,
    'user': 'root',
    'password': '',
    'db': 'thinkdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    }
# 慢查询数据库连接信息
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'thinkdb',
    'password': '123456',
    'db': 'fthinkdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    }
##########################全局消息模块#################################
#全局消息
@login_required
def get_message(username):
    messages = Messages.query.filter_by(recipient=username).order_by(Messages.add_time.desc()).all()
    first_10 = Messages.query.filter_by(recipient=username).order_by(Messages.add_time.desc()).limit(5)
    unread_count = Messages.query.filter(and_(Messages.recipient == username, Messages.is_read == 0)).count()
    total = Messages.query.filter_by(recipient=username).count()
    return (first_10,messages,unread_count,total)
#消息中心
@login_required
@app.route('/messages/')
def messages_center():
    username = current_user.username
    href_name = "消息列表"
    sub_title = "查看所有消息"
    single_message = Messages.query.filter_by(recipient=username).all()
    return render_template('message.html', username=username, myuserid=current_user.id, single_message=single_message,href_name=href_name, sub_title=sub_title, messages=get_message(current_user.username))


#查看消息
@login_required
@app.route('/messages/<messages_id>')
def view_message(messages_id):
    username = current_user.username
    href_name = "单条消息"
    sub_title = "查看所有消息"
    single_message = Messages.query.filter_by(id=messages_id).first()
    single_message.is_read = 1
    db.session.commit()
    return render_template('message.html', username=username, myuserid=current_user.id, single_message=single_message,href_name=href_name, sub_title=sub_title, messages=get_message(current_user.username))
#删除消息
@login_required
@app.route('/delmessage/<messages_id>/')
def delmessage(messages_id):
    single_message = Messages.query.filter_by(id=messages_id).first()
    if single_message is not None:
        db.session.delete(single_message)
        db.session.commit()
        return redirect(url_for('messages_center'))
    else:
        return redirect(url_for('messages_center'))


#User Login Auth
@app.route('/')
def index():
    if not current_user.is_anonymous:
        if request.method == 'GET':
            #return render_template('index.html',username=current_user.username,myuserid=current_user.id, messages=get_message(current_user.username))
            return redirect(url_for('dbcenter'))
    return redirect(url_for('login'))

@app.route('/login/',methods=['GET','POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user is None:
            flash("用户不存在.")
            return render_template('login.html', form=loginform)
        elif user is not None and user.password == loginform.password.data:
            if user.status != "正常":
                flash("用户已过期或被锁定，请联系管理员")
                return render_template('login.html', form=loginform)
            else:
                login_user(user,True)
            return redirect(request.args.get('next') or url_for('index'))
        flash("密码错误.")
    return render_template('login.html',form=loginform)
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

#用户管理中心
@app.route('/usercenter/',methods=['GET','POST'])
@login_required
def usercenter():
    username = current_user.username
    if username:
        group_info = User_Group.query.all()
        user_info = User.query.all()
        return render_template('users.html',username=username,myuserid=current_user.id,group_info=group_info, user_info= user_info,messages=get_message(current_user.username))
    else:
        return redirect(url_for('login'))
#新增用户
@app.route('/newuser',methods=['GET','POST'])
@login_required
def newuser():
    username = current_user.username
    sub_title = "用户管理"
    href_name = "添加新用户"
    newuserform = ChangeUserForm()
    newuserform.group_id.choices = [(v.id, v.group_name) for v in User_Group.query.all()]
    if newuserform.validate_on_submit():
        newuserdata = User(username=newuserform.username.data,password=newuserform.password.data,group_id=newuserform.group_id.data,real_name=newuserform.real_name.data,email=newuserform.email.data,status=newuserform.status.data)
        if(User.query.filter_by(username=newuserform.username.data).first()):
            flash(u'用户名已存在')
            return render_template('user_info.html', username=username,myuserid=current_user.id, objForm=newuserform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
        else:
            if(User.query.filter_by(email=newuserform.email.data).first()):
                flash(u'邮件地址已被注册')
                return render_template('user_info.html', username=username,myuserid=current_user.id, objForm=newuserform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
            else:
                db.session.add(newuserdata)
                db.session.commit()
        return redirect(url_for('usercenter'))
    else:
        return render_template('user_info.html',username=username,myuserid=current_user.id,objForm=newuserform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
#删除用户
@app.route('/deluser/<user_id>',methods=['GET','POST'])
@login_required
def deluser(user_id):
    username = current_user.username
    if username:
        deluser= User.query.filter(User.id==user_id).first()
        db.session.delete(deluser)
        db.session.commit()
        group_info = User_Group.query.all()
        user_info = User.query.all()
        return render_template('users.html',username=username,myuserid=current_user.id,group_info=group_info, user_info= user_info,messages=get_message(current_user.username))
    else:
        return redirect(url_for('login'))
#修改用户
@app.route('/changeuser/<user_id>',methods=['GET','POST'])
@login_required
def changeuser(user_id):
    username = current_user.username
    sub_title = "用户管理"
    href_name = "更改用户"
    changeuserform = ChangeUserForm()
    changeuserform.group_id.choices = [(v.id, v.group_name) for v in User_Group.query.all()]
    if request.method == "GET":
        olddata = User.query.filter_by(id=user_id).first()
        changeuserform.username.data = olddata.username
        changeuserform.real_name.data = olddata.real_name
        changeuserform.password.data = olddata.password
        changeuserform.email.data = olddata.email
        changeuserform.status.data = olddata.status
        changeuserform.group_id.data = olddata.group_id
        return render_template('user_info.html', objForm=changeuserform, username=username,myuserid=current_user.id,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
    elif changeuserform.validate_on_submit():
        changeduser = User.query.filter_by(id=user_id).first()
        changeduser.password = changeuserform.password.data
        changeduser.email = changeuserform.email.data
        changeduser.real_name = changeuserform.real_name.data
        changeduser.status = changeuserform.status.data
        changeduser.group_id = changeuserform.group_id.data
        db.session.commit()
        return redirect(url_for('usercenter'))
    else:
        return render_template('user_info.html', objForm=changeuserform, username=username,myuserid=current_user.id,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))

#用户组管理

#新增用户组
@app.route('/newusergroup/',methods=['GET','POST'])
@login_required
def newusergroup():
    sub_title = "用户管理"
    href_name = "添加用户组"
    username = current_user.username
    newform = UserGroupForm()
    if newform.validate_on_submit():
        newuserdata = User_Group(group_name=newform.group_name.data,introduction=newform.introduction.data)
        if(User_Group.query.filter_by(group_name=newform.group_name.data).first()):
            flash(u'用户组已存在')
            return render_template('user_info.html', username=username,myuserid=current_user.id, objForm=newform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
        else:
            db.session.add(newuserdata)
            db.session.commit()
        return redirect(url_for('usercenter'))
    else:
        return render_template('user_info.html',username=username,myuserid=current_user.id,objForm=newform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
#删除用户组
@app.route('/delusergroup/<group_id>',methods=['GET','POST'])
@login_required
def delusergroup(group_id):
    username = current_user.username
    if username:
        delusergroup= User_Group.query.filter(User_Group.id==group_id).first()
        db.session.delete(delusergroup)
        db.session.commit()
        group_info = User_Group.query.all()
        user_info = User.query.all()
        return render_template('users.html',username=username,myuserid=current_user.id,group_info=group_info, user_info= user_info,messages=get_message(current_user.username))
    else:
        return redirect(url_for('login'))
#修改用户组
@app.route('/changeusergroup/<group_id>',methods=['GET','POST'])
@login_required
def changeusergroup(group_id):
    username = current_user.username
    sub_title = "用户管理"
    href_name = "更改用户组"
    changeuserform = UserGroupForm()
    if request.method == "GET":
        olddata = User_Group.query.filter_by(id=group_id).first()
        changeuserform.group_name.data = olddata.group_name
        changeuserform.introduction.data = olddata.introduction
        return render_template('user_info.html', objForm=changeuserform, username=username,myuserid=current_user.id,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
    elif changeuserform.validate_on_submit():
        changeduser = User_Group.query.filter_by(id=group_id).first()
        changeduser.group_name = changeuserform.group_name.data
        changeduser.introduction = changeuserform.introduction.data
        db.session.commit()
        return redirect(url_for('usercenter'))
    else:
        return render_template('user_info.html', objForm=changeuserform, username=username,myuserid=current_user.id,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))

#数据库管理中心
@app.route('/dbcenter/',methods=['GET','POST'])
@login_required
def dbcenter():
    username = current_user.username
    sub_title = "数据库管理"
    href_name = "数据库管理中心"
    if username:
        db_type = Data_Center.query.all()
        databases_info = db.session.query(MySQL_Databases.id,MySQL_Databases.name,Data_Center.name.label('datacenter_name'),Db_Cluster.name.label('cluster_name'),MySQL_Databases.ip,MySQL_Databases.port,MySQL_Databases.version,MySQL_Databases.is_master,MySQL_Databases.is_slave,MySQL_Databases.status,MySQL_Databases.add_time,MySQL_Replication.master_host).outerjoin(MySQL_Replication,MySQL_Databases.name==MySQL_Replication.db_name)\
            .outerjoin(Data_Center).outerjoin(Db_Cluster).all()
        cluster_info = Db_Cluster.query.all()
        return render_template('databases.html',username=username,myuserid=current_user.id,group_info=db_type,cluster_info=cluster_info,database_info=databases_info,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
    else:
        return redirect(url_for('login'))


#新增数据中心
@app.route('/newdbtype/',methods=['GET','POST'])
@login_required
def newdbtype():
    sub_title = "数据库管理"
    href_name = "添加数据中心"
    username = current_user.username
    newform = DataCenterForm()
    if newform.validate_on_submit():
        newdata = Data_Center(name=newform.name.data,introduction=newform.introduction.data)
        if(Data_Center.query.filter_by(name=newform.name.data).first()):
            flash(u'数据库中心已存在')
            return render_template('db_type.html', username=username,myuserid=current_user.id, objForm=newform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
        else:
            db.session.add(newdata)
            db.session.commit()
        return redirect(url_for('dbcenter'))
    else:
        return render_template('db_type.html',username=username,myuserid=current_user.id,objForm=newform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
#删除数据库分组
@app.route('/deldbgroup/<type_id>',methods=['GET','POST'])
@login_required
def deldbtype(type_id):
    username = current_user.username
    if username:
        delusergroup= Data_Center.query.filter(Data_Center.id==type_id).first()
        db.session.delete(delusergroup)
        db.session.commit()
        return redirect(url_for('dbcenter'))
    else:
        return redirect(url_for('login'))
#修改数据库分组
@app.route('/changedbgroup/<type_id>',methods=['GET','POST'])
@login_required
def changedbtype(type_id):
    username = current_user.username
    sub_title = "数据库管理"
    href_name = "修改数据中心"
    newform = DataCenterForm()
    if request.method == "GET":
        olddata = Data_Center.query.filter_by(id=type_id).first()
        newform.name.data = olddata.name
        newform.introduction.data = olddata.introduction
        return render_template('db_type.html', objForm=newform, username=username,myuserid=current_user.id,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
    elif newform.validate_on_submit():
        newdata = Data_Center.query.filter_by(id=type_id).first()
        newdata.name = newform.name.data
        newdata.introduction = newform.introduction.data
        db.session.commit()
        return redirect(url_for('dbcenter'))
    else:
        return render_template('db_type.html', objForm=newform, username=username,myuserid=current_user.id,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
###################数据库集群信息###############################
#新增数据库集群
@app.route('/newdbcluster/',methods=['GET','POST'])
@login_required
def newdbcluster():
    sub_title = "数据库管理"
    href_name = "添加数据库集群"
    username = current_user.username
    newform = DbClusterForm()
    if request.method == "GET":
        return render_template('db_type.html', username=username,myuserid=current_user.id, objForm=newform, href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
    elif newform.validate_on_submit():
        newdata = Db_Cluster(name=newform.name.data,introduction=newform.introduction.data,status=newform.status.data,applicant=newform.applicant.data)
        if(Data_Center.query.filter_by(name=newform.name.data).first()):
            flash(u'数据库集群已存在')
            return render_template('db_type.html', username=username,myuserid=current_user.id, objForm=newform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
        else:
            db.session.add(newdata)
            db.session.commit()
        return redirect(url_for('dbcenter'))
    else:
        return render_template('db_type.html',username=username,myuserid=current_user.id,objForm=newform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
#删除数据库集群
@app.route('/deldbcluster/<cluster_id>',methods=['GET','POST'])
@login_required
def deldbcluster(cluster_id):
    username = current_user.username
    sub_title = "数据库管理"
    if username:
        deldbcluster= Db_Cluster.query.filter(Db_Cluster.id==cluster_id).first()
        db.session.delete(deldbcluster)
        db.session.commit()
        db_type = Data_Center.query.all()
        cluster_info = Db_Cluster.query.all()
        databases_info = MySQL_Databases.query.all()
        return redirect(url_for('dbcenter'))
    else:
        return redirect(url_for('login'))
#修改数据库集群
@app.route('/changedbcluster/<cluster_id>',methods=['GET','POST'])
@login_required
def changedbcluster(cluster_id):
    username = current_user.username
    sub_title = "数据库管理"
    href_name = "修改数据库集群"
    newform = DbClusterForm()
    if request.method == "GET":
        olddata = Db_Cluster.query.filter_by(id=cluster_id).first()
        newform.name.data = olddata.name
        newform.applicant.data = olddata.applicant
        newform.status.data = olddata.status
        newform.introduction.data = olddata.introduction
        return render_template('db_type.html', objForm=newform, username=username,myuserid=current_user.id,href_name=href_name,sub_title=sub_title)
    elif newform.validate_on_submit():
        newdata = Db_Cluster.query.filter_by(id=cluster_id).first()
        newdata.name = newform.name.data
        newdata.applicant = newform.applicant.data
        newdata.status = newform.status.data
        newdata.introduction = newform.introduction.data
        db.session.commit()
        return redirect(url_for('dbcenter'))
    else:
        return render_template('db_type.html', objForm=newform, username=username,myuserid=current_user.id,href_name=href_name,sub_title=sub_title)
###################数据库信息###############################
#新增数据库
@app.route('/newdb/',methods=['GET','POST'])
@login_required
def newdb():
    sub_title = "数据库管理"
    href_name = "添加MySQL实例"
    username = current_user.username
    newform = DbForm()
    newform.datacenter_id.choices = [(v.id, v.name) for v in Data_Center.query.all()]
    newform.cluster_id.choices = [(v.id, v.name) for v in Db_Cluster.query.all()]
    if newform.validate_on_submit():
        newdata = MySQL_Databases(cluster_id=newform.cluster_id.data, name=newform.name.data,
                                  introduction=newform.introduction.data,
                                  applicant=newform.applicant.data,
                                  datacenter_id=newform.datacenter_id.data, version=newform.version.data,
                                  ip=newform.ip.data,
                                  port=newform.port.data)
        if(MySQL_Databases.query.filter_by(name=newform.name.data).first()):
            flash(u'数据库名称已存在')
            return render_template('db_type.html', username=username,myuserid=current_user.id, objForm=newform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
        db.session.add(newdata)
        db.session.commit()
        return redirect(url_for('dbcenter'))
    else:
        return render_template('db_type.html',username=username,myuserid=current_user.id,objForm=newform,href_name=href_name,sub_title=sub_title,messages=get_message(current_user.username))
#修改数据库
@app.route('/changedb/<db_id>',methods=['GET','POST'])
@login_required
def changedb(db_id):
    username = current_user.username
    sub_title = "数据库管理"
    href_name = "修改MySQL实例"
    newform = DbForm()
    newform.datacenter_id.choices = [(v.id, v.name) for v in Data_Center.query.all()]
    newform.cluster_id.choices = [(v.id, v.name) for v in Db_Cluster.query.all()]
    if request.method == "GET":
        olddata = MySQL_Databases.query.filter_by(id=db_id).first()
        newform.name.data = olddata.name
        newform.datacenter_id.data = olddata.datacenter_id
        newform.cluster_id.data = olddata.cluster_id
        newform.version.data = olddata.version
        newform.ip.data = olddata.ip
        newform.port.data = olddata.port
        newform.applicant.data = olddata.applicant
        newform.introduction.data = olddata.introduction
        return render_template('db_type.html', objForm=newform, username=username,myuserid=current_user.id,href_name=href_name,sub_title=sub_title, messages=get_message(current_user.username))
    elif (MySQL_Databases.query.filter(and_(MySQL_Databases.name==newform.name.data,MySQL_Databases.id != int(db_id))).first()):
        flash(u'数据库名称已存在')
        return render_template('db_type.html', objForm=newform, username=username,myuserid=current_user.id, href_name=href_name,sub_title=sub_title, messages=get_message(current_user.username))
    elif newform.validate_on_submit():
        olddata = MySQL_Databases.query.filter_by(id=db_id).first()
        olddata.cluster_id=newform.cluster_id.data
        olddata.name=newform.name.data
        olddata.introduction=newform.introduction.data
        olddata.applicant=newform.applicant.data
        olddata.datacenter_id=newform.datacenter_id.data
        olddata.version=newform.version.data
        olddata.ip=newform.ip.data
        olddata.port=newform.port.data
        if ((newform.is_master.data == "alone" and newform.master_id.data != -2)):
            flash(u'主库ID不正确，非主从的独立主机请填写：-2')
            return render_template('db_type.html', username=username,myuserid=current_user.id, objForm=newform, href_name=href_name,sub_title=sub_title, messages=get_message(current_user.username))
        elif (newform.is_master.data == "slave"):
            if((newform.master_id.data == int(db_id) or (newform.master_id.data != db_id and (not MySQL_Databases.query.filter_by(id=newform.master_id.data).first())))):
                flash(u'主库ID不正确，请填写实际主库对应的ID')
                print(newform.data)
                return render_template('db_type.html', username=username,myuserid=current_user.id, objForm=newform, href_name=href_name,sub_title=sub_title, messages=get_message(current_user.username))
        elif (newform.is_master.data == "master"):
            if(newform.master_id.data == int(db_id) or ((newform.master_id.data != -1)  and not MySQL_Databases.query.filter_by(id=newform.master_id.data).first())):
                flash(u'主库ID不正确，非级联主库请填写：-1，级联主库：请填写对应主库的实际ID')
                return render_template('db_type.html', username=username,myuserid=current_user.id, objForm=newform, href_name=href_name,sub_title=sub_title, messages=get_message(current_user.username))
        db.session.commit()
        return redirect(url_for('dbcenter'))
    return render_template('db_type.html', username=username,myuserid=current_user.id, objForm=newform, href_name=href_name, sub_title=sub_title, messages=get_message(current_user.username))
#删除数据库集群
@app.route('/deldb/<db_id>',methods=['GET','POST'])
@login_required
def deldb(cluster_id):
    username = current_user.username
    sub_title = "数据库管理"
    if username:
        deldbcluster= Db_Cluster.query.filter(Db_Cluster.id==cluster_id).first()
        db.session.delete(deldbcluster)
        db.session.commit()
        db_type = Data_Center.query.all()
        cluster_info = Db_Cluster.query.all()
        databases_info = MySQL_Databases.query.all()
        return redirect(url_for('dbcenter'))
    else:
        return redirect(url_for('login'))

#慢查询分析页面
#慢查询分析页面
@app.route('/slowquery/',methods=['GET','POST'])
@login_required
def slowquery():
    # 创建数据库连接
    username = current_user.username
    sub_title = "慢查询分析"
    href_name = "慢查询列表"
    slowsearchform = SlowSearchForm()
    if request.method == "GET":
        if request.args.get('start_time') is None or request.args.get('start_time')=='':
            start_time = (datetime.datetime.now() + datetime.timedelta(days=-3)).strftime("%Y-%m-%d")
            start_time = str(start_time) + " 00:00:00"
        else:
            start_time = datetime.datetime.strptime(request.args.get('start_time'),"%m/%d/%Y")
        if request.args.get('end_time') is None or request.args.get('end_time')=='':
            end_time = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%m:%S")
        else:
            end_time = datetime.datetime.strptime(request.args.get('end_time'),"%m/%d/%Y")
            #end_time = str(end_time) + " 23:59:59"
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        # 执行sql语句，进行查询
        sql = 'select B.serverid_max,format(sum(B.Query_time_median)/count(*),2) as "avg",sum(ts_cnt) as "times",A.checksum, A.last_seen,B.db_max, B.user_max,format(min(B.query_time_min),2) as query_time_min,format(max(B.query_time_max),2) as "query_time_max",A.fingerprint,if(locate("|",B.sample),SUBSTRING_INDEX(SUBSTRING_INDEX(B.sample,"|*",-1),"*|",1),"")  as "sample"  FROM mysql_slow_query_review A JOIN  mysql_slow_query_review_history B ON A.checksum = B.checksum WHERE  1 AND A.last_seen BETWEEN %s AND %s GROUP BY A.checksum'
        cursor.execute(sql,(start_time, end_time))
        # 获取查询结果
        slowquery = cursor.fetchall()
        # 最慢的10条语句，进行查询
        top10slowest_sql = 'select B.serverid_max, format(sum(B.Query_time_median)/count(*),2) as "avg",sum(ts_cnt) as "times",A.checksum, A.last_seen,B.db_max, B.user_max,format(min(B.query_time_min),2) as query_time_min,format(max(B.query_time_max),2) as "query_time_max",A.fingerprint,SUBSTRING_INDEX(SUBSTRING_INDEX(B.sample,"|*",-1),"*|",1) as "sample"  FROM mysql_slow_query_review A JOIN  mysql_slow_query_review_history B ON A.checksum = B.checksum WHERE  1 AND A.last_seen BETWEEN %s AND %s GROUP BY A.checksum  ORDER BY sum(B.Query_time_median)/count(*) desc limit 10'
        cursor.execute(top10slowest_sql, (start_time, end_time))
        # 获取最慢10条查询结果
        top10slowest = cursor.fetchall()
        # 最频繁的10条语句，进行查询
        top10frequent_sql = 'select B.serverid_max, format(sum(B.Query_time_median)/count(*),2) as "avg",sum(ts_cnt) as "times",A.checksum, A.last_seen,B.db_max, B.user_max,format(min(B.query_time_min),2) as query_time_min,format(max(B.query_time_max),2) as "query_time_max",A.fingerprint,if(locate("|",B.sample),SUBSTRING_INDEX(SUBSTRING_INDEX(B.sample,"|*",-1),"*|",1),"")  as "sample"  FROM mysql_slow_query_review A JOIN  mysql_slow_query_review_history B ON A.checksum = B.checksum WHERE  1 AND A.last_seen BETWEEN %s AND %s GROUP BY A.checksum  ORDER BY times desc limit 10'
        cursor.execute(top10frequent_sql, (start_time, end_time))
        # 获取最慢10条查询结果
        top10frequent = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('slowquery.html', username=username,myuserid=current_user.id,slowquery=slowquery, href_name=href_name, sub_title=sub_title,messages=get_message(current_user.username),top10slowest=top10slowest,top10frequent=top10frequent,slowsearchform=slowsearchform)


#慢查询详情页面
@app.route('/slowdetails/<checksum>',methods=['GET','POST'])
@login_required
def slowdetails(checksum):
    # 创建数据库连接
    username = current_user.username
    sub_title = "慢查询列表"
    href_name = "慢查询详情"
    start_time = (datetime.datetime.now() + datetime.timedelta(days = -28)).strftime("%Y-%m-%d")
    end_time = (datetime.datetime.now()).strftime("%Y-%m-%d")
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    # 执行sql语句，进行查询
    sql = 'select A.*,B.*,sum(B.ts_cnt) as "ts_cnt" FROM mysql_slow_query_review A RIGHT JOIN  mysql_slow_query_review_history B ON A.checksum = B.checksum WHERE  1 AND A.last_seen BETWEEN %s AND %s  AND A.checksum = %s GROUP BY A.checksum'
    cursor.execute(sql,(start_time, end_time,checksum))
    # 获取查询结果
    slowquery = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('slowquery.html', username=username,myuserid=current_user.id,slowquery=slowquery, href_name=href_name, sub_title=sub_title,messages=get_message(current_user.username))

#######################################工单模块#########################################
#工单列表页面
@app.route('/tickets/',methods=['GET','POST'])
@login_required
def tickets():
    # 创建数据库连接
    username = current_user.username
    sub_title = "我的工单"
    href_name = "我的工单列表"
    tickets_list = Tickets.query.filter_by(applicant=username,is_delete = 0).order_by(Tickets.tickets_num.desc())
    return render_template('tickets.html', username=username,myuserid=current_user.id,tickets_list=tickets_list, href_name=href_name, sub_title=sub_title,messages=get_message(current_user.username))

#查看工单
@app.route('/ticketview/<tickets_id>/',methods=['GET','POST'])
@login_required
def ticketview(tickets_id):
    username = current_user.username
    sub_title = "查看工单"
    objForm=TicketsForm()
    tickets_data = Tickets.query.filter_by(id=tickets_id).first()
    href_name = "工单编号："+ str(tickets_data.tickets_num)
    #objForm = tickets_data
    if request.method == "GET":
        objForm.tickets_num.data = tickets_data.tickets_num
        objForm.applicant.data= tickets_data.applicant
        objForm.db_id.data = tickets_data._database.name
        objForm.auditor.data = tickets_data.auditor
        objForm.add_time.data = tickets_data.add_time
        objForm.sqlcontent.data = tickets_data.sqlcontent
        objForm.status.data = tickets_data.status
        objForm.audit_advise.data = tickets_data.audit_advise
        objForm.is_execute.data = tickets_data.is_execute
    #objForm.audit_advise = ''
        return render_template('tickets.html',username=username,myuserid=current_user.id,objForm=objForm, href_name=href_name, sub_title=sub_title,messages=get_message(current_user.username))
    else:
        objForm.tickets_num.data = tickets_data.tickets_num
        objForm.applicant.data = tickets_data.applicant
        objForm.db_id.data = tickets_data._database.name #用外键转化为dbname
        objForm.auditor.data = tickets_data.auditor
        objForm.add_time.data = tickets_data.add_time
        objForm.sqlcontent.data = tickets_data.sqlcontent
        objForm.status.data = tickets_data.status
        objForm.is_execute.data = tickets_data.is_execute
        #定义执行动作格式
        # 执行还是校验
        operation_check = '--enable-check;'
        operation_execute = '--enable-execute;--enable-ignore-warnings;--enable-force;'
        #拼装目标数据库信息
        target_db = MySQL_Databases.query.filter_by(id=tickets_data.db_id).first()
        sql_format_start1 = "/*--user=%s;--password=%s;--host=%s;--port=%d;" % (target_db.user,target_db.password,target_db.ip,target_db.port)
        sql_format_start2 = "*/\ninception_magic_start;"
        sql_format_end = "inception_magic_commit;"
        if ('check' in request.form.values()):
            # 拼接sQL语句
            sql_content = objForm.sqlcontent.data
            sql = sql_format_start1 + operation_check + sql_format_start2 + "\n" + sql_content + "\n" + sql_format_end
            try:
                connection = pymysql.connect(**inception_config)
                cur = connection.cursor()
                cur.execute(sql)
                result = cur.fetchall()
                num_fields = len(cur.description)
                field_names = [i[0] for i in cur.description]
                # 打印出来Inception对MySQL语句的审计结果
                for row in result:
                    print(row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|", row[5], "|", row[6], "|",row[7], "|", row[8], "|", row[9], "|", row[10])
                cur.close()
                connection.close()
            except Exception as err:
                return render_template('tickets.html', username=username,myuserid=current_user.id,objForm=objForm, href_name=href_name,sub_title=sub_title, result=result,messages=get_message(current_user.username))
        elif ('pass' in request.form.values()):
            sql_content = tickets_data.sqlcontent
            sql = sql_format_start1 + operation_check + sql_format_start2 + "\n" + sql_content + "\n" + sql_format_end
            try:
                connection = pymysql.connect(**inception_config)
                cur = connection.cursor()
                cur.execute(sql)
                result = cur.fetchall()
                num_fields = len(cur.description)
                field_names = [i[0] for i in cur.description]
                # 打印出来Inception对MySQL语句的审计结果
                for row in result:
                    print(row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|", row[5], "|", row[6], "|",row[7], "|", row[8], "|", row[9], "|", row[10])
                cur.close()
                connection.close()
            except Exception as err:
                count = 0
                for i in result:
                    if (i['errormessage']) != "None":
                        count = count + 1
                if count > 0:
                    return render_template('tickets.html', username=username, myuserid=current_user.id, objForm=objForm,href_name=href_name, sub_title=sub_title, result=result,messages=get_message(current_user.username))

            olddata = Tickets.query.filter_by(id=tickets_id).first()
            olddata.status = "通过"
            olddata.audit_advise = current_user.username + " < " + datetime.datetime.now().strftime("%Y-%m-%d %H:%S") + " > 通过。\n" + objForm.audit_advise.data
            db.session.commit()
            message_title = "工单<" + str(olddata.tickets_num) + ">通过审核"
            message_content = "Dear " + olddata.applicant + ":\n您在 <" + str(olddata.add_time) + "> 提交的工单:<" + str(olddata.tickets_num) + ">已通过审核！"
            messages = Messages(recipient=olddata.applicant, sender=username, title=message_title,content=message_content,add_time=datetime.datetime.now())
            db.session.add(messages)
            db.session.commit()
            return redirect(url_for('ticketview', tickets_id=tickets_id))
        if objForm.validate_on_submit():
            if ('reject' in request.form.values()):
                olddata = Tickets.query.filter_by(id=tickets_id).first()
                olddata.status = "拒绝"
                olddata.audit_advise = current_user.username + " < "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%S") +" > 拒绝。\n" + objForm.audit_advise.data
                db.session.commit()
                message_title = "工单<" + str(olddata.tickets_num) + ">被拒！"
                message_content = "Dear " + olddata.applicant + ":\n    < "+username+" >拒绝了您在 <" + str(olddata.add_time) + "> 提交的工单:<" + str(olddata.tickets_num) + ">！，具体原因请在我的工单出查看!"
                messages = Messages(recipient=olddata.applicant, sender=username, title=message_title,content=message_content,add_time=datetime.datetime.now())
                db.session.add(messages)
                db.session.commit()
                return redirect(url_for('tickets'))
                #return render_template('tickets.html', username=username, objForm=objForm, href_name=href_name,sub_title=sub_title, result=result)
            elif ('execute' in request.form.values() and tickets_data.is_execute == 0):
                sql_content = tickets_data.sqlcontent
                sql = sql_format_start1 + operation_execute + sql_format_start2 + "\n" + sql_content + "\n" + sql_format_end
                try:
                    connection = pymysql.connect(**inception_config)
                    cur = connection.cursor()
                    cur.execute(sql)
                    result = cur.fetchall()
                    num_fields = len(cur.description)
                    field_names = [i[0] for i in cur.description]
                    # 打印出来Inception对MySQL语句的审计结果
                    for row in result:
                        print(row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|", row[5], "|", row[6], "|",row[7], "|", row[8], "|", row[9], "|", row[10])
                    cur.close()
                    connection.close()
                except Exception as err:
                    count = 0
                    for i in result:
                        if (i['errormessage']) != "None":
                            count = count + 1
                    if count >0:
                        return render_template('tickets.html', username=username,myuserid=current_user.id,objForm=objForm, href_name=href_name,sub_title=sub_title, result=result,messages=get_message(current_user.username))
                olddata = Tickets.query.filter_by(id=tickets_id).first()
                olddata.status = "通过"
                olddata.is_execute = 1
                olddata.audit_advise = current_user.username + " < "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%S") +" > 执行。\n" + objForm.audit_advise.data
                db.session.commit()
                message_title = "工单<" + str(olddata.tickets_num) + ">已执行!"
                message_content = "Dear " + olddata.applicant + ":\n  <"+username+" >执行了您在 <" + str(olddata.add_time) + "> 提交的工单:<" + str(olddata.tickets_num) + ">！"
                messages = Messages(recipient=olddata.applicant, sender=username, title=message_title,content=message_content,add_time=datetime.datetime.now())
                db.session.add(messages)
                db.session.commit()
                return redirect(url_for('ticketview', tickets_id=tickets_id))
        else:
            return  render_template('tickets.html',username=username,myuserid=current_user.id,objForm=objForm, href_name=href_name, sub_title=sub_title,messages=get_message(current_user.username))
    return redirect(url_for('tickets'))

#删除工单
@app.route('/deltickets/<tickets_id>')
@login_required
def deltickets(tickets_id):
    username = current_user.username
    sub_title = "查看工单"
    ticket = Tickets.query.filter_by(id=tickets_id).first()
    if ticket is not None:
        ticket.is_delete = 1
        db.session.commit()
        message_title = "工单<"+str(ticket.tickets_num)+">被删除"
        message_content = "Dear " +username + ":您在 <"+str(ticket.add_time)+"> 提交的工单:<" + str(ticket.tickets_num) + ">已被DBA删除！如需再次查看具体内容，请联系DBA！"
        messages = Messages(recipient=ticket.applicant, sender=username, title=message_title,content=message_content,add_time=datetime.datetime.now())
        db.session.add(messages)
        db.session.commit()
    return redirect(url_for('tickets'))
#DDL变更页面
@app.route('/ddl/',methods=['GET','POST'])
@login_required
def ddl():
    # 初始化表单
    username = current_user.username
    sub_title = "工单系统"
    href_name = "表结构变更"
    objForm = TargetDbForm()
    objForm.db_id.choices = [(v.id, v.name) for v in MySQL_Databases.query.all()]
    if objForm.validate_on_submit():
        # 192.168.79.128
        # 执行还是校验
        # 查找所选目标数据库信息
        target_db = MySQL_Databases.query.filter_by(id=objForm.db_id.data).first()
        operation_check = '--enable-check;'
        operation_execute = '--enable-execute;--enable-ignore-warnings;--enable-force;'
        sql_format_start1 = "/*--user=%s;--password=%s;--host=%s;--port=%d;" % (
        target_db.user, target_db.password, target_db.ip, target_db.port)
        sql_format_start2 = "*/\ninception_magic_start;"
        sql_format_end = "inception_magic_commit;"
        if ('check' in request.form.values()):
            sql_content = request.form['sqlarea']
            sql = sql_format_start1 + operation_check + sql_format_start2 + "\n" + sql_content + "\n" + sql_format_end
            try:
                connection = pymysql.connect(**inception_config)
                cur = connection.cursor()
                cur.execute(sql)
                result = cur.fetchall()
                num_fields = len(cur.description)
                field_names = [i[0] for i in cur.description]
                # 打印出来Inception对MySQL语句的审计结果
                for row in result:
                    print(row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|", row[5], "|", row[6], "|",row[7], "|", row[8], "|", row[9], "|", row[10])
                cur.close()
                connection.close()
            except Exception as err:
                return render_template('dml.html', username=username, myuserid=current_user.id, objForm=objForm,href_name=href_name, sub_title=sub_title, result=result,messages=get_message(current_user.username))
        elif ('submit' in request.form.values()):
            # 获取DBA团队用户名
            users = User.query.filter_by(group_id=1).all()
            # 生成工单号
            tickets_num = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + str(random.randint(100, 999))
            auditor = "test01"  # 后期需要判断，直接反馈给上级或者DBA团队
            add_time = datetime.datetime.now()
            sqlcontent = request.form['sqlarea']
            introduction = request.form['ticket_introduction']
            db_id = request.form['db_id']
            status = "待审核"
            type = "DDL"
            tickets = Tickets(tickets_num=tickets_num, applicant=username, auditor=auditor, add_time=add_time,status=status, sqlcontent=sqlcontent, db_id=db_id,introduction=introduction,type=type)
            db.session.add(tickets)
            db.session.commit()
            # 写消息到数据库
            for u in users:
                messages = Messages(recipient=u.username, sender=username, title="DML工单：" + tickets_num,content=username + "   提交了新工单:" + tickets_num + " 需审核，请尽快处理！")
                db.session.add(messages)
            db.session.commit()
            messages = Messages(recipient=username, sender=username, title="提交新DML工单：" + tickets_num,content="Dear " + username + ":\n   您在<" + str(datetime.datetime.now()) + ">提交了新工单:" + tickets_num + "。 请在我们的工单查看工单进度")
            db.session.commit()
            return redirect('/tickets/')
    return render_template('dml.html', username=username, myuserid=current_user.id, objForm=objForm,href_name=href_name, sub_title=sub_title,messages=get_message(current_user.username))

#DML提交页面
@app.route('/dml/',methods=['GET','POST'])
@login_required
def dml():
    #初始化表单
    username = current_user.username
    sub_title = "工单系统"
    href_name = "仅限于DML语句(增删改查)"
    objForm = TargetDbForm()
    objForm.db_id.choices = [(v.id, v.name) for v in MySQL_Databases.query.all()]
    if objForm.validate_on_submit():
        #192.168.79.128
        # 执行还是校验
        #查找所选目标数据库信息
        target_db = MySQL_Databases.query.filter_by(id=objForm.db_id.data).first()
        operation_check = '--enable-check;'
        operation_execute = '--enable-execute;--enable-ignore-warnings;--enable-force;--enable-remote-backup'
        sql_format_start1 = "/*--user=%s;--password=%s;--host=%s;--port=%d;" % (target_db.user,target_db.password,target_db.ip,target_db.port)
        sql_format_start2 = "*/\ninception_magic_start;"
        sql_format_end = "inception_magic_commit;"
        if ('check' in request.form.values()):
            sql_content = request.form['sqlarea']
            sql = sql_format_start1 + operation_check + sql_format_start2 + "\n" + sql_content + "\n" + sql_format_end
            try:
                connection = pymysql.connect(**inception_config)
                cur = connection.cursor()
                cur.execute(sql)
                result = cur.fetchall()
                num_fields = len(cur.description)
                field_names = [i[0] for i in cur.description]
                # 打印出来Inception对MySQL语句的审计结果
                for row in result:
                    print(row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|", row[5], "|", row[6], "|",row[7], "|",row[8], "|", row[9], "|", row[10])
                cur.close()
                connection.close()
            except Exception as err:
                return render_template('dml.html', username=username,myuserid=current_user.id, objForm=objForm, href_name=href_name,sub_title=sub_title, result=result,messages=get_message(current_user.username))
        elif('submit' in request.form.values()):
            # 获取DBA团队用户名
            users = User.query.filter_by(group_id=1).all()
            #生成工单号
            tickets_num = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))+str(random.randint(100,999))
            auditor = "test01"  #后期需要判断，直接反馈给上级或者DBA团队
            add_time = datetime.datetime.now()
            sqlcontent =  request.form['sqlarea']
            introduction = request.form['ticket_introduction']
            type = "DML"
            db_id = request.form['db_id']
            status = "待审核"
            tickets = Tickets(tickets_num=tickets_num,introduction=introduction,applicant=username,auditor=auditor,add_time=add_time,status=status,sqlcontent=sqlcontent,db_id=db_id,type=type)
            db.session.add(tickets)
            db.session.commit()
            #写消息到数据库
            for u in users:
                messages = Messages(recipient=u.username,sender=username,title="DML工单："+tickets_num,content=username + "   提交了新工单:"+tickets_num+" 需审核，请尽快处理！")
                db.session.add(messages)
            db.session.commit()
            messages = Messages(recipient=username, sender=username, title="提交新DML工单：" + tickets_num,content="Dear "+ username + ":\n   您在<"+str(datetime.datetime.now())+">提交了新工单:" + tickets_num + "。 请在我们的工单查看工单进度")
            db.session.commit()
            return redirect('/tickets/')
    return render_template('dml.html', username=username,myuserid=current_user.id, objForm=objForm, href_name=href_name, sub_title=sub_title,messages=get_message(current_user.username))




@app.route('/tables/')
def tables():
    return render_template('table.html',messages=get_message(current_user.username))

@app.route('/form/')
def form():
    return render_template('form.html',messages=get_message(current_user.username))

@app.route('/charts/')
def charts():
    return render_template('chart.html',messages=get_message(current_user.username))

@app.route('/typography/')
def typography():
    return render_template('typography.html',messages=get_message(current_user.username))


@app.route('/tasks/')
def tasks():
    return render_template('tasks.html',messages=get_message(current_user.username))


@app.route('/ui/')
def ui():
    return render_template('ui.html',messages=get_message(current_user.username))

@app.route('/widgets/')
def widgets():
    return render_template('widgets.html',messages=get_message(current_user.username))
@app.route('/calendar/')
def calendar():
    return render_template('calendar.html',messages=get_message(current_user.username))
@app.route('/file-manager/')
def filemanager():
    return render_template('file-manager.html',messages=get_message(current_user.username))
@app.route('/icons/')
def icons():
    return render_template('icon.html',messages=get_message(current_user.username))


async def fun(cluster_id):
    dbname = {}
    dbarry = []
    db = MySQL_Databases.query.filter_by(cluster_id=cluster_id).all()
    print("异步开始")
    for i in db:
        dbname['name'] = i.name
        dbarry.append(dbname)
    #await asyncio.sleep(2)
    print("guo le 10 miao")
    return 1
@app.route('/getdata/<cluster_id>')
def getdata(cluster_id):
    loop = asyncio.get_event_loop()
    print("begin")
    loop.run_until_complete(fun(cluster_id))
    loop.close()
    print("End")
    return 33