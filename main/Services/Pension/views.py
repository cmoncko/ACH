from flask import Blueprint, request, jsonify
from main.Services.Pension.models import Pension
from main.Teams.Members.models import MemberProfile
from main.Services.Pension.models import PensionPayment
from main.extensions import db 
from datetime import datetime

pension=Blueprint('pension',__name__,url_prefix='/pension')

@pension.route('/pension-details')
def pensionDetails():
    try:
        page=request.args['page']
        per_page=request.args['per_page']
        search=request.args['search']
        if search:
            data=[]
            members=MemberProfile.query.filter(MemberProfile.name.contains(search))
            for member in members:
                member_id=member.id
                name=member.name
                details=Pension.query.filter(Pension.member_id==member_id)
                for detail in details:
                    pension_id=detail.id
                    reference_no=detail.reference_no
                    pension_amount=detail.pension_monthly
                    approval_no=detail.approval_no
                    start_date=detail.start_date
                    end_date=detail.end_date
                    pension_payments=PensionPayment.query.filter(PensionPayment.pension_id==pension_id)
                    total_issued_amount=0
                    for payment in pension_payments:
                        total_issued_amount+=payment.amount
                    status=detail.status
                    remarks=detail.remarks
                    info={
                        "reference_no":reference_no,
                        "name":name,
                        "pension_amount":pension_amount,
                        "approval_no":approval_no,
                        "start_date":start_date,
                        "end_date":end_date,
                        "total_amount_issued":total_issued_amount,
                        "status":status,
                        "remarks":remarks
                    }
                    data.append(info)
            return jsonify({
                "data":data
            })
        else:
            data=[]
            details=Pension.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            for detail in details:
                    member_id=detail.member_id
                    pension_id=detail.id
                    reference_no=detail.reference_no
                    pension_amount=detail.pension_monthly
                    approval_no=detail.approval_no
                    start_date=detail.start_date
                    end_date=detail.end_date
                    members=MemberProfile.query.filter(MemberProfile.name.contains(search))
                    for member in members:
                        name=member.name
                    pension_payments=PensionPayment.query.filter(PensionPayment.pension_id==pension_id)
                    total_issued_amount=0
                    for payment in pension_payments:
                        total_issued_amount+=payment.amount
                    status=detail.status
                    remarks=detail.remarks

                    info={
                        "reference_no":reference_no,
                        "name":name,
                        "pension_amount":pension_amount,
                        "approval_no":approval_no,
                        "start_date":start_date,
                        "end_date":end_date,
                        "total_amount_issued":total_issued_amount,
                        "status":status,
                        "remarks":remarks
                    }
                    data.append(info)
            return jsonify({
                "data":data
            })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@pension.route('/approve/<int:id>',methods=['PUT'])
def update(id):
    try:
        data=request.get_json()
        entry=Pension.query.get(id)
        if not entry:
            return jsonify({
                "message":f"no pension request for id {id}"
            })
        entry.issued_on=datetime.now().strftime("%Y-%m-%d")
        entry.status=data.get('status')
        entry.start_date=data.get('start_date')
        entry.end_date=data.get('end_date')
        entry.remarks=data.get('remarks')
        db.session.commit()
        return jsonify({
            "id":id,
            "status":data.get('status'),
            "end_date":entry.end_date,
            "start_date":entry.start_date,
            "issued_on":entry.issued_on,
            "remarks":data.get('remarks')
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })