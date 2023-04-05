from flask import Blueprint,request,jsonify
from main.utils import permission_required,token_required,loger
from main.Teams.Incharge.models import Employee
from main.extensions import db

incharge=Blueprint('incharge',__name__,url_prefix='/incharge')

@incharge.route('/new-incharge',methods=['POST'])
@token_required
@permission_required('edit_team')
def newIncharge():
    data=request.get_json()
    name=data.get('name')
    dob=data.get('dob')
    image_path=data.get('image_path')
    gender=data.get('gender')
    if not gender:
        gender=0
    address=data.get("address")
    if not address:
        loger('warning').warning("address must entered.")
        return jsonify({"status":False,"data":"","message":"address must entered.","error":""}),200
    city=data.get('city')
    if not city:
        loger('warning').warning("city must entered.")
        return jsonify({"status":False,"data":"","message":"city must entered.","error":""}),200
    district=data.get('district')
    if not district:
        loger('warning').warning("district must entered.")
        return jsonify({"status":False,"data":"","message":"district must entered.","error":""}),200
    state=data.get('state')
    if not state:
        loger('warning').warning("state must entered.")
        return jsonify({"status":False,"data":"","message":"state must entered.","error":""}),200
    pincode=data.get('pincode')
    if not pincode:
        loger('warning').warning("pincode must entered.")
        return jsonify({"status":False,"data":"","message":"pincode must entered.","error":""}),200
    aadhar=data.get('aadhar')
    if not aadhar:
        loger('warning').warning("aadhar no must entered.")
        return jsonify({"status":False,"data":"","message":"aadhar no must entered.","error":""}),200
    mobile=data.get('mobile')
    if not mobile:
        loger('warning').warning("mobile.no must entered.")
        return jsonify({"status":False,"data":"","message":"mobile no must entered.","error":""}),200
    join_date=data.get('join_date')
    if not join_date:
        loger('warning').warning("join date must entered.")
        return jsonify({"status":False,"data":"","message":"join date must entered.","error":""}),200
    salary=data.get('salary')
    if not salary:
        loger('warning').warning("salary must entered.")
        return jsonify({"status":False,"data":"","message":"salary must entered.","error":""}),200
    relieving_date=data.get('relieving_date')   

    try:
        incharge=Employee(name=name,
                        dob=dob,
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
                        relieving_date=relieving_date)
        db.session.add(incharge)
        db.session.commit()
        loger("info").info("one incharge added successfully,")
        return jsonify({"status":True,"data":Employee.to_json(incharge),"msg":"one incharge added successfully,","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"data":"","msg":"","eroor":str(e)}),500

@incharge.route('/show-incharges')
@token_required
@permission_required('read_team')
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
            data=[Employee.to_json(i) for i in employees]
            if not data:
                loger("warning").warning("No data returned.")
                return jsonify({"status":False,"data":"","message":"No data returned.","error":""}),200
            return jsonify({"status":True,"msg":"","data": data,"total_incharges":total_incharges,"error":""}),201
        else:
            employees=Employee.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            data=[Employee.to_json(i) for i in employees]
            if not data:
                loger("warning").warning("No data returned.")
                return jsonify({"status":False,"data":"","message":"No data returned.","error":""}),200
            return jsonify({"status":True,"msg":"","data": data,"total_incharges":total_incharges,"error":""}),201  

    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"data":"","msg":"","eroor":str(e)}),500
    
@incharge.route('/incharge-profile/<int:id>')
@token_required
@permission_required('read_team')
def inchargeProfile(id):
    try:
        incharge=Employee.query.get(id)
        if not incharge:
            loger("warning").warning("incharge not exist.")
            return jsonify({"status":False,"data":"","message":"incharge not exist.","error":""}),200
        loger("info").info("incharge profile viewed")
        return jsonify({"status":True,"data":[Employee.profile(incharge)],"msg":"","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"data":"","msg":"","eroor":str(e)}),500   
    
@incharge.route('/update-incharge/<int:id>',methods=['PUT'])
@token_required
@permission_required('edit_team')
def updateIncharge(id):
    try:
        data=request.get_json()
        incharge=Employee.query.get(id)
        if not incharge:
            loger("warning").warning("incharge not exist.")
            return jsonify({"status":False,"data":"","message":"incharge not exist.","error":""}),200
        incharge.status=data.get('status')
        incharge.name=data.get('name')
        incharge.dob=data.get('dob')
        incharge.gender=data.get('gender')
        incharge.address=data.get('address')
        incharge.city=data.get('city')
        incharge.district=data.get('district')
        incharge.state=data.get('state')
        incharge.pincode=data.get('pincode')
        incharge.aadhar=data.get('aadhar')
        incharge.mobile=data.get('mobile')
        incharge.join_date=data.get('join_date')  
        db.session.commit()
        loger("info").info("incharge updated successfully.")
        return jsonify({"status":True,"data":[Employee.to_json(incharge)],"msg":"incharge updated successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"data":"","msg":"","eroor":str(e)}),500

@incharge.route('/delete-incharge/<int:id>',methods=['DELETE'])
@token_required
@permission_required('delete_team')
def deleteIncharge(id):
    try:
        incharge=Employee.query.get(id)
        if not incharge:
            loger("warning").warning("incharge not exist.")
            return jsonify({"status":False,"data":"","message":"incharge not exist.","error":""}),200
        db.session.delete(incharge)
        db.session.commit()
        loger("info").info("incharge deleted successfully.")
        return jsonify({"status":True,"data":"","msg":"incharge deleted successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"data":"","msg":"","eroor":str(e)}),500