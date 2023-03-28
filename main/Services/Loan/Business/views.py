from flask import Blueprint, request, jsonify
from main.Services.Loan.Business.models import BusinessLoans, BusinessLoanPayment
from main.Teams.Members.models import MemberProfile
from main.extensions import db
from datetime import datetime

business_loan=Blueprint('business_loan',__name__,url_prefix='/business-loan')

@business_loan.route('/all-loans')
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
                loans=BusinessLoans.query.filter(BusinessLoans.member_id==id)
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
            loans=BusinessLoans.query.paginate(page=page,per_page=per_page,error_out=False)
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
                    if status==1:
                        all_emis=BusinessLoanPayment.query.filter(BusinessLoanPayment.loan_id==SL_id)
                        penalty_ids=[]
                        for emi in all_emis:
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
                                entry=BusinessLoanPayment.query.get(emi_id)
                                entry.penalty_amount=200
                                entry.total_amount=entry.amount+200
                                db.session.commit()

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
    
@business_loan.route('/issue/<int:id>',methods=['PUT'])
def issue(id):
    try:
        data=request.get_json()
        issued_on=data.get('issued_on')
        status=data.get('status')
        comments=data.get('comments')
        loan=BusinessLoans.query.get(id)
        print(loan)
        if not loan:
            return jsonify({
                "message":"loan not exist."
            })
        loan.issued_on=issued_on
        loan.comments=comments
        loan.status=status

        date_list=str(loan.EMI_start_date).split('-')
        month=int(date_list[1])#8
        year=int(date_list[0])
        for i in range(loan.number_of_emi):#24
            entry=BusinessLoanPayment(member_id=loan.member_id,
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
     
@business_loan.route('/all-emi/<int:id>')
def allLoan(id):
    try:
        details=BusinessLoanPayment.query.filter(BusinessLoanPayment.loan_id==id)
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
        return jsonify({
                "data":data
            })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@business_loan.route('/pay-loan/<int:id>',methods=['PUT'])
def payloan(id):
    data=request.get_json()
    emi=BusinessLoanPayment.query.get(id)
    if not emi:
        return jsonify({
            "message":"id not found (or) emi not exist."
        })
    emi.status=data.get('status')
    if data.get('status')==1:
        emi.paid_date=data.get('paid_date')
    else:
        emi.paid_date=None
    db.session.commit()
    return jsonify({
        "id":id,
        "status":emi.status,
        "month":emi.month,
        "year":emi.year,
        "paid_date":emi.paid_date,
        "amount":emi.amount ,
        "penalty":emi.penalty_amount,
        "total":emi.total_amount
    })