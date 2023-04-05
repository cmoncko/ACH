from flask import Blueprint, request, jsonify
from main.utils import token_required, permission_required, loger
from werkzeug.security import generate_password_hash
from main.Settings.Admin.models import CompanyInfo, UserRoleMapping, AppUser
from main.extensions import db

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route('/add-company-info', methods=['POST'])
def addCompanyInfo():
    try:
        data = request.get_json()
        if not data.get('name'):
            loger("warning").warning("name must be entered")
            return ({"status": False, "data": "", "msg": "Name must be entered", "error": ""}), 200
        if not data.get('Address'):
            loger("warning").warning("Address must be entered")
            return ({"status": False, "data": "", "msg": "Address must be entered", "error": ""}), 200
        if not data.get('district'):
            loger("warning").warning("district must be entered")
            return ({"status": False, "data": "", "msg": "district must be entered", "error": ""}), 200
        if not data.get('state'):
            loger("warning").warning("state must be entered")
            return ({"status": False, "data": "", "msg": "state must be entered", "error": ""}), 200
        if not data.get('pincode'):
            loger("warning").warning("pincode must be entered")
            return ({"status": False, "data": "", "msg": "pincode must be entered", "error": ""}), 200
        if not data.get('mobile'):
            loger("warning").warning("mobile must be entered")
            return ({"status": False, "data": "", "msg": "mobile must be entered", "error": ""}), 200
        if not data.get('email'):
            loger("warning").warning("email must be entered")
            return ({"status": False, "data": "", "msg": "email must be entered", "error": ""}), 200
        entry = CompanyInfo(name=data.get('name'),
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
        data={'id': entry.id,
            'name': entry.name,
            'logo': entry.logo,
            'Address': entry.Address,
            'district': entry.district,
            'state': entry.state,
            'pincode': entry.pincode,
            'mobile_no': entry.mobile_no,
            'website': entry.website,
            'email': entry.email}
        loger("info").info("email must be entered")
        return jsonify({"status": True, "data": data, "msg": "company info added", "error": ""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500

@admin.route('/show-company-info/<int:id>')
def showCompanyInfo(id):
    try:
        entry = CompanyInfo.query.get(id)
        if not entry:
            loger("warning").warning("Company info not exist")
            return jsonify({"status": False, "data": "", "msg": "Company info not exist.", "error": ""}), 200
        data = {'id': entry.id,
                'name': entry.name,
                'logo': entry.logo,
                'Address': entry.Address,
                'district': entry.district,
                'state': entry.state,
                'pincode': entry.pincode,
                'mobile_no': entry.mobile_no,
                'website': entry.website,
                'email': entry.email}
        loger("info").info("company info viewed")
        return jsonify({"status": True,
                        "data": data,
                        "msg": "Company info updated.", "error": ""}), 200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


@admin.route('/update-company-info/<int:id>', methods=['PUT'])
def updateAdmin(id):
    try:
        data = request.get_json()
        entry = CompanyInfo.query.get(id)
        if not entry:
            loger("warning").warning("Company info not exist")
            return jsonify({"status": False, "data": "", "msg": "Company info not exist.", "error": ""}), 200
        entry.name = data.get('name')
        entry.logo = data.get('logo')
        entry.Address = data.get('Address')
        entry.district = data.get('district')
        entry.state = data.get('state')
        entry.pincode = data.get('pincode')
        entry.mobile_no = data.get('mobile_no')
        entry.website = data.get('website')
        entry.email = data.get('email')
        db.session.commit()
        data = {'id': entry.id,
                'name': entry.name,
                'logo': entry.logo,
                'Address': entry.Address,
                'district': entry.district,
                'state': entry.state,
                'pincode': entry.pincode,
                'mobile_no': entry.mobile_no,
                'website': entry.website,
                'email': entry.email}
        loger("info").info("company info updated")
        return jsonify({"status": True,
                        "data": data,
                        "msg": "Company info updated.", "error": ""}), 204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


@admin.route('/add-user', methods=['POST'])
def addUser():
    try:
        data = request.get_json()
        role_id = data.get('role_id')
        if not UserRoleMapping.query.get(role_id):
            loger("warning").warning("role doesn't exist.")
            return jsonify({"status": False,
                            "data": "",
                            "msg": "role doesn't exist.", "error": ""}), 200
        entry = AppUser(name=data.get('name'),
                        role_id=role_id,
                        user_name=data.get('user_name'),
                        image_path=data.get('image_path'),
                        encrypted_password=generate_password_hash(data.get('encrypted_password')),
                        email=data.get('email'),
                        mobile=data.get('mobile'))
        email_exist = AppUser.query.filter(
            AppUser.email == data.get('email')).count()
        user_exist = AppUser.query.filter(
            AppUser.user_name == data.get('user_name')).count()
        mobile_exist = AppUser.query.filter(
            AppUser.mobile == data.get('mobile')).count()
        if user_exist > 0:
            loger("warning").warning("user_name not available.")
            return jsonify({"status": False,
                            "data": "",
                            "msg": "user_name not available.", "error": ""}), 200
        elif email_exist > 0:
            loger("warning").warning("email already exist.")
            return jsonify({"status": False,
                            "data": "",
                            "msg": "email already exist.", "error": ""}), 200
        elif mobile_exist > 0:
            loger("warning").warning("mobile number already exist.")
            return jsonify({"status": False,
                            "data": "",
                            "msg": "mobile number already exist.", "error": ""}), 200
        db.session.add(entry)
        db.session.commit()
        data={
            "id": entry.id,
            "name": entry.name,
            "user_name": entry.user_name,
            "role_id": entry.role_id,
            "image_path": entry.image_path,
            "encrypted_password": entry.encrypted_password,
            "email": entry.email,
            "mobile": entry.mobile
        }
        loger("info").info("user added.")
        return jsonify({"status": True,
                        "data": data,
                        "msg": "user added.", "error": ""}), 201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


@admin.route('/update-user/<int:id>', methods=['PUT'])
@token_required
@permission_required('read_team')
def updateUser(id):
    try:
        data = request.get_json()
        entry = AppUser.query.get(id)
        if not entry:
            loger("warning").warning("user not exist.")
            return jsonify({"status":False,"data": "","msg": "user not exist.", "error": ""}),200
        email_exist = AppUser.query.filter(
            AppUser.email == data.get('email')).count()
        user_exist = AppUser.query.filter(
            AppUser.user_name == data.get('user_name')).count()
        mobile_exist = AppUser.query.filter(
            AppUser.mobile == data.get('mobile')).count()
        uname = entry.user_name != data.get('user_name')
        email = entry.email != data.get('email')
        mobile = entry.mobile != data.get('mobile')
        entry.name = data.get('name'),
        entry.role_id = data.get('role_id'),
        if not UserRoleMapping.query.get(data.get('role_id')):
            loger("warning").warning("role not exist.")
            return jsonify({"status":False,"data": "","msg": "role not exist.", "error": ""}),200
        entry.user_name = data.get('user_name'),
        entry.image_path = data.get('image_path'),
        entry.encrypted_password = generate_password_hash(data.get('encrypted_password')),
        entry.email = data.get('email'),
        entry.mobile = data.get('mobile')
        if uname and user_exist > 0:
            loger("warning").warning("user_name not available.")
            return jsonify({"status":False,"data": "","msg": "user_name not available.", "error": ""}),200
        if email and email_exist > 0:
            loger("warning").warning("email already exist.")
            return jsonify({"status":False,"data": "","msg": "email already exist.", "error": ""}),200
        if mobile and mobile_exist > 0:
            loger("warning").warning("mobile number already exist.")
            return jsonify({"status":False,"data": "","msg": "mobile number already exist.", "error": ""}),200
        db.session.commit()
        data={"id": entry.id,
            "name": entry.name,
            "user_name": entry.user_name,
            "role_id": entry.role_id,
            "image_path": entry.image_path,
            "encrypted_password": entry.encrypted_password,
            "email": entry.email,
            "mobile": entry.mobile}
        loger("info").info("user updated.")
        return jsonify({"status":False,"data": data,"msg": "user updated.", "error": ""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


@admin.route('/show-users')
@token_required
@permission_required('admin')
def showUsers():
    try:
        users = AppUser.query.all()
        data = []
        for entry in users:
            info = {
                "id": entry.id,
                "name": entry.name,
                "user_name": entry.user_name,
                "role_id": entry.role_id,
                "image_path": entry.image_path,
                "encrypted_password": entry.encrypted_password,
                "email": entry.email,
                "mobile": entry.mobile
            }
            data.append(info)
        if not data:
            loger("warning").warning("no data")
            return jsonify({"status": False,
                        "data": data,
                        "msg": "No data", "error": ""}), 200
        loger("info").info("user details viewed")
        return jsonify({"status": True,
                        "data": data,
                        "msg": "", "error": ""}), 200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


@admin.route('/add-user-permissions', methods=['POST'])
def addUserPermissions():
    try:
        data = request.get_json()
        role = data.get('role')
        if not role:
            loger("warning").warning("role must be entered.")
            return jsonify({"status": False,
                        "data": "",
                        "msg": "role must be entered.", "error": ""}), 200
        access = data.get('access')
        if not access:
            loger("warning").warning("access must be entered.")
            return jsonify({"status": False,
                        "data": "",
                        "msg": "access must be entered.", "error": ""}), 200
        roles=UserRoleMapping.query.all()
        for r in roles:
            if r.role==role:
                loger("warning").warning("role already exist.")
                return jsonify({"status": False,
                        "data": "",
                        "msg": "role already exist.", "error": ""}), 200
        role = UserRoleMapping(role=role, access=access)
        db.session.add(role)
        db.session.commit()
        loger("info").info("role added successfully.")
        return jsonify({"status": True,
                        "data": {"id": role.id,
                                 "role": role.role,
                                 "access": role.access
                                 },
                        "msg": "role added successfully", "error": ""}), 201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


@admin.route('/show-roles')
def showUserPermissions():
    try:
        data = []
        roles = UserRoleMapping.query.all()
        for role in roles:
            data.append(
                {"id": role.id, "role": role.role, "access": role.access})
        if not data:
            loger("warning").warning("roles not exist")
            return jsonify({"status": True,
                    "data": data,
                    "msg": "roles not exist", "error": ""}), 200
        loger("warning").info("roles viewed.")
        return jsonify({"status": True,
                        "data": data,
                        "msg": "roles viewed", "error": ""}), 200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


@admin.route('/update-role/<int:id>', methods=['PUT'])
def updateRole(id):
    try:
        data = request.get_json()
        role = UserRoleMapping.query.get(id)
        if not role:
            loger("warning").warning("role doesn't exist.")
            return jsonify({"status": False,
                            "role": "",
                            "msg": "role doesn't exist", "error": ""}), 201
        role.access = data.get('access')
        if not role.access:
            loger("warning").warning("access not entered.")
            return jsonify({"status": False,
                            "role": "",
                            "msg": "access not entered", "error": ""}), 201
        db.session.commit()
        loger("info").info("role updated successfully")
        return jsonify({"status": True,
                        "role": {"id": role.id,
                                 "role": role.role,
                                 "access": role.access
                                 },
                        "msg": "role updated successfully", "error": ""}), 201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


@admin.route('/delete-role/<int:id>', methods=['DELETE'])
def deleteRole(id):
    try:
        data = request.get_json()
        role = UserRoleMapping.query.get(id)
        if not role:
            loger("warning").warning("role doesn't exist.")
            return jsonify({"status": False,
                            "role": "",
                            "msg": "role doesn't exist.", "error": ""}), 201
        db.session.delete(role)
        db.session.commit()
        loger("info").info("role deleted successfully")
        return jsonify({"status": True,
                        "role": {"id": role.id,
                                 "role": role.role,
                                 "access": role.access
                                 },
                        "msg": "role deleted successfully", "error": ""}), 204
    except Exception as e:
        loger("error").error(str(e))
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
