from flask import Blueprint,request,jsonify
from main.extensions import db
from main.Settings.Services.models import BenefitType
from main.Settings.Funds.models import MasterData

settingServices=Blueprint('settingServices',__name__,url_prefix='/settings-services')

@settingServices.route('/add-benefit',methods=['POST'])
def addBenefitType():
    try:
        data=request.get_json()
        name=data.get('name')

        entry=BenefitType(name=name)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            'id':entry.id,
            'name':entry.name
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@settingServices.route('/show-all')
def showAll():
    try:
        benefits=BenefitType.query.all()
        data=[]
        for benefit in benefits:
            id=benefit.id
            name=benefit.name
            data.append({"id":id,"name":name})
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@settingServices.route('/delete/<int:id>',methods=['DELETE'])
def delete(id):
    try:
        entry=BenefitType.query.get(id)
        Benefit_id=entry.id
        name=entry.name
        db.session.delete(entry)
        db.session.commit()
        return jsonify({
            "message":f'deleted benefit id is {Benefit_id} name is {name}'
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
        
@settingServices.route('/add-minage',methods=['POST'])
def addMinAge():
    try:
        data=request.get_json()
        prperty="minage"
        value=data.get("value")

        entry=MasterData(property=property,value=value)
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            'id':entry.id,
            'name':entry.property,
            'value':entry.value
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@settingServices.route('/show-minage')
def showMinAge():
    try:
        details=MasterData.query.filter(MasterData.property=='minage')
        data=[]
        for i in details:
            data.append({"id":i.id,
		    "property":i.property,
		    "value":i.value})
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
@settingServices.route('/update-minage/<int:id>',methods=['PUT'])
def updateMinAge(id):
    try:
        details=MasterData.query.get(id)
        data=request.get_json()
        details.value=data.get('value')
        db.session.commit()
        return jsonify({"id":details.id,
		    "property":details.property,
		    "value":details.value})
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
