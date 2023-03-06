from flask import Blueprint,jsonify,request
from main.extensions import db
from datetime import datetime
from main.Teams.Members.models import MemberProfile
from main.Funds.Savings.models import Savings

savings=Blueprint('savings',__name__,url_prefix="/savings")

@savings.route('/pay-savings',methods=['POST'])
def savingsPayment():
    try:
        data=request.get_json()
        member_id=data.get('member_id')
        transaction_amount=data.get('transaction_amount')
        transaction_date=data.get('transaction_date')
        trans_date_list=str(transaction_date).split('-')
        date_now=datetime(int(trans_date_list[0]),int(trans_date_list[1]),int(trans_date_list[2]))
        year=date_now.strftime("%Y")
        month=date_now.strftime("%m")
        week=date_now.strftime("%V")
        transaction_type=0
        final_balance=transaction_amount
        fbalances=Savings.query.filter(Savings.member_id==member_id)
        final=0
        for fbalance in fbalances:
            final=fbalance.final_balance
        
        final_balance+=final

        member=[MemberProfile.to_json(i) for i in MemberProfile.query.filter(MemberProfile.id==member_id)]

        if len(member)<1:
            return jsonify({
                "message":"Member is not exist"
            })
        else:
            entry=Savings(member_id=member_id,
                          transaction_amount=transaction_amount,
                          transaction_date=transaction_date,
                          year=year,
                          month=month,
                          week=week,
                          transaction_type=transaction_type,
                          final_balance=final_balance)
            db.session.add(entry)
            db.session.commit()

            return jsonify({
                "message":"payment detail added successfully."
            })
    
    except Exception as e:
        return jsonify({
            "message":str(e)
        })
    
@savings.route('/withdraw',methods=['POST'])
def withdraw():
    try:
        data=request.get_json()
        member_id=data.get('member_id')
        transaction_amount=data.get('transaction_amount')
        transaction_date=data.get('transaction_date')
        trans_date_list=str(transaction_date).split('-')
        date_now=datetime(int(trans_date_list[0]),int(trans_date_list[1]),int(trans_date_list[2]))
        year=date_now.strftime("%Y")
        month=date_now.strftime("%m")
        week=date_now.strftime("%V")
        transaction_type=1
        
        member=[MemberProfile.to_json(i) for i in MemberProfile.query.filter(MemberProfile.id==member_id)]

        if len(member)<1:
            return jsonify({
                "message":"Member is not exist"
            })
        else:        
            fbalances=Savings.query.filter(Savings.member_id==member_id)
            final_balance=0
            for fbalance in fbalances:
                final=fbalance.final_balance
            if final>transaction_amount:
                final_balance=final-transaction_amount
                
                entry=Savings(member_id=member_id,
                          transaction_amount=transaction_amount,
                          transaction_date=transaction_date,
                          year=year,
                          month=month,
                          week=week,
                          transaction_type=transaction_type,
                          final_balance=final_balance)
                db.session.add(entry)
                db.session.commit()
    
                return jsonify({
                    "message":"withdraw detail added successfully."
                })
            
            else:
                return jsonify({
                    "message":"Insufficient fund!"
                })
    
    except Exception as e:
        return jsonify({
            "message":str(e)
        })

@savings.route('/savings-details')
def santhaDetails():
    try:
        page=request.args['page']
        per_page=request.args['per_page']
        search=request.args['search']
        if search:
            mem_details=MemberProfile.query.filter((MemberProfile.id.contains(search) | 
                                                (MemberProfile.name.contains(search))))
            data=[]
            for member in mem_details:
                mem_id=member.id
                name=member.name
                
                paymentDetails=Savings.query.filter((Savings.member_id==mem_id)&(Savings.transaction_type==0))
                withdrawDetails=Savings.query.filter((Savings.member_id==mem_id)&(Savings.transaction_type==1))

                savingExist=False
                total_savings=0
                total_withdraw=0

                for withdraw in withdrawDetails:
                    total_withdraw+=withdraw.transaction_amount

                print(mem_id)
                for detail in paymentDetails:
                   savingExist=True
                   previous_payment=detail.transaction_amount 
                   received_on=detail.transaction_date
                
                   date_list=str(received_on).split('-')
                   date_obj=datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
                   month=date_obj.strftime('%b')
                   tweek=date_obj.strftime('%V')
                   week=tweek+"th"
                   
                   total_savings+=detail.transaction_amount
                
                current_savings=total_savings-total_withdraw
                interest=2
                nweek=datetime.now().strftime("%V")
                dues=int(nweek)-int(tweek)

                if savingExist:
                    info={"id":mem_id,
                         "name":name,
                         "previous_payment":previous_payment,
                         "month":month,
                         "week":week,
                         "received_on":received_on,
                         "total_savings":total_savings,
                         "dues":dues,
                         "interest":interest,
                         "total_withdraw":total_withdraw,
                         "current_savings":current_savings}
                    data.append(info)
            return jsonify({
                    "data":data
                })
        else:
            mem_details=MemberProfile.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
            data=[]
            
            for member in mem_details:
                mem_id=member.id
                name=member.name
                
                paymentDetails=Savings.query.filter((Savings.member_id==mem_id)&(Savings.transaction_type==0))
                withdrawDetails=Savings.query.filter((Savings.member_id==mem_id)&(Savings.transaction_type==1))

                savingExist=False
                total_savings=0
                total_withdraw=0

                for withdraw in withdrawDetails:
                    total_withdraw+=withdraw.transaction_amount


                for detail in paymentDetails:
                   savingExist=True
                   previous_payment=detail.transaction_amount 
                   received_on=detail.transaction_date
                
                   date_list=str(received_on).split('-')
                   date_obj=datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
                   month=date_obj.strftime('%b')
                   tweek=date_obj.strftime('%V')
                   week=tweek+"th"
                   
                   total_savings+=detail.transaction_amount
                
                current_savings=total_savings-total_withdraw
                interest=2
                nweek=datetime.now().strftime("%V")
                dues=int(nweek)-int(tweek)

                if savingExist:
                    info={"id":mem_id,
                         "name":name,
                         "previous_payment":previous_payment,
                         "month":month,
                         "week":week,
                         "received_on":received_on,
                         "total_savings":total_savings,
                         "dues":dues,
                         "interest":interest,
                         "total_withdraw":total_withdraw,
                         "current_savings":current_savings}
                    data.append(info)
            return jsonify({
                    "data":data
                })

    except Exception as e:
        return jsonify({
            "error":str(e)
        })

@savings.route('saving/<int:id>')
def savingPayments(id):
    try:
        payments=Savings.query.filter((Savings.member_id==id) & (Savings.transaction_type==0))
        member=MemberProfile.query.filter(MemberProfile.id==id)
        memberExist=False
        paymentExist=False
        for mem in member:
            memberExist=True
            name=mem.name
        data=[]
        for payment in payments:
            paymentExist=True
            pid=payment.id
            amount=payment.transaction_amount
            month=payment.month
            x=datetime(2020,month,1)
            pmonth=x.strftime("%B")
            week=str(payment.week)+"th"
            received_on=str(payment.transaction_date)

            info={
                "id":pid,
                "amount":amount,
                "month":pmonth,
                "week":week,
                "received_on":received_on
            }
            data.append(info)
        if memberExist:
            if paymentExist:
                return jsonify({
                    "name":name,
                    "id":id,
                    "data":data
                })
            else:
                return jsonify({
                    "message":"No payments exist!"
                })
        else:
            return jsonify({
                    "message":"Member Not Exist!"
                })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    
@savings.route('withdraw/<int:id>')
def savingWithdraws(id):
    try:
        withdraws=Savings.query.filter((Savings.member_id==id) & (Savings.transaction_type==1))
        member=MemberProfile.query.filter(MemberProfile.id==id)
        memberExist=False
        withdrawExist=False
        for mem in member:
            name=mem.name
            memberExist=True
        data=[]
        for withdraw in withdraws:
            withdrawExist=True
            pid=withdraw.id
            amount=withdraw.transaction_amount
            received_on=str(withdraw.transaction_date)

            info={
                "id":pid,
                "amount":amount,
                "received_on":received_on
            }
            data.append(info)
        if memberExist:
            if withdrawExist:
                return jsonify({
                    "name":name,
                    "id":id,
                    "data":data
                })
            else:
                return jsonify({
                    "message":"No withdraws exist!"
                })
        else:
            return jsonify({
                    "message":"Member Not Exist!"
                })
    except Exception as e:
        return jsonify({
            "error":str(e)
        })