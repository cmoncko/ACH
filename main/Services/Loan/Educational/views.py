from flask import Blueprint, request, jsonify
from main.utils import token_required,permission_required,loger
from main.Services.Loan.Educational.models import EducationalLoanPayment,EducationLoans
from main.Teams.Members.models import MemberProfile
from main.extensions import db
from datetime import datetime

educational_loan=Blueprint('educational_loan',__name__,url_prefix='/educational-loan')
warning="warning"
info="info"
error="error"

@educational_loan.route('/all-loans')
def showAllLoans():
    try:
        page=int(request.args['page'])
        per_page=int(request.args['per_page'])
        search=request.args['search']
        if search:
            members=MemberProfile.query.filter(MemberProfile.name.contains(search))
            data=[]
            for member in members:
                id=member.id
                name=member.name
                loans=EducationLoans.query.filter(EducationLoans.member_id==id)
                for loan in loans:
                    EL_id=loan.id
                    ref_no=loan.ref_no
                    loan_amount=loan.loan_amount
                    approval_no=loan.approval_no
                    loan_approved_date=loan.loan_approved_date
                    tenure=str(loan.number_of_emi)+" months"
                    EMI=loan.EMI_amount
                    issued_on=loan.issued_on
                    status=loan.status
                    info={
                        "EL_id":EL_id,
                        "name":name,
                        "ref_no":ref_no,
                        "loan_amount":loan_amount,
                        "approval_no":approval_no,
                        "loan_approved_date":loan_approved_date,
                        "tenure":tenure,
                        "EMI":EMI,
                        "issued_on":issued_on,
                        "status":status
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
            loans=EducationLoans.query.paginate(page=page,per_page=per_page,error_out=False)
            for loan in loans:
                    mem_id=loan.member_id
                    EL_id=loan.id
                    ref_no=loan.ref_no
                    loan_amount=loan.loan_amount
                    approval_no=loan.approval_no
                    loan_approved_date=loan.loan_approved_date
                    tenure=str(loan.number_of_emi)+" months"
                    EMI=loan.EMI_amount
                    issued_on=loan.issued_on
                    status=loan.status
                    if status==1:
                        all_emis=EducationalLoanPayment.query.filter(EducationalLoanPayment.loan_id==EL_id)
                        penalty_ids=[]
                        for emi in all_emis:
                            if int(emi.penalty_amount)==200:
                                continue
                            dateNow=datetime.now().strftime("%Y-%m-%d").split('-')
                            month=int(dateNow[1])
                            year=int(dateNow[0])
                            date=int(dateNow[2])
                            if int(emi.penalty_amount)==200:
                                continue
                            elif emi.month<=month and emi.year==year and date>5:
                                penalty_ids.append(emi.id)
                        if len(penalty_ids)<1:
                            pass
                        else:
                            for emi_id in penalty_ids:
                                entry=EducationalLoanPayment.query.get(emi_id)
                                entry.penalty_amount=200
                                entry.total_amount=entry.amount+200
                                db.session.commit()

                    members=MemberProfile.query.filter(MemberProfile.id==mem_id).first()
                    name=members.name
                    info={
                        "EL_id":EL_id,
                        "name":name,
                        "ref_no":ref_no,
                        "loan_amount":loan_amount,
                        "approval_no":approval_no,
                        "loan_approved_date":loan_approved_date,
                        "tenure":tenure,
                        "EMI":EMI,
                        "issued_on":issued_on,
                        "status":status
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
    
@educational_loan.route('/issue/<int:id>',methods=['PUT'])
def issue(id):
    try:
        data=request.get_json()
        issued_on=data.get('issued_on')
        if not issued_on:
            message="issued_on must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        status=data.get('status')
        if not status:
            message="status must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        comments=data.get('comments')
        loan=EducationLoans.query.get(id)
        if not loan:
            message="loan not exist"
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        loan.issued_on=issued_on
        loan.comments=comments
        loan.status=status

        date_list=str(loan.EMI_start_date).split('-')
        month=int(date_list[1])#8
        year=int(date_list[0])
        for i in range(loan.number_of_emi):#24
            entry=EducationalLoanPayment(member_id=loan.member_id,
                                     loan_id=id,
                                     month=month,
                                     year=year,
                                     emi_count=loan.number_of_emi,
                                     amount=loan.EMI_amount,
                                     total_amount=loan.EMI_amount
                                     )
            db.session.add(entry)
            db.session.commit()
            month+=1
            if month>12:
                month=1
                year+=1
        data=[{"EL_id":id,"issued_on":loan.issued_on,"comments":loan.comments,"status":loan.status}]
        message=f"Loan issued, id:{id}"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),204
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
     
@educational_loan.route('/all-emi/<int:id>')
def allLoan(id):
    try:
        details=EducationalLoanPayment.query.filter(EducationalLoanPayment.loan_id==id)
        data=[]
        for detail in details:
            id=detail.id
            EMI_amount=detail.amount
            penalty_amount=detail.penalty_amount
            total_amount=detail.total_amount
            paid_date=detail.paid_date
            status=detail.status
            info={"id":id,
                  "EMI_amount":EMI_amount,
                  "penalty_amount":penalty_amount,
                  "total_amount":total_amount,
                  "paid_date":paid_date,
                  "status":status}
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
    
@educational_loan.route('/pay-loan/<int:id>',methods=['PUT'])
def payloan(id):
    try:
        data=request.get_json()
        emi=EducationalLoanPayment.query.get(id)
        if not emi:
            message="emi not exist."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        emi.status=data.get('status')
        if not data.get('status'):
            message="status must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        emi.paid_date=data.get('paid_date')
        if not data.get('paid_date'):
            message="paid_date must be entered."
            loger(warning).warning(message)
            return jsonify({"status":False,"data":"","message":message,"error":""}),200
        db.session.commit()
        data=[{"id":id,
            "status":emi.status,
            "month":emi.month,
            "year":emi.year,
            "paid_date":emi.paid_date,
            "amount":emi.amount ,
            "penalty":emi.penalty_amount,
            "total":emi.total_amount}]
        message="loan paid"
        loger(info).info(message)
        return jsonify({"status":True,"data":data,"message":message,"error":""}),204
    except Exception as e:
        loger(error).error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500