from main.utils import monthDates,datetime
from flask import Blueprint,jsonify,request
from main.Services.Loan.Business.models import BusinessLoanPayment
from main.Services.Loan.Savings.models import SavingsLoansPayment
from main.Services.Loan.Educational.models import EducationalLoanPayment
from main.extensions import db
from main.utils import token_required,permission_required,loger
warning="warning"
info="info"
error="error"

collection=Blueprint("collection",__name__,url_prefix="/collection")

@collection.route('/savings-loan-monthly')
def SavingsMonthlyCollection():
    try:
        page=request.args['page']
        per_page=request.args['per_page']
        data=[]
        month=datetime.now().month
        sL_col=SavingsLoansPayment.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
        for detail in sL_col:
            if detail.status!=1:
                continue
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
        if not data:
             loger("warning").warning("no data returned")
             return jsonify({"status":False,"data":data,"msg":"","error":""}),200
        loger("info").info("santha details viewed.")
        return jsonify({"status":True,"data":data,"msg":"","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
    
@collection.route('/business-loan-monthly')
def BusinessMonthlyCollection():
    try:
        page=request.args['page']
        per_page=request.args['per_page']
        data=[]
        month=datetime.now().month
        BL_col=BusinessLoanPayment.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
        for detail in BL_col:
            if detail.status!=1:
                continue
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
        if not data:
             loger("warning").warning("no data returned")
             return jsonify({"status":False,"data":data,"msg":"","error":""}),200
        loger("info").info("santha details viewed.")
        return jsonify({"status":True,"data":data,"msg":"","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500
    
@collection.route('/educational-loan-monthly')
def EducationMonthlyCollection():
    try:
        page=request.args['page']
        per_page=request.args['per_page']
        data=[]
        month=datetime.now().month
        EL_col=EducationalLoanPayment.query.paginate(page=int(page),per_page=int(per_page),error_out=False)
        for detail in EL_col:
            if detail.status!=1:
                continue
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
        if not data:
             loger("warning").warning("no data returned")
             return jsonify({"status":False,"data":data,"msg":"","error":""}),200
        loger("info").info("santha details viewed.")
        return jsonify({"status":True,"data":data,"msg":"","error":""}),200
    except Exception as e:
        loger("error").error(str(e))
        return jsonify({"status":False,"msg":"","error":str(e)}),500