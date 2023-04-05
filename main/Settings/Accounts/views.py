from flask import Blueprint,jsonify,request
from main.utils import loger
from main.Settings.Accounts.models import BankAccounts,CategorySubcategory
from main.Settings.Funds.models import MasterData
from main.extensions import db

settings_accounts=Blueprint('settings-accounts',__name__,url_prefix='/settings-accounts')

#category
@settings_accounts.route('/add-category',methods=["POST"])
def addCategory():
    try:
        data=request.get_json()
        property='category'
        value=data.get('value')
        if not value:
            loger("warning").warning("value not entered")
            return jsonify({"satus":False,
                        "data":"",
                        "msg":"value not entered.",
                        "error":""}),200
        entry=MasterData(property=property,
                         value=value)
        db.session.add(entry)
        db.session.commit()
        loger("info").info("category added successfully.")
        return jsonify({"satus":True,
                        "data":{"id":entry.id,"property":entry.property,"value":entry.value},
                        "msg":"category added successfully.",
                        "error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,
                        "data":"","msg":"",
                        "error":str(e)
        }),500
    
@settings_accounts.route('/show-all-categories')
def showAllCategories():
    try:
        categories=MasterData.query.filter(MasterData.property=='category')
        data=[]
        for i in categories:
            id=i.id
            property=i.property
            value=i.value
            info={
                "id":id,
                "property":property,
                "value":value
            }
            data.append(info)
        if not data:
            msg="category not exist!!"
            loger(level="warning").warning(msg)
            return jsonify({"status":False,"data":"","msg":msg,"error":""}),200
        loger(level="info").info("success")
        return jsonify({
           "status":True,"data":data,"msg":"","error":""
        }),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
           "status":False,"data":"","msg":"","error":str(e)
        }),500

@settings_accounts.route('/delete-category/<int:id>',methods=["DELETE"])
def deleteCategory(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            msg="category not exist!!"
            loger(level="warning").warning(msg)
            return jsonify({"status":False,"data":"","msg":msg,"error":""}),200
        db.session.delete(entry)
        db.session.commit()
        loger(level="info").info("category deleted successfully.")
        return jsonify({"status":True,"data":"","msg":"category deleted successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
           "status":False,"data":"","msg":"","error":str(e)
        }),500

#Expense
@settings_accounts.route('/add-expense',methods=['POST'])
def addExpense():
    try:
        data=request.get_json()
        TYPE='Expense'
        CATEGORY=data.get('CATEGORY')
        if not CATEGORY:
            loger("warning").warning("category not entered")
            return jsonify({"satus":False,
                        "data":"",
                        "msg":"category not entered.",
                        "error":""}),200
        SUBCATEGORY=data.get('SUBCATEGORY')
        if not SUBCATEGORY:
            loger("warning").warning("subcategory not entered")
            return jsonify({"satus":False,
                        "data":"",
                        "msg":"subcategory not entered.",
                        "error":""}),200
        expense=CategorySubcategory.query.filter(CategorySubcategory.SUBCATEGORY==SUBCATEGORY).first()
        if expense:
            msg="expense already exist!!"
            loger(level="warning").warning(msg)
            return jsonify({"status":False,"data":"","msg":msg,"error":""}),200
        entry=CategorySubcategory(TYPE=TYPE,
                         CATEGORY=CATEGORY,
                         SUBCATEGORY=SUBCATEGORY)
        db.session.add(entry)
        db.session.commit()
        data=[{
            "id":entry.id,
            "TYPE":entry.TYPE,
            "CATEGORY":entry.CATEGORY,
            "SUBCATEGORY":entry.SUBCATEGORY
            }]
        loger("info").info("expense category added successfully.")
        return jsonify({"satus":True,
                        "data":data,
                        "msg":"expense category added successfully.",
                        "error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
           "status":False,"data":"","msg":"","error":str(e)
        }),500
    
@settings_accounts.route('/show-all-expenses')
def showAllExpenses():
    try:
        expenses=CategorySubcategory.query.filter(CategorySubcategory.TYPE=='Expense')
        data=[]
        for i in expenses:
            id=i.id
            type=i.TYPE
            category=i.CATEGORY
            subcategory=i.SUBCATEGORY
            info={
                "id":id,
                "TYPE":type,
                "CATEGORY":category,
                "SUBCATEGORY":subcategory
            }
            data.append(info)
        if not data:
            msg="no data!!"
            loger(level="warning").warning(msg)
            return jsonify({"status":False,"data":data,"msg":msg,"error":""}),200
        loger(level="info").info("success")
        return jsonify({
           "status":True,"data":data,"msg":"","error":""
        }),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
           "status":False,"data":"","msg":"","error":str(e)
        }),500

@settings_accounts.route('/delete-expense/<int:id>',methods=["DELETE"])
def deleteExpense(id):
    try:
        entry=CategorySubcategory.query.get(id)
        if not entry:
            msg="expense category not exist!!"
            loger(level="warning").warning(msg)
            return jsonify({"status":False,"data":"","msg":msg,"error":""}),200
        db.session.delete(entry)
        db.session.commit()
        msg="category deleted successfully."
        loger(level="info").warning(msg)
        return jsonify({"status":True,"data":"","msg":msg,"error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"data":"","msg":"","error":str(e)}),500

#Bank Details
@settings_accounts.route('/add-bank-details',methods=['POST'])
def addBankDetails():
    try:
        data=request.get_json()
        acc_number=data.get('acc_number')
        if not acc_number:
            loger("warning").warning("account number not entered")
            return jsonify({"satus":False,
                        "data":"",
                        "msg":"account_no not entered.",
                        "error":""}),200
        account_name=data.get('account_name')
        if not account_name:
            loger("warning").warning("account_name not entered")
            return jsonify({"satus":False,
                        "data":"",
                        "msg":"account_name not entered.",
                        "error":""}),200
        branch=data.get('branch')
        if not branch:
            loger("warning").warning("branch not entered")
            return jsonify({"satus":False,
                        "data":"",
                        "msg":"branch not entered.",
                        "error":""}),200
        IFSC_code=data.get('IFSC_code')
        if not IFSC_code:
            loger("warning").warning("IFSC_code not entered")
            return jsonify({"satus":False,
                        "data":"",
                        "msg":"IFSC_code not entered.",
                        "error":""}),200
        entry=BankAccounts(acc_number=acc_number,
                           account_name=account_name,
                           branch=branch,
                           IFSC_code=IFSC_code)
        db.session.add(entry)
        db.session.commit()
        data={
            "id":entry.id,
            "acc_number":acc_number,
            "account_name":account_name,
            "branch":branch,
            "IFSC_code":IFSC_code
        }
        msg="bank details added successfully"
        loger(level="info").info(msg)
        return jsonify({"status":True,"data":data,"msg":msg,"error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"data":"","msg":"","error":str(e)}),500
    
@settings_accounts.route('/all-bank-details')
def allBankDetails():
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
        if not data:
            msg="no data!!"
            loger(level="warning").warning(msg)
            return jsonify({"status":False,"data":data,"msg":msg,"error":""}),200
        loger(level="info").info("success")
        return jsonify({
           "status":True,"data":data,"msg":"","error":""
        }),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
           "status":False,"data":"","msg":"","error":str(e)
        }),500
    
@settings_accounts.route('/delete-bank-detail/<int:id>',methods=['DELETE'])
def delete(id):
    try:
        entry=BankAccounts.query.get(id)
        if not entry:
            msg="bank account not exist!!"
            loger(level="warning").warning(msg)
            return jsonify({"status":False,"data":"","msg":msg,"error":""}),200
        db.session.delete(entry)
        db.session.commit()
        msg="deleted successfully."
        loger(level="info").info(msg)
        return jsonify({"status":False,"data":"","msg":msg,"error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({
           "status":False,"data":"","msg":"","error":str(e)
        }),500