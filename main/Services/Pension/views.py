from flask import Blueprint, request, jsonify, session
from main.utils import token_required,permission_required,loger
from main.Services.Pension.models import Pension
from main.Teams.Members.models import MemberProfile
from main.Services.Pension.models import PensionPayment
from main.extensions import db 
from datetime import datetime

pension=Blueprint('pension',__name__,url_prefix='/pension')
info="info"
warning="warning"
error="error"

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
                        "id":detail.id,
                        "member_id":member_id,
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
            if not data:
                message="No data"
                loger(warning).warning(message)
                return jsonify({"status":False,"data":data,"message":message,"error":""}),200
            message="data returned"
            loger(info).info(message)
            return jsonify({"status":True,"data":data,"message":message,"error":""}),200
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
                        member_id=member.id
                    pension_payments=PensionPayment.query.filter(PensionPayment.pension_id==pension_id)
                    total_issued_amount=0
                    for payment in pension_payments:
                        total_issued_amount+=payment.amount
                    status=detail.status
                    remarks=detail.remarks

                    info={
                        "id":detail.id,
                        "member_id":member_id,
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
    
@pension.route('/approve/<int:id>',methods=['PUT'])
def update(id):
    try:
        data=request.get_json()
        user=session.get('loginData')
        user_id=user.get('userId')
        entry=Pension.query.get(id)
        if not entry:
            message="pension not exist"
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        entry.issued_on=datetime.now().strftime("%Y-%m-%d")
        entry.status=data.get('status')
        if not data.get('status'):
            message="status must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        entry.start_date=data.get('start_date')
        if not data.get('start_date'):
            message="start_date must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        entry.end_date=data.get('end_date')
        entry.approved_by=user_id
        entry.remarks=data.get('remarks')
        db.session.commit()
        data=[{"id":id,
             "status":entry.status,
             "end_date":entry.end_date,
             "start_date":entry.start_date,
             "issued_on":entry.issued_on,
             "remarks":entry.remarks
              }]
        message=f"Pension approved for id: {id}"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),204
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500

@pension.route('/pay-pension',methods=['POST'])
def payPension():
    try:
        data=request.get_json()
        member_id=data.get('member_id')
        if not member_id or member_id=="":
            message="end_date must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        month=data.get('month')
        year=data.get('year')
        if not year or month:
            message="year (or) month must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        paid_date=data.get('paid_date')
        if not paid_date or paid_date=="":
            message="paid_date must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        amount=data.get('amount')
        if not amount or amount=="":
            message="amount must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        pension_id=data.get('pension_id')
        if not pension_id or pension_id=="":
            message="pension_id must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        detail=Pension.query.get(pension_id)
        if not detail:
            msg="pension not exist."
            loger(warning).warning(msg)
            return jsonify({"status":False,"data":"","message":msg,"error":""}),200
        if detail.status==(0 or 2 or 3):
            msg="pension have to approved."
            loger(warning).warning(msg)
            return jsonify({"status":False,"data":"","message":msg,"error":""}),200
        entry=PensionPayment(member_id=member_id,
                             pension_id=pension_id,
                             amount=amount,
                             month=month,
                             year=year,
                             paid_date=paid_date)
        db.session.add(entry)
        db.session.commit()
        data=[{"id":entry.id,
               "member_id":entry.member_id,
               "pension_id":entry.pension_id,
               "paid_date":entry.paid_date,
               "amountt":entry.amount,
               "year":entry.year,
               "month":entry.month
               }]
        message=f"Pension payment entered, id: {entry.id}"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),201
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500

@pension.route('/profile/<int:id>')
def veiwPayment(id):
    try:
        data=[]
        member=MemberProfile.query.get(id)
        if not member:
            loger('warning').warning("member not exist.")
            return jsonify({"status":False,"data":"","message":"member not exist.","error":""}),200
        payments=PensionPayment.query.filter(PensionPayment.member_id==id)
        for payment in payments:
            payment_id=payment.id
            amount=payment.amount
            month=payment.month
            year=payment.year
            paid_on=payment.paid_date
            info={
                "payment_id":payment_id,
                "member_id":member.id,
                "amount":amount,
                "month":month,
                "year":year,
                "paid_on":paid_on
            } 
            data.append(info)
        if not data:
            message="No data"
            loger(warning).warning(message)
            return jsonify({"status":False,"data":data,"message":message,"error":""}),200
        message="pension payment(s) showed"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),200
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
