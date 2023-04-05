from flask import Blueprint,request,jsonify,session
from main.utils import token_required,permission_required,loger
from main.Services.AccountClosing.models import AccountClosing
from main.Teams.Members.models import MemberProfile
from main.extensions import db

account_closing=Blueprint('accountclosing',__name__,url_prefix="/account-closing")
warning="warning"
info="info"
error="error"

@account_closing.route('/show')
def show():
    try:
        page=request.args['page']
        per_page=request.args["per_page"]
        search= request.args['search']
        if search:
            data=[]
            member=MemberProfile.query.filter(MemberProfile.name.contains(search))
            for i in member:
                member_id=i.id
                name=i.name
                details=AccountClosing.query.filter(AccountClosing.member_id==member_id)
                for i in details:
                    id=i.id
                    member_id=i.member_id
                    status=i.status
                    closed_by=i.closed_by
                    closed_on=i.closed_on
                    remarks=i.remarks
                    reference_no=i.reference_no
                    request_id=i.request_id
                    info={
                        "id":id,
                        "member_id":member_id,
                        "status":status,
                        "closed_by":closed_by,
                        "closed_on":closed_on,
                        "remarks":remarks,
                        "reference_no":reference_no,
                        "request_id":request_id,
                        "name":name
                        }
                    data.append(info)
            if not data:
                message="No data"
                loger(warning).warning(message)
                return jsonify({"status":False,"data":data,"message":message,"error":""}),200
            message="data returned"
            loger(info).info(message)
            return jsonify({"status":True,"data":data,"message":message,"error":""}),204
        else:
            data=[]
            details=AccountClosing.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            for i in details:
                mem_id=i.member_id
                name=MemberProfile.query.get(mem_id).name
                id=i.id
                status=i.status
                closed_by=i.closed_by
                closed_on=i.closed_on
                remarks=i.remarks
                reference_no=i.reference_no
                request_id=i.request_id
                info={"id":id,
                    "member_id":member_id,
                    "status":status,
                    "closed_by":closed_by,
                    "closed_on":closed_on,
                    "remarks":remarks,
                    "reference_no":reference_no,
                    "request_id":request_id,
                    "name":name
                    }
                data.append(info)
            if not data:
                message="No data"
                loger(warning).warning(message)
                return jsonify({"status":False,"data":data,"message":message,"error":""}),200
            message="data returned"
            loger(info).info(message)
            return jsonify({"status":True,"data":data,"message":message,"error":""}),204
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500

@account_closing.route("/update/<int:id>",methods=['PUT'])
def update(id):
    try:
        user=session.get("userData")
        user_id=user.get("userId")
        data =request.get_json()
        entry=AccountClosing.query.get(id)
        if not entry:
            message="closing request not exist"
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        status=data.get("status")
        if not status:
            message="status must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        closed_on=data.get("closed_on")
        if not closed_on:
            message="closed_on must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        remarks=data.get("remarks")
        entry.status=status
        entry.closed_by=user_id
        entry.closed_on=closed_on
        entry.remarks=remarks

        db.session.commit()
        data={"id":entry.id,
            "status":entry.status,
            "closed_by":entry.closed_by,
            "closed_on":entry.closed_on,
            "remarks":entry.remarks}
        message=f"Closing request accepted, id:{id}"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),204
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500

    



                    


        
