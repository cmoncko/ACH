from flask import Blueprint,request,jsonify
from main.Settings.Teams.models import Address
from main.Settings.Funds.models import MasterData
from main.extensions import db

settingsTeams=Blueprint('settingsteams',__name__,url_prefix="/settings-team")

@settingsTeams.route("/add-address",methods=["POST"])
def addAddress():
    try:
        data = request.get_json()
        city=data.get("city")
        cities=[]
        data=Address.query.all()
        for i in data:
            c=i.city
            cities.append(c)
        if city in cities:
            return jsonify({
                "message":"already city exist"
            })
        district=data.get("district")
        state=data.get("state")
        country=data.get("country")
        pincode=data.get("pincode")
        entry=Address(city=city,district=district,state=state,country=country,pincode=pincode)

        db.session.add(entry)
        db.session.commit()

        return jsonify({
            "id":entry.id,
            "city":entry.city,
            "district":entry.district,
            "state":entry.state,
            "country":entry.country,
            "pincode":entry.pincode,
            
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

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
        return jsonify({
            "data":result
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@settingsTeams.route('/delete-address/<int:id>',methods=['DELETE'])           
def deleteaddress(id):
    try:
        data=Address.query.get(id)
        if data is None:
            return jsonify({
                "message":"city not exist"
            })

        db.session.delete(data)
        db.session.commit()

        return jsonify({
            "message":"deleted sucessfully"
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@settingsTeams.route("/add-nominee",methods=["POST"])    
def addnominee():
    try:
        data=request.get_json()
        property="relation"
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
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@settingsTeams.route('/delete-nominee/<int:id>',methods=["DELETE"])
def deltenomimee(id):
    try:
        data=MasterData.query.get(id)
        if data is None:
            return jsonify({
                "message":"nominee not exist"
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







            

         
        
