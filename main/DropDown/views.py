from flask import Blueprint, jsonify, request
from main.utils import token_required, permission_required, loger
from main.Teams.Members.models import MemberProfile
from main.Teams.Incharge.models import Employee
from main.Settings.Funds.models import MasterData
from main.Settings.Services.models import BenefitType
from main.Settings.Teams.models import Address
from main.Settings.Admin.models import UserRoleMapping
from main.Settings.Accounts.models import CategorySubcategory,BankAccounts

drop_down=Blueprint('drop_down',__name__,url_prefix="/drop-down")

@drop_down.route('/address')
def dropAddress():
    try:
        address=Address.query.all()
        data=[{"id":i.id, "city":i.city,"district":i.district,"state":i.state,"pincode":i.pincode,"country":i.country} for i in address]
        if not data:
            msg="Address not exist"
            loger(level="warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="Address viewed"
        loger("info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500

@drop_down.route('/nominee')
def dropNominee():
    try:
        nominees=MasterData.query.filter(MasterData.property=="relation")
        data=[{"id":i.id, "value":i.value} for i in nominees]
        if not data:
            msg="nominee relation not exist"
            loger(level="warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="Nominee relation viewed"
        loger(level="info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
        "status": False, "data": "", "msg": "","error":str(e)
        }),500

@drop_down.route('/santha-year')
def dropSanthaYear():
    try:
        santha_year=MasterData.query.filter(MasterData.property=="Santha Year")
        data=[{"id":i.id, "value":i.value} for i in santha_year]
        if not data:
            msg="santha year not exist"
            loger(level="warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="santha year viewed"
        loger(level="info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500

@drop_down.route('/santha-amount')
def showSanthaAmount():
    try:
        santha_amount=MasterData.query.filter(MasterData.property=="Amount Per Year Rs")
        data=[{"id":i.id, "value":i.value} for i in santha_amount]
        if not data:
            msg="santha amount not exist"
            loger(level="warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="santha amount viewed"
        loger(level="info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500

@drop_down.route('/members')
def dropMembers():
    try:
        members=MemberProfile.query.filter(MemberProfile.is_leader==0)
        data=[{"id":i.id, "name":i.name} for i in members]
        if not data:
            msg="members not exist"
            loger(level="warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="members viewed"
        loger(level="info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500

@drop_down.route('/leaders')
def dropLeaders():
    try:
        leaders=MemberProfile.query.filter(MemberProfile.is_leader==1)
        data=[{"id":i.id, "name":i.name} for i in leaders]
        if not data:
            msg="leaders not exist"
            loger(level="warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="leaders viewed"
        loger(level="info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500
    
@drop_down.route('/incharges')
def dropIncharges():
    try:
        incharges=Employee.query.all()
        data=[{"id":i.id, "name":i.name} for i in incharges]
        if not data:
            msg="Incharges not exist"
            loger(level="warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="Incharges viewed"
        loger(level="info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500
    
@drop_down.route('/category')
def dropCategory():
    try:
        categorys=MasterData.query.filter(MasterData.property=="category")
        data=[{"id":i.id, "value":i.value} for i in categorys]
        if not data:
            msg="categories not exist"
            loger(level="warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="categories viewed"
        loger(level="info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500
    
@drop_down.route('/category-subcategory')
def dropCategorySubcategory():
    try:
        categorys=CategorySubcategory.query.all()
        data=[{"id":i.id, "category":i.CATEGORY,"subcategory":i.SUBCATEGORY} for i in categorys]
        if not data:
            msg="category-subcategory not exist"
            loger(level="warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="category-subcategory viewed"
        loger(level="info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500

@drop_down.route('/bank-details')
def dropBankDetails():
    try:
        bank_details=BankAccounts.query.all()
        data=[{"id":i.id, "account_name":i.account_name,"account_number":i.acc_number,"branch":i.branch,"IFSC_code":i.IFSC_code} for i in bank_details]
        if not data:
            msg="bank-details not exist"
            loger("warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="bank-details viewed"
        loger("info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500
    
@drop_down.route('/benefits-type')
def dropBenefitsType():
    try:
        benefit_details=BenefitType.query.all()
        data=[{"id":i.id, "name":i.name} for i in benefit_details]
        if not data:
            msg="benefit types not exist"
            loger("warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="benefit types viewed"
        loger("info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500
    
@drop_down.route('/role-id-type')
def dropRoleIdType():
    try:
        role_details=UserRoleMapping.query.all()
        data=[{"id":i.id, "role_id":i.role,"access":i.access} for i in role_details]
        if not data:
            msg="roles not exist"
            loger(level="warning").warning(msg)
            return jsonify({"status": False, "data": "", "msg": msg, "error": ""}),200
        msg="roles viewed"
        loger(level="info").info(msg)
        return jsonify({"status": True, "data": data, "msg": msg, "error": ""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
            "status": False, "data": "", "msg": "","error":str(e)
        }),500