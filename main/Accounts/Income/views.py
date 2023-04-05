from flask import Blueprint, jsonify, request
from main.utils import token_required,permission_required,loger
from main.Accounts.Income.models import Income
from main.Settings.Funds.models import MasterData
from main.extensions import db
import uuid
warning="warning"
info="info"
error="error"
income=Blueprint('income',__name__,url_prefix='/income')

# @income.route('/category-dropdown')
# def categoryDropdown():
#     try:
#         categories=MasterData.query.filter(MasterData.property=='category')
#         data=[]
#         for i in categories:
#             info={"id":i.id,
#                   "property":i.property,
#                   "value":i.value}
#             data.append(info)
#         return jsonify({
#             "data":data
#         })
#     except Exception as e:
#         return jsonify({
#             "error":str(e)
#         })

@income.route('/add-income-details',methods=['POST'])
def addIncomeDetail():
    try:
        data=request.get_json()
        received_from=data.get('received_from')
        received_date=data.get('received_date')
        amount=data.get('amount')
        category_id=data.get('category_id')
        category=MasterData.query.get(category_id)
        if not category:
            return jsonify({
                "message":"category not exist."
            })
        description=data.get('description')
        ref_no=uuid.uuid4().hex[:8]
        entry=Income(received_from=received_from,
                     received_date=received_date,
                     amount=amount,
                     category_id=category_id,
                     description=description,
                     ref_no=ref_no)
        db.session.add(entry)
        db.session.commit()
        data=[{
            "id":entry.id,
            "received_from":entry.received_from,
            "received_date":entry.received_date,
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

@income.route('/show-income-details')
def showIncomeDetails():
    try:
        page=int(request.args['page'])
        per_page=int(request.args['per_page'])
        search=request.args['search']
        if search:
            pass
        else:
            details=Income.query.paginate(page=page,per_page=per_page,error_out=False)
            data=[]
            for detail in details:
                id=detail.id
                received_from=detail.received_from
                received_date=detail.received_date
                amount=detail.amount
                category_id=detail.category_id
                description=detail.description
                ref_no=detail.ref_no
                info={"id":id,
                    "received_from":received_from,
                    "received_date":received_date,
                    "category_id":category_id,
                    "description":description,
                    "amount":amount,
                    "ref_no":ref_no}
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
    
@income.route('/update/<int:id>',methods=['PUT'])
def update(id):
    try:
        data=request.get_json()
        entry=Income.query.get(id)
        if not entry:
            message="income not exist."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        entry.received_from=data.get('received_from')
        entry.received_date=data.get('received_date')
        entry.amount=data.get('amount')
        entry.category_id=data.get('category_id')
        db.session.commit()
        data=[{
            "id":id,
            'received_from':entry.received_from,
            'received_date':entry.received_date,
            'amount':entry.amount,
            'category_id':entry.category_id
        }]
        message="income deleted"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),204
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
    
@income.route('/delete/<int:id>',methods=['DELETE'])
def delete(id):
    try:
        entry=Income.query.get(id)
        if not entry:
            message="income not exist."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        db.session.delete(entry)
        db.session.commit()
        message="income deleted"
        loger(info).info(message)
        return jsonify({"status":True,"data":"","message":message,"error":""}),204
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500