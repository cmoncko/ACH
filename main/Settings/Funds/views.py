from flask import Blueprint,request,jsonify
from main.utils import loger
from main.Settings.Funds.models import MasterData
from main.extensions import db

#santha
settingsfunds=Blueprint("settingsfunds",__name__,url_prefix="/settings-funds")

@settingsfunds.route("/add-amount",methods=["POST"])
def addAmount():
    try:
        data=request.get_json()
        property="Amount Per Year Rs"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter 'Amount Per Year Rs'.")
            return jsonify({"satus":False,"data":"","msg":"enter 'Amount Per Year Rs'.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("santha amount added successfully.")
        return jsonify({"satus":True,"data":data,"msg":"santha amount added successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settingsfunds.route("/update-santha-amount/<int:id>",methods=["POST"])
def updateAmount(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("santha amount not exist.")
            return jsonify({"satus":False,"data":"","msg":"santha amount not exist.","error":""}),200
        if entry.property!="Amount Per Year Rs":
            loger("warning").warning("this is not santha amount.")
            return jsonify({"satus":False,"data":"","msg":"this is not santha amount.","error":""}),200
        data=request.get_json()
        entry.value=data.get("value")
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("santha amount updated successfully.")
        return jsonify({"satus":True,"data":data,"msg":"santha amount updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsfunds.route("/add-santhayear",methods=["POST"])
def santhaYear():
    try:
        data=request.get_json()
        property="Santha Year"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter 'Santha Year'.")
            return jsonify({"satus":False,"data":"","msg":"enter 'Santha Year'.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("santha year added successfully.")
        return jsonify({"satus":True,"data":data,"msg":"santha year added successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsfunds.route('/show-santhayear')    
def showSanthaYear():
    try:
        data=MasterData.query.filter(MasterData.property=="Santha Year")
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
        if not result:
            loger("warning").warning("No data'.")
            return jsonify({"satus":False,"data":data,"msg":"","error":""}),200
        loger("info").info("santha years viewed.")
        return jsonify({"satus":True,"data":data,"msg":"","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsfunds.route("/delete-santhayear/<int:id>",methods=["DELETE"])
def deleteSanthaYear(id):
    try:
        data=MasterData.query.get(id)
        if not data:
            loger("warning").warning("santha year not exist.")
            return jsonify({"satus":False,"data":"","msg":"santha year not exist.","error":""}),200
        if data.property!="Santha Year":
            loger("warning").warning("this is not santha year.")
            return jsonify({"satus":False,"data":"","msg":"this is not santha year.","error":""}),200
        db.session.delete(data)
        db.session.commit()
        loger("info").info("santha year deleted.")
        return jsonify({"satus":True,"data":"","msg":"santha year deleted.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

#Savings

@settingsfunds.route("/add-min",methods=["POST"])
def memberToPayMin():
    try:
        data=request.get_json()
        property="Min"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter 'Min' for savings.")
            return jsonify({"satus":False,"data":"","msg":"enter 'Min' for savings.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={"id":entry.id,
            "property":entry.property,
            "value":entry.value}
        loger("info").info("min amount added for savings.")
        return jsonify({"satus":True,"data":"","msg":"min amount added for savings.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settingsfunds.route("/update-min/<int:id>",methods=["POST"])
def updateMinAmount(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("min amount not exist.")
            return jsonify({"satus":False,"data":"","msg":"min amount not exist.","error":""}),200
        if entry.property!="Min":
            loger("warning").warning("this is not min amount.")
            return jsonify({"satus":False,"data":"","msg":"this is not min amount.","error":""}),200
        data=request.get_json()
        entry.value=data.get("value")
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Saving Min amount updated successfully.")
        return jsonify({"satus":True,"data":data,"msg":"Saving Min amount updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsfunds.route("/add-max",methods=["POST"])
def memberToPayMax():
    try:
        data=request.get_json()
        property="Max"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter 'Max' for savings.")
            return jsonify({"satus":False,"data":"","msg":"enter 'Max' for savings.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={"id":entry.id,
            "property":entry.property,
            "value":entry.value}
        loger("info").info("max amount added for savings.")
        return jsonify({"satus":True,"data":"","msg":"max amount added for savings.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsfunds.route("/update-max/<int:id>",methods=["POST"])
def updateMaxAmount(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("max amount not exist.")
            return jsonify({"satus":False,"data":"","msg":"max amount not exist.","error":""}),200
        if entry.property!="Max":
            loger("warning").warning("this is not max amount.")
            return jsonify({"satus":False,"data":"","msg":"this is not max amount.","error":""}),200
        data=request.get_json()
        entry.value=data.get("value")
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Saving Max amount updated successfully.")
        return jsonify({"satus":True,"data":data,"msg":"Saving Max amount updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

#withdraw

@settingsfunds.route("/add-minimum-balance",methods=["POST"])
def minimumBalance():
    try:
        data=request.get_json()
        property="To Maintain Minimum Balance of Rs"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter 'To Maintain Minimum Balance of Rs' for savings.")
            return jsonify({"satus":False,"data":"","msg":"enter 'To Maintain Minimum Balance of Rs' for savings.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={"id":entry.id,
            "property":entry.property,
            "value":entry.value}
        loger("info").info("'To Maintain Minimum Balance of Rs' added for savings.")
        return jsonify({"satus":True,"data":"","msg":"'To Maintain Minimum Balance of Rs' added for savings.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsfunds.route("/update-minimum-balance/<int:id>",methods=["POST"])
def updateMinimumBalance(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("To Maintain Minimum Balance amount not exist.")
            return jsonify({"satus":False,"data":"","msg":"To Maintain Minimum Balance amount not exist.","error":""}),200
        if entry.property!="To Maintain Minimum Balance of Rs":
            loger("warning").warning("this is not Maintain Minimum Balance amount.")
            return jsonify({"satus":False,"data":"","msg":"this is not Maintain Minimum Balance amount.","error":""}),200
        data=request.get_json()
        entry.value=data.get("value")
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("To Maintain Minimum Balance amount updated successfully.")
        return jsonify({"satus":True,"data":data,"msg":"To Maintain Minimum Balance amount updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsfunds.route("/add-annual-interest",methods=["POST"])
def annualInterstSaving():
    try:
        data=request.get_json()
        property="Annual Interest On Savings (Ex: 5%)"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter 'Annual Interest On Savings (Ex: 5%)' for savings.")
            return jsonify({"satus":False,"data":"","msg":"enter 'Annual Interest On Savings (Ex: 5%)' for savings.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={"id":entry.id,
            "property":entry.property,
            "value":entry.value}
        loger("info").info("'Annual Interest On Savings (Ex: 5%)' added for savings.")
        return jsonify({"satus":True,"data":"","msg":"'Annual Interest On Savings (Ex: 5%)' added for savings.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsfunds.route("/update-annual-interest/<int:id>",methods=["POST"])
def updateAnnualInterest(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("Annual interest amount not exist.")
            return jsonify({"satus":False,"data":"","msg":"Annual interest amount not exist.","error":""}),200
        if entry.property!="Annual Interest On Savings (Ex: 5%)":
            loger("warning").warning("this is not Annual interest amount.")
            return jsonify({"satus":False,"data":"","msg":"this is not Annual interest amount.","error":""}),200
        data=request.get_json()
        entry.value=data.get("value")
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Annual interest amount updated successfully.")
        return jsonify({"satus":True,"data":data,"msg":"Annual interest amount updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsfunds.route("/add-account-closing",methods=['POST'])    
def accountClosingFees():
    try:
        data=request.get_json()
        property="Account Closing Fees"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter 'Account Closing Fees' for savings.")
            return jsonify({"satus":False,"data":"","msg":"enter 'Account Closing Fees' for savings.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={"id":entry.id,
            "property":entry.property,
            "value":entry.value}
        loger("info").info("'Account Closing Fees' added for savings.")
        return jsonify({"satus":True,"data":"","msg":"'Account Closing Fees' added for savings.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settingsfunds.route("/update-account-closing/<int:id>",methods=["POST"])
def updateAccountClosing(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("Account Closing Fees amount not exist.")
            return jsonify({"satus":False,"data":"","msg":"Account Closing Fees amount not exist.","error":""}),200
        if entry.property!="Account Closing Fees":
            loger("warning").warning("this is not Account Closing Fees amount.")
            return jsonify({"satus":False,"data":"","msg":"this is not Account Closing Fees amount.","error":""}),200
        data=request.get_json()
        entry.value=data.get("value")
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("Account Closing Fees amount updated successfully.")
        return jsonify({"satus":True,"data":data,"msg":"Account Closing Fees amount updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500