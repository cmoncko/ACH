from flask import Blueprint,jsonify,request
from main.extenstions import db
from datetime import datetime
from main.Teams.Members.models import MemberProfile
from main.Funds.Santha.models import SanthaPayments

santha=Blueprint('santha',__name__,url_prefix="/santha")

@santha.route('/pay-santha',methods=['POST'])
def paySantha():
    try:
        data=request.get_json()
        member_id=data.get('member_id')
        santha_for_year=1000
        santha_amount=data.get('santha_amount')
        santhas=SanthaPayments.query.filter(SanthaPayments.member_id==member_id)
        tamount=santha_amount
        for san in santhas:
            tamount+=san.received_amount
        received_amount=tamount
        received_date=datetime.now().strftime("%Y-%m-%d")

        member=[MemberProfile.to_json(i) for i in MemberProfile.query.filter(MemberProfile.id==member_id)]

        if len(member)<1:
            return jsonify({
                "message":"Member is not exist"
            })
        else:
            entry=SanthaPayments(member_id=member_id,
                                 santha_for_year=santha_for_year,
                                 santha_amount=santha_amount,
                                 received_amount=received_amount,
                                 received_date=received_date)

            db.session.add(entry)
            db.session.commit()

            return jsonify({
                "message":"santha details added successfully."
            })
    
    except Exception as e:
        return jsonify({
            "message":str(e)
        })

@santha.route('/santha-details')
def santhaDetails():
    try:
        page=request.args['page']
        per_page=request.args['per_page']
        search=request.args['search']
        if search:
            details=MemberProfile.query.filter((MemberProfile.id.contains(search) | 
                                                (MemberProfile.name.contains(search)) |
                                                ()))
    except Exception as e:
        return jsonify({
            "error":str(e)
        })