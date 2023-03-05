from flask import Blueprint,jsonify,request
from main.Services.Requests.models import LoanRequest
from main.Teams.Members.models import MemberProfile
from main.extensions import db

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