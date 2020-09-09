import random
from numbers import Number
from django.shortcuts import HttpResponse, render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
 # Create your views here.
from .models import Inquiry, Account,Transaction
from .models import Loan
from .models import BasicDetails
from django.contrib import messages
import decimal

#  function for the render first poge of site

def home(request):
     return render(request, 'login/login.html')

# functions for generating acount number

def randomGen():
     # return a 6 digit random number
     return int(random.uniform(100000, 999999))

# function to render sign page form

def sign(request):
     return  render(request,'login/sign.html')

# funstion for render to login poage
def rlogin(request):
     return render(request,'login/rlogin.html')

# functions for handle sign

def handleSignup(request):
     if request.method=='POST':
         username=request.POST['username']
         address=request.POST['address']
         fname=request.POST['fname']
         lname=request.POST['lname']
         sex=request.POST['sex']
         annual=request.POST['annual']
         email=request.POST['email']
         mobile=request.POST['mobile']
         occupation=request.POST['occupation']
         dob=request.POST['dob']
         pass1=request.POST['pass1']
         pass2=request.POST['pass2']
         # check for errors
         if  User.objects.filter(username__iexact=username).exists():
             messages.error(request, 'username already exist')
             return redirect('/sign')
         if len(pass1)<5:
             messages.error(request, 'password should be atleast 5 characters')
             return redirect('/sign')
         if len(pass1)>8:
             messages.error(request, 'password should be not  8 characters')
             return redirect('/sign')
         if len(username)<6:
             messages.error(request, 'username must be greater then 6 characters ')
             return redirect('/sign')
         if not username.isalnum() :
             messages.error(request, 'username should only contain  characters  and numbers')
             return redirect('/sign')
         if pass1!=pass2:
             messages.error(request, 'passwords do not match')
             return redirect('/sign')


         # creating new user   user

         curr_user = User.objects.create_user(username, email, pass1)
         curr_user.first_name = fname
         curr_user.last_name = lname

         # filling the basic details
         fill_basic_details = BasicDetails()
         fill_basic_details.sex = sex
         fill_basic_details.address = address
         fill_basic_details.annual_income = annual
         fill_basic_details.mobile = mobile
         fill_basic_details.occupation = occupation
         fill_basic_details.dob = dob
         fill_basic_details.user = curr_user


         # Updating the stats table
         account_details = Account()
         account_details.account_number = randomGen()  # random account number for every new user
         account_details.balance = 0
         # account_details.account_type=account_type
         account_details.user = curr_user

         # saving all
         fill_basic_details.save()
         curr_user.save()
         account_details.save()


         messages.success(request,'your account has been successfully created')
         return redirect('/')
     else:
         return HttpResponse('404-not fond')

# funstion for hadle login of the user

def handleLogin(request):
      username=request.POST['loginusername']
      pwd=request.POST['loginpass']
      user=authenticate(username=username,password=pwd)
      if user is not None:
             login(request,user)
             messages.success(request, 'Login successfully  Enjoy our services ')
             return redirect('/')
      else:
            messages.error(request, 'invalid credentilas ')
            return redirect('/')

# functions for the hadle logout of user

def handleLogout(request):
     logout(request)
     messages.success(request,'logout successfully')
     return redirect('/')

# function for the checking balance of the current user

def checkbalance(request):
         try:
           curr_user=Account.objects.get(user=request.user)
           curr_balance=curr_user.balance
           params = {"balance": curr_balance,"msg":"Your balance is : "}
           return render(request, 'login/service.html', params)
         except Account.DoesNotExist:
           c="Acount number does not exitst please Enter correct acount number"
           params = {"correct": c}
           return render(request, 'login/checkbalance.html', params)

# functions for the render to the transfer page

def transfer(request):
    try:
        curr_user = Account.objects.get(user=request.user)
        curr_balance = curr_user.balance
        params = {"balance": curr_balance}
        return render(request, 'login/transfer.html', params)
    except Account.DoesNotExist:
        msg = "User does not exist "
        params = {"correct": msg}
        return  render(request,'login/transfer.html',params)

# function for the hadle transfer  amount

def transfer1(request):
     if request.method == 'POST':
         raccno = request.POST['raccno']
         amount = request.POST['amount']
         curr_user = Account.objects.get(user=request.user)
         curr_balance = curr_user.balance
         sender_account = Account.objects.get(user=request.user)
     try:
         reciver_account = Account.objects.get(account_number=raccno)
     except Account.DoesNotExist:
         msg = "Invalid account number"
         params = {"correct": msg,"balance": curr_balance}
         return render(request, 'login/transfer.html', params)
     sender_balance = sender_account.balance
     sender_balance = decimal.Decimal(sender_balance)
     trasaction_amount = decimal.Decimal(amount)
     if trasaction_amount > sender_balance:
         msg = "Insufficient balance "
         params = {"correct": msg,"balance": curr_balance}
         return render(request, 'login/transfer.html', params)
     if trasaction_amount > decimal.Decimal(20000):
         msg = "You can not transfer more then 20000 Rs."
         params = {"correct": msg,"balance": curr_balance}
         return render(request, 'login/transfer.html', params)
     if int(raccno)==curr_user.account_number:
         msg = "Same account number You Can not send it to itself "
         params = {"correct": msg, "balance": curr_balance}
         return render(request, 'login/transfer.html', params)
     updated_balance =  sender_balance-trasaction_amount
     sender_account.balance = updated_balance
     sender_account.save()
     curr_transactions=Transaction()
     curr_transactions.sender=sender_account
     curr_transactions.receiver= reciver_account
     curr_transactions.amount=trasaction_amount
     curr_transactions.save()
     reciever_updated_balance=decimal.Decimal(reciver_account.balance)+trasaction_amount
     reciver_account.balance=reciever_updated_balance
     reciver_account.save()

     curr_user = Account.objects.get(user=request.user)
     curr_balance = curr_user.balance

     msg = "Amount transefered Successfully!!!"
     params = {"correct": msg,"balance": curr_balance}
     return render(request, 'login/transfer.html', params)

