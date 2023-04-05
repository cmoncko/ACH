from flask import Blueprint, request, jsonify
from main.utils import token_required,permission_required,loger
from main.Services.Benefits.models import Benefits
from main.Settings.Services.models import BenefitType
from main.Teams.Members.models import MemberProfile
from main.extensions import db

benefits=Blueprint('benefits',__name__,url_prefix='/benefits')
warning="warning"
info="info"
error="error"

@benefits.route('/all-benefits')
def allBenefits():
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
                details=Benefits.query.filter(Benefits.member_id==member_id)
                for detail in details:
                    reference_no=detail.reference_no
                    benefit_type_id=detail.benefit_type_id
                    benefit_type=BenefitType.query.get(benefit_type_id).name
                    approval_no=detail.approval_no
                    approved_on=detail.approved_on
                    issued_on=detail.issued_on
                    status=detail.status
                    remarks=detail.remarks
                    info={
                        "reference_no":reference_no,
                        "name":name,
                        "benefit_type":benefit_type,
                        "approval_no":approval_no,
                        "approved_on":approved_on,
                        "issued_on":issued_on,
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
            details=Benefits.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            for detail in details:
                member_id=detail.member_id
                benefit_type_id=detail.benefit_type_id
                benefit_type=BenefitType.query.get(benefit_type_id).name
                reference_no=detail.reference_no
                approval_no=detail.approval_no
                approved_on=detail.approved_on
                issued_on=detail.issued_on
                status=detail.status
                remarks=detail.remarks
                members=MemberProfile.query.filter(MemberProfile.id==member_id)
                for member in members:
                    name=member.name

                info={
                    "reference_no":reference_no,
                    "name":name,
                    "benefit_type":benefit_type,
                    "approval_no":approval_no,
                    "approved_on":approved_on,
                    "issued_on":issued_on,
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

@benefits.route('/approve/<int:id>',methods=['PUT'])
def update(id):
    try:
        data=request.get_json()
        entry=Benefits.query.get(id)
        if not entry:
            message="benefit not exist"
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        entry.issued_on=data.get('issued_on')
        if not data.get('issued_on'):
            message="issued_on must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        entry.status=data.get('status')
        if not data.get('status'):
            message="status must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        entry.remarks=data.get('remarks')
        db.session.commit()
        data=[{"id":id,
            "status":data.get('status'),
            "issued_on":data.get('issued_on'),
            "remarks":data.get('remarks')
        }]
        message=f"Benefit approved, id:{id}"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),204
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500