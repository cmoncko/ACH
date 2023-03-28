from flask import Blueprint,request,jsonify
from main.utils import token_required,permission_required
from main.extensions import db
from main.Teams.Members.models import MemberProfile
from main.Services.Loan.Business.models import BusinessLoans
from main.Services.Loan.Educational.models import EducationLoans
from main.Services.Loan.Savings.models import SavingsLoans
from main.Services.Pension.models import Pension

member=Blueprint('member',__name__,url_prefix='/member')

@member.route('/add-member',methods=['POST'])
@token_required
@permission_required('edit_team')
def AddMembers():
    try:
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
@token_required
@permission_required('read_team')
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
        
    except Exception as e:
        return jsonify({
            "msg": str(e)
        })
    
@member.route('/member-profile/<int:id>')
@token_required
@permission_required('read_team')
def memProfile(id):
    try:
        member=MemberProfile.query.get(id)
        if not member:
                return jsonify({
                    "message":"member not exist."
                })
        if member.is_leader!=0:
            return jsonify({
                "message":"This is not member"
            })
        return jsonify(MemberProfile.profile(member))
    except Exception as e:
         return jsonify({
             "error":str(e)
        })
    
@member.route('/update-member/<int:id>',methods=['PUT'])
@token_required
@permission_required('edit_team')
def updateMembers(id):
    try:
        data=request.get_json()
        member=MemberProfile.query.get(id)
        if not member:
                return jsonify({
                    "message":"member not exist."
                })
        if member.is_leader!=1:
            return jsonify({
                "message":"This is not member"
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
    
@member.route('/delete-member/<int:id>',methods=['DELETE'])
@token_required
@permission_required('delete_team')
def deletemember(id):
    try:
        member=MemberProfile.query.get(id)
        if not member:
                return jsonify({
                    "message":"member not exist."
                })
        if member.is_leader!=0:
            return jsonify({
                "message":"This is not member"
            })
        SL_loan_active=False
        BL_loan_active=False
        EL_loan_active=False
        pension_active=False
        pension=Pension.query.filter(Pension.member_id==id)
        # SL_loan=SavingsLoans.query.filter(SavingsLoans.member_id==id)
        SL_loan=SavingsLoans.query.filter((SavingsLoans.member_id==id)&(SavingsLoans.status==1)).count()
        print(SL_loan)
        BL_loan=BusinessLoans.query.filter(BusinessLoans.member_id==id)
        EL_loan=EducationLoans.query.filter(EducationLoans.member_id==id)
        for i in SL_loan:
            if i.status==1:
                SL_loan_active=True
        for i in BL_loan:
            if i.status==1:
                BL_loan_active=True
        for i in EL_loan:
            if i.status==1:
                EL_loan_active=True
        for i in pension:
            if i.status==1:
                pension_active=True
        if EL_loan_active or BL_loan_active or SL_loan_active or pension_active:
            return jsonify({
                    "message":"can't delete member, loan(or)pension is active."
            })
        db.session.delete(member)
        db.session.commit()
        return jsonify({
            "message":"member deleted successfully."
        })
    except Exception as e:
        return jsonify({
            "message":str(e)
        })