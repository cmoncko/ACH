from main.extensions import *
from main.Teams.Members.models import MemberProfile
from main.Teams.Incharge.models import  Employee
from main.Accounts.Income.models import Income
from main.Accounts.Expense.models import Expense
from main.Settings.Funds.models import MasterData
from main.Settings.Accounts.models import CategorySubcategory
import csv
from uuid import uuid4
import pandas as pd
import json

import_csv=Blueprint("import",__name__,url_prefix='/import')

# #----------------------IMPORT MEMBER PROFILE

@import_csv.route('/member',methods=['POST'])
def import_mamber_data():
    try:
        new_file=request.files.get('file')
        f_format=new_file.filename
        if not new_file:
            return jsonify({"message":"csv file missing"})
        if f_format=='xlsx':    
            travel_df = pd.read_excel(new_file)
            cities = travel_df.to_dict('records')
        elif f_format=='csv':    
            travel_df = pd.read_csv(new_file)
            cities = travel_df.to_dict('records')
        else:
            return jsonify({"message":"file format can't support."})
        data=[]
        try:
            for i in cities:           
                member=MemberProfile.query.all()
                for j in member:
                    if j.mobile_no==i['mobile_no']:
                        continue
                    if j.auth_data==i['auth_data']:
                        continue
                leader_id=0
                if i['is_leader']==1:
                    leader_id=None
                elif i['is_leader']==0:
                    if pd.isnull(i['leader_id']) or pd.isnull(i['leader_id']):
                        return jsonify({"message":"Leader Id is missing."})
                    leader_id=int(i['leader_id'])
                    leader=MemberProfile.query.filter_by(id=leader_id).filter_by(is_leader=1).first()
                    if leader==None:
                       return jsonify({"message":"Leader not exist."})
                else:    
                    return jsonify({"message":"Member type is missing."})


                if MemberProfile.query.filter_by(status=0).filter_by(mobile_no=i['mobile_no'],auth_data=i['auth_data']).first():
                    return jsonify({"message":"Duplicate Entry."})
                if not Employee.query.filter_by(id=i['incharge_id']).first():
                    return jsonify({"message":"incharge does not exist"}),404    

                gender=i['gender']
                if pd.isnull(i['gender']):
                    gender=0

                if pd.isnull(i['nominee_name']) or pd.isnull(i['nominee_relation']):
                    return jsonify({"message":"nominee details are missing."})

                auth_type_id=0
                if i['auth_type_id']=="aadhar_id":
                    auth_type_id=0
                elif i['auth_type_id']=="driving_lisence":
                    auth_type_id=1
                elif i['auth_type_id']=="voter_id":
                    auth_type_id=2
                elif i['auth_type_id'] in (0,1,2):
                    auth_type_id=i['auth_type_id']    
                else:
                    return jsonify({"message":"invalid auth-type (mandatory:aadhar_id-0/driving_lisence-1/voter_id-2)"}) 

                # dob=datetime.strftime(i['DOB'],"%Y-%m-%d")
                nominee_mobileno=i['nominee_mobileno']
                nominee_DOB=i['nominee_DOB']
                nominee_aadharno=i['nominee_aadharno']
                comments=i['comments']
                print(comments,type(comments))
                join_date=i['join_date']
                if pd.isnull(i['nominee_mobileno']):
                    nominee_mobileno=None
                if pd.isnull(i['nominee_aadharno']):
                    nominee_aadharno=None
                if pd.isnull(i['join_date']):
                    join_date=None
                if pd.isnull(i['comments']):
                    comments=None
                if pd.isnull(i['nominee_DOB']):
                    nominee_DOB=None
                member=MemberProfile(
                    user_id=i['user_id'], 
                    name=i['name'],
                    DOB=i['DOB'],
                    gender=gender,
                    address=i['address'],
                    city=i['city'],
                    state=i['state'],
                    district=i['district'],
                    pincode=i['pincode'],
                    auth_data=i['auth_data'],
                    auth_type_id=auth_type_id,
                    mobile_no=i['mobile_no'],
                    join_date=join_date,
                    is_leader=i['is_leader'],
                    leader_id=leader_id,
                    incharge_id=i['incharge_id'],
                    comments=comments,
                    nominee_name=i['nominee_name'],
                    nominee_relation=i['nominee_relation'],
                    nominee_DOB=nominee_DOB,
                    nominee_mobileno=nominee_mobileno,
                    nominee_adhaarno=nominee_aadharno
                )
                data.append(member)
        except:
            return jsonify({"message":"can't import incharge, some field(s) missing."})
        if data:
            db.session.add_all(data)
            db.session.commit()   
            return jsonify({"message":"successfully imported"})
        else:
            return jsonify({"message":"No data"})    

    except Exception as e:
        return jsonify({"meassge":str(e)})

