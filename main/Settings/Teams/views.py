from flask import Blueprint,request,jsonify
from main.utils import loger
from main.Settings.Teams.models import Address
from main.Settings.Funds.models import MasterData
from main.extensions import db

settingsTeams=Blueprint('settingsteams',__name__,url_prefix="/settings-team")

@settingsTeams.route("/add-address",methods=["POST"])
def addAddress():
    try:
        data = request.get_json()
        city=data.get("city")
        exist=Address.query.filter_by(citiy=city).first()
        if exist:
            loger("warning").warning("city already exist.")
        district=data.get("district")
        if not district:
            loger("warning").warning("district should be entered!")
            return jsonify({"status":False,"data":"","msg":"district should be entered!","error":""}),200
        state=data.get("state")
        if not state:
            loger("warning").warning("state should be entered!")
            return jsonify({"status":False,"data":"","msg":"state should be entered!","error":""}),200
        country=data.get("country")
        if not country:
            loger("warning").warning("country should be entered!")
            return jsonify({"status":False,"data":"","msg":"country should be entered!","error":""}),200
        pincode=data.get("pincode")
        if not pincode:
            loger("warning").warning("pincode should be entered!")
            return jsonify({"status":False,"data":"","msg":"pincode should be entered!","error":""}),200
        entry=Address(city=city,district=district,state=state,country=country,pincode=pincode)
        db.session.add(entry)
        db.session.commit()
        data={"id":entry.id,
            "city":entry.city,
            "district":entry.district,
            "state":entry.state,
            "country":entry.country,
            "pincode":entry.pincode}
        loger("info").info("address added successfully")
        return jsonify({"status":True,"data":data,"msg":"address added successfull.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsTeams.route("/show-all")
def showalladress():
    try:
        data=Address.query.all()
        result=[]
        for i in data:
            id=i.id
            city=i.city
            district=i.district
            state=i.state
            country=i.country
            pincode=i.pincode

            temp={"id":id,
                  "city":city,
                  "district":district,
                  "state":state,
                  "country":country,
                  "pincode":pincode
                  }
            result.append(temp)
        if not result:
            loger("warning").warning("no data")
            return jsonify({"satus":False,"data":result,"msg":"no data.","error":""}),200
        loger("info").info("address viewed.")
        return jsonify({"satus":True,"data":result,"msg":"address viewed","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsTeams.route('/delete-address/<int:id>',methods=['DELETE'])           
def deleteaddress(id):
    try:
        data=Address.query.get(id)
        if not data:
            loger("warning").warning("address not exist")
            return jsonify({"satus":False,"data":"","msg":"address not exist","error":""}),200
        db.session.delete(data)
        db.session.commit()

        loger("info").info("address deleted.")
        return jsonify({"satus":True,"data":"","msg":"address deleted","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsTeams.route("/add-nominee",methods=["POST"])    
def addnominee():
    try:
        data=request.get_json()
        property="relation"
        value=data.get("value")
        if not value:
            loger("warning").warning("relation should be entered!")
            return jsonify({"status":False,"data":"","msg":"relation should be entered!","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={"property":entry.property,
            "value":entry.value}
        loger("info").info("nominee relation added.")
        return jsonify({"satus":True,"data":data,"msg":"nominee relation added","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsTeams.route('/all-nominee')    
def shownominee():
    try:
        nominees=MasterData.query.filter(MasterData.property=="relation")
        data=[]
        for i in nominees:
            id=i.id
            property=i.property
            value=i.value
            info={"property":property,
                  "value":value,
                  "id":id}
            data.append(info)
        if not data:
            loger("warning").warning("no data")
            return jsonify({"satus":False,"data":data,"msg":"no data.","error":""}),200
        loger("info").info("nominee relation viewed.")
        return jsonify({"satus":True,"data":data,"msg":"nominee relation viewed","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingsTeams.route('/delete-nominee/<int:id>',methods=["DELETE"])
def deltenomimee(id):
    try:
        data=MasterData.query.get(id)
        if not data:
            loger("warning").warning("relation not exist")
            return jsonify({"satus":False,"data":"","msg":"relation not exist","error":""}),200
        if data.property!="relation":
            loger("warning").warning("this is not relation.")
            return jsonify({"satus":False,"data":"","msg":"this is not relation.","error":""}),200
        db.session.delete(data)
        db.session.commit()
        loger("info").info("relation deleted.")
        return jsonify({"satus":True,"data":"","msg":"relation deleted","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500