from flask import Blueprint,request,jsonify
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


@settingsfunds.route("/add-santhayear",methods=["POST"])
def santhaYear():
    try:
        data=request.get_json()
        property="Santha Year"
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
        return jsonify({
            "data":result
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@settingsfunds.route("/delete-santhayear/<int:id>",methods=["DELETE"])
def deleteSanthaYear(id):
    try:
        data=MasterData.query.get(id)
        if data is None:
            return jsonify({
                "message":"data not exist"
            })
        db.session.delete(data)
        db.session.commit()
        return jsonify({
            "message":"deleted successfully"
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

#Savings

@settingsfunds.route("/add-min",methods=["POST"])
def memberToPayMin():
    try:
        data=request.get_json()
        property="Min"
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
    
@settingsfunds.route("/add-max",methods=["POST"])
def memberToPayMax():
    try:
        data=request.get_json()
        property="Max"
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


#withdraw

@settingsfunds.route("/add-minimum-balance",methods=["POST"])
def minimumBalance():
    try:
        data=request.get_json()
        property="To Maintain Minimum Balance of Rs"
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

@settingsfunds.route("/add-annual-interest",methods=["POST"])
def annualInterstSaving():
    try:
        data=request.get_json()
        property="Annual Interest On Savings (Ex: 5%)"
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

@settingsfunds.route("/add-account-closing",methods=['POST'])    
def accountClosingFees():
    try:
        data=request.get_json()
        property="Account Closing Fees"
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
    
    




