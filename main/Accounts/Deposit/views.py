from flask import Blueprint, jsonify, request
from main.Accounts.Deposit.models import BankTransactions
from main.Settings.Accounts.models import BankAccounts
from main.Teams.Incharge.models import Employee
from main.extensions import db

deposit=Blueprint('deposit',__name__,url_prefix='/deposit')

@deposit.route('/bank-dropdown')
def bankDropdown():
    try:
        details=BankAccounts.query.all()
        data=[]
        for i in details:
            id=i.id
            branch=i.branch
            acc_number=i.acc_number
            account_name=i.account_name
            IFSC_code=i.IFSC_code
            info={
                "id":id,
                "acc_number":acc_number,
                "account_name":account_name,
                "branch":branch,
                "IFSC_code":IFSC_code
                  }
            data.append(info)
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@deposit.route('/incharge-dropdown')
def inchargeDropdown():
    try:
        empDetails=Employee.query.all()
        data=[]
        for i in empDetails:
            id=i.id
            name=i.name
            mobile_number=i.mobile
            info={
                "id":id,
                "name":name,
                "mobile_number":mobile_number
                  }
            data.append(info)
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })