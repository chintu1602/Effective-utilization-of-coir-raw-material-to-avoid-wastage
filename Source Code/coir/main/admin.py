from django.contrib import admin

# Register your models here.
from .models import industryRequirement, farmerRequest, feedbacks, transactions

admin.site.register(industryRequirement)
admin.site.register(farmerRequest)
admin.site.register(feedbacks)
admin.site.register(transactions)