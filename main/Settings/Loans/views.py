from flask import Blueprint,request,jsonify
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
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@settings_loans.route('/put-eligibility/<int:id>',methods=["PUT"])
def update_eligibility(id):
    try:
        data=request.get_json()
        value=data.get("value")
        entry=MasterData.query.get(id)
        entry.value=value
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@settings_loans.route("/get-eligibility")
def show_eligibility():
    data=MasterData.query.filter(MasterData.property=="Minimum Amount In Savings Rs")
    result=[]
    for i in data:
        id=i.id
        property=i.property
        value=i.value
        info={
            "id":id,
            "property":property,
            "value":value
        }
        result.append(info)
    return jsonify({
        "data":result
    })

#criteria:
@settings_loans.route("/post-criteria",methods=["POST"])
def criteria():
    try:
        data=request.get_json()
        minimum_amount=data.get("minimum_amount")
        maximum_amount=data.get("maximum_amount")
        loan_amount=data.get("loan_amount")
        entry=LoanCriteria(minimum_amount=minimum_amount,
                        maximum_amount=maximum_amount,
                        loan_amount=loan_amount)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "minimum_amount":entry.minimum_amount,
            "maximum_amount":entry.maximum_amount,
            "loan_amount":entry.loan_amount
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

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
        return jsonify({
            "data":result
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@settings_loans.route("/delete-criteria/<int:id>",methods=["DELETE"])
def delete_criteria(id):
    try:
        data=LoanCriteria.query.get(id)
        if data is None:
            return jsonify({
                "message":"data is not exist"
            })
        db.session.delete(data)
        db.session.commit()
        return jsonify({
            "message":"data deleted succesfully"
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

#Repayment tenure:
@settings_loans.route("/post-repayment-tenure",methods=["POST"])
def repaymentTenure():
    try:
        data=request.get_json()
        property="Repayment_Tenure"
        value=data.get("value")
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "property":property,
            "value":value
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@settings_loans.route("/get-repayment-tenure")
def getRepaymentTenure():
    try:
        data=MasterData.query.filter(MasterData.property=="Repayment_Tenure")
        result=[]
        for i in data:
            id=i.id
            repaymentTenure=i.property
            value=i.value
            info={
                "id":id,
                "property":repaymentTenure,
                "value":value
            }
            result.append(info)
        return jsonify({
            "data":result
        }) 
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@settings_loans.route("/put-repayment-tenure/<int:id>",methods=["PUT"])
def updateRepaymentTenure(id):
    try:
        data=request.get_json()
        value=data.get("value")
        entry=MasterData.query.get(id)
        entry.value=value
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

#Repayment due days:
@settings_loans.route("/post-repayment-days",methods=["POST"])
def postRepaymentDays():
    try:
        data=request.get_json()
        property="Repayment_days"
        value=data.get("value")
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "property":entry.property,
            "value":entry.value
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@settings_loans.route("/get-repayment-days")
def getRepaymentDays():
    try:
        data=MasterData.query.filter(MasterData.property=="Repayment_days")
        result=[]
        for i in data:
            id=i.id
            property=i.property
            value=i.value
            info={
                "id":id,
                "property":property,
                "value":value
            }  
            result.append(info) 
        return jsonify({
            "data":result
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@settings_loans.route("/put-repayment-days/<int:id>",methods=["PUT"])
def updateReypaymentDays(id):
    try:
        data=request.get_json()
        value=data.get("value")
        entry=MasterData.query.get(id)
        entry.value=value
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

#Fine Amount For Defaulters Rs :
@settings_loans.route("/post-amount-defaulters",methods=["POST"])
def amountDefaulters():
    try:
        data=request.get_json()
        property="Amount For Defaulters"
        value=data.get("value")
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@settings_loans.route('/get-amount-defaulters')
def getAmountDefaulters():
    try:
        data=MasterData.query.filter(MasterData.property=="Amount For Defaulters")
        result=[]
        for i in data:
            id=i.id
            property=i.property
            value=i.value
            info={
                "id":id,
                "property":property,
                "value":value
            }
            result.append(info)
        return jsonify({
            "data":result
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@settings_loans.route("/put-amount-defaulters/<int:id>",methods=["PUT"])
def updateAmountDefaulters(id):
    try:
        data=request.get_json()
        value=data.get("value")
        entry=MasterData.query.get(id)
        entry.value=value
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "properety":entry.property,
            "value":entry.value
        })
    except Exception  as e:
        return jsonify({
            "error":str(e)
        })

#Black list(or Block list):
@settings_loans.route("/post-emi-notpaid",methods=["POST"])
def blacklist():
    try:
        data=request.get_json()
        property="EMI not paid for months"
        value=data.get("value")
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@settings_loans.route("/get-emi-notpaid")
def getBlackList():
    try:
        data=MasterData.query.filter(MasterData.property=="EMI not paid for months")
        result=[]
        for i in data:
            id=i.id
            property=i.property
            value=i.value
            info={
                "id":id,
                "property":property,
                "value":value
            } 
            result.append(info)
        return jsonify({
            "data":result
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
   
@settings_loans.route("/put-emi-notpaid/<int:id>",methods=["PUT"])   
def updateBlackList(id):
    try:
        data=request.get_json()
        value=data.get("value")
        entry=MasterData.query.get(id)
        entry.value=value
        db.session.commit()
        return jsonify({
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })