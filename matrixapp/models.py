from distutils.command.upload import upload
from pyexpat import model
from tkinter import CASCADE
# from turtle import update
from django.db import models
from django.contrib.auth.models import AbstractUser

# import uuid
from .utils import generate_ref_code

# Create your models here.

class CustomUser(AbstractUser):
    USER = (
        ('1', 'HOD'),
        ('2', 'Agent'),
        ('3', 'Customer'),

    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to = 'media/profile_pic')
    user_id = models.CharField(max_length=12,blank=True)
    # user_id=models.CharField(max_length=50, default=code)
    rank = models.IntegerField(blank=True,null=True)
    

    def save(self, *args, **kwargs):
        if self.user_id == "":
            user_id = ("SSR"+generate_ref_code())
            self.user_id = user_id
        super().save(*args, **kwargs)

    
class HOD(models.Model):
    
 
    # id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return str(self.admin)


    

class SuperAgent(models.Model):
    # code = str(uuid.uuid4()).replace("-", "")[:6]
    # user_id=models.CharField(max_length=50, default=code)
    
    # percentage = models.IntegerField()
    # owner = models.ForeignKey(to=CustomUser,on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=50)
    mobile_no = models.BigIntegerField(null=True,blank=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)   
    objects=models.Manager()

     
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name



class phase(models.Model):
    phase = models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True, auto_now=False,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now_add=False, auto_now=True,null=True,blank=True)
    objects=models.Manager()

    def __str__(self):
        return self.phase
   

class AddPlot(models.Model):
    
    plot_no = models.CharField(max_length=10)
    plot_size = models.IntegerField(null=True,blank=True)
    # plc_rate = models.IntegerField(null=True,blank=True)
    # plc = models.IntegerField(null=True,blank=True)
    plot_rate = models.IntegerField(null=True,blank=True)
    phase = models.ForeignKey(phase,on_delete=models.CASCADE,null=True,blank=True)
    # discount = models.IntegerField(null=True,blank=True)
    objects=models.Manager()


    def __str__(self):
        return str(self.plot_no)

class Fundtransfer(models.Model):
    user_id = models.CharField(max_length=300)
    # user_id=models.CharField(primary_key=True,max_length=50, default=user_code, editable=False)
    amount = models.CharField(max_length=50)
    objects=models.Manager()


    def _str_(self):
        return self.user_id + " " + self.amount
    

class BookPlot(models.Model):
    owner = models.ForeignKey(to=CustomUser,on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=25)
    # user_code = str(uuid.uuid4()).replace("-", "")[:4]
    user_id = models.CharField(max_length=300)
    phase = models.CharField(max_length=100,null=True,blank=True)
    # user_id=models.CharField(primary_key=True,max_length=50, default=user_code, editable=False)
    plot_number = models.CharField(max_length=25)
    Payable_amout = models.IntegerField(null=True, blank=True)
    payment_amount = models.IntegerField(null=True, blank=True)
    remaining_amount = models.IntegerField(null=True, blank=True,default=0)    
    # Mnthly_Installment = models.IntegerField(null=True, blank=True)
    # number_of_Installment = models.IntegerField(null=True,blank=True)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100,null=True,blank=True)
    mobile_no = models.BigIntegerField(null=True,blank=True)
    payment_mode = models.CharField(max_length=10,null=True,blank=True)
    remarks = models.TextField()
    receipt = models.ImageField(upload_to = 'receipt/', null= True, blank=True)
    joinig_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    plot_size =models.CharField(max_length=100,null=True,blank=True)
    addresss = models.CharField(max_length=5000,null=True,blank=True)
    mail = models.CharField(max_length=50,null=True,blank=True)
    account_no = models.CharField(max_length=50,null=True,blank=True,default=0)
    ifsc_code = models.CharField(max_length=100,null=True,blank=True)
    check_no = models.CharField(max_length=100,null=True,blank=True)
    status = models.IntegerField(default=0)
    objects=models.Manager()
    
    

    # def save(self, *args, **kwargs):
    #     if self.user_code == "":
    #         code = generate_ref_code()
    #         self.code = code
    #     super().save(*args, **kwargs)
    # def __str__(self):
    #     return self.ref_id+" "+ str(self.Payable_amout)
    def __str__(self):
        return self.ref_id+" "+ str(self.payment_amount)+" " +str(self.Payable_amout)
    

 
 

