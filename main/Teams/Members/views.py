from flask import Blueprint,request,jsonify
from main.utils import token_required,permission_required,loger
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
        if not user_id:
            loger('warning').warning("userid must entered.")
            return jsonify({"status":False,"data":"","message":"userid must entered.","error":""}),200
        if members != None:
            loger('warning').warning("userid already exist.")
            return jsonify({"status":False,"data":"","message":"userid already exist.","error":""}),200
        members=MemberProfile.query.filter(MemberProfile.user_id==user_id).first()
        if members != None:
            loger('warning').warning("userid already exist.")
            return jsonify({"status":False,"data":"","message":"userid already exist.","error":""}),200
        name=data.get('name')
        if not name:
            loger('warning').warning("name must entered.")
            return jsonify({"status":False,"data":"","message":"name must entered.","error":""}),200
        DOB=data.get('DOB')
        if not DOB:
            loger('warning').warning("DOB must entered.")
            return jsonify({"status":False,"data":"","message":"DOB must entered.","error":""}),200
        image_path=data.get('image_path')
        gender=data.get('gender')
        address=data.get('address')
        if not address:
            loger('warning').warning("address must entered.")
            return jsonify({"status":False,"data":"","message":"address must entered.","error":""}),200
        city=data.get('city')
        if not city:
            loger('warning').warning("city must entered.")
            return jsonify({"status":False,"data":"","message":"city must entered.","error":""}),200
        district=data.get('district')
        if not district:
            loger('warning').warning("district must entered.")
            return jsonify({"status":False,"data":"","message":"district must entered.","error":""}),200
        state=data.get('state')
        if not state:
            loger('warning').warning("state must entered.")
            return jsonify({"status":False,"data":"","message":"state must entered.","error":""}),200
        pincode=data.get('pincode')
        if not pincode:
            loger('warning').warning("pincode must entered.")
            return jsonify({"status":False,"data":"","message":"pincode must entered.","error":""}),200
        auth_type_id=data.get('auth_type_id')
        auth_data=data.get('auth_data')
        if not auth_data:
            loger('warning').warning("auth data must entered.")
            return jsonify({"status":False,"data":"","message":"auth data must entered.","error":""}),200
        auth_path=data.get('auth_path')
        mobile_no=data.get('mobile_no')
        if not mobile_no:
            loger('warning').warning("mobile no must entered.")
            return jsonify({"status":False,"data":"","message":"mobile no must entered.","error":""}),200
        join_date=data.get('join_date')
        if not join_date:
            loger('warning').warning("join date must entered.")
            return jsonify({"status":False,"data":"","message":"join date must entered.","error":""}),200
        is_leader=0
        leader_id=data.get('leader_id')
        if not leader_id:
            loger('warning').warning("leader id must entered.")
            return jsonify({"status":False,"data":"","message":"leader id must entered.","error":""}),200
        incharge_id=data.get('incharge_id')
        if not incharge_id:
            loger('warning').warning("incharge id must entered.")
            return jsonify({"status":False,"data":"","message":"incharge id must entered.","error":""}),200
        status=data.get('status')
        last_status_change_date=data.get('last_status_change_date')
        comments=data.get('comments')
        nominee_name=data.get('nominee_name')
        if not nominee_name:
            loger('warning').warning("nominee name must entered.")
            return jsonify({"status":False,"data":"","message":"nominee name must entered.","error":""}),200
        nominee_DOB=data.get('nominee_BOB')
        nominee_relation=data.get('nominee_relation')
        if not nominee_relation:
            loger('warning').warning("nominee relation must entered.")
            return jsonify({"status":False,"data":"","message":"nominee relation must entered.","error":""}),200
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
        loger("info").info("one member added successfully,")
        return jsonify({"status":True,"data":MemberProfile.to_json(member),"msg":"one member added successfully,","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
    
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
            data=[MemberProfile.to_json(i) for i in member]
            if not data:
                loger('warning').warning("no data returned.")
                return jsonify({"status":False,"data":"","message":"no data returned.","error":""}),200
            loger("info").info("member(s) viewed.")
            return jsonify({"status":True,"data": data,"total_members": all_members.total,"error":""}),201

        else:
            members=MemberProfile.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            data=[MemberProfile.to_json(member) for member in members.items]
            if not data:
                loger('warning').warning("no data returned.")
                return jsonify({"status":False,"data":"","message":"no data returned.","error":""}),200
            loger("info").info("member(s) viewed.")
            return jsonify({"status":True,"data": data,"total_members": all_members.total,"error":""}),201
        
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
    
@member.route('/member-profile/<int:id>')
@token_required
@permission_required('read_team')
def memProfile(id):
    try:
        member=MemberProfile.query.get(id)
        if not member:
                loger('warning').warning("member not exist.")
                return jsonify({"status":False,"data":"","message":"member not exist.","error":""}),200
        if member.is_leader!=0:
            loger('warning').warning("This is not member.")            
            return jsonify({"status":False,"message":"This is not member","error":""}),200
        return jsonify(MemberProfile.profile(member))
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
    
@member.route('/update-member/<int:id>',methods=['PUT'])
@token_required
@permission_required('edit_team')
def updateMembers(id):
    try:
        data=request.get_json()
        member=MemberProfile.query.get(id)
        if not member:
                loger('warning').warning("member not exist.")
                return jsonify({"status":False,"data":"","message":"member not exist.","error":""}),200
        if member.is_leader!=0:
            loger('warning').warning("This is not member.")            
            return jsonify({"status":False,"message":"This is not member","error":""}),200
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
        loger("info").info("member updated successfully,")
        return jsonify({"status":True,"data":MemberProfile.to_json(member),"msg":"member updated successfully,","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
    
@member.route('/delete-member/<int:id>',methods=['DELETE'])
@token_required
@permission_required('delete_team')
def deletemember(id):
    try:
        member=MemberProfile.query.get(id)
        if not member:
            loger('warning').warning("member not exist.")
            return jsonify({"status":False,"data":"","message":"member not exist.","error":""}),200
        if member.is_leader!=0:
            loger('warning').warning("This is not member.")            
            return jsonify({"status":False,"message":"This is not member","error":""}),200
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
            loger('warning').warning("can't delete member, loan(or)pension is active.")            
            return jsonify({"status":False,"message":"can't delete member, loan(or)pension is active.","error":""}),200
        db.session.delete(member)
        db.session.commit()
        loger("info").info("member deleted successfully,")
        return jsonify({"status":True,"data":MemberProfile.to_json(member),"msg":"member deleted successfully,","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500