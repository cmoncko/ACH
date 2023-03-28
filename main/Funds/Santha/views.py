from flask import Blueprint,jsonify,request
from main.extensions import db
from datetime import datetime
from main.Settings.Funds.models import MasterData
from main.Teams.Members.models import MemberProfile
from main.Funds.Santha.models import SanthaPayments

santha=Blueprint('santha',__name__,url_prefix="/santha")

@santha.route('/pay-santha',methods=['POST'])
def paySantha():
    try:
        data=request.get_json()
        member_id=data.get('member_id')
        santha_for_year=data.get('santha_for_year')
        santha_amount=MasterData.query.filter_by(property="Amount Per Year Rs").first()
        if not santha_amount.value or santha_amount.value=="":
            return jsonify({
                "message":"Add santha per year amount at (Settings -> Funds -> Santha -> Amount Per Year Rs)"
            })
        santha_amount=int(santha_amount.value)
        received_amount=data.get('received_amount')
        received_date=data.get('received_date')

        member=[MemberProfile.to_json(i) for i in MemberProfile.query.filter(MemberProfile.id==member_id)]

        if len(member)<1:
            return jsonify({
                "message":"Member is not exist"
            })
        else:
            entry=SanthaPayments(member_id=member_id,
                                 santha_for_year=santha_for_year,
                                 santha_amount=santha_amount,
                                 received_amount=received_amount,
                                 received_date=received_date)

            db.session.add(entry)
            db.session.commit()

            return jsonify({
                "message":"santha details added successfully."
            })
    
    except Exception as e:
        return jsonify({
            "message":str(e)
        })

@santha.route('/santha-details')
def santhaDetails():
    try:
        page=request.args['page']
        per_page=request.args['per_page']
        search=request.args['search']
        if search:
            data=[]
            members=MemberProfile.query.filter((MemberProfile.id.contains(search)) | 
                                                (MemberProfile.name.contains(search)))
            for member in members:
                member_id=member.id
                name=member.name
                join_date=member.join_date
                
                #calculate term
                date_list=str(join_date).split('-')
                year_join=int(date_list[0])
                year_now=int(datetime.now().strftime("%Y"))
                term=year_now-year_join

                joinDateObj=datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
                joindate=joinDateObj.strftime("%d-%b-%Y") #join date eg(12-Jan-2020)
                santha_amount=term*60
                received_amount=0
            
                santha_details=SanthaPayments.query.filter(SanthaPayments.member_id==member_id)
                for detail in santha_details:
                    received_amount+=detail.received_amount

                due_amount=santha_amount-received_amount
                if due_amount<1:
                    isDue="No"
                else:
                    isDue="Yes"
                
                if isDue=="No" and term==0:
                    days_elapsed=0
                else:
                    #calculate leap year
                    leap_year=0
                    for i in range(term-1):
                        year_join+=1
                        if (year_join==400)or(year_join%4==0 and year_join%100!=0):
                            leap_year+=1

                    if int(received_amount)<60: 
                        days_elapsed=((term-1)*365)+int(datetime.now().strftime("%j"))+leap_year
                    else:
                        before_days=((term-1)-(received_amount//60))*365
                        if before_days==0:
                            days_elapsed=int(datetime.now().strftime("%j"))
                        else:
                            days_elapsed=before_days+leap_year
                info={
                    "member_id":member_id,
                    "name":name,
                    "join_date":joindate,
                    "term":term,
                    "santha_amount":santha_amount,
                    "received_amount":received_amount,
                    "is_due":isDue,
                    "due_amount":due_amount,
                    "days_elapsed":int(days_elapsed)
                }
                data.append(info)

            return jsonify({
                "data":data
            })
        else:
            data=[]
            members=MemberProfile.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            for member in members:
                member_id=member.id
                name=member.name
                join_date=member.join_date
                
                #calculate term
                date_list=str(join_date).split('-')
                year_join=int(date_list[0])
                year_now=int(datetime.now().strftime("%Y"))
                term=year_now-year_join

                joinDateObj=datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
                joindate=joinDateObj.strftime("%d-%b-%Y") #join date eg(12-Jan-2020)
                santha_amount=term*60
                received_amount=0
            
                santha_details=SanthaPayments.query.filter(SanthaPayments.member_id==member_id)
                for detail in santha_details:
                    received_amount+=detail.received_amount

                due_amount=santha_amount-received_amount
                if due_amount<1:
                    isDue="No"
                else:
                    isDue="Yes"
                
                if isDue=="No" and term==0:
                    days_elapsed=0
                else:
                    #calculate leap year
                    leap_year=0
                    for i in range(term):
                        year_join+=1
                        if (year_join==400)or(year_join%4==0 and year_join%100!=0):
                            leap_year+=1
                    # print(leap_year)
                    print(received_amount)
                    print(received_amount<60)
                    if int(received_amount)<60: 
                        days_elapsed=((term-1)*365)+int(datetime.now().strftime("%j"))+leap_year
                    else:
                        before_days=((term-1)-(received_amount//60))*365
                        if before_days==0:
                            days_elapsed=int(datetime.now().strftime("%j"))
                        else:
                            days_elapsed=before_days+leap_year
                info={
                    "member_id":member_id,
                    "name":name,
                    "join_date":joindate,
                    "term":term,
                    "santha_amount":santha_amount,
                    "received_amount":received_amount,
                    "is_due":isDue,
                    "due_amount":due_amount,
                    "days_elapsed":int(days_elapsed)
                }
                data.append(info)

            return jsonify({
                "data":data
            })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@santha.route('/profile/<int:id>')
def profileDetails(id):
    try:
        details=SanthaPayments.query.filter(SanthaPayments.member_id==id)
        data=[]
        for detail in details:
            payment_id=detail.id
            santha_year=detail.santha_for_year
            received_amount=detail.received_amount
            received_date=detail.received_date

            info={
                "payment_id":payment_id,
                "santha_year":santha_year,
                "received_amount":received_amount,
                "received_date":str(received_date)
            }
            data.append(info)
        return jsonify({
            "data":data
        })
    except Exception as e:
        return jsonify({"error":str(e)})