class Customer(models.Model):
    # owner = models.ForeignKey(to=CustomUser,on_delete=models.CASCADE)
    
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,unique=False)
    customer_id = models.CharField(max_length=10,null=True,blank=True)
    cust_father_name = models.CharField(max_length=50,null=True,blank=True)
    cust_mobileno = models.BigIntegerField(null=True,blank=True)
    addresss = models.CharField(max_length=5000,null=True,blank=True)
    password = models.CharField(max_length=50,null=True,blank=True)
    objects=models.Manager()

    
    def __str__(self):
        return str(self.customer_name)
    




class Kyc(models.Model):
    cust_id = models.CharField(max_length=300)
    # user_id=models.CharField(primary_key=True,max_length=50, default=user_code, editable=False)
    accountname = models.CharField(max_length=25)
    accountno = models.IntegerField(null=True, blank=True)
    IFSCno = models.CharField(null=True, blank=True,max_length=25)
    Pancardno = models.CharField(null=True,blank=True,max_length=25)


class FundDetails(models.Model):
    owner = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    ref_id = models.CharField(max_length=50,null=True,blank=True)
    plot_number = models.CharField(max_length=25,null=True,blank=True)
    Total_amount = models.CharField(max_length=25,null=True,blank=True)
    user_name = models.CharField(max_length=50,null=True,blank=True)
    amount = models.CharField(max_length=50,null=True,blank=True)
    joinig_date=models.DateTimeField(auto_now_add=False,null=True,blank=True)
    payment_amount = models.BigIntegerField(null=True, blank=True)
    Payable_amout = models.IntegerField(null=True, blank=True)

    def __str__(self):
       return self.user_id+" "+ str(self.payment_amount)+" " +str(self.Payable_amout)+" " +str(self.plot_number)+" " +str(self.joinig_date)





class Installment(models.Model):
    owner = models.ForeignKey(to=CustomUser,on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=25)
    # user_code = str(uuid.uuid4()).replace("-", "")[:4]
    user_id = models.CharField(max_length=300)
    # user_id=models.CharField(primary_key=True,max_length=50, default=user_code, editable=False)
    plot_number = models.CharField(max_length=25)
    Payable_amout = models.IntegerField(null=True, blank=True)
    remaining_amount = models.IntegerField(null=True, blank=True)
    payment_amount = models.BigIntegerField(null=True, blank=True)
    
    # Mnthly_Installment = models.IntegerField(null=True, blank=True)
    # number_of_Installment = models.IntegerField(null=True,blank=True)
    name = models.CharField(max_length=100)
    # father_name = models.CharField(max_length=100,null=True,blank=True)
    mobile_no = models.BigIntegerField(null=True,blank=True)
    payment_mode = models.CharField(max_length=10,null=True,blank=True)
    remarks = models.TextField()
    receipt = models.ImageField(upload_to = 'receipt/', null= True, blank=True)
    joinig_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    plot_size = models.CharField(max_length=100,null=True,blank=True)
    addresss = models.CharField(max_length=5000,null=True,blank=True)
    mail = models.CharField(max_length=50,null=True,blank=True)
    status = models.IntegerField(default=0)
    # def save(self, *args, **kwargs):
    #     if self.user_code == "":
    #         code = generate_ref_code()
    #         self.code = code
    #     super().save(*args, **kwargs)
    def __str__(self):
        return self.ref_id+" "+ str(self.payment_amount)+" " +str(self.Payable_amout)+" " +str(self.plot_number)+" " +str(self.joinig_date)

    