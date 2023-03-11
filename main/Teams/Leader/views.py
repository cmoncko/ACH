from flask import Blueprint,request,jsonify
from main.Teams.Members.models import MemberProfile
from main.extensions import db
from main.Teams.Incharge.models import Employee

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
                "data": [Employee.to_json(i) for i in leader],
                "total_members": count
            })

        else:
            leaders=MemberProfile.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            data=[]
            for leader in leaders:
                if leader.is_leader!=1:
                    continue
                data.append(Employee.to_json(leader))    
            return jsonify({
                "data":data,
                "total_leaders": count
            })
        
    except Exception as e:
        return jsonify({
            "msg": str(e)
        })    
    
