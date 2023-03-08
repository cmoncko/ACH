from flask import Blueprint,jsonify,request
from main.Services.Requests.models import LoanRequest
from main.Teams.Members.models import MemberProfile
from main.Services.Benefits.models import Benefits
from main.Services.Pension.models import Pension
from main.extensions import db
from datetime import datetime
import uuid

requests=Blueprint('request',__name__,url_prefix='/request')

@requests.route('/send-request',methods=['POST'])
def sendRequest():
    try:
        data=request.get_json()
        requested_by=data.get('requested_by')
        member=[MemberProfile.to_json(i) for i in MemberProfile.query.filter(MemberProfile.id==requested_by)]

        if len(member)<1:
            return jsonify({
                "message":"Member is not exist"
            })
        
        appied_on=data.get('applied_on')
        comments=data.get('comments')
        request_loan_type=data.get('request_loan_type')
        loan_amount=None
        number_of_emi=None
        interest_rate=None
        approved_on=None
        action_by_user=None
        pension_monthly_amount=None
        benefit_type_id=None
        final_payable_amount=None 

        if request_loan_type==0 or request_loan_type==1 or request_loan_type==2:
            loan_amount=data.get('loan_amount')
            print(type(loan_amount),loan_amount)
            number_of_emi=data.get("number_of emi")
            print(type(number_of_emi),number_of_emi)
            interest_rate=data.get('interest_rate')
            print(interest_rate)
            EMI_amount=(loan_amount/number_of_emi)+interest_rate
            final_payable_amount=EMI_amount*number_of_emi

        if request_loan_type==3:
            benefit_type_id=data.get('benefit_type_id')
        if request_loan_type==4:
            pension_monthly_amount=data.get('pension_monthly_amount')

        entry=LoanRequest(requested_by=requested_by,
                          appied_on=appied_on,
                          comments=comments,
                          request_loan_type=request_loan_type,
                          loan_amount=loan_amount,
                          number_of_emi=number_of_emi,
                          interest_rate=interest_rate,
                          approved_on=approved_on,
                          action_by_user=action_by_user,
                          pension_monthly_amount=pension_monthly_amount,
                          benefit_type_id=benefit_type_id,
                          final_payable_amount=final_payable_amount)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "message":"Request sended successfully."
        })
    except Exception as e:
        print(e)
        return jsonify({
            "error":str(e)
        })

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
            return jsonify({
                "data":data
            })
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
            return jsonify({
                "data":data
            })

    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@requests.route('profile/<int:id>')
def profileDetails(id):
    try:
        details=LoanRequest.query.filter(LoanRequest.requested_by==id)
        data=[]
        for detail in details:
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

        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@requests.route('/approve/<int:id>',methods=['PUT'])
def approve(id):
    try:
        data=request.get_json()
        loan_request=LoanRequest.query.get(id)
        loan_request.status=data.get('status')
        loan_request.approved_on=data.get('approved_on')
        loan_request.comments=data.get('comments')

        if data.get('status')==1:
            if loan_request.request_loan_type==3:
                entry=Benefits(member_id=loan_request.requested_by,
                               benefit_type_id=loan_request.benefit_type_id,
                               approved_on=loan_request.approved_on,
                               reference_no=uuid.uuid4().hex[:8],
                               approval_no=loan_request.id)
                db.session.add(entry)
            elif loan_request.request_loan_type==4:
                entry=Pension(member_id=loan_request.requested_by,
                              pension_monthly=loan_request.pension_monthly_amount,
                              approved_on=loan_request.approved_on,
                              reference_no=uuid.uuid4().hex[:8],
                              approval_no=loan_request.id)
                db.session.add(entry)
            db.session.commit()
            return jsonify({
                "message":"approved"
            })
        else:
            db.session.commit()
            return jsonify({
                "message":"rejected"
            }) 
    except Exception as e:
        return jsonify({
            "error":str(e)
        })