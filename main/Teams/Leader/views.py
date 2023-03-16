from flask import Blueprint,request,jsonify
from main.Teams.Members.models import MemberProfile
from main.extensions import db

leader=Blueprint('leader',__name__,url_prefix='/leader')

@leader.route('/new-leader',methods=['POST'])
def newIncharge():
    try:
        data=request.get_json()
        user_id=data.get('user_id')
        name=data.get('name')
        DOB=data.get('DOB')
        image_path=data.get('image_path')
        gender=data.get('gender')
        address=data.get('address')
        city=data.get('city')
        district=data.get('district')
        state=data.get('state')
        pincode=data.get('pincode')
        auth_type_id=data.get('auth_type_id')
        auth_data=data.get('auth_data')
        auth_path=data.get('auth_path')
        mobile_no=data.get('mobile_no')
        join_date=data.get('join_date')
        is_leader=1
        leader_id=data.get('leader_id')
        incharge_id=data.get('incharge_id')
        status=data.get('status')
        last_status_change_date=data.get('last_status_change_date')
        comments=data.get('comments')
        nominee_name=data.get('nominee_name')
        nominee_DOB=data.get('nominee_BOB')
        nominee_relation=data.get('nominee_relation')
        nominee_mobileno=data.get('nominee_mobileno')
        nominee_adhaarno=data.get('nominee_adhaarno')

        members=MemberProfile.query.all()
        id=[]
        for i in members:
            id.append(i.user_id)
        if user_id in id:
            return jsonify({
                "message":"UserId is already exist!"
            })

        leader=MemberProfile(user_id=user_id,
                             name=name,
                             DOB=DOB,
                             image_path=image_path,
                             gender=gender,
                             address=address,
                             city=city,
                             district=district,
                             state=state,
                             pincode=pincode,
                             auth_type_id=auth_type_id,
                             auth_data=auth_data,
                             auth_path=auth_path,
                             mobile_no=mobile_no,
                             join_date=join_date,
                             is_leader=is_leader,
                             leader_id=leader_id,
                             incharge_id=incharge_id,
                             status=status,
                             last_status_change_date=last_status_change_date,
                             comments=comments,
                             nominee_name=nominee_name,
                             nominee_adhaarno=nominee_adhaarno,
                             nominee_DOB=nominee_DOB,
                             nominee_mobileno=nominee_mobileno,
                             nominee_relation=nominee_relation)

        db.session.add(leader)
        db.session.commit()
        return jsonify({
        "msg":"one leader added successfully"
        })
    except Exception as e:
        return jsonify({
        "msg":str(e)
        })

@leader.route('/show-leaders')
def showIncharges():
    try:
        search=request.args['search']
        page=request.args['page']
        per_page=request.args['per_page']
        leaders=MemberProfile.query.filter(MemberProfile.is_leader==1)
        count=0
        for i in leaders:
            count+=1
        if search:
            leader=MemberProfile.query.filter(((MemberProfile.name.contains(search)) | 
                                              (MemberProfile.mobile_no.contains(search)) | 
                                              (MemberProfile.id.contains(search)))&
                                              (MemberProfile.is_leader==1))
            return jsonify({
                "data": [MemberProfile.to_json(i) for i in leader],
                "total_members": count
            })

        else:
            leaders=MemberProfile.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            data=[]
            for leader in leaders:
                if leader.is_leader!=1:
                    continue
                data.append(MemberProfile.to_json(leader))    
            return jsonify({
                "data":data,
                "total_leaders": count
            })
        
    except Exception as e:
        return jsonify({
            "msg": str(e)
        })    
    
@leader.route('/leader-profile/<int:id>')
def leaderProfile(id):
    try:
        leader=MemberProfile.query.get(id)
        if not leader:
                return jsonify({
                    "message":"leader not exist."
                })
        if leader.is_leader!=1:
            return jsonify({
                "message":"This is not leader"
            })
        return jsonify(MemberProfile.profile(leader))
    except Exception as e:
        return jsonify({
            "erroe":str(e)
        })
    
@leader.route('/update-leader/<int:id>',methods=['PUT'])
def updateLeader(id):
    try:
        data=request.get_json()
        member=MemberProfile.query.get(id)
        if not leader:
                return jsonify({
                    "message":"leader not exist."
                })
        if member.is_leader!=1:
            return jsonify({
                "message":"This is not leader"
            })
        member.name=data.get('name')
        member.DOB=data.get('DOB')
        member.gender=data.get('gender')
        member.address=data.get('address')
        member.city=data.get('city')
        member.district=data.get('district')
        member.state=data.get('state')
        member.pincode=data.get('pincode')
        member.auth_type_id=data.get('auth_type_id')
        member.auth_data=data.get('auth_data')
        member.mobile_no=data.get('mobile_no')
        member.join_date=data.get('join_date')
        member.leader_id=data.get('leader_id')
        member.incharge_id=data.get('incharge_id')
        member.nominee_name=data.get('nominee_name')
        member.nominee_DOB=data.get('nominee_BOB')
        member.nominee_relation=data.get('nominee_relation')
        member.nominee_mobileno=data.get('nominee_mobileno')
        member.nominee_adhaarno=data.get('nominee_adhaarno')
        db.session.commit()
        return jsonify({
        "msg":"member updated successfully"
        })
    except Exception as e:
        return jsonify({
        "msg":str(e)
        })

@leader.route('/delete-leader/<int:id>',methods=['DELETE'])
def deleteLeader(id):
    try:
        leader=MemberProfile.query.get(id)
        if not leader:
                return jsonify({
                    "message":"leader not exist."
                })
        if leader.is_leader!=1:
            return jsonify({
                "message":"This is not leader"
            })
        db.session.delete(leader)
        db.session.commit()
        return jsonify({
            "message":"leader deleted successfully."
        })
    except Exception as e:
        return jsonify({
            "message":str(e)
        })