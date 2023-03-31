from flask import Blueprint,request,jsonify,session
from main.Services.AccountClosing.models import AccountClosing
from main.Teams.Members.models import MemberProfile
from main.extensions import db

account_closing=Blueprint('accountclosing',__name__,url_prefix="/account-closing")

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
                    i=i.id
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
            return jsonify({
                "data":data
            })
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
            return jsonify({
                "data":data
            })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@account_closing.route("/update/<int:id>",methods=['PUT'])
def update(id):
    try:
        
        user=session.get("userData")
        user_id=user.get("userId")
        data =request.get_json()
        entry=AccountClosing.query.get(id)
        status=data.get("status")
        closed_on=data.get("closed_on")
        remarks=data.get("remarks")
        entry.status=status
        entry.closed_by=user_id
        entry.closed_on=closed_on
        entry.remarks=remarks

        db.session.commit()

        return jsonify({
            "status":entry.status,
            "closed_by":entry.closed_by,
            "closed_on":entry.closed_on,
            "remarks":entry.remarks
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

    



                    


        