@import_csv.route('/incharge',methods=['POST'])
def import_employee_data():
    try:
        file=request.files.get('file')
        f_format=file.filename.split('.')[-1]
        if not file:
            return jsonify({"message":"file missing"})
        if f_format=='xlsx':    
            travel_df = pd.read_excel(file)
            cities = travel_df.to_dict('records')
        elif f_format=='csv':    
            travel_df = pd.read_csv(file)
            cities = travel_df.to_dict('records')
        else:
            return jsonify({"message":"file format can't support."})
        try:
            data=[]
            for i in cities:
                name=i['name']
                if pd.isnull(name):
                    return jsonify({"message name can't be empty."})
                gender=i['gender']
                if pd.isnull(gender):
                    return jsonify({"message gender can't be empty."})
                dob=i['DOB']
                if pd.isnull(dob):
                    return jsonify({"message DOB can't be empty."})
                address=i['address']
                if pd.isnull(address):
                    return jsonify({"message address can't be empty."})
                city=i['city']
                if pd.isnull(city):
                    return jsonify({"message city can't be empty."})
                district=i['district']
                if pd.isnull(district):
                    return jsonify({"message district can't be empty."})
                state=i['state']
                if pd.isnull(state):
                    return jsonify({"message state can't be empty."})
                pincode=i['pincode']
                if pd.isnull(pincode):
                    return jsonify({"message pincode can't be empty."})
                mobile=i['mobile']
                if pd.isnull(mobile):
                    return jsonify({"message mobile can't be empty."})
                aadhar=i['aadhar']
                if pd.isnull(aadhar):
                    return jsonify({"message aadhar can't be empty."})
                salary=i['salary']
                if pd.isnull(salary):
                    return jsonify({"message salary can't be empty."})
                join_date=i['join_date']
                if pd.isnull(join_date):
                    return jsonify({"message join_date can't be empty."})
                if Employee.query.filter_by(status=0).filter_by(mobile=mobile,aadhar=aadhar).first():
                    return jsonify({"message":"Duplicate Entry."})
                if Employee.query.filter((Employee.name==name)&(Employee.dob==dob)).first():
                    return jsonify({"message":"Duplicate Entry."})
                employee=Employee(name=name,dob=dob,gender=gender,address=address,city=city
                                  ,state=state,district=district,salary=salary,mobile=mobile,
                                  aadhar=aadhar,join_date=join_date,pincode=pincode)
                data.append(employee)
        except:
            return jsonify({"message":"can't import incharge, some field(s) missing."})
        if data:
            print(data)
            db.session.add_all(data)
            db.session.commit()   
            return jsonify({"message":"successfully imported"})
        else:
            return jsonify({"message":"No data"})    
    except Exception as e:
        return jsonify({"messge":str(e)})

