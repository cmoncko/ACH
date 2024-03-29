from flask import Blueprint,jsonify,request, session
from main.utils import token_required,permission_required,loger
from main.Services.Requests.models import LoanRequest
from main.Teams.Members.models import MemberProfile
from main.Services.Benefits.models import Benefits
from main.Services.Pension.models import Pension
from main.Services.Loan.Savings.models import SavingsLoans
from main.Services.Loan.Business.models import BusinessLoans
from main.Services.Loan.Educational.models import EducationLoans
from main.Services.AccountClosing.models import AccountClosing
from main.extensions import db
from datetime import datetime
import uuid

requests=Blueprint('request',__name__,url_prefix='/request')

@requests.route('/send-request',methods=['POST'])
def sendRequest():
    try:
        data=request.get_json()

        requested_by=data.get('requested_by')
        if not requested_by:
            loger('warning').warning("requested_by must entered.")
            return jsonify({"status":False,"data":"","message":"requested_by must entered.","error":""}),200
        appied_on=data.get('applied_on')
        if not appied_on:
            loger('warning').warning("appied_on must entered.")
            return jsonify({"status":False,"data":"","message":"appied_on must entered.","error":""}),200
        comments=data.get('comments')
        request_loan_type=data.get('request_loan_type')
        if not request_loan_type:
            loger('warning').warning("request_loan_type must entered.")
            return jsonify({"status":False,"data":"","message":"request_loan_type must entered.","error":""}),200

        member=MemberProfile.query.filter(MemberProfile.id==requested_by).first()

        if not member:
            loger('warning').warning("member not exist.")
            return jsonify({"status":False,"data":"","message":"member not exist.","error":""}),200

        if request_loan_type==0 or request_loan_type==1 or request_loan_type==2:
            loan_amount=data.get('loan_amount')
            if not loan_amount:
                loger('warning').warning("loan_amount must entered.")
                return jsonify({"status":False,"data":"","message":"loan_amount must entered.","error":""}),200
            number_of_emi=data.get('number_of emi')
            if not loan_amount:
                loger('warning').warning("loan_amount must entered.")
                return jsonify({"status":False,"data":"","message":"loan_amount must entered.","error":""}),200
            EMI_amount=(loan_amount/number_of_emi)
            interest_rate=float(f"{(EMI_amount*0.08):.2f}")
            EMI_amount=float(f"{EMI_amount:.2f}")
            final_payable_amount=float(f"{(EMI_amount*number_of_emi):.2f}")

            entry=LoanRequest(requested_by=requested_by,
                          appied_on=appied_on,
                          EMI_amount=EMI_amount,
                          comments=comments,
                          request_loan_type=request_loan_type,
                          loan_amount=loan_amount,
                          number_of_emi=number_of_emi,
                          interest_rate=interest_rate,
                          final_payable_amount=final_payable_amount)

        if request_loan_type==3:
            benefit_type_id=data.get('benefit_type_id')
            if not benefit_type_id:
                loger('warning').warning("benefit_type_id must entered.")
                return jsonify({"status":False,"data":"","message":"benefit_type_id must entered.","error":""}),200
            if not Benefits.query.get(benefit_type_id):
                loger('warning').warning("benefit not exist.")
                return jsonify({"status":False,"data":"","message":"benefit not exist.","error":""}),200
            entry=LoanRequest(requested_by=requested_by,
                          appied_on=appied_on,
                          comments=comments,
                          request_loan_type=request_loan_type,
                          benefit_type_id=benefit_type_id,)
        if request_loan_type==4:
            pension_monthly_amount=data.get('pension_monthly_amount')
            if not pension_monthly_amount:
                loger('warning').warning("pension_monthly_amount must entered.")
                return jsonify({"status":False,"data":"","message":"pension_monthly_amount must entered.","error":""}),200
            entry=LoanRequest(requested_by=requested_by,
                          appied_on=appied_on,
                          comments=comments,
                          request_loan_type=request_loan_type,
                          pension_monthly_amount=pension_monthly_amount)
        
        if request_loan_type==5:
            entry=LoanRequest(requested_by=requested_by,
                          appied_on=appied_on,
                          comments=comments,
                          request_loan_type=request_loan_type)

        db.session.add(entry)
        db.session.commit()
        loger("info").info("request sended successfully,")
        return jsonify({"status":True,"data":MemberProfile.to_json(member),"msg":"request sended successfully,","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500

@requests.route('/show-details')
def showDetails():
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
                details=LoanRequest.query.filter(LoanRequest.requested_by==member_id)
                for detail in details:
                    loan_id=detail.id
                    request_type=detail.request_loan_type
                    applied_date=detail.appied_on
                    applied_on=str(applied_date)
                    date=str(detail.approved_on)
                    
                    #calculate days elapsed
                    if date=="None":
                        date_list=str(applied_on).split('-')
                        x=datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
                        y=datetime.now()
                        a=x.strftime("%j")
                        b=y.strftime("%j")
                    else:
                        date_list=str(applied_on).split('-')
                        date_list2=str(date).split('-')
                        x=datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
                        y=datetime(int(date_list2[0]),int(date_list2[1]),int(date_list2[2]))
                        a=x.strftime("%j")
                        b=y.strftime("%j")
                    days_elapsed=int(b)-int(a)

                    approval_status=detail.status

                    info={
                        "id":loan_id,
                        "name":name,
                        "request_type":request_type,
                        "applied_on":applied_on,
                        "days_elapsed":days_elapsed,
                        "approval_status":approval_status,
                        "date":date
                    }
                    data.append(info)
            if not data:
                loger("warning").warning("no data returned")
                return jsonify({"status":False,"data":"","msg":"","error":""}),200
            loger("info").info("request(s) viewed.")
            return jsonify({"status":True,"data":data,"msg":"","error":""}),200
        else:
            data=[]
            details=LoanRequest.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            for detail in details:
                loan_id=detail.id
                member_id=detail.requested_by
                request_type=detail.request_loan_type
                applied_date=detail.appied_on
                applied_on=str(applied_date)
                date=str(detail.approved_on)
                    
                #calculate days elapsed
                if date=="None":
                    date_list=str(applied_on).split('-')
                    x=datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
                    y=datetime.now()
                    a=x.strftime("%j")
                    b=y.strftime("%j")
                else:
                    date_list=str(applied_on).split('-')
                    date_list2=str(date).split('-')
                    x=datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
                    y=datetime(int(date_list2[0]),int(date_list2[1]),int(date_list2[2]))
                    a=x.strftime("%j")
                    b=y.strftime("%j")
                
                days_elapsed=int(b)-int(a)
                approval_status=detail.status
                members=MemberProfile.query.filter(MemberProfile.id==member_id)
                for member in members:
                    name=member.name

                info={
                    "id":loan_id,
                    "name":name,
                    "request_type":request_type,
                    "applied_on":applied_on,
                    "days_elapsed":days_elapsed,
                    "approval_status":approval_status,
                    "date":date
                }
                data.append(info)
            if not data:
                loger("warning").warning("no data returned")
                return jsonify({"status":False,"data":"","msg":"","error":""}),200
            loger("info").info("request(s) viewed.")
            return jsonify({"status":True,"data":data,"msg":"","error":""}),200

    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500

@requests.route('profile/<int:id>')
def profileDetails(id):
    try:
        detail=LoanRequest.query.get(id)
        if not detail:
            loger('warning').warning("request not exist.")
            return jsonify({"status":False,"data":"","message":"request not exist.","error":""}),200
        data=[]
        loan_id=detail.id
        request_type=detail.request_loan_type
        approved_date=detail.approved_on
        approval_status=detail.status
        info ={
            "id":loan_id,
            "request_type":request_type,
            "approved_date":approved_date,
            "approval_status":approval_status
        }
        data.append(info)
        if not data:
                loger("warning").warning("no data returned")
                return jsonify({"status":False,"data":"","msg":"","error":""}),200
        loger("info").info("request(s) viewed.")
        return jsonify({"status":True,"data":data,"msg":"","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
    
@requests.route('/approve/<int:id>',methods=['PUT'])
def approve(id):
    try:
        user=session.get('loginData')
        user_id=user.get('userId')
        data=request.get_json()
        loan_request=LoanRequest.query.get(id)
        if not loan_request:
            loger('warning').warning("request not exist.")
            return jsonify({"status":False,"data":"","message":"request not exist.","error":""}),200
        loan_request.status=data.get('status')
        loan_request.approved_on=data.get('approved_on')
        loan_request.comments=data.get('comments')
        loan_request.action_by_user=user_id

        if data.get('status')==1:

            #Benefits
            if loan_request.request_loan_type==3:
                entry=Benefits(member_id=loan_request.requested_by,
                               benefit_type_id=loan_request.benefit_type_id,
                               approved_by=user_id,
                               approved_on=loan_request.approved_on,
                               reference_no=uuid.uuid4().hex[:8],
                               approval_no=loan_request.id)
                db.session.add(entry)

            #Pension 
            elif loan_request.request_loan_type==4:
                pension_details=Pension.query.filter(Pension.member_id==loan_request.requested_by)
                for i in pension_details:
                    loger('warning').warning("already pension exist.")
                    return jsonify({"status":False,"data":"","message":"already pension exist.","error":""}),200
                entry=Pension(member_id=loan_request.requested_by,
                              approved_by=user_id,
                              pension_monthly_payment=loan_request.pension_monthly_amount,
                              approved_on=loan_request.approved_on,
                              reference_no=uuid.uuid4().hex[:8],
                              approval_no=loan_request.id)
                db.session.add(entry)
                
            #Savings Loan
            elif loan_request.request_loan_type==0:
                saving_loan=SavingsLoans.query.filter(SavingsLoans.member_id==loan_request.requested_by).first()
                if saving_loan:
                    loger('warning').warning("already saving_loan exist.")
                    return jsonify({"status":False,"data":"","message":"already saving_loan exist.","error":""}),200
                EMI_start_date=data.get('EMI_start_date')
                date_list=EMI_start_date.split('-')
                if loan_request.number_of_emi==12:
                    year=int(date_list[0])+1
                else:
                    year=int(date_list[0])+2
                loan_end_date=f'{year}-{int(date_list[1])-1}-{date_list[2]}'
                entry=SavingsLoans(member_id=loan_request.requested_by,
                              loan_amount=loan_request.loan_amount,
                              number_of_emi=loan_request.number_of_emi,
                              loan_approved_by=user_id,
                              EMI_amount=loan_request.EMI_amount,
                              interest_rate=loan_request.interest_rate,
                              finaly_payable_amount=loan_request.final_payable_amount,
                              monthly_penalty_amount=200,
                              EMI_start_date=EMI_start_date,
                              loan_end_date=loan_end_date,
                              loan_approved_date=loan_request.approved_on,
                              ref_no=uuid.uuid4().hex[:8],
                              approval_no=loan_request.id)
                db.session.add(entry)
            
            #Business Loan
            elif loan_request.request_loan_type==1:
                business_loan=BusinessLoans.query.filter(BusinessLoans.member_id==loan_request.requested_by).first()
                if business_loan:
                    loger('warning').warning("already business_loan exist.")
                    return jsonify({"status":False,"data":"","message":"already business_loan exist.","error":""}),200
                EMI_start_date=data.get('EMI_start_date')
                date_list=EMI_start_date.split('-')
                if loan_request.number_of_emi==12:
                    year=int(date_list[0])+1
                else:
                    year=int(date_list[0])+2
                loan_end_date=f'{year}-{int(date_list[1])-1}-{date_list[2]}'
                entry=BusinessLoans(member_id=loan_request.requested_by,
                              loan_amount=loan_request.loan_amount,
                              loan_approved_by=user_id,
                              number_of_emi=loan_request.number_of_emi,
                              EMI_amount=loan_request.EMI_amount,
                              interest_rate=loan_request.interest_rate,
                              finaly_payable_amount=loan_request.final_payable_amount,
                              monthly_penalty_amount=200,
                              EMI_start_date=EMI_start_date,
                              loan_end_date=loan_end_date,
                              loan_approved_date=loan_request.approved_on,
                              ref_no=uuid.uuid4().hex[:8],
                              approval_no=loan_request.id)
                db.session.add(entry)

            #Educational Loan
            elif loan_request.request_loan_type==2:
                educational_loan=EducationLoans.query.filter(EducationLoans.member_id==loan_request.requested_by).first()
                if educational_loan:
                    loger('warning').warning("already educational_loan exist.")
                    return jsonify({"status":False,"data":"","message":"already educational_loan exist.","error":""}),200
                EMI_start_date=data.get('EMI_start_date')
                date_list=EMI_start_date.split('-')
                if loan_request.number_of_emi==12:
                    year=int(date_list[0])+1
                else:
                    year=int(date_list[0])+2
                loan_end_date=f'{year}-{int(date_list[1])-1}-{date_list[2]}'
                entry=EducationLoans(member_id=loan_request.requested_by,
                              loan_amount=loan_request.loan_amount,
                              loan_approved_by=user_id,
                              number_of_emi=loan_request.number_of_emi,
                              EMI_amount=loan_request.EMI_amount,
                              interest_rate=loan_request.interest_rate,
                              finaly_payable_amount=loan_request.final_payable_amount,
                              monthly_penalty=200,
                              EMI_start_date=EMI_start_date,
                              loan_end_date=loan_end_date,
                              loan_approved_date=loan_request.approved_on,
                              ref_no=uuid.uuid4().hex[:8],
                              approval_no=loan_request.id)
                db.session.add(entry)

            #Account Closing
            elif loan_request.request_loan_type==5:
                entry=AccountClosing(member_id=loan_request.requested_by,
                                     reference_no=uuid.uuid4().hex[:8],
                                     request_id=loan_request.id)
                db.session.add(entry)

            db.session.commit()
            data=[{"id":id,"status":loan_request.status,"approved_on":loan_request.approved_on,"comments":loan_request.comments,"user_id":user_id}]
            loger("info").info("Request approved.")
            return jsonify({"status":True,"data":data,"msg":"Request approved","error":""}),204
        elif data.get('status')==2:
            db.session.commit()
            data=[{"id":id,"status":loan_request.status,"rejected_on":loan_request.approved_on,"comments":loan_request.comments,"user_id":user_id}]
            loger("info").info("Request rejected.")
            return jsonify({"status":True,"data":data,"msg":"Request rejected","error":""}),204
        else:
            loger("warning").warning("enter a valid status.")
            return jsonify({"status":False,"data":"","msg":"enter a valid status","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500