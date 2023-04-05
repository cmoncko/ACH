from flask import Blueprint,request,jsonify
from main.utils import loger
from main.extensions import db
from main.Settings.Services.models import BenefitType
from main.Settings.Funds.models import MasterData

settingServices=Blueprint('settingServices',__name__,url_prefix='/settings-services')

@settingServices.route('/add-benefit',methods=['POST'])
def addBenefitType():
    try:
        data=request.get_json()
        name=data.get('name')
        if not name:
            loger("warning").warning("name should be entered!")
            return jsonify({"status":False,"data":"","msg":"name should be entered!","error":""}),200
        entry=BenefitType(name=name)
        db.session.add(entry)
        db.session.commit()
        data={"id":entry.id,"name":entry.name}
        loger("info").info("benefit type added")
        return jsonify({"status":True,"data":data,"msg":"benefit type added","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settingServices.route('/show-all-benefits')
def showAll():
    try:
        benefits=BenefitType.query.all()
        data=[]
        for benefit in benefits:
            id=benefit.id
            name=benefit.name
            data.append({"id":id,"name":name})
        if not data:
            loger("warning").warning("no data")
            return jsonify({"satus":False,"data":data,"msg":"no data.","error":""}),200
        loger("info").info("benefit(s) viewed.")
        return jsonify({"satus":True,"data":data,"msg":"benefit(s) viewed","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
@settingServices.route('/delete-benefit/<int:id>',methods=['DELETE'])
def delete(id):
    try:
        entry=BenefitType.query.get(id)
        if not entry:
            loger("warning").warning("benefit not exist.")
            return jsonify({"satus":False,"data":"","msg":"minage not exist.","error":""}),200
        db.session.delete(entry)
        db.session.commit()
        loger("info").info("benefit deleted successfully.")
        return jsonify({"satus":True,"data":"","msg":"benefit deleted successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settingServices.route('/add-minage',methods=['POST'])
def addMinAge():
    try:
        data=request.get_json()
        property="minage"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter minage.")
            return jsonify({"satus":False,"data":"","msg":"enter minage.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("minage added successfully.")
        return jsonify({"satus":True,"data":data,"msg":"minage added successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settingServices.route('/show-minage/<int:id>')
def showMinAge(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("minage not exist.")
            return jsonify({"satus":False,"data":"","msg":"minage not exist.","error":""}),200
        if entry.property!='minage':
            loger("warning").warning("this is not minage.")
            return jsonify({"satus":False,"data":"","msg":"this is not minage.","error":""}),200
        info={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("minage viewed successfully.")
        return jsonify({"satus":True,"data":info,"msg":"minage viewed successfully.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
@settingServices.route('/update-minage/<int:id>',methods=['PUT'])
def updateMinAge(id):
    try:
        details=MasterData.query.get(id)
        if not details:
            loger("warning").warning("minage not exist.")
            return jsonify({"satus":False,"data":"","msg":"minage not exist.","error":""}),200
        if details.property!='minage':
            loger("warning").warning("this is not minage.")
            return jsonify({"satus":False,"data":"","msg":"this is not minage.","error":""}),200
        data=request.get_json()
        details.value=data.get('value')
        db.session.commit()
        info={
            "id":details.id,
            "property":details.property,
            "value":details.value
        }
        loger("info").info("minage updated successfully.")
        return jsonify({"satus":True,"data":info,"msg":"minage updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingServices.route('/add-maxage',methods=['POST'])
def addMaxAge():
    try:
        data=request.get_json()
        property="maxage"
        value=data.get("value")
        if not value:
            loger("warning").warning("enter maxage.")
            return jsonify({"satus":False,"data":"","msg":"enter maxage.","error":""}),200
        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        data={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("maxage added successfully.")
        return jsonify({"satus":True,"data":data,"msg":"maxage added successfully.","error":""}),201
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500
    
@settingServices.route('/show-maxage/<int:id>')
def showMaxAge(id):
    try:
        entry=MasterData.query.get(id)
        if not entry:
            loger("warning").warning("maxage not exist.")
            return jsonify({"satus":False,"data":"","msg":"maxage not exist.","error":""}),200
        if entry.property!='maxage':
            loger("warning").warning("this is not maxage.")
            return jsonify({"satus":False,"data":"","msg":"this is not maxage.","error":""}),200
        info={
            "id":entry.id,
            "property":entry.property,
            "value":entry.value
        }
        loger("info").info("maxage viewed successfully.")
        return jsonify({"satus":True,"data":info,"msg":"maxage viewed successfully.","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500

@settingServices.route('/update-maxage/<int:id>',methods=['PUT'])
def updateMaxAge(id):
    try:
        details=MasterData.query.get(id)
        if not details:
            loger("warning").warning("maxage not exist.")
            return jsonify({"satus":False,"data":"","msg":"maxage not exist.","error":""}),200
        if details.property!='maxage':
            loger("warning").warning("this is not maxage.")
            return jsonify({"satus":False,"data":"","msg":"this is not maxage.","error":""}),200
        data=request.get_json()
        details.value=data.get('value')
        db.session.commit()
        info={
            "id":details.id,
            "property":details.property,
            "value":details.value
        }
        loger("info").info("maxage updated successfully.")
        return jsonify({"satus":True,"data":info,"msg":"maxage updated successfully.","error":""}),204
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"satus":False,"data":"","msg":"","error":str(e)}),500