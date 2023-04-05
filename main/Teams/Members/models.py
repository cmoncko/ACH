from ...extensions import db
from main.Funds.Santha.models import SanthaPayments
from main.Funds.Savings.models import Savings
from main.Services.Requests.models import LoanRequest
from main.Services.Loan.Business.models import BusinessLoans
from main.Services.Loan.Educational.models import EducationLoans
from main.Services.Loan.Savings.models import SavingsLoans
from main.Services.Pension.models import Pension
from main.Services.Benefits.models import Benefits
from main.Settings.Services.models import BenefitType
from datetime import datetime

class MemberProfile(db.Model):
    id=db.Column(db.BigInteger,primary_key=True)
    user_id=db.Column(db.String(50),nullable=False,unique=True)
    name=db.Column(db.String(50),nullable=False)
    DOB=db.Column(db.Date(),nullable=False)
    image_path=db.Column(db.String(250))
    gender=db.Column(db.Integer(),server_default="0")
    address=db.Column(db.String(255),nullable=False)
    city=db.Column(db.String(120),nullable=False)
    district=db.Column(db.String(120),nullable=False)
    state=db.Column(db.String(120),nullable=False)
    pincode=db.Column(db.Integer(),nullable=False)
    auth_type_id=db.Column(db.Integer(),server_default="0")
    auth_data=db.Column(db.String(100),nullable=False)
    auth_path=db.Column(db.String(255))
    mobile_no=db.Column(db.BigInteger(),nullable=False)
    join_date=db.Column(db.Date(),nullable=False)
    leaving_date=db.Column(db.Date())
    is_leader=db.Column(db.Integer(),server_default='0')
    leader_id=db.Column(db.BigInteger())
    incharge_id=db.Column(db.BigInteger())
    status=db.Column(db.Integer(),nullable=False,server_default="0")
    last_status_change_date=db.Column(db.Date())
    comments=db.Column(db.String(255))
    nominee_name=db.Column(db.String(255),nullable=False)
    nominee_DOB=db.Column(db.Date())
    nominee_relation=db.Column(db.String(255),nullable=False)
    nominee_mobileno=db.Column(db.BigInteger())
    nominee_adhaarno=db.Column(db.BigInteger())
    created_on=db.Column(db.DateTime, server_default=db.func.now())
    # SL=db.relationship("SavingsLoans",casecade="all,delete",backref="member_profile")
    # SL_payment=db.relationship("SavingsLoanPaym",secondary="savings_loan_payment",casecade="all,delete")
    # savings=db.relationship("Savings",secondary="savings",casecade="all,delete")
    # EL=db.relationship("EducationLoan",secondary="education_loan",casecade="all,delete")
    # EL_payment=db.relationship("EducationalLoanPayment",secondary="educational_loan_payment",casecade="all,delete")
    # santha=db.relationship("SanthaPayments",secondary="santha_payments",casecade="all,delete")
    # BL=db.relationship("BusinessLoan",secondary="business_loan",casecade="all,delete")
    # pension=db.relationship("Pension",secondary="pension",casecade="all,delete")
    # pension_payment=db.relationship("PensionPayment",secondary="pension_payment",casecade="all,delete")
    # benefits=db.relationship("Benefits",secondary="benefits",casecade="all,delete")
    # loan_request=db.relationship("LoanRequest",secondary="loan_request",casecade="all,delete")
    # BL_payment=db.relationship("BusinessLoanPayment",secondary="business_loan_payment",casecade="all,delete")
    

    def __repr__(self):
        return f'<UserId:{self.id}>'
    
    def to_json(self):
        dob=self.DOB
        dob_date_list=str(dob).split('-') #it return ['year','month','date']
        day=datetime.now().strftime("%Y-%m-%d")# date of today
        date_now=day.split("-") #it return ['year','month','date']
        dyear=int(dob_date_list[0]) # convert string to integer
        dmonth=int(dob_date_list[1]) # '''
        ddate=int(dob_date_list[2]) # '''
        nyear=int(date_now[0]) # '''
        nmonth=int(date_now[1]) # '''
        ndate=int(date_now[2]) # '''

        # check the month and date grater than or equal to dob month and date
        if (nmonth>= dmonth) & (ndate>=ddate): 
            age=nyear-dyear # if true return absoult value
        else:
            age=nyear-dyear
        return {
           "id":self.id,
           "user_id":self.user_id,
           "name":self.name, 
           "age":age,
           "gender":self.gender,
           "city":self.city,
           "mobile_no":self.mobile_no,
           "leader_id":self.leader_id,
           "incharge_id":self.incharge_id
        }
    
    def profile(self):
        dob=self.DOB
        dob_date_list=str(dob).split('-') #it return ['year','month','date']
        day=datetime.now().strftime("%Y-%m-%d")# date of today
        date_now=day.split("-") #it return ['year','month','date']
        dyear=int(dob_date_list[0]) # convert string to integer
        dmonth=int(dob_date_list[1]) # '''
        ddate=int(dob_date_list[2]) # '''
        nyear=int(date_now[0]) # '''
        nmonth=int(date_now[1]) # '''
        ndate=int(date_now[2]) # '''

        # check the month and date grater than or equal to dob month and date
        if (nmonth>= dmonth) & (ndate>=ddate): 
            age=nyear-dyear # if true return absoult value
        else:
            age=nyear-dyear
        #Funds/Balance
        santha_payments=SanthaPayments.query.filter(SanthaPayments.member_id==self.id)
        balance=0
        for payment in santha_payments:
            balance+=payment.received_amount
        #Fund/Savings & withdraw
        paymentDetails=Savings.query.filter((Savings.member_id==self.id)&(Savings.transaction_type==0))
        withdrawDetails=Savings.query.filter((Savings.member_id==self.id)&(Savings.transaction_type==1))
        total_savings=0
        total_withdraw=0
        for withdraw in withdrawDetails:
            total_withdraw+=withdraw.transaction_amount 
        for detail in paymentDetails:
            total_savings+=detail.transaction_amount
        current_savings=total_savings-total_withdraw
        #Loans
        savingLoan=0
        businessLoan=0
        EducationalLoan=0
        SL_detail=SavingsLoans.query.filter(SavingsLoans.member_id==self.id)
        for i in SL_detail:
            if i.status==1:
                savingLoan+=i.loan_amount
        BL_detail=BusinessLoans.query.filter(BusinessLoans.member_id==self.id)
        for i in BL_detail:
            if i.status==1:
                businessLoan+=i.loan_amount
        EL_detail=EducationLoans.query.filter(EducationLoans.member_id==self.id)
        for i in EL_detail:
            if i.status==1:
                EducationalLoan+=i.loan_amount
        #pension
        pension_amount=0
        pension_detail=Pension.query.filter(Pension.member_id==self.id)
        for i in pension_detail:
            if i.status==1:
                pension_amount+=i.pension_monthly_payment
        #Benefits
        benefit_type=""
        benefit_detail=Benefits.query.filter(Benefits.member_id==self.id)
        for i in benefit_detail:
            if i.status==1:
                benefit_type_id=i.benefit_type_id
                benefit=BenefitType.query.get(benefit_type_id)
                benefit_type=benefit.name
        #Request
        requests=LoanRequest.query.filter(LoanRequest.requested_by==self.id)
        total=requests.count()
        approved=0
        pending=0
        rejected=0
        for i in requests:
            if i.status==0:
                pending+=1
            if i.status==1:
                approved+=1
            if i.status==2:
                rejected+=1

        return {self.name:{
                    "id":self.id,
                    "DOB":dob, 
                    "age":age,
                    "gender":self.gender,
                    "city":self.city,
                    "state":self.state,
                    "district":self.district,
                    "address":self.address,
                    "leaving_date":self.leaving_date,
                    "image_path":self.image_path,
                    "is_leader":self.is_leader,
                    "auth_type_id":self.auth_type_id,
                    "auth_data":self.auth_data,
                    "mobile_no":self.mobile_no,
                    "leader_id":self.leader_id,
                    "status":self.status,
                    "incharge_id":self.incharge_id
                    },
                "Funds":{"Balance":balance,
                         "Savings":current_savings,
                         "Withdraw":total_withdraw},
                "Loans":{"SavingsLoan":savingLoan,
                         "BusinessLoan":businessLoan,
                         "EducationalLoan":EducationalLoan},
                "Pension":{"per_month":pension_amount},
                "Benefits":benefit_type,
                "Requests":{"total_request":total,
                            "Approved":approved,
                            "Pending":pending,
                            "Rejected":rejected}
                }