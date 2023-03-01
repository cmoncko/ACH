from flask import Blueprint,request,jsonify
from main.Teams.Incharge.models import Employee
from main.extenstions import db
from datetime import datetime

incharge=Blueprint('incharge',__name__,url_prefix='/incharge')

@incharge.route('/new-incharge',methods=['POST'])
def newIncharge():
    data=request.get_json()
    status=data.get('status')
    name=data.get('name')
    dob=data.get('dob')
    image_path=data.get('image_path')
    gender=data.get('gender')
    address=data.get('address')
    city=data.get('city')
    district=data.get('district')
    state=data.get('state')
    pincode=data.get('pincode')
    aadhar=data.get('aadhar')
    mobile=data.get('mobile')
    join_date=data.get('join_date')
    salary=data.get('salary')
    relieving_date=data.get('relieving_date')   
    employee_type=0

    try:
        incharge=Employee(name=name,
                        dob=dob,
                        status=status,
                        image_path=image_path,
                        gender=gender,
                        address=address,
                        city=city,
                        district=district,
                        state=state,
                        pincode=pincode,
                        aadhar=aadhar,
                        mobile=mobile,
                        join_date=join_date,
                        salary=salary,
                        relieving_date=relieving_date,
                        employee_type=employee_type)
        db.session.add(incharge)
        db.session.commit()
        return jsonify({
            "message":"Incharge added successully"
        })
    except Exception as e:
        return jsonify({
            "message":str(e)
        })

@incharge.route('/show-incharges')
def showIncharges():
    try:
        page=request.args['page']
        per_page=request.args['page']
        search=request.args['search']
        
        all_employees=Employee.query.filter(Employee.employee_type==1)
        total_incharges=0
        for emp in all_employees:
            total_incharges+=1

        if search:
            employees=Employee.query.filter(((Employee.name.contains(search)) | 
                                              (Employee.mobile.contains(search)) | 
                                              (Employee.id.contains(search)))
                                              & (Employee.employee_type==0))
            data=[]
            for employee in employees:
                id=employee.id
                name=employee.name
                dob=employee.dob
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
                mobile_no=employee.mobile
                address=employee.address
                gender=employee.gender

                info={"id":id,
                      "name":name,
                      "gender":gender,
                      "age":age,
                      "mobile":mobile_no,
                      "address":address}
                
                data.append(info)

            return jsonify({
                "data": data,
                "total_incharges": total_incharges
            })
        else:
            employees=Employee.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            data=[]
            for employee in employees:
                if employee.employee_type!=0:
                    continue
                id=employee.id
                name=employee.name
                dob=employee.dob
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
                mobile_no=employee.mobile
                address=employee.address
                gender=employee.gender

                info={"id":id,
                      "name":name,
                      "gender":gender,
                      "age":age,
                      "mobile":mobile_no,
                      "address":address}
                
                data.append(info)
            
            return jsonify({
                "data":data,
                "total_incharges":total_incharges
            })

    except Exception as e:
        return jsonify({
            "error":str(e)
        })    
    