@import_csv.route('/income',methods=['POST'])
def import_income():
    try:
        file=request.files.get('file')
        f_format=file.filename.split('.')[-1]
        if not file:
            return jsonify({"message":"file missing"})
        if f_format=='xlsx':    
            travel_df = pd.read_excel(file)
            cities = travel_df.to_dict('records')
        elif f_format=='csv':    
            travel_df = pd.read_csv(file)
            cities = travel_df.to_dict('records')
        else:
            return jsonify({"message":"file format can't support."})
        try:
            data=[]
            for i in cities:
                GST=i['GST']
                if pd.isnull(GST):
                    GST=0.00
                received_from=i['received_from']
                if pd.isnull(received_from):
                    received_from=None
                received_date=i['received_date']
                if pd.isnull(received_date):
                    return jsonify({"message Received date can't be empty."})
                amount=i['amount']
                if pd.isnull(amount):
                    return jsonify({"message amount can't be empty."})
                description=i['description']
                if pd.isnull(description):
                    description=None
                category_id=i['category_id']
                if pd.isnull(category_id):
                    category_id=None
                else:
                    cat=MasterData.query.get(category_id)
                    if cat.property!='category':
                        return jsonify({"message":"category not exist."})
                total=GST+amount
                income=Income(received_date=received_date,
                              total=total,
                              GST=GST,
                              received_from=received_from,
                              amount=amount,
                              ref_no=uuid4().hex[:8],
                              description=description,
                              category_id=category_id)
                data.append(income)
        except:
            return jsonify({"message":"can't import income, some field(s) missing."})
        if data:
            print(data)
            db.session.add_all(data)
            db.session.commit()   
            return jsonify({"message":"successfully imported"})
        else:
            return jsonify({"message":"No data"})    
    except Exception as e:
        return jsonify({"messge":str(e)})
            
@import_csv.route('/expense',methods=['POST'])
def import_expense():
    try:
        file=request.files.get('file')
        f_format=file.filename.split('.')[-1]
        if not file:
            return jsonify({"message":"file missing"})
        if f_format=='xlsx':    
            travel_df = pd.read_excel(file)
            cities = travel_df.to_dict('records')
        elif f_format=='csv':    
            travel_df = pd.read_csv(file)
            cities = travel_df.to_dict('records')
        else:
            return jsonify({"message":"file format can't support."})
        try:
            data=[]
            for i in cities:
                GST=i['GST']
                if pd.isnull(GST):
                    GST=0.00
                paid_to=i['paid_to']
                if pd.isnull(paid_to):
                    paid_to=None
                paid_date=i['paid_date']
                if pd.isnull(paid_date):
                    return jsonify({"message Received date can't be empty."})
                amount=i['amount']
                if pd.isnull(amount):
                    return jsonify({"message amount can't be empty."})
                description=i['description']
                if pd.isnull(description):
                    description=None
                category_id=i['category_id']
                if pd.isnull(category_id):
                    return jsonify({"message category_id can't be empty."})
                else:
                    cat=MasterData.query.get(category_id)
                    if not cat:
                        return jsonify({"message":"category not exist."})
                total=GST+amount
                expense=Expense(paid_date=paid_date,
                              total=total,
                              GST=GST,
                              paid_to=paid_to,
                              amount=amount,
                              ref_no=uuid4().hex[:8],
                              description=description,
                              category_id=category_id)
                data.append(expense)
        except:
            return jsonify({"message":"can't import expense, some field(s) missing."})
        if data:
            print(data)
            db.session.add_all(data)
            db.session.commit()   
            return jsonify({"message":"successfully imported"})
        else:
            return jsonify({"message":"No data"})    
    except Exception as e:
        return jsonify({"messge":str(e)})
# # @app.route("/getPlotCSV",methods=['GET','POST'])
# # def getPlotCSV():
# #     member=Member_Profile.query.all()
# #     with open('member.csv', 'w', newline='') as file:
# #         fieldnames = ["id",'name']
# #         writer = csv.DictWriter(file, fieldnames=fieldnames)
# #         writer.writeheader()
# #         for i in member:
# #             print(i)
# #             writer.writerow({'id':i.id, 'name':i.name})
# #     send_file("member.csv",as_attachment=True,mimetype='text/csv')
# #     return jsonify({"message":"done"})