# rendering to team page

def team1(request):
     return render(request,'login/team.html')

def contact(request):
     return render(request,'login/contact.html')

# savinng the contact details of the user

def contacts(request):
     if request.method == 'POST':
         name = request.POST['name']
         phon = request.POST['phon']
         email = request.POST['email']
         code=request.POST['code']
         curr_user=Inquiry(name=name,phone=phon,email=email,pin_code=code)
         curr_user.save()
         msg = "Sended"
         params = {"correct": msg}
     return render(request, 'login/contact.html', params)

# rendering to the services page after login
def about(request):
    return   render(request,'login/about.html')
def service(request):
     return render(request,'login/service.html')

# rendering to the loan form

def loan(request):
       return render(request, 'login/loan.html')
# saving applied loan details

def apply_loan(request):
     if request.method == 'POST':
         user_from_acount=Account.objects.get(user=request.user)
         loanamount = request.POST['loanamount']
         loantype = request.POST['loantype']
         print(type(loantype))
         periodmonths = request.POST['periodmonths']
         adhar1=request.POST['adhar']
         pan=request.POST['pan']
         photo=request.POST['photo']
         periodmonths_in_int=int(periodmonths)
         if periodmonths_in_int >60:
             msg= "loan period should be less then 60"
             params = {"msg": msg}
             return render(request, 'login/loan.html', params)
         for user_from_loan in Loan.objects.filter(acount=user_from_acount):
            checking_for_loantype=user_from_loan.loan_type
            if  checking_for_loantype==loantype:
                params = {'msg': "Your already applied this loan type try another"}
                return render(request,'login/loan.html',params)
         curr_user=Loan()
         curr_user.loan_amount=loanamount
         curr_user.loan_type=loantype
         curr_user.loan_period_in_months=periodmonths
         curr_user.acount=user_from_acount
         curr_user.adhar_card=adhar1
         curr_user.pan_card=pan
         curr_user.photo=photo
         if str(loantype)=="Home Loan":
             curr_user.intrest_rate=8.0
         if str(loantype)=="Car Loan":
             curr_user.intrest_rate=12.0
         if str(loantype)=="Bussiness Loan":
             curr_user.intrest_rate=10.0
         if str(loantype)=="Personal Loan":
             curr_user.intrest_rate=15.0
         curr_user.save()
         params={'msg':"Laon Applied Successfully"}
         return render(request, 'login/loan.html',params)

def loan_status(request):
    user_from_acount = Account.objects.get(user=request.user)
    to_send = []
    for user_loan in Loan.objects.filter(acount=user_from_acount):
         loan_amount=user_loan.loan_amount
         loan_type=user_loan.loan_type
         acount=user_loan.acount
         loan_status=user_loan.loan_status
         loan_period_in_months=user_loan.loan_period_in_months
         intrest_rate=user_loan.intrest_rate
         loan_id=user_loan.id
         params={'loan_id':loan_id,'loan_amount':loan_amount,'loan_type':loan_type,'acount':acount,'loan_status':
         loan_status,'loan_period_in_months':loan_period_in_months,'intrest_rate':intrest_rate}
         to_send.append(params)
    if not to_send:
      msg="You are not  apllied any loan"
      params={"msg":msg}
      return render(request, 'login/loanstatus.html',params)
    context={'to_send':to_send}
    return  render(request,'login/loanstatus.html',context)
def term_conditions(request):
    return render(request,'login/term_conditions.html')

# function for the checking loan status

def statement(request):
    return  render(request,'login/statement.html')

def statement1(request):
     user_from_acount = Account.objects.get(user=request.user)
     user=Transaction.objects.filter(sender=user_from_acount).order_by('-timeStamp')
     params = {'data1': user, 'msg': "Full sending  Details of user:", 'msg1': "Reciever"
         , 'msg2': "amonut", 'msg3': "Date and Time"}
     return render(request, 'login/showstatement.html', params)


def statement2(request):
    user_from_acount = Account.objects.get(user=request.user)
    user = Transaction.objects.filter(receiver=user_from_acount).order_by('-timeStamp')
    params = {'data1': user, 'msg': "Full  recieving   Details of user:", 'msg1': "Recieved by"
        , 'msg2': "amonut", 'msg3': "Date and Time"}
    return render(request, 'login/showstatement1.html', params)


def  statement3(request):
    user_from_acount = Account.objects.get(user=request.user)
    user= Transaction.objects.filter(receiver=user_from_acount).order_by('-timeStamp')[:5]
    params = {'data1': user,'msg': "Full sending  Details of user:", 'msg4': "Sender", 'msg1': "Reciever"
         , 'msg2': "amonut", 'msg3': "Date and Time"}
    return render(request, 'login/showstatement3.html', params)

def  statement4(request):
    user_from_acount = Account.objects.get(user=request.user)
    user= Transaction.objects.filter(sender=user_from_acount).order_by('-timeStamp')[:5]
    params = {'data1': user,'msg': "five  recieving  Details of user:",  'msg1': "Recieved by"
         , 'msg2': "amonut", 'msg3': "Date and Time"}
    return render(request, 'login/showstatement4.html', params)
