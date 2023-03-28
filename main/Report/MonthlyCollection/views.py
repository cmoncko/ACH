from main.utils import monthDates,datetime
from flask import Blueprint,jsonify,request
from main.Services.Loan.Business.models import BusinessLoanPayment
from main.Services.Loan.Savings.models import SavingsLoansPayment
from main.Services.Loan.Educational.models import EducationalLoanPayment
from main.extensions import db

collection=Blueprint("collection",__name__,url_prefix="/collection")

@collection.route('/savings-loan-monthly')
def SavingsMonthlyCollection():
    try:
        data=[]
        month=datetime.now().month
        sL_col=SavingsLoansPayment.query.filter_by(status=1).all()
        for detail in sL_col:
            paid_month=detail.paid_date.month
            if paid_month==month:
                id=detail.id
                EMI_amount=detail.amount
                penalty_amount=detail.penalty_amount
                total_amount=detail.total_amount
                paid_date=detail.paid_date
                status=detail.status
                info={"id":id,
                    "EMI_amount":EMI_amount,
                    "penalty_amount":penalty_amount,
                    "total_amount":total_amount,
                    "paid_date":paid_date,
                    "status":status}
                data.append(info)
        if len(data)<1:
            return jsonify({"status": False, "data": "", "msg": "No payments There", "error": ""}), 200
        return jsonify({"status": True, "data":data, "msg": "", "error": ""}), 201
    except Exception as e:
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500
    
@collection.route('/business-loan-monthly')
def BusinessMonthlyCollection():
    try:
        data=[]
        month=datetime.now().month
        BL_col=BusinessLoanPayment.query.filter_by(status=1).all()
        for detail in BL_col:
            paid_month=detail.paid_date.month
            if paid_month==month:
                id=detail.id
                EMI_amount=detail.amount
                penalty_amount=detail.penalty_amount
                total_amount=detail.total_amount
                paid_date=detail.paid_date
                status=detail.status
                info={"id":id,
                    "EMI_amount":EMI_amount,
                    "penalty_amount":penalty_amount,
                    "total_amount":total_amount,
                    "paid_date":paid_date,
                    "status":status}
                data.append(info)
        if len(data)<1:
            return jsonify({"status": False, "data": "", "msg": "No payments There", "error": ""}), 200
        return jsonify({"status": True, "data":data, "msg": "successfully logged-in", "error": ""}), 201
    except Exception as e:
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500
    
@collection.route('/educational-loan-monthly')
def EducationMonthlyCollection():
    try:
        data=[]
        month=datetime.now().month
        EL_col=EducationalLoanPayment.query.filter_by(status=1).all()
        for detail in EL_col:
            paid_month=detail.paid_date.month
            if paid_month==month:
                id=detail.id
                EMI_amount=detail.amount
                penalty_amount=detail.penalty_amount
                total_amount=detail.total_amount
                paid_date=detail.paid_date
                status=detail.status
                info={"id":id,
                    "EMI_amount":EMI_amount,
                    "penalty_amount":penalty_amount,
                    "total_amount":total_amount,
                    "paid_date":paid_date,
                    "status":status}
                data.append(info)
        if len(data)<1:
            return jsonify({"status": False, "data": "", "msg": "No payments There", "error": ""}), 200
        return jsonify({"status": True, "data":data, "msg": "successfully logged-in", "error": ""}), 201
    except Exception as e:
        return jsonify({"status": False, "data": "", "msg": "", "error": str(e)}), 500