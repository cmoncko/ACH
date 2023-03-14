from flask import Blueprint,jsonify,request
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
        entry=MasterData(property=property,
                         value=value)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
            })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
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
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@settings_accounts.route('/delete-category/<int:id>',methods=["DELETE"])
def deleteCategory(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            return jsonify({
                "message":"category not exist."
            })
        db.session.delete(entry)
        db.session.commit()
        return jsonify({
            "messgae":"category deleted successfully."
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

#Expense
@settings_accounts.route('/add-expense',methods=['POST'])
def addExpense():
    try:
        data=request.get_json()
        TYPE='Expense'
        CATEGORY=data.get('CATEGORY')
        SUBCATEGORY=data.get('SUBCATEGORY')
        expenses=CategorySubcategory.query.filter(CategorySubcategory.SUBCATEGORY==SUBCATEGORY)
        subCategoryExist=False
        for i in expenses:
            subCategoryExist=True
        if subCategoryExist:
            return jsonify({
                "message":"expense already exist"
            })
        entry=CategorySubcategory(TYPE=TYPE,
                         CATEGORY=CATEGORY,
                         SUBCATEGORY=SUBCATEGORY)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "TYPE":entry.TYPE,
            "CATEGORY":entry.CATEGORY,
            "SUBCATEGORY":entry.SUBCATEGORY
            })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

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
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@settings_accounts.route('/delete-expense/<int:id>',methods=["DELETE"])
def deleteExpense(id):
    try:
        entry=CategorySubcategory.query.get(id)
        if not entry:
            return jsonify({
                "message":"expense not exist."
            })
        db.session.delete(entry)
        db.session.commit()
        return jsonify({
            "messgae":"category deleted successfully."
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

#Bank Details
@settings_accounts.route('/add-bank-details',methods=['POST'])
def addBankDetails():
    try:
        data=request.get_json()
        acc_number=data.get('acc_number')
        account_name=data.get('account_name')
        branch=data.get('branch')
        IFSC_code=data.get('IFSC_code')
        entry=BankAccounts(acc_number=acc_number,
                           account_name=account_name,
                           branch=branch,
                           IFSC_code=IFSC_code)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "acc_number":acc_number,
            "account_name":account_name,
            "branch":branch,
            "IFSC_code":IFSC_code
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
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
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@settings_accounts.route('/delete-bank-detail/<int:id>',methods=['DELETE'])
def delete(id):
    try:
        entry=BankAccounts.query.get(id)
        if not entry:
            return jsonify({
                "message":"Bank Account not exist."
            })
        db.session.delete(entry)
        db.session.commit()
        return jsonify({
            "message":"deleted successfully."
        })
    except Exception as e:
        return jsonify({
          "error":str(e)  
        })