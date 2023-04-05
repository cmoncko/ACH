from flask import Blueprint, jsonify, request, session
from main import app
from main.Settings.Admin.models import AppUser
import jwt
from datetime import datetime,timedelta
from werkzeug.security import check_password_hash,generate_password_hash
# from TMS_Api.Utils import sendEmailOtp, verifyOtp,token_generate,technical_log,error_log
from main.extensions import db
from main.utils import loger

auth = Blueprint("Auth", __name__, url_prefix="/Auth")

@auth.route("/login", methods=['POST'])
def loginAuthData():
    try:
        json_data = request.get_json()

        loginData = {
            "email": json_data.get("email"),
            "password": json_data.get("password")
        }
        authData = AppUser.query.filter_by(email=loginData.get("email")).first()

        if authData is None:
            loger(level="warning").warning("Invalid user credential!!!")
            return jsonify({"status": False, "data": "", "msg": "Invalid user credential!!!", "error": ""}),200
        if not check_password_hash(authData.encrypted_password, loginData.get("password")):
            loger(level="warning").warning("Invalid password!!!")
            return jsonify({"status": False, "data": "", "msg": "Invalid password!!!", "error": ""}), 200
        token=jwt.encode({
                    "id":authData.id,
                    "exp":datetime.utcnow()+timedelta(hours=10)
                }, app.config['SECRET_KEY'])
        if token is not None:
            session['loginData'] = {
                "userId": authData.id,
                "email": authData.email,
                "mobileNo": authData.mobile,
                "username": authData.user_name
            }
        loger(level="info").info("successfully logged-in") 
        return jsonify({"status": True, "token":token, "msg": "successfully logged-in", "error": ""}), 201
    except Exception as e:
        loger(level="error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


@auth.route("/logout", methods=['GET'])
def logoutAuthData():
    try:
        if session.get("loginData") is None or session.get("loginData") == "":
            loger(level="warning").warning("you already logged-out")
            return jsonify({"status": False, "data": "", "msg": "you already logged-out", "error": ""}), 200
        session.pop("loginData")
        loger(level="info").info("successfully logged-out")
        return jsonify({"status": True, "data": "", "msg": "successfully logged-out", "error": ""}), 201
    except Exception as e:
        loger(level="error").error(str(e))
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


# @auth.route("/email-otp", methods=['POST'])
# def sendOTP():
#     try:
#         data = request.get_json()
#         check_email = User.isEmailExist(data.get("email"))
#         if check_email == True:
#             sendEmailOtp(data.get("email"))
#             technical_log().info({"status":True, "data":data.get("email"), "msg":"Email sent"})
#             return jsonify({"status":True, "data":data.get("email"), "msg":"Email sent","error":""}), 200
#         elif check_email == False:
#             technical_log().warning({"status":False, "data":data.get("email"), "msg":"Email Not Found"})
#             return jsonify({"status":False, "data":data.get("email"), "msg":"Email Not Found","error":""}), 200
#         technical_log().info({"status": False, "data": data.get("email"), "msg": "Email Not Found"})
#         return jsonify({"status": False, "data": data.get("email"), "msg": "Email Not Found", "error": ""}), 200
#     except Exception as e:
#         print(e)
#         error_log().error({"status": False, "data": "", "msg": "", "error": str(e)})
#         return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


# @auth.route("/verify-otp", methods=['POST'])
# def verifyEmailOTP():
#     try:
#         data = request.get_json()
#         if data:
#             success = verifyOtp(data.get("OTP"))
#             if success == True:
#                 technical_log().info({"status": True, "data": success, "msg": "OTP Verified"})
#                 return jsonify({"status": True, "data": success, "msg": "OTP Verified", "error": ""}), 200
#             else:
#                 technical_log().warning({"status": False, "data": "", "msg": "Verification Failed"})
#                 return jsonify({"status": False, "data": "", "msg": "Verification Failed", "error": ""}), 200
#         else:
#             technical_log().warning({"status": False, "data": "No data", "msg": "Enter OTP"})
#             return jsonify({"status": False, "data": "No data", "msg": "Enter OTP", "error": ""}), 200
#     except Exception as e:
#         error_log().error({"status": False, "data": "", "msg": "", "error": str(e)})
#         return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500


# @auth.route("/resetpassword", methods=["PUT"])
# def resetPassword():
#     try:
#         data = request.get_json()
#         try:
#             find_email = User.query.filter_by(email=data.get("email")).first()
#             email = find_email.email
#         except AttributeError:
#             technical_log().warning({"status": False, "data": data.get("email"), "msg": "user not found"})
#             return jsonify({"status": False, "data": data.get("email"), "msg": "user not found", "error": ""}), 200
#         password_one = data.get("type_password")
#         password_two = data.get("re-type_password")
#         if password_one == password_two:
#             if check_password_hash(find_email.password, password_two):
#                 technical_log().warning({"status": False, "data": email, "msg": "You enter old password"})
#                 return jsonify({"status": False, "data": email, "msg": "You enter old password", "error": ""}), 200
#             else:
#                 find_email.password = generate_password_hash(data.get("re-type_password"))
#                 db.session.commit()
#                 technical_log().info({"status": True, "data": email, "msg": "Password reset success!"})
#                 return jsonify({"status": True, "data": email, "msg": "Password reset success!", "error": ""}), 200
#         else:
#             technical_log().warning({"status": False, "data": "", "msg": "Password not match"})
#             return jsonify({"status": False, "data": "", "msg": "Password not match", "error": ""}), 200
#     except Exception as e:
#         technical_log().error({"status": False, "data": "", "msg": "", "error": str(e)})
#         return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500
