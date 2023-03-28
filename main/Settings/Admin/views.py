from flask import Blueprint,request,jsonify
from main.utils import token_required,permission_required
from werkzeug.security import generate_password_hash
from main.Settings.Admin.models import CompanyInfo, UserRoleMapping, AppUser
from main.extensions import db

admin=Blueprint("admin",__name__,url_prefix="/admin")

@admin.route('/add-company-info',methods=['POST'])
def addCompanyInfo():
    try:
        data=request.get_json()
        entry=CompanyInfo(name=data.get('name'),
                          logo=data.get('logo'),
                          Address=data.get('Address'),
                          district=data.get('district'),
                          state=data.get('state'),
                          pincode=data.get('pincode'),
                          mobile_no=data.get('mobile_no'),
                          website=data.get('website'),
                          email=data.get('email'))
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            'id':entry.id,
            'name':entry.name,
            'logo':entry.logo,
            'Address':entry.Address,
            'district':entry.district,
            'state':entry.state,
            'pincode':entry.pincode,
            'mobile_no':entry.mobile_no,
            'website':entry.website,
            'email':entry.email
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@admin.route('/show-company-info/<int:id>')
def showCompanyInfo(id):
    try:
        entry=CompanyInfo.query.get(id)
        return jsonify({
            'id':entry.id,
            'name':entry.name,
            'logo':entry.logo,
            'Address':entry.Address,
            'district':entry.district,
            'state':entry.state,
            'pincode':entry.pincode,
            'mobile_no':entry.mobile_no,
            'website':entry.website,
            'email':entry.email
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@admin.route('/update-company-info/<int:id>',methods=['PUT'])
def updateAdmin(id):
    try:
        data=request.get_json()
        entry=CompanyInfo.query.get(id)
        entry.name=data.get('name')
        entry.logo=data.get('logo')
        entry.Address=data.get('Address')
        entry.district=data.get('district')
        entry.state=data.get('state')
        entry.pincode=data.get('pincode')
        entry.mobile_no=data.get('mobile_no')
        entry.website=data.get('website')
        entry.email=data.get('email')
        db.session.commit()
        return jsonify({'id':entry.id,
            'name':entry.name,
            'logo':entry.logo,
            'Address':entry.Address,
            'district':entry.district,
            'state':entry.state,
            'pincode':entry.pincode,
            'mobile_no':entry.mobile_no,
            'website':entry.website,
            'email':entry.email})
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@admin.route('/add-user',methods=['POST'])
def addUser():
    try:
        data=request.get_json()
        role_id=data.get('role_id')
        if not UserRoleMapping.query.get(role_id):
            return jsonify({"status": False, 
                         "data":"",
                         "msg": "role doesn't exist.", "error": ""}),201
        entry=AppUser(name=data.get('name'),
                      role_id=role_id,
                      user_name=data.get('user_name'),
                      image_path=data.get('image_path'),
                      encrypted_password=generate_password_hash(data.get('encrypted_password')),
                      email=data.get('email'),
                      mobile=data.get('mobile'))
        email_exist=AppUser.query.filter(AppUser.email==data.get('email')).count()
        user_exist=AppUser.query.filter(AppUser.user_name==data.get('user_name')).count()
        mobile_exist=AppUser.query.filter(AppUser.mobile==data.get('mobile')).count()
        if user_exist>0:
            return jsonify({
                "message":"user_name not available."
            })
        elif email_exist>0:
            return jsonify({
                "message":"email already exist."
            })
        elif mobile_exist>0:
            return jsonify({
                "message":"mobile number already exist."
            })
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "name":entry.name,
            "user_name":entry.user_name,
            "role_id":entry.role_id,
            "image_path":entry.image_path,
            "encrypted_password":entry.encrypted_password,
            "email":entry.email,
            "mobile":entry.mobile
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@admin.route('/update-user/<int:id>',methods=['PUT'])
@token_required
@permission_required('read_team')
def updateUser(id):
    try:
        data=request.get_json()
        entry=AppUser.query.get(id)
        if not entry:
            return jsonify({
                "message":"user not exist"
            })
        email_exist=AppUser.query.filter(AppUser.email==data.get('email')).count()
        user_exist=AppUser.query.filter(AppUser.user_name==data.get('user_name')).count()
        mobile_exist=AppUser.query.filter(AppUser.mobile==data.get('mobile')).count()
        uname=entry.user_name != data.get('user_name')
        email=entry.email !=data.get('email')
        mobile=entry.mobile != data.get('mobile')
        entry.name=data.get('name'),
        entry.role_id=data.get('role_id'),
        if not UserRoleMapping.query.get(data.get('role_id')):
            return jsonify({"status": False, 
                         "data":"",
                         "msg": "role doesn't exist.", "error": ""}),201
        entry.user_name=data.get('user_name'),
        entry.image_path=data.get('image_path'),
        entry.encrypted_password=generate_password_hash(data.get('encrypted_password')),
        entry.email=data.get('email'),
        entry.mobile=data.get('mobile')
        if uname and user_exist>0:
            return jsonify({
                "message":"user_name not available."
            })
        elif email and email_exist>0:
            return jsonify({
                "message":"email already exist."
            })
        elif mobile and mobile_exist>0:
            return jsonify({
                "message":"mobile number already exist."
            })
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "name":entry.name,
            "user_name":entry.user_name,
            "role_id":entry.role_id,
            "image_path":entry.image_path,
            "encrypted_password":entry.encrypted_password,
            "email":entry.email,
            "mobile":entry.mobile
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@admin.route('/show-users')
@token_required
@permission_required('admin')
def showUsers():
    try:
        users=AppUser.query.all()
        data=[]
        for entry in users:
            info={
                "id":entry.id,
                "name":entry.name,
                "user_name":entry.user_name,
                "role_id":entry.role_id,
                "image_path":entry.image_path,
                "encrypted_password":entry.encrypted_password,
                "email":entry.email,
                "mobile":entry.mobile
            }
            data.append(info)
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@admin.route('/add-user-permissions',methods=['POST'])
def addUserPermissions():
    try:
        data=request.get_json()
        role=data.get('role')
        access=data.get('access')
        role=UserRoleMapping(role=role,access=access)
        db.session.add(role)
        db.session.commit()
        return jsonify({"status": True, 
                        "role":{"id":role.id,
                                "role_id":role.role,
                                "access":role.access
                                },
                         "msg": "role added successfully", "error": ""}), 201
    except Exception as e:
        # error_log().error({"status": False, "data": "", "msg": "", "error": str(e)})
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500

@admin.route('/show-roles')    
def showUserPermissions():
    try:
        data=[]
        roles=UserRoleMapping.query.all()
        for role in roles:
            data.append({"id":role.id,"role":role.role,"access":role.access})
        return jsonify({"status": True, 
                        "data":data,
                         "msg": "role added successfully", "error": ""}), 201
    except Exception as e:
        # error_log().error({"status": False, "data": "", "msg": "", "error": str(e)})
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500

@admin.route('/update-role/<int:id>',methods=['PUT'])
def updateRole(id):
    try:
        data=request.get_json()
        role=UserRoleMapping.query.get(id)
        if not role:
            return jsonify({"status": False, 
                         "role":"",
                         "msg": "role doesn't exist", "error": ""}), 201    
        role.access=data.get('access')
        db.session.commit()
        return jsonify({"status": True, 
                        "role":{"id":role.id,
                                "role":role.role,
                                "access":role.access
                                },
                         "msg": "role updated successfully", "error": ""}), 201
    except Exception as e:
        # error_log().error({"status": False, "data": "", "msg": "", "error": str(e)})
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500
    
@admin.route('/delete-role/<int:id>',methods=['DELETE'])
def deleteRole(id):
    try:
        data=request.get_json()
        role=UserRoleMapping.query.get(id)
        if not role:
            return jsonify({"status": False, 
                         "role":"",
                         "msg": "role doesn't exist.", "error": ""}), 201    
        db.session.delete(role)
        db.session.commit()
        return jsonify({"status": True, 
                        "role":{"id":role.id,
                                "role":role.role,
                                "access":role.access
                                },
                         "msg": "role deleted successfully", "error": ""}), 201
    except Exception as e:
        # error_log().error({"status": False, "data": "", "msg": "", "error": str(e)})
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500
        
# from datetime import datetime
# @admin.route('/test')
# def test():
#     try:
#         dates=[]
#         x=datetime.now()
#         date=x.strftime("%Y-%m-%d")
#         w=int(x.strftime("%w"))
#         dates.append(date)
#         date_list=date.split('-')
#         day=int(date_list[2])
#         for i in range(1,w):
#             day-=1
#             date=f"{date_list[0]}-{date_list[1]}-{str(day)}"
#             dates.append(date) 
#         return jsonify({
#             "dates":dates
#         })
#     except :
#         return jsonify({"":""})