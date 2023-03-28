from main.Services.Loan.Business.models import BusinessLoans
from main.extensions import *
from main.Teams.Members.models import MemberProfile
from main.Teams.Incharge.models import  Employee
from main.Funds.Santha.models import SanthaPayments
from main.Funds.Savings.models import Savings
from main.Settings.Accounts.models import CategorySubcategory
from main.Accounts.Income.models import Income
from main.Accounts.Expense.models import Expense

export=Blueprint('export',__name__,url_prefix='/export')

@export.route("/export-member",methods=['POST','GET'])
def Export_member():
    member=MemberProfile.query.filter_by(is_leader=0).all()
    name="export_member"
    with open(f'main/excel_files/{name}.csv', 'w', newline='') as file:
        fieldnames = ['id','user_id','name','dob','gender','address','city','state','leaving_date','district','pincode','auth_type_id','nominee_relation','auth_data','auth_type_id','mobile_no','join_date','is_leader','leader_id','incharge_id','nominee_dob','nominee_mobile_no','nominee_aadhar_no',"nominee_name"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for i in member:
            writer.writerow(
                {'id':i.id,
                'user_id':i.user_id,
                'name':i.name,
                'dob':i.DOB,
                'gender':i.gender,
                'address':i.address,
                'city':i.city,
                'state':i.state,
                'district':i.district,
                'pincode':i.pincode,
                'auth_type_id':i.auth_type_id,
                'auth_data':i.auth_data,
                'auth_type_id':i.auth_type_id,
                'mobile_no':i.mobile_no,
                'join_date':i.join_date,
                'leaving_date':i.leaving_date,
                'is_leader':i.is_leader,
                'leader_id':i.leader_id,
                'incharge_id':i.incharge_id,
                'nominee_dob':i.nominee_DOB,
                'nominee_mobile_no':i.nominee_mobileno,
                'nominee_name':i.nominee_name,
                'nominee_relation':i.nominee_relation,
                'nominee_aadhar_no':i.nominee_adhaarno})
    file.close()        
    path = f"excel_files/{name}.csv"
    return send_file(path, as_attachment=True)

@export.route("/export-leader",methods=['GET','POST'])
def export_leader():
    member=MemberProfile.query.filter_by(is_leader=1).all()
    name="export_leader"
    with open(f'main/excel_files/{name}.csv', 'w', newline='') as file:
        fieldnames = ['id','user_id','name','dob','gender','address','city','state','district','leaving_date','pincode','auth_type_id','nominee_relation','auth_data','auth_type_id','mobile_no','join_date','is_leader','incharge_id','nominee_dob','nominee_mobile_no','nominee_aadhar_no',"nominee_name"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for i in member:
            writer.writerow(
                {'id':i.id,
                'user_id':i.user_id,
                'name':i.name,
                'dob':i.DOB,
                'gender':i.gender,
                'address':i.address,
                'city':i.city,
                'state':i.state,
                'district':i.district,
                'pincode':i.pincode,
                'auth_type_id':i.auth_type_id,
                'auth_data':i.auth_data,
                'auth_type_id':i.auth_type_id,
                'mobile_no':i.mobile_no,
                'join_date':i.join_date,
                'leaving_date':i.leaving_date,
                'is_leader':i.is_leader,
                'incharge_id':i.incharge_id,
                'nominee_dob':i.nominee_DOB,
                'nominee_mobile_no':i.nominee_mobileno,
                'nominee_name':i.nominee_name,
                'nominee_relation':i.nominee_relation,
                'nominee_aadhar_no':i.nominee_adhaarno})
    file.close()        
    path = f"excel_files/{name}.csv"
    return send_file(path, as_attachment=True)

@export.route("/export-incharge",methods=['GET','POST'])
def export_employee():
    member=Employee.query.filter_by(employee_type=0).all()
    name="export_incharge"
    with open(f'main/excel_files/{name}.csv', 'w', newline='') as file:
        fieldnames = ["name","pincode","id","employee_type","DOB","gender","city","state","district","address","status","join_date","salary","relieving_date","image_path","aadhar_number","mobile_no"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for i in member:
            writer.writerow(Employee.emp_export(i))
    file.close()        
    path = f"excel_files/{name}.csv"
    return send_file(path, as_attachment=True)

@export.route('/export-santha',methods=['GET',"POST"])
def export_santha():
    try:
        data=[]
        members=MemberProfile.query.all()
        name="export_santha"
        with open(f'main/excel_files/{name}.csv', 'w', newline='') as file:
            fieldnames = ["member_id","name","join_date","term","santha_amount","received_amount","is_due","due_amount","days_elapsed"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for member in members:
                member_id=member.id
                mem_name=member.name
                join_date=member.join_date
                
                #calculate term
                date_list=str(join_date).split('-')
                year_join=int(date_list[0])
                year_now=int(datetime.now().strftime("%Y"))
                term=year_now-year_join

                joinDateObj=datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
                joindate=joinDateObj.strftime("%d-%b-%Y") #join date eg(12-Jan-2020)
                santha_amount=term*60
                received_amount=0
            
                santha_details=SanthaPayments.query.filter(SanthaPayments.member_id==member_id)
                for detail in santha_details:
                    received_amount+=detail.received_amount

                due_amount=santha_amount-received_amount
                if due_amount<1:
                    isDue="No"
                else:
                    isDue="Yes"
                
                if isDue=="No" and term==0:
                    days_elapsed=0
                else:
                    #calculate leap year
                    leap_year=0
                    for i in range(term):
                        year_join+=1
                        if (year_join==400)or(year_join%4==0 and year_join%100!=0):
                            leap_year+=1
                    # print(leap_year)
                    print(received_amount)
                    print(received_amount<60)
                    if int(received_amount)<60: 
                        days_elapsed=((term-1)*365)+int(datetime.now().strftime("%j"))+leap_year
                    else:
                        before_days=((term-1)-(received_amount//60))*365
                        if before_days==0:
                            days_elapsed=int(datetime.now().strftime("%j"))
                        else:
                            days_elapsed=before_days+leap_year
                writer.writerow({
                    "member_id":member_id,
                    "name":mem_name,
                    "join_date":joindate,
                    "term":term,
                    "santha_amount":santha_amount,
                    "received_amount":received_amount,
                    "is_due":isDue,
                    "due_amount":due_amount,
                    "days_elapsed":int(days_elapsed)
                })

                # writer.writerow({
                #     "reference_no":i.reference_no,
                #     "member_name":i.name,
                #     "members_profile_id":i.id,
                #     "join_date":i.join_date,
                #     "santha_amount":santha_amount*(terms+1),
                #     "terms":terms+1,
                #     "day_elapsed":day_elapsed,
                #     "due_amount":due_amount,
                #     "received_amount":received_amount,
                #     "is_due":is_due
                # })
        file.close()        
        path = f"excel_files/{name}.csv"
        return send_file(path, as_attachment=True)            
    except Exception as e:
        return jsonify({"message":str(e),"status":False}),500

@export.route("/export-savings",methods=['GET',"POST"])
def export_member_savings():
    try:
        member_profile=MemberProfile.query.all()
        name="export_member_savings"
        with open(f'main/excel_files/{name}.csv', 'w', newline='') as file:
            fieldnames = ["id","name","previous_payment","month","week","received_on","total_savings","dues","interest","total_withdraw","current_savings"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            if member_profile:
                data=[]
                for member in member_profile:
                    mem_id=member.id
                    mem_name=member.name

                    paymentDetails=Savings.query.filter((Savings.member_id==mem_id)&(Savings.transaction_type==0))
                    withdrawDetails=Savings.query.filter((Savings.member_id==mem_id)&(Savings.transaction_type==1))

                    savingExist=False
                    total_savings=0
                    total_withdraw=0

                    for withdraw in withdrawDetails:
                        total_withdraw+=withdraw.transaction_amount

                    week="0th"
                    tweek=0
                    for detail in paymentDetails:
                       savingExist=True
                       previous_payment=detail.transaction_amount 
                       received_on=detail.transaction_date

                       date_list=str(received_on).split('-')
                       date_obj=datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
                       month=date_obj.strftime('%b')
                       tweek=date_obj.strftime('%V')
                       week=tweek+"th"

                       total_savings+=detail.transaction_amount

                    current_savings=total_savings-total_withdraw
                    interest=2
                    nweek=datetime.now().strftime("%V")
                    dues=int(nweek)-int(tweek)

                    if savingExist:
                        writer.writerow({"id":mem_id,
                             "name":mem_name,
                             "previous_payment":previous_payment,
                             "month":month,
                             "week":week,
                             "received_on":received_on,
                             "total_savings":total_savings,
                             "dues":dues,
                             "interest":interest,
                             "total_withdraw":total_withdraw,
                             "current_savings":current_savings})                                
        file.close()        
        path = f"excel_files/{name}.csv"
        return send_file(path, as_attachment=True)      
    except Exception as e:
        return jsonify({"message":str(e),"status":False}),500   

# @export.route('/export-request',methods=['GET',"POST"])
# def export_request_list():
#     # try:
#         request_details=db.session.query(MemberProfile,LoanRequest).filter(LoanRequest.requested_by==MemberProfile.id).all()
        
#         data=[]
#         name="export_request_details"
#         with open(f'main/excel_files/{name}.csv', 'w', newline='') as file:
#             fieldnames = ["request_id","name","member_id","request_type","date","applied_on","day_elapsed","approved_status","pension_amount","loan_amount","number_of_emi","interest_rate","benefit_type","comments",]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
       
#             for i in request_details:
#                 request_type=""
#                 status=""
#                 total_pending_request=0
#                 total_approved_request=0
#                 total_rejected_request=0
#                 total_closed_request=0
#                 if i.LoanRequest.status==0:
#                     status="pending"
#                 if i.LoanRequest.status==1:
#                     status="approved"
#                 if i.LoanRequest.status==2:
#                     status="rejected"
#                 if i.LoanRequest.request_loan_type==0:
#                     request_type="savings"
#                 if i.LoanRequest.request_loan_type==1:
#                     request_type="business"
#                 if i.LoanRequest.request_loan_type==2:
#                     request_type="education"        
#                 if i.LoanRequest.request_loan_type==3:
#                     request_type="benefits"        
#                 if i.LoanRequest.request_loan_type==4:
#                     request_type="pension"
#                 if i.LoanRequest.status==0:
#                     total_pending_request+=1
#                 if i.LoanRequest.status==1:
#                     total_approved_request+=1    
#                 if i.LoanRequest.status==2:
#                     total_rejected_request+=1    
#                 if i.LoanRequest.status==3:
#                     total_closed_request+=1      

#                 created_date=date(i.LoanRequest.appied_on.year,i.LoanRequest.appied_on.month,i.LoanRequest.appied_on.day)
#                 current_date=date(datetime.today().year,datetime.today().month,datetime.today().day)        
#                 days_elapsed=(created_date-current_date).days
#                 writer.writerow(
#                     {
#                         "request_id":i.LoanRequest.id,
#                         "name":i.MemberProfile.name,
#                         "member_id":i.MemberProfile.id,
#                         "request_type":request_type,
#                         "applied_on":str(i.LoanRequest.appied_on),
#                         "day_elapsed":abs(days_elapsed),
#                         "approved_status":status,
#                         "pension_amount":i.LoanRequest.EMI_amount,
#                         "loan_amount":i.LoanRequest.loan_amount,
#                         "number_of_emi":i.LoanRequest.number_of_emi,
#                         "interest_rate":i.LoanRequest.interest_rate,
#                         "benefit_type":i.LoanRequest.benefit_type_id,
#                         "comments":i.LoanRequest.comments
#                     })           
#         file.close()        
#         path = f"excel_files/{name}.csv"
#         return send_file(path, as_attachment=True)           
#     # except Exception as e:
#         return jsonify({"error":str(e)})
        
# @expoert.route("/expor-pension",methods=['GET',"POST"])
# def export_pension():
#     try:
#         pension=Pension.query.all()
#         approved_amount=0
#         count=0
#         amount_issued=0
#         name="export_pension_details"
#         with open(f'excel_files/{name}.csv', 'w', newline='') as file:
#             fieldnames = ["member_id","member_name","pension_id","total_pension_payment_amount","status","status_name","pension_monthly_amount","start_date","end_date","reference_no","approved_no","approved_date","approved_by","remarks","created_on",]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#             if pension:
#                 for i in pension:
#                     count+=1
#                     approved_amount+=i.pension_monthly_amount
#                     if i.status==1:
#                         amount_issued+=i.pension_monthly_amount
#                     member_name=Member_Profile.query.filter_by(id=i.member_id).first()
#                     total_pension_payment_amount=0
                    
#                     pension=Pension.query.filter_by(member_id=member_name.id).first()
#                     pension_payment=Pension_Payment.query.filter_by(pension_id=pension.id).all()
#                     for j in pension_payment:
                    
#                         total_pension_payment_amount+=j.amount
                    
#                     status=""
#                     if i.status==0:
#                         status="pending"
#                     if i.status==1:
#                         status="active"
#                     if i.status==2:
#                         status="closed"    
#                     writer.writerow(
#                         {   
#                             "pension_id":i.id,
#                             "total_pension_payment_amount":total_pension_payment_amount,
#                             "member_id":i.member_id,
#                             "member_name":member_name.name,
#                             "status":i.status,
#                             "status_name":status,
#                             "pension_monthly_amount":i.pension_monthly_amount,
#                             "start_date":str(i.start_date),
#                             "end_date":str(i.end_date),
#                             "approved_by":i.approved_by_id,
#                             "remarks":i.remarks,
#                             "created_on":str(i.created_on),
#                             "reference_no":i.reference_no,
#                             "approved_no":i.approved_no,
#                             "approved_date":str(i.approved_date),
#                         })                           
#         file.close()        
#         path = f"excel_files/{name}.csv"
#         return send_file(path, as_attachment=True)     
    
#     except Exception as e:
#         return jsonify({"message":str(e),"status":False}) 

# @app.route("/export_benefit",methods=['GET',"POST"])
# def export_benefit():
#     try:
#         benefits=Benefits.query.all()
#         name="export_benefits"
#         with open(f'excel_files/{name}.csv', 'w', newline='') as file:
#             fieldnames = ["benefits_id","member_id","member_name","status","status_name","benefit_type","approved_on","approved_no","approved_by","issued_on","remarks","created_on","reference_no"]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#             for i in benefits:
#                 if benefits:
#                     member=Member_Profile.query.filter_by(id=i.member_profile_id).first()
#                     member_name=member.name
#                     status=""
#                     if i.status==0:
#                         status="pending"
#                     if i.status==1:
#                         status="active"
#                     if i.status==2:
#                         status="closed"
#                     writer.writerow(
#                     {
#                         "benefits_id":i.id,
#                         "member_id":i.member_profile_id,
#                         "member_name":member_name,
#                         "status":i.status,
#                         "status_name":status,
#                         "benefit_type":i.benefit_type,
#                         "approved_on":str(i.approved_date),
#                         "approved_no":i.approved_no,
#                         "approved_by":i.approval_by_id,
#                         "issued_on":str(i.issued_on),
#                         "remarks":i.remarks,
#                         "created_on":str(i.created_on),
#                         "reference_no":i.reference_no,
#                     }
#                 )
#         file.close()        
#         path = f"excel_files/{name}.csv"
#         return send_file(path, as_attachment=True)             
                
        
#     except Exception as e:
#         return jsonify({"message":str(e),"status":False}),500   

# @app.route("/export_savings_loan",methods=['GET','POST'])
# def export_savings_loan():
#     try:
      
#         savings_loan=Savings_Loan.query.all()
#         name="export_savings_loan"
#         with open(f'excel_files/{name}.csv', 'w', newline='') as file:
#             fieldnames = ["member_id","member_name","issued_date","savings_loan_id", "status", "status_name", "member_id", "loan_amount","emi_amount","interest_rate","final_payment_amount","monthly_penalty_amount","penalty_interest_percentage","months_to_charge_penalty_interest","number_of_emi","tenure","emi_start_date","loan_end_date","emi_on_date","comments","loan_approved_by","created_on","approved_on","approved_no","reference_no",]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#             for i in savings_loan:
#                 writer.writerow(Savings_Loan.json(i))
#         file.close()        
#         path = f"excel_files/{name}.csv"
#         return send_file(path, as_attachment=True)        
       
#     except Exception as e:
#         return jsonify({"message":str(e),"status":False})   

# @app.route("/export_business_loan",methods=['GET','POST'])
# def export_business_loan():
#     try:
      
#         business_loan=Business_Loans.query.all()
#         name="export_business_loan"
#         with open(f'excel_files/{name}.csv', 'w', newline='') as file:
#             fieldnames = ["member_id","member_name","issued_date","business_loan_id", "status", "status_name", "member_id", "loan_amount","emi_amount","interest_rate","final_payment_amount","monthly_penalty_amount","penalty_interest_percentage","months_to_charge_penalty_interest","number_of_emi","tenure","emi_start_date","loan_end_date","emi_on_date","comments","loan_approved_by","created_on","approved_on","approved_no","reference_no",]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#             for i in business_loan:
#                 writer.writerow(Business_Loans.json(i))
#         file.close()        
#         path = f"excel_files/{name}.csv"
#         return send_file(path, as_attachment=True)        
       
#     except Exception as e:
#         return jsonify({"message":str(e),"status":False})   

# @app.route("/export_education_loan",methods=['GET','POST'])
# def export_education_loan():
#     try:
      
#         education_loan=Education_Loans.query.all()
#         name="export_education_loan"
#         with open(f'excel_files/{name}.csv', 'w', newline='') as file:
#             fieldnames = ["member_id","member_name","issued_date","education_loan_id", "status", "status_name", "member_id", "loan_amount","emi_amount","interest_rate","final_payment_amount","monthly_penalty_amount","penalty_interest_percentage","months_to_charge_penalty_interest","number_of_emi","tenure","emi_start_date","loan_end_date","emi_on_date","comments","loan_approved_by","created_on","approved_on","approved_no","reference_no",]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#             for i in education_loan:
#                 writer.writerow(Education_Loans.json(i))
#         file.close()        
#         path = f"excel_files/{name}.csv"
#         return send_file(path, as_attachment=True)        
       
#     except Exception as e:
#         return jsonify({"message":str(e),"status":False})   

@export.route('/export-income',methods=['GET','POST'])
def export_income():
    try:
        details=Income.query.all()
        name="export_income"
        with open(f'main/excel_files/{name}.csv', 'w', newline='') as file:
            fieldnames = ["id","received_from","received_date","category_id","description","amount","ref_no"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for detail in details:
                id=detail.id
                received_from=detail.received_from
                received_date=detail.received_date
                amount=detail.amount
                category_id=detail.category_id
                description=detail.description
                ref_no=detail.ref_no
                writer.writerow({"id":id,
                    "received_from":received_from,
                    "received_date":received_date,
                    "category_id":category_id,
                    "description":description,
                    "amount":amount,
                    "ref_no":ref_no})
        file.close()        
        path = f"excel_files/{name}.csv"
        return send_file(path, as_attachment=True)
    except Exception as e:
        return jsonify({"message":str(e),"status":False}) 

@export.route('/export-expense',methods=['GET','POST'])
def export_expense():
    try:
        details=Expense.query.all()
            
        name="export_expense"
        with open(f'main/excel_files/{name}.csv', 'w', newline='') as file:
            fieldnames = ["id","received_from","received_date","category_id","description","amount","ref_no","category","sub_category"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for detail in details:
                id=detail.id
                paid_to=detail.paid_to
                paid_date=detail.paid_date
                amount=detail.amount
                category_id=detail.category_id
                cat_subcat=CategorySubcategory.query.get(category_id)
                category=cat_subcat.CATEGORY
                subcategory=cat_subcat.SUBCATEGORY
                description=detail.description
                ref_no=detail.ref_no
                writer.writerow({"id":id,
                    "received_from":paid_to,
                    "received_date":paid_date,
                    "category_id":category_id,
                    "category":category,
                    "sub_category":subcategory,
                    "description":description,
                    "amount":amount,
                    "ref_no":ref_no})
        file.close()        
        path = f"excel_files/{name}.csv"
        return send_file(path, as_attachment=True)
    except Exception as e:
        return jsonify({"message":str(e),"status":False})   