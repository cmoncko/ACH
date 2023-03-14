from flask import Blueprint, request, jsonify
from main.Accounts.Expense.models import Expense
from main.Settings.Accounts.models import CategorySubcategory
from main.extensions import db
import uuid

expense=Blueprint('expense',__name__,url_prefix='/expense')

@expense.route('/category-subcategory-dropdown')
def categorySubcategoryDropdown():
    try:
        categories=CategorySubcategory.query.all()
        data=[]
        for i in categories:
            info={"id":i.id,
                  "TYPE":i.TYPE,
                  "CATEGORY":i.CATEGORY,
                  "SUBCATEGORY":i.SUBCATEGORY}
            data.append(info)
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@expense.route('/add-expense-details',methods=['POST'])
def addExpenseDetail():
    try:
        data=request.get_json()
        paid_to=data.get('paid_to')
        paid_date=data.get('received_date')
        amount=data.get('amount')
        category_id=data.get('category_id')
        category=CategorySubcategory.query.get(category_id)
        if not category:
            return jsonify({
                "message":"category not exist."
            })
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
        return jsonify({
            "id":entry.id,
            "received_from":entry.paid_to,
            "received_date":entry.paid_date,
            "category_id":entry.category_id,
            "description":entry.description,
            "amount":entry.amount,
            "ref_no":entry.ref_no
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

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
                description=detail.description
                ref_no=detail.ref_no
                info={"id":id,
                    "received_from":paid_to,
                    "received_date":paid_date,
                    "category_id":category_id,
                    "description":description,
                    "amount":amount,
                    "ref_no":ref_no}
                print(info)
                data.append(info)
            return jsonify({
                "data":data
            })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@expense.route('/update/<int:id>',methods=['PUT'])
def update(id):
    try:
        data=request.get_json()
        entry=Expense.query.get(id)
        if not entry:
            return jsonify({
                "message":"expense detail not exist."
            })
        entry.paid_to=data.get('paid_to')
        entry.paid_date=data.get('paid_date')
        entry.amount=data.get('amount')
        entry.category_id=data.get('category_id')
        db.session.commit()
        return jsonify({
            "id":id,
            'paid_to':entry.paid_to,
            'paid_date':entry.paid_date,
            'amount':entry.amount,
            'category_id':entry.category_id
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@expense.route('/delete/<int:id>',methods=['DELETE'])
def delete(id):
    try:
        entry=Expense.query.get(id)
        if not entry:
            return jsonify({
                "message":"expense detail not exist."
            })
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message":"deleted successfully"})
    except Exception as e:
        return jsonify({
            "error":str(e)
        })