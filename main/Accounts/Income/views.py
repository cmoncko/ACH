from flask import Blueprint, jsonify, request
from main.Accounts.Income.models import Income
from main.Settings.Funds.models import MasterData
from main.extensions import db
import uuid

income=Blueprint('income',__name__,url_prefix='/income')

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
        return jsonify({
            "id":entry.id,
            "received_from":entry.received_from,
            "received_date":entry.received_date,
            "category_id":entry.category_id,
            "description":entry.description,
            "amount":entry.amount,
            "ref_no":entry.ref_no
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

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
                print(info)
                data.append(info)
            return jsonify({
                "data":data
            })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })