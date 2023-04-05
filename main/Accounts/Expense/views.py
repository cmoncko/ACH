from flask import Blueprint, request, jsonify
from main.Accounts.Expense.models import Expense
from main.Settings.Accounts.models import CategorySubcategory
from main.extensions import db
import uuid
from main.utils import token_required,permission_required,loger
warning="warning"
info="info"
error="error"
expense=Blueprint('expense',__name__,url_prefix='/expense')

# @expense.route('/category-subcategory-dropdown')
# def categorySubcategoryDropdown():
#     try:
#         categories=CategorySubcategory.query.all()
#         data=[]
#         for i in categories:
#             info={"id":i.id,
#                   "TYPE":i.TYPE,
#                   "CATEGORY":i.CATEGORY,
#                   "SUBCATEGORY":i.SUBCATEGORY}
#             data.append(info)
#         return jsonify({
#             "data":data
#         })
#     except Exception as e:
#         return jsonify({
#             "error":str(e)
#         })

@expense.route('/add-expense-details',methods=['POST'])
def addExpenseDetail():
    try:
        data=request.get_json()
        paid_to=data.get('paid_to')
        if not paid_to:
            message="paid_to must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        paid_date=data.get('received_date')
        if not paid_date:
            message="paid_date must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        amount=data.get('amount')
        if not amount:
            message="amount must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        category_id=data.get('category_id')
        if not category_id:
            message="category_id must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        category=CategorySubcategory.query.get(category_id)
        if not category:
            message="category not exist."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        description=data.get('description')
        ref_no=uuid.uuid4().hex[:8]
        entry=Expense(paid_to=paid_to,
                     paid_date=paid_date,
                     amount=amount,
                     category_id=category_id,
                     description=description,
                     ref_no=ref_no)
        db.session.add(entry)
        db.session.commit()
        data=[{
            "id":entry.id,
            "received_from":entry.paid_to,
            "received_date":entry.paid_date,
            "category_id":entry.category_id,
            "description":entry.description,
            "amount":entry.amount,
            "ref_no":entry.ref_no
        }]
        message="expense added"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),201
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500

@expense.route('/show-expense-details')
def showExpenseDetails():
    try:
        page=int(request.args['page'])
        per_page=int(request.args['per_page'])
        search=request.args['search']
        if search:
            pass
        else:
            details=Expense.query.paginate(page=page,per_page=per_page,error_out=False)
            data=[]
            for detail in details:
                id=detail.id
                paid_to=detail.paid_to
                paid_date=detail.paid_date
                amount=detail.amount
                category_id=detail.category_id
                cat_subcat=CategorySubcategory.query.get(category_id)
                category=cat_subcat.CATEGORY
                subcategory=cat_subcat.SUBCATEGORY
                description=detail.description
                ref_no=detail.ref_no
                info={"id":id,
                    "received_from":paid_to,
                    "received_date":paid_date,
                    "category":category_id,
                    "category":category,
                    "sub_category":subcategory,
                    "description":description,
                    "amount":amount,
                    "ref_no":ref_no}
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
    
@expense.route('/update/<int:id>',methods=['PUT'])
def update(id):
    try:
        data=request.get_json()
        entry=Expense.query.get(id)
        if not entry:
            message="expense not exist."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        entry.paid_to=data.get('paid_to')
        entry.paid_date=data.get('paid_date')
        entry.amount=data.get('amount')
        entry.category_id=data.get('category_id')
        entry.description=data.get('description')
        db.session.commit()
        data=[{"id":id,
        'paid_to':entry.paid_to,
        'paid_date':entry.paid_date,
        'amount':entry.amount,
        'category_id':entry.category_id,
        'description':entry.description}]
        message="expense updated"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),204
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
    
@expense.route('/delete/<int:id>',methods=['DELETE'])
def delete(id):
    try:
        entry=Expense.query.get(id)
        if not entry:
            message="expense not exist."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        db.session.delete(entry)
        db.session.commit()
        message="expense deleted"
        loger(info).info(message)
        return jsonify({"status":True,"data":"","message":message,"error":""}),204
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500