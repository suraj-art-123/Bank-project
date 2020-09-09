from django.db import models
from django.contrib.auth.models import User

# Table for basic details of user

class BasicDetails (models.Model):
    # (Name, Sex, DOB, Annual income, Email, Mobile number, Occupation)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    sex = models.CharField(max_length = 1, default = None)
    annual_income = models.IntegerField(default = 0)
    mobile = models.CharField(max_length = 11,default = 0,unique=True)
    occupation = models.CharField(max_length = 50, default = None)
    address=models.CharField(max_length=1000)
    dob = models.DateField(default = None)

    def __str__(self):
        return  self.user.username

# Table for account details of user

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.IntegerField(unique=True)
    balance = models.DecimalField(max_digits=12,decimal_places=2)
    created_at=models.DateField(auto_now_add=True)
    account_type=models.CharField(max_length=30,default="SAVINGS")
    #user_name = models.CharField(max_length = 150, default = None)
    class ReadonlyMeta:
         readonly=["balance"]
         readonly=["account_number"]
         readonly=["account_type"]
    def __str__(self):
          return  self.user.username

# Table for contact to Bank

class Inquiry(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    pin_code = models.CharField(max_length=30)

    def __str__(self):
        return "Message from " + self.name

# Table for the Loan Status and form

class Loan(models.Model):
    loan_amount=models.DecimalField(max_digits=12,decimal_places=2)
    loan_type=models.CharField(max_length=40)
    acount=models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    loan_status = models.CharField(max_length=15, default="pending",choices=[('approved', 'approved'), ('pass by bank', 'pass by bank')])
    loan_period_in_months = models.IntegerField()
    intrest_rate = models.DecimalField(max_digits=4,decimal_places=2,default=5.5)
    adhar_card = models.ImageField(upload_to="media/", default="")
    pan_card = models.ImageField(upload_to="media/" ,default="")
    photo= models.ImageField(upload_to="media/" ,default="")

    class ReadonlyMeta:
        readonly = ["loan_amount"]

class Transaction(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="sender_transactions",null=True,blank=True)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="receiver_transactions",null=True,blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

