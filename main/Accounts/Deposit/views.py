from flask import Blueprint, jsonify, request
from main.utils import token_required,permission_required,loger
from main.Accounts.Deposit.models import BankTransactions
from main.Settings.Accounts.models import BankAccounts
from main.Teams.Incharge.models import Employee
from main.extensions import db
from uuid import uuid4

deposit=Blueprint('deposit',__name__,url_prefix='/deposit')
warning="warning"
info="info"
error="error"

# @deposit.route('/bank-dropdown')
# def bankDropdown():
#     try:
#         details=BankAccounts.query.all()
#         data=[]
#         for i in details:
#             id=i.id
#             branch=i.branch
#             acc_number=i.acc_number
#             account_name=i.account_name
#             IFSC_code=i.IFSC_code
#             info={
#                 "id":id,
#                 "acc_number":acc_number,
#                 "account_name":account_name,
#                 "branch":branch,
#                 "IFSC_code":IFSC_code
#                   }
#             data.append(info)
#         return jsonify({
#             "data":data
#         })
#     except Exception as e:
#         return jsonify({
#             "error":str(e)
#         })
    
# @deposit.route('/incharge-dropdown')
# def inchargeDropdown():
#     try:
#         empDetails=Employee.query.all()
#         data=[]
#         for i in empDetails:
#             id=i.id
#             name=i.name
#             mobile_number=i.mobile
#             info={
#                 "id":id,
#                 "name":name,
#                 "mobile_number":mobile_number
#                   }
#             data.append(info)
#         return jsonify({
#             "data":data
#         })
#     except Exception as e:
#         return jsonify({
#             "error":str(e)
#         })
    
@deposit.route('/add-deposit-details',methods=["POST"])
def addDepositDetails():
    try:
        data=request.get_json()
        bank_id=data.get('bank_id')
        if not bank_id:
            message="bank_id be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        detail=BankAccounts.query.get(bank_id)
        if not detail:
            message="bank detail not exist."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        transfer_type=0
        transaction_date=data.get('transaction_date')
        if not transaction_date:
            message="transaction_date must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        amount=data.get('amount')
        if not amount:
            message="amount must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        balance=0
        balances=BankTransactions.query.filter_by(bank_id=bank_id)
        for l_balance in balances:
            balance=l_balance
        balance+=amount
        deposited_by=data.get('deposited_by')
        if not deposited_by:
            message="deposited_by must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        reference_no=uuid4().hex[:8]
        entry=BankTransactions(bank_id=bank_id,
                               transaction_date=transaction_date,
                               transfer_type=transfer_type,
                               amount=amount,
                               balance=balance,
                               deposited_by=deposited_by,
                               reference_no=reference_no,)
        db.session.add(entry)
        db.session.commit()
        data=[{"id":entry.id,
            "bank_id":bank_id,
            "transfer_type":transfer_type,
            "transaction_date":transaction_date,
            "transaction_type":entry.transaction_type,
            "amount":amount,
            "balance":balance,
            "deposited_by":deposited_by,
            "reference_no":reference_no
            }]
        message="deposit added"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),201
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
    
@deposit.route('/show-deposit-details')
def showDepositDetails():
    try:
        page=int(request.args['page'])
        per_page=int(request.args['per_page'])
        search=request.args['search']
        if search:
            details=Employee.query.filter(Employee.name==search)
            data=[]
            for i in details:
                id=i.id
                name=i.name
                deposits=BankTransactions.query.filter((BankTransactions.deposited_by==str(id))&
                                                       (BankTransactions.transaction_type==0))
                for deposit in deposits:
                    info={
                    "id":deposit.id,
                    "bank_id":deposit.bank_id,
                    "transaction_type":deposit.transaction_type,
                    "transaction_date":deposit.transaction_date,
                    "amount":deposit.amount,
                    "deposited_by":deposit.deposited_by,
                    "reference_no":deposit.reference_no,
                    "name":name
                    }
                    data.append(info)
            if not data:
                message="No data"
                loger(warning).warning(message)
                return jsonify({"status":False,"data":data,"message":message,"error":""}),200
            message="data returned"
            loger(info).info(message)
            return jsonify({"status":True,"data":data,"message":message,"error":""}),200
        else:
            deposits=BankTransactions.query.paginate(page=page,per_page=per_page,error_out=False)
            data=[]
            for i in deposits:
                if i.transaction_type==1:
                    continue
                emp_id=int(i.deposited_by)
                employee=Employee.query.get(emp_id)
                info={
                    "id":i.id,
                    "bank_id":i.bank_id,
                    "transaction_type":i.transaction_type,
                    "transaction_date":i.transaction_date,
                    "amount":i.amount,
                    "deposited_by":i.deposited_by,
                    "reference_no":i.reference_no,
                    "name":employee.name
                    }
                data.append(info)
            if not data:
                message="No data"
                loger(warning).warning(message)
                return jsonify({"status":False,"data":data,"message":message,"error":""}),200
            message="data returned"
            loger(info).info(message)
            return jsonify({"status":True,"data":data,"message":message,"error":""}),200
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500