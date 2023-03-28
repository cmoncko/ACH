from flask import Blueprint, jsonify, request
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
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@drop_down.route('/nominee')
def dropNominee():
    try:
        nominees=MasterData.query.filter(MasterData.property=="relation")
        data=[{"id":i.id, "value":i.value} for i in nominees]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@drop_down.route('/santha-year')
def dropSanthaYear():
    try:
        santha_year=MasterData.query.filter(MasterData.property=="Santha Year")
        data=[{"id":i.id, "value":i.value} for i in santha_year]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@drop_down.route('/santha-amount')
def showSanthaAmount():
    try:
        santha_amount=MasterData.query.filter(MasterData.property=="Amount Per Year Rs")
        data=[{"id":i.id, "value":i.value} for i in santha_amount]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@drop_down.route('/members')
def dropMembers():
    try:
        members=MemberProfile.query.filter(MemberProfile.is_leader==0)
        data=[{"id":i.id, "name":i.name} for i in members]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@drop_down.route('/leaders')
def dropLeaders():
    try:
        leaders=MemberProfile.query.filter(MemberProfile.is_leader==1)
        data=[{"id":i.id, "name":i.name} for i in leaders]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@drop_down.route('/incharges')
def dropIncharges():
    try:
        incharges=Employee.query.all()
        data=[{"id":i.id, "name":i.name} for i in incharges]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@drop_down.route('/category')
def dropCategory():
    try:
        categorys=MasterData.query.filter(MasterData.property=="category")
        data=[{"id":i.id, "value":i.value} for i in categorys]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@drop_down.route('/category-subcategory')
def dropCategorySubcategory():
    try:
        categorys=CategorySubcategory.query.all()
        data=[{"id":i.id, "category":i.CATEGORY,"subcategory":i.SUBCATEGORY} for i in categorys]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@drop_down.route('/bank-details')
def dropBankDetails():
    try:
        bank_details=BankAccounts.query.all()
        data=[{"id":i.id, "account_name":i.account_name,"account_number":i.acc_number,"branch":i.branch,"IFSC_code":i.IFSC_code} for i in bank_details]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@drop_down.route('/benefits-type')
def dropBenefitsType():
    try:
        benefit_details=BenefitType.query.all()
        data=[{"id":i.id, "name":i.name} for i in benefit_details]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@drop_down.route('/role-id-type')
def dropRoleIdType():
    try:
        role_id_details=UserRoleMapping.query.all()
        data=[{"id":i.id, "role_id":i.role_id,"access":i.access} for i in role_id_details]
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })