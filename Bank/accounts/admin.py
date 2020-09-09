from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Account
from .models import Inquiry
from .models import Loan
from .models import Transaction
from .models import BasicDetails
# # Register your models here

admin.site.register(Account)
admin .site.register(BasicDetails)
admin.site.register(Inquiry)
admin.site.register(Loan)
admin.site.register(Transaction)
