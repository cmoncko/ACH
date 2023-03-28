from flask import Blueprint,jsonify
from main.extensions import db
from sqlalchemy import text
from main.Teams.Members.models import MemberProfile
from main.Teams.Incharge.models import Employee
from main.Services.Requests.models import LoanRequest
from main.Services.Benefits.models import Benefits
from main.Services.Pension.models import Pension
from main.Services.Loan.Savings.models import SavingsLoans
from main.Services.Loan.Business.models import BusinessLoans
from main.Services.Loan.Educational.models import EducationLoans
from main.Settings.Teams.models import Address
from datetime import datetime
from main.Funds.Santha.models import SanthaPayments
from main.Funds.Savings.models import Savings
from main.Services.Loan.Savings.models import SavingsLoansPayment
from main.Services.Loan.Educational.models import EducationalLoanPayment
from main.Services.Loan.Business.models import BusinessLoanPayment
from main.Accounts.Income.models import Income
from main.Accounts.Expense.models import Expense


dashboard=Blueprint("dashboard",__name__,url_prefix="/dashboard")

@dashboard.route("/general")
def teams():
    try:
        #Team
        team=MemberProfile.query.all()
        member=0
        leader=0
        for i in team:
            if i.is_leader==0:
                member+=1
            else:
                leader+=1
        data1=Employee.query.all()
        incharge=0
        for i in data1:
            incharge+=1
        total_team=member+leader+incharge

        #Requests and Approvel
        requests=0
        under_review=0
        approved=0
        rejected=0
        request_approvel=LoanRequest.query.all()
        for i in request_approvel:
            requests+=1
            if i.status==0:
                under_review+=1
            if i.status==1:
                approved+=1
            if i.status==2:
                rejected+=1

        #Benefits:
        bunder_review=0
        bapproved=0
        brejected=0
        benefits=Benefits.query.all()
        for i in benefits:
            if i.status==0:
                bunder_review+=1
            if i.status==1:
                bapproved+=1
            if i.status==2:
                brejected+=1    
        
        #Pension
        punder_review=0
        papproved=0
        prejected=0
        pension=Pension.query.all()
        for i in pension:
            if i.status==0:
                punder_review+=1
            if i.status==1:
                papproved+=1
            if i.status==2:
                prejected+=1
        
        #Savings Loan
        slunder_review=0
        slapproved=0
        slrejected=0
        savingsloans=SavingsLoans.query.all()
        for i in savingsloans:
            if i.status==0:
                slunder_review+=1
            if i.status==1:
                slapproved+=1
            if i.status==2:
                slrejected+=1

        #Business Loan
        blunder_review=0
        blapproved=0
        blrejected=0
        bussinessloans=BusinessLoans.query.all()
        for i in bussinessloans:
            if i.status==0:
                blunder_review+=1
            if i.status==1:
                blapproved+=1
            if i.status==2:
                blrejected+=1

        #Educational Loan
        elunder_review=0
        elapproved=0
        elrejected=0
        educationalloans=EducationLoans.query.all()
        for i in educationalloans:
            if i.status==0:
                elunder_review+=1
            if i.status==1:
                elapproved+=1
            if i.status==2:
                elrejected+=1

        #Teams count by place
        address=Address.query.all()
        team_count_by_place=[]
        for i in address:
            city=i.city
            member_count=MemberProfile.query.filter(MemberProfile.city==city).count()
            incharge_count=Employee.query.filter(Employee.city==city).count()
            total_count=member_count+incharge_count
            info={"city":total_count}
            team_count_by_place.append(info)

        return jsonify({"Teams":{
            "Total teams":total_team,
            "member":member,
            "leader":leader,
            "incharge":incharge
        },"Request and approvals":{
            "request":requests,
            "under_review":under_review,
            "approved":approved,
            "rejected":rejected
        },"Benefits":{
            "under_review":bunder_review,
            "approved":bapproved,
            "rejected":brejected
        },"Pension":{
            "under_review":punder_review,
            "approved":papproved,
            "rejected":prejected
        },"Savings Loans":{
            "under_review":slunder_review,
            "approved":slapproved,
            "rejected":slrejected
        },"Bussiness Loan":{
            "under_review":blunder_review,
            "approved":blapproved,
            "rejected":blrejected
        },"Educational Loan":{
            "under_review":elunder_review,
            "approved":elapproved,
            "rejected":elrejected
        },"Team count by place":{
            "Teams count by place":team_count_by_place
        }
        
        }) 
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@dashboard.route("/finance")
def totalIncome():
    # try:
        #monthly income and expense
        monthly=datetime.now()
        month=monthly.month

        # total income:
        total_income=Income.query.all() 
        total_monthly_income=0
        for i in total_income:
            if i.received_date.month==month:
                total_monthly_income+=i.amount
                
        #total expense:
        total_expense=Expense.query.all()
        total_monthly_expense=0
        for i in total_expense:
            if i.paid_date.month==month:
                total_monthly_expense+=i.amount
              

        #Savigs Loans:
        released_amount=db.session.execute(text("SELECT sum(loan_amount) from savings_loans where status=1"))
        for i in released_amount:
            if i[0] is None:
                release_amount=float(0)
            else:
                release_amount=float(i[0])

        received_amount=db.session.execute(text("select sum(amount) from ACH.savings_loans_payment where status=1"))
        for i in received_amount:
            if i[0] is None:
                receive_amount=float(0)
            else:
                receive_amount=float(i[0])

        pending_amount=release_amount-receive_amount

        #Bussiness Loan:
        rel_business=db.session.execute(text("select sum(loan_amount) from ACH.business_loans where status=1"))
        for i in rel_business:
            if i[0] is None:
                business_rel=float(0)
            else:
                business_rel=float(i[0])

        receive_business=db.session.execute(text('select sum(amount) from ACH.business_loan_payment where status=1'))
        for i in receive_business:
            if i[0] is None:
                business_receive=float(0)
            else:
                business_receive=float(i[0])

        business_pending=business_rel-business_receive
        
        #Education Loan:
        rel_education=db.session.execute(text("select sum(loan_amount) from ACH.education_loans where status=1"))
        for i in rel_education:
            if i[0]==None:
                education_rel=float(0)
            else:
                education_rel=float(i[0])

        receive_education=db.session.execute(text("select sum(amount) from ACH.educational_loan_payment where status=1"))
        for i in receive_education:
            if i[0]== None:
                education_receive=float(0)
            else:
                education_receive=float(i[0])

        education_pending=education_rel-education_receive

        #Loans
        tot_rel_amount=education_rel+business_rel+release_amount
        tot_receive_amount=education_receive+business_receive+receive_amount
        tot_pending_amount=education_pending+business_pending+pending_amount

        #Pension
        beneficiaries=Pension.query.all()
        count=0
        for i in beneficiaries:
            if i.status==1:
                count+=1
        released_Pension=db.session.execute(text("select sum(total_amount_issued) from ACH.pension"))
        for i in released_Pension:
            if i[0] is None:
                pension_released=float(0)
            else:
                pension_released=float(i[0])

        #Santha 
        total_santha=db.session.execute(text("select sum(santha_amount) from ACH.santha_payments"))
        for i in total_santha:
            if i[0] is None:
                santha_total=float(0)
            else:
                santha_total=float(i[0])

        received_santha=db.session.execute(text("select sum(received_amount) from ACH.santha_payments"))
        for i in received_santha:
            if i[0] is None:
                santha_receive=float(0)
            else:
                santha_receive=float(i[0])
        pending_amount=santha_total-santha_receive

        #Income
        tot_income=db.session.execute(text("select sum(amount) from ACH.income"))
        for i in tot_income:
            if i[0] is None:
                income_total=float(0)
            else:
                income_total=float(i[0])

        #Expense
        tot_expense=db.session.execute(text("select sum(amount) from ACH.expense"))
        for i in tot_expense:
            if i[0] is None:
                expense_total=float(0)
            else:
                expense_total=float(i[0])
        
        #Amount in Bank
        tot_bank_amount=db.session.execute(text("select sum(amount) from ACH.bank_transactions where transaction_type=0"))
        for i in tot_bank_amount:
            if i[0] is None:
                bank_amount=float(0)
            else:
                bank_amount=float(i[0])

        #Cash in Hand
        cash_in_hand=income_total-bank_amount

        #Profit/Loss
        profit_loss=abs(income_total-expense_total)

        #dates
        dates=[]
        x=datetime.now()
        date=x.strftime("%Y-%m-%d")
        w=int(x.strftime("%w"))
        dates.append(date)
        date_list=date.split("-")
        day=int(date_list[2])
        for i in range(1,w):
            day-=1
            if day<10:
                date=f"{date_list[0]}-{date_list[1]}-0{str(day)}"
            else:
                date=f"{date_list[0]}-{date_list[1]}-{str(day)}"
            dates.append(date)
        
        #weekly collection.

        #weekly santha collection
        weekly_santha=SanthaPayments.query.all()
        santha_amount=0
        for i in weekly_santha:
            if i.received_date in dates:
                santha_amount+=i.santha_amount

        #weekly savings 
        weekly_savings=Savings.query.filter(Savings.transaction_type==0) 
        weekly_withdraw=Savings.query.filter(Savings.transaction_type==1) 
        savings_weekly=0
        withdraw_weekly=0
        for i in weekly_savings:
            if i.transaction_date in dates:
                savings_weekly+=i.transaction_amount
        for i in weekly_withdraw:
            if i.transaction_date in dates:
                withdraw_weekly+=i.transaction_amount
        tot_weekly_savings=savings_weekly-withdraw_weekly

        #weekly loans collection
        tot_weekly_loans=0
        weekly_Savings_loans=SavingsLoansPayment.query.filter(SavingsLoansPayment.status==1)
        for i in weekly_Savings_loans:
            if i.paid_date in dates:
                tot_weekly_loans+=i.amount
        weekly_education_loans=EducationalLoanPayment.query.filter(EducationalLoanPayment.status==1)
        for i in weekly_education_loans:
            if i.paid_date in dates:
                tot_weekly_loans+=i.amount
        weekly_bussiness_loans=BusinessLoanPayment.query.filter(BusinessLoanPayment.status==1)
        for i in weekly_bussiness_loans:
            if i.paid_date in dates:
                tot_weekly_loans+=i.amount


        return jsonify({
            "Monthly Income/Expense":{
            "Total Income":total_monthly_income,
            "Total Expense":total_monthly_expense
            },
            "Savings Loan":{
            "Released Amount":release_amount,
            "Received Amount":receive_amount,
            "Pendig Amount":pending_amount
            },
            "Business Loan":{
            "Released Amount":business_rel,
            "Received Amount":business_receive,
            "Pending Amount":business_pending
            },
            "Education Loan":{
            "Released Amount":education_rel,
            "Received Amount":education_receive,
            "Pending Amount":education_pending,
            },
            "Loans":{
            "Released Amount":tot_rel_amount,
            "Received Amount":tot_receive_amount,
            "Pending Amount":tot_pending_amount
            },
            "Pension":{
            "Beneficiaries":count,
            "Released Amount":pension_released
            },
            "Santha":{
            "Total Santha Amount":santha_total,
            "Received Amount":santha_receive,
            "Pending Amount":pending_amount
            },
            "Overall Income/Expense":{
            "Income":income_total,
            "Expense":expense_total,
            "Cash in Hand":cash_in_hand,
            "Amount in Bank":bank_amount,
            "Profit/Loss":profit_loss
            },
            "Dues":{
            "Santha":pending_amount,
            "Savings":"you find it",
            "Loans":tot_pending_amount
            },
            "weekly collection":{
            "santha":santha_amount,
            "savings":tot_weekly_savings,
            'loans':tot_weekly_loans
            }
        })
    # except Exception as e:
    #     return jsonify({"":str(e)})
