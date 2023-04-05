from flask import Blueprint,request,jsonify
from main.utils import loger
from main.extensions import db
from main.Settings.Funds.models import MasterData
from main.Settings.Loans.models import LoanCriteria

settings_loans=Blueprint("settingsLoans",__name__,url_prefix="/settings-loans")

#Eligibility:
@settings_loans.route('/post-eligibility',methods=["POST"])
def eligibility():
    try:
        data=request.get_json()
        property="Minimum Amount In Savings Rs"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter Minimum amount'.")
            return jsonify({"satus":False,"data":"","msg":"enter Minimum amount.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("eligibility added successfully.")
        return jsonify({"satus":True,"data":data,"msg":"eligibility added successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settings_loans.route('/update-eligibility/<int:id>',methods=["PUT"])
def update_eligibility(id):
    try:
        data=request.get_json()
        value=data.get("value")
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("eligibility not exist.")
            return jsonify({"satus":False,"data":"","msg":"eligibility not exist.","error":""}),200
        if entry.property!="Amount Per Year Rs":
            loger("warning").warning("this is not eligibility.")
            return jsonify({"satus":False,"data":"","msg":"this is not eligibility.","error":""}),200
        entry.value=value
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("eligibility updated successfully.")
        return jsonify({"satus":True,"data":data,"msg":"eligibility updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settings_loans.route("/get-eligibility/<int:id>")
def show_eligibility(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("eligibility not exist.")
            return jsonify({"satus":False,"data":"","msg":"eligibility not exist.","error":""}),200
        if entry.property!="Amount Per Year Rs":
            loger("warning").warning("this is not eligibility.")
            return jsonify({"satus":False,"data":"","msg":"this is not eligibility.","error":""}),200
        info={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("eligibility viewed successfully.")
        return jsonify({"satus":True,"data":info,"msg":"eligibility viewed successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

#criteria:
@settings_loans.route("/post-criteria",methods=["POST"])
def criteria():
    try:
        data=request.get_json()
        minimum_amount=data.get("minimum_amount")
        if not minimum_amount:
            loger("warning").warning("minimum amount not exist.")
            return jsonify({"satus":False,"data":"","msg":"minimum amount not exist.","error":""}),200
        maximum_amount=data.get("maximum_amount")
        if not maximum_amount:
            loger("warning").warning("maximum amount not exist.")
            return jsonify({"satus":False,"data":"","msg":"maximum amount not exist.","error":""}),200
        loan_amount=data.get("loan_amount")
        if not loan_amount:
            loger("warning").warning("loan amount not exist.")
            return jsonify({"satus":False,"data":"","msg":"loan amount not exist.","error":""}),200
        entry=LoanCriteria(minimum_amount=minimum_amount,
                        maximum_amount=maximum_amount,
                        loan_amount=loan_amount)
        db.session.add(entry)
        db.session.commit()
        data={
            "minimum_amount":entry.minimum_amount,
            "maximum_amount":entry.maximum_amount,
            "loan_amount":entry.loan_amount
        }
        loger("info").info("criteria added successfully.")
        return jsonify({"satus":True,"data":data,"msg":"criteria added successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settings_loans.route("/get-criteria")
def show_criteria():
    try:
        data=LoanCriteria.query.all()
        result=[]
        for i in data:
            id=i.id
            minimum_amount=i.minimum_amount
            maximum_amount=i.maximum_amount
            loan_amount=i.loan_amount
            info={
                "id":id,
                "minimum_amount":minimum_amount,
                "maximum_amount":maximum_amount,
                "loan_amount":loan_amount
            }
            result.append(info)
        if not result:
            loger("warning").warning("no dat")
            return jsonify({"satus":False,"data":result,"msg":"no data.","error":""}),200
        loger("info").info("criterias viewed.")
        return jsonify({"satus":True,"data":result,"msg":"criterias viewed.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settings_loans.route("/delete-criteria/<int:id>",methods=["DELETE"])
def delete_criteria(id):
    try:
        data=LoanCriteria.query.get(id)
        if not data:
            loger("warning").warning("criteria not exist")
            return jsonify({"satus":False,"data":"","msg":"criteria not exist.","error":""}),200
        db.session.delete(data)
        db.session.commit()
        loger("info").info("criteria deleted.")
        return jsonify({"satus":True,"data":"","msg":"criteria deleted.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

#Repayment tenure:
@settings_loans.route("/post-repayment-tenure",methods=["POST"])
def repaymentTenure():
    try:
        data=request.get_json()
        property="Repayment_Tenure"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter Repayment_Tenure'.")
            return jsonify({"satus":False,"data":"","msg":"enter Repayment_Tenure.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Repayment_Tenure added successfully.")
        return jsonify({"satus":True,"data":data,"msg":"Repayment_Tenure added successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settings_loans.route("/get-repayment-tenure/<int:id>")
def getRepaymentTenure(id):
    try:
        data=MasterData.query.get(id)
        if not data:
            loger("warning").warning("repayment not exist.")
            return jsonify({"satus":False,"data":"","msg":"repayment not exist.","error":""}),200
        if data.property!="Repayment_Tenure":
            loger("warning").warning("this is not repayment.")
            return jsonify({"satus":False,"data":"","msg":"this is not repayment.","error":""}),200
        info={
            "id":data.id,
            "property":data.property,
            "value":data.value
        }
        loger("info").info("Repayment_Tenure viewed successfully.")
        return jsonify({"satus":True,"data":info,"msg":"Repayment_Tenure viewed successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settings_loans.route("/update-repayment-tenure/<int:id>",methods=["PUT"])
def updateRepaymentTenure(id):
    try:
        data=request.get_json()
        value=data.get("value")
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("repayment tenure not exist.")
            return jsonify({"satus":False,"data":"","msg":"repayment tenure not exist.","error":""}),200
        if entry.property!="Repayment_Tenure":
            loger("warning").warning("this is not repayment.")
            return jsonify({"satus":False,"data":"","msg":"this is not repayment.","error":""}),200
        entry.value=value
        db.session.commit()
        info={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Repayment_Tenure updated successfully.")
        return jsonify({"satus":True,"data":info,"msg":"Repayment_Tenure updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

#Repayment due days:
@settings_loans.route("/post-repayment-days",methods=["POST"])
def postRepaymentDays():
    try:
        data=request.get_json()
        property="Repayment_Due_days"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter Repayment_Due_days'.")
            return jsonify({"satus":False,"data":"","msg":"enter Repayment_Due_days.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Repayment_Due_days added successfully.")
        return jsonify({"satus":True,"data":data,"msg":"Repayment_Due_days added successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settings_loans.route("/get-repayment-days/<int:id>")
def getRepaymentDays(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("Repayment_Due_days not exist.")
            return jsonify({"satus":False,"data":"","msg":"Repayment_Due_days not exist.","error":""}),200
        if entry.property!="Repayment_Due_days":
            loger("warning").warning("this is not Repayment_Due_days.")
            return jsonify({"satus":False,"data":"","msg":"this is not Repayment_Due_days.","error":""}),200
        info={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Repayment_Due_days viewed successfully.")
        return jsonify({"satus":True,"data":info,"msg":"Repayment_Due_days viewed successfully.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settings_loans.route("/update-repayment-days/<int:id>",methods=["PUT"])
def updateReypaymentDays(id):
    try:
        data=request.get_json()
        value=data.get("value")
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("Repayment_Due_days not exist.")
            return jsonify({"satus":False,"data":"","msg":"Repayment_Due_days not exist.","error":""}),200
        if entry.property!="Repayment_Due_days":
            loger("warning").warning("this is not Repayment_Due_days.")
            return jsonify({"satus":False,"data":"","msg":"this is not Repayment_Due_days.","error":""}),200
        entry.value=value
        db.session.commit()
        info={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Repayment_Due_days updated successfully.")
        return jsonify({"satus":True,"data":info,"msg":"Repayment_Due_days updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

#Fine Amount For Defaulters Rs :
@settings_loans.route("/post-amount-defaulters",methods=["POST"])
def amountDefaulters():
    try:
        data=request.get_json()
        property="Amount For Defaulters"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter Amount For Defaulters'.")
            return jsonify({"satus":False,"data":"","msg":"enter Amount For Defaulters.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Amount For Defaulters added successfully.")
        return jsonify({"satus":True,"data":data,"msg":"Amount For Defaulters added successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settings_loans.route('/get-amount-defaulters/<int:id>')
def getAmountDefaulters(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("Amount For Defaulters not exist.")
            return jsonify({"satus":False,"data":"","msg":"Amount For Defaulters not exist.","error":""}),200
        if entry.property!="Amount For Defaulters":
            loger("warning").warning("this is not Amount For Defaulters.")
            return jsonify({"satus":False,"data":"","msg":"this is not Amount For Defaulters.","error":""}),200
        info={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Amount For Defaulters viewed successfully.")
        return jsonify({"satus":True,"data":info,"msg":"Amount For Defaulters viewed successfully.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settings_loans.route("/update-amount-defaulters/<int:id>",methods=["PUT"])
def updateAmountDefaulters(id):
    try:
        data=request.get_json()
        value=data.get("value")
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("Amount For Defaulters not exist.")
            return jsonify({"satus":False,"data":"","msg":"Amount For Defaulters not exist.","error":""}),200
        if entry.property!="Amount For Defaulters":
            loger("warning").warning("this is not Amount For Defaulters.")
            return jsonify({"satus":False,"data":"","msg":"this is not Amount For Defaulters.","error":""}),200
        entry.value=value
        db.session.commit()
        info={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Amount For Defaulters updated successfully.")
        return jsonify({"satus":True,"data":info,"msg":"Amount For Defaulters updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

#Black list(or Black list):
@settings_loans.route("/post-emi-notpaid",methods=["POST"])
def blacklist():
    try:
        data=request.get_json()
        property="How Many Months EMI Not Paid?"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter 'How Many Months EMI Not Paid?'.")
            return jsonify({"satus":False,"data":"","msg":"enter 'How Many Months EMI Not Paid?'.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("'How Many Months EMI Not Paid?' added successfully.")
        return jsonify({"satus":True,"data":data,"msg":"'How Many Months EMI Not Paid?' added successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settings_loans.route("/get-emi-notpaid/<int:id>")
def getBlackList(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("'How Many Months EMI Not Paid?' not exist.")
            return jsonify({"satus":False,"data":"","msg":"'How Many Months EMI Not Paid?' not exist.","error":""}),200
        if entry.property!='How Many Months EMI Not Paid?':
            loger("warning").warning("this is not 'How Many Months EMI Not Paid?'.")
            return jsonify({"satus":False,"data":"","msg":"this is not 'How Many Months EMI Not Paid?'.","error":""}),200
        info={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("'How Many Months EMI Not Paid?' viewed successfully.")
        return jsonify({"satus":True,"data":info,"msg":"'How Many Months EMI Not Paid?' viewed successfully.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
   
@settings_loans.route("/put-emi-notpaid/<int:id>",methods=["PUT"])   
def updateBlackList(id):
    try:
        data=request.get_json()
        value=data.get("value")
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("'How Many Months EMI Not Paid?' not exist.")
            return jsonify({"satus":False,"data":"","msg":"'How Many Months EMI Not Paid?' not exist.","error":""}),200
        if entry.property!='How Many Months EMI Not Paid?':
            loger("warning").warning("this is not 'How Many Months EMI Not Paid?'.")
            return jsonify({"satus":False,"data":"","msg":"this is not 'How Many Months EMI Not Paid?'.","error":""}),200
        entry.value=value
        db.session.commit()
        info={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("'How Many Months EMI Not Paid?' updated successfully.")
        return jsonify({"satus":True,"data":info,"msg":"'How Many Months EMI Not Paid?' updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500