from flask import Blueprint,request,jsonify
from main.extensions import db
from main.Teams.Members.models import MemberProfile

member=Blueprint('member',__name__,url_prefix='/member')

@member.route('/add-member',methods=['POST'])
def AddMembers():
    data=request.get_json()
    user_id=data.get('user_id')
    members=MemberProfile.query.filter(MemberProfile.user_id==user_id)
    memberExist=False
    for member in members:
        memberExist=True
    if memberExist:
        return jsonify({
            "message":"userid already exist."
        })
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
    is_leader=0
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

    try:
        member=MemberProfile(user_id=user_id,
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

        db.session.add(member)
        db.session.commit()
        return jsonify({
        "msg":"one member added successfully"
        })
    except Exception as e:
        return jsonify({
        "msg":str(e)
        })
    
@member.route('/show-members')
def showMembers():
    try:
        search=request.args['search']
        page=request.args['page']
        per_page=request.args['per_page']
        all_members=MemberProfile.query.paginate(page=0,per_page=0,error_out=False)
        if search:
            member=MemberProfile.query.filter((MemberProfile.name.contains(search)) | 
                                              (MemberProfile.mobile_no.contains(search)) | 
                                              (MemberProfile.id.contains(search)))
            return jsonify({
                "data": [MemberProfile.to_json(i) for i in member],
                "total_members": all_members.total
            })

        else:
            members=MemberProfile.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            return jsonify({
                "data":[MemberProfile.to_json(member) for member in members.items],
                "total_members": all_members.total
            })
        
        # else:
        #     members=MemberProfile.query.all()
        #     print(members)
        #     return jsonify({
        #         "data":[MemberProfile.to_json(member) for member in members]
        #     })
        
    except Exception as e:
        return jsonify({
            "msg": str(e)
        })
