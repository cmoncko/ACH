from flask import Blueprint, request, jsonify
from main.Services.Loans.Savings.models import SavingsLoans, SavingsLoansPayment
from main.Teams.Members.models import MemberProfile
from main.extensions import db
from datetime import datetime

savings_loan=Blueprint('savings_loan',__name__,url_prefix='/savings-loan')

@savings_loan.route('/all-loans')
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
                loans=SavingsLoans.query.filter(SavingsLoans.member_id==id)
                for loan in loans:
                    SL_id=loan.id
                    ref_no=loan.ref_no
                    loan_amount=loan.loan_amount
                    approval_no=loan.approval_no
                    loan_approved_date=loan.loan_approved_date
                    tenure=str(loan.number_of_emi)+" months"
                    EMI=loan.EMI_amount
                    issued_on=loan.issued_on
                    status=loan.status
                    info={
                        "SL_id":SL_id,
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
            return jsonify({
                "data":data
            })
        else:
            data=[]
            loans=SavingsLoans.query.paginate(page=page,per_page=per_page,error_out=False)
            for loan in loans:
                    mem_id=loan.member_id
                    SL_id=loan.id
                    ref_no=loan.ref_no
                    loan_amount=loan.loan_amount
                    approval_no=loan.approval_no
                    loan_approved_date=loan.loan_approved_date
                    tenure=str(loan.number_of_emi)+" months"
                    EMI=loan.EMI_amount
                    issued_on=loan.issued_on
                    status=loan.status
                    members=MemberProfile.query.filter(MemberProfile.id==mem_id)
                    for member in members:
                         name=member.name
                    info={
                        "SL_id":SL_id,
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
            return jsonify({
                "data":data
            })

    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@savings_loan.route('/issue/<int:id>',methods=['PUT'])
def issue(id):
     try:
        data=request.get_json()
        issued_on=data.get('issued_on')
        status=data.get('status')
        comments=data.get('comments')
        loan=SavingsLoans.query.get(id)
        loan.issued_on=issued_on
        loan.comments=comments
        loan.status=status

        date_list=str(loan.EMI_start_date).split('-')
        month=int(date_list[1])#8
        year=int(date_list[0])
        for i in range(loan.number_of_emi):#24
            entry=SavingsLoansPayment(member_id=loan.member_id,
                                     loan_id=id,
                                     month=month,
                                     year=year,
                                     emi_count=loan.number_of_emi,
                                     amount=loan.EMI_amount,
                                     )
            db.session.add(entry)
            db.session.commit()
            month+=1
            if month>12:
                month=1
                year+=1
        return jsonify({
            "SL_id":id,
            "issued_on":loan.issued_on,
            "comments":loan.comments,
            "status":loan.status
        })
     except Exception as e:
          return jsonify({
               "error":str(e)
            })
     
@savings_loan.route('/all-emi/<int:id>')
def allLoan(id):
    try:
        details=SavingsLoansPayment.query.filter(SavingsLoansPayment.loan_id==id)
        data=[]
        for detail in details:
            id=detail.id
            EMI_amount=detail.amount
            penalty_amount=0
            dateNow=datetime.now().strftime("%Y-%m-%d").split('-')
            month=int(dateNow[1])
            year=int(dateNow[0])
            date=int(dateNow[2])
            if detail.month<month and detail.year==year and date>5:
                penalty_amount+=200
            total_amount=penalty_amount+EMI_amount
            paid_date=detail.paid_date
            status=detail.status
            info={"id":id,
                  "EMI_amount":EMI_amount,
                  "penalty_amount":penalty_amount,
                  "total_amount":total_amount,
                  "paid_date":paid_date,
                  "status":status}
            data.append(info)
        return jsonify({
                "data":data
            })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@savings_loan.route('/pay-loan',methods=['POST'])
def payloan():
    pass