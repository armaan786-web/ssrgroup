import dis
import json
# import requests
from multiprocessing import context

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from matrixapp.models import SuperAgent, AddPlot,HOD,BookPlot, CustomUser, Customer,Kyc,Fundtransfer,FundDetails,Installment,phase
from django.contrib import messages
# from django.http import HttpResponse, HttpResponseRedirect
import csv
import datetime
from django.contrib.auth.models import User


import MySQLdb

# import requests

# import sqlite3 as sql
# from tkinter import *
# from tkinter import ttk
# from tabulate import tabulate


     
 


@login_required(login_url='/')
def HOME(request):
    agent_count1=SuperAgent.objects.all().count()
    customer_count1 = Customer.objects.all().count()
    plot_count1 = AddPlot.objects.all().count
    book_plot_count1 = BookPlot.objects.all().count
    return render(request, 'HOD/home.html',{"agent_count":agent_count1,"customer_count1":customer_count1,'plot_count1':plot_count1,"book_plot_count1":book_plot_count1})

def  cancelledplote(request):
    return render(request, 'HOD/cancelledplote.html')

def  bookingdetails(request):
    return render(request, 'HOD/bookingdetail.html')

def  agrrement(request):
    return render(request, 'HOD/agreement.html')


def ADD_USER(request):
    current_user = request.user
    if request.method == "POST":
        cust_id = request.POST.get('cust_id')
        user_name = request.POST.get('name')
        # customer_name = username
        father_name = request.POST.get('father_name')
        mob_no = request.POST.get('mob_no')
        addresss = request.POST.get('addresss')
        mail = request.POST.get('mail')
        password=request.POST.get("password") 
        # if CustomUser.objects.filter(email = mail).exists():
        #     messages.warning(request, "Email is already Taken")
        #     return redirect('add_user')
        
        if CustomUser.objects.filter(username = user_name).exists():
            messages.warning(request, "Username is already Taken")
            return redirect('add_user')

        if Customer.objects.filter(customer_id = cust_id).exists():
                messages.warning(request, "Customer Id is already Taken")
                return redirect('add_user')
        
        

        else:
            user = CustomUser(
                username = user_name,
                email = mail,
                user_type = 3,
            )
            user.set_password(password)
            user.save()

            customer =  Customer(owner=user,customer_id=cust_id,cust_father_name=father_name,cust_mobileno=mob_no,addresss=addresss,password=password)
        # customer =  Customer(customer_id=cust_id)
            
            owner=customer.owner=request.user
            customer.owner = owner
            customer.save()
            messages.success(request, "Customer ID Added Successfully !!")

        # print(cust_id)

    return render(request,'HOD/add_user.html')

def CUSTOMER_VIEW(request):
    customer = Customer.objects.all()
    context = {
        'customer' : customer
    }

    return render(request,'HOD/view_customer.html',context)


def customer_export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    # response['Content-Disposition'] = 'attachment; filename="Approve Po.csv"'
    response['Content-Disposition'] = 'attachment; filename= customerDetails'+ str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Customer ID', 'Customer Name', "Father's Name", 'Mobile No'])
    customer = Customer.objects.all()
    for approve in customer:
        print(approve)
    
        writer.writerow(
                    [approve.customer_id, 
				approve.customer_name, 
				approve.cust_father_name, 
				approve.cust_mobileno])
           

    return response



def EDIT_CUSTOMER(request,id):
    # SuperAgent.objects.get(admin=staff_id)
    customer = Customer.objects.get(owner=id)
    
    
    
    context = {
        'customer': customer,
        'id':id
    }
    return render(request, 'HOD/customer_edit.html', context)



def  addplot(request):
    phse = phase.objects.all()
    context = {
        'phse':phse
    }
    if request.method == "POST":
        plot_no = request.POST.get("plot_no")
        plot_size = request.POST.get("plot_size")
        # plc_rate = request.POST.get("plc_rate")
        # plc = request.POST.get("plc")
        plot_rate = request.POST.get("plot_rate")
        phase_id = request.POST.get("phase_id")    
        # discount = request.POST.get("discount")
        # print("plotttttt", plot_no, "plot size:", plot_size)
        # add_plot = AddPlot(plot_no= plot_no)
        # add_plot = {'plot_no':plot_no,'plot_size':plot_size, 'plc_rate':plc_rate,'plc':plc, 'plot_rate':plot_rate, 'discount': discount}
        phse_name = phase.objects.get(id = phase_id)
        add_plot = AddPlot(plot_no= plot_no,plot_size = plot_size, plot_rate = plot_rate,phase=phse_name)
        # headers={'Content-Type: application/json'}
       
        
        if AddPlot.objects.filter(plot_no = plot_no , phase = phse_name ).exists():
            messages.warning(request, "Plot No. is already Taken")
            return redirect('addplot')
        # read = requests.post('http://127.0.0.1:8000/api/plot/',json=add_plot,headers=headers)

        
        
        add_plot.save()
        messages.success(request, "Record  Add Successfully")


        
    return render(request, 'HOD/addplot.html',context)

def VIEWPlotNo(request):
    plotno = AddPlot.objects.all()
    
    return render(request,'HOD/viewplotno.html',{'plotno':plotno})    


def PLOTDETAILS_export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    # response['Content-Disposition'] = 'attachment; filename="Approve Po.csv"'
    response['Content-Disposition'] = 'attachment; filename= PLOTDetails'+ str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Plot No', 'Plot Size', 'Plot Rate', 'Discount'])
    plot = AddPlot.objects.all()
    for approve in plot:
        print(approve)
    
        writer.writerow(
                    [approve.plot_no, 
				approve.plot_size, 
				
				approve.plot_rate,
				approve.discount])
           

    return response



def EDIT_PlotNo(request,id): 
    phse=phase.objects.all()
    plot_no = AddPlot.objects.filter(id=id)
    context = {
        'plot_no':plot_no,
        'phse':phse

        
    }
    return render(request, 'HOD/edit_plotno.html', context)    
   





def UPDATE_PlotNo(request):
    if request.method == "POST":
        plot_id = request.POST.get("plot_id")
        plot_no = request.POST.get('plot_no')
        plot_size = request.POST.get('plot_size')
        plcrate = request.POST.get('plc_rate')
        plc = request.POST.get('plc')
        plot_rate = request.POST.get('plot_rate')
        discount = request.POST.get('discount')
        plot_phase = request.POST.get('phase')


        phse_name = phase.objects.get(id = plot_phase)
       
        plot = AddPlot.objects.get(id=plot_id)
        plot.plot_no = plot_no
        plot.plot_size = plot_size
        plot.plc_rate = plcrate
        plot.plc = plc
        plot.plot_rate = plot_rate
        plot.discount = discount
        plot.phase = phse_name
        
       
        plot.save()
        messages.success(request, "Record Updated Add Successfully")
        return redirect('view_plotno')
    return render(request,"HOD/edit_plotno.html")


def DELETE_PlotNo(request,id):

    plot = AddPlot.objects.get(id=id)
    
    # customer = CustomUser.objects.get(id=admin)
    
    plot.delete()
    
    messages.success(request,"Record are Successfully Deleted")
    return redirect('view_plotno')
         


@login_required(login_url='/')
def  bookplot(request):
    # cust_idd = Customer.objects.all()
    phase_name = phase.objects.all()
    # try:
    #     if request.method =="POST":

    #         searched = request.POST['searched']
    #         print(searched)
    #         venues = Customer.objects.filter(customer_id__contains=searched)
    #         return render(request, 'HOD/bookplot.html',{'searched':searched,'venues':venues})
    #     else:
    #         return render(request, 'HOD/bookplot.html',{})


    # except MultiValueDictKeyError:
    #     is_private = False
    
        
       

        
    # else:
    #     return render(request, 'HOD/bookplot.html',{})

   
    # book_plot.owner = owner

    selected_customer_id = None
    selected_plot_no = None
    customer_Id = Customer.objects.all()
    plot_no = AddPlot.objects.all()
    current_user = request.user
    code = current_user.user_id
    
    rank = current_user.rank

    
   
    # context = {
    #     'code': code,
    #     'rank':rank,
    # }
    
    plot_number = AddPlot.objects.all()
   
    # print(customer_Id)
    

    
    # user_profile = HOD.objects.all()
  

  
  
    

    if request.method =="POST":
        if 'newsletter_sub' in request.POST:
        
            selected_customer_id = request.POST.get("user_id")
            customer_Id = customer_Id.filter(customer_id=selected_customer_id)

            selected_plot_no = request.POST.get("plot_noff")
            print("aaaaaaaarrrrrrrrrrrr",selected_plot_no)
            # phase_id1 = request.POST.get("phase_id")
            
            plot2 = AddPlot.objects.filter(phase=selected_plot_no)
            print("Eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",plot2)
            plot_no = AddPlot.objects.filter(id=selected_plot_no)
            print("ggggggggggggggggggggggggggggggggggggggggggggg",plot_no)
            
            # return render(request, 'HOD/bookplot.html',context)




            
           
        

        
        
        # context = {

        #     'cus_id':cus_id,
        #     'customer_Id':customer_Id,
        #     'selected_customer_id':selected_customer_id  
        # }
        # return render(request, 'HOD/bookplot.html',context)
        if 'demo' in request.POST:

        
            ref_id = request.POST.get('ref_id')
        
            user_id = request.POST.get('user_id')
        
            plot_number = request.POST.get('plot_number')
            amount = int(request.POST.get('amount'))
            booking_amount = int(request.POST.get('booking_amount'))
            remaining_amount = amount-booking_amount
            # print(remaining_amount)
            # Mnthly_Installment = request.POST.get('Mnthly_installment')
            # no_Installment = request.POST.get('no_Installment')
            name = request.POST.get('name')
            father_name = request.POST.get('father_name')
            mobile_number = request.POST.get('mobile_number')
            payment_mode = request.POST.get('payment_mode')
            remarks = request.POST.get('remarks')
            receipt = request.FILES.get('receipt')
            plot_size = request.POST.get('plot_size')
            mail = request.POST.get('mail')
            addresss = request.POST.get('addresss')
            account_no = request.POST.get('account_no')
            ifsc_code = request.POST.get('ifsc_code')
            check_no = request.POST.get('check_no')
            phsee = request.POST.get('phase')
            # print("dddddddddddddddddd",account_no,ifsc_code,check_no)

            book_plot = BookPlot(ref_id= ref_id,user_id=user_id,plot_number = plot_number, Payable_amout = amount,payment_amount=booking_amount,remaining_amount=remaining_amount, name = name,father_name = father_name , mobile_no = mobile_number, payment_mode = payment_mode ,remarks=remarks,receipt=receipt ,plot_size=plot_size,addresss=addresss,mail=mail,account_no=account_no,ifsc_code=ifsc_code,check_no=check_no,phase=phsee)
            owner=book_plot.owner=request.user
           
            # installmentt = Installment()
            # print("heloooooo",owner)
            book_plot.owner = owner


            isntallment = Installment(ref_id= ref_id,user_id=user_id,plot_number = plot_number, Payable_amout = amount,payment_amount = booking_amount,remaining_amount=remaining_amount,name = name, mobile_no = mobile_number, payment_mode = payment_mode ,remarks=remarks,receipt=receipt,plot_size=plot_size ,addresss=addresss,mail=mail)
            owner=isntallment.owner=request.user
            # print("heloooooo",owner)
            isntallment.owner = owner

            # if Installment.objects.filter(plot_number = plot_number).exists():
            #     messages.warning(request, "Plot Number is already Taken")
            #     return redirect('bookplot')
            
            

           

            if BookPlot.objects.filter(plot_number = plot_number,phase=phsee).exists():
                messages.warning(request, "Plot Number is already Taken")
                return redirect('bookplot')
                
            # if BookPlot.objects.filter(plot_number = plot_number).exists():
            #     messages.warning(request, "Plot Number is already Taken")
            #     return redirect('bookplot')
            
            
            book_plot.save()
            isntallment.save()
            messages.success(request,"Booking Plot Successfully")
            return redirect('bookplot')
    cus_id = Customer.objects.order_by('customer_id').values_list('customer_id', flat=True)
    plot_num = AddPlot.objects.order_by('plot_no').values_list('plot_no', flat=True)
        

    context = {
    'code':code,
    'rank':rank,
    'plot_number':plot_number,
    'cus_id':cus_id,
    'customer_Id':customer_Id,
    'selected_customer_id':selected_customer_id,
    'plot_num':plot_num,
    'plot_no':plot_no,
    'selected_plot_no':selected_plot_no,
    # 'cust_idd':cust_idd,
    'phase_name':phase_name,
    
    
    # 'customer_id':customer_Id,
    

    }
    return render(request, 'HOD/bookplot.html', context)


def  approvedplote(request):
    # user_profile = HOD.objects.get()
    # # user_profile = HOD.objects.get()
    # hod_code = user_profile
    # code = hod_code.user_id
    # print(code)
   

    booking_data = BookPlot.objects.all()
   

    context = {
        'booking_data': booking_data,
        
        
        # 'code' : code

    }
    # approval = BookPlot.objects.all()#.order_by('uname')
    # return render(request,'show.html',)
    

    return render(request, 'HOD/approvedplote.html', context)


def EDIT_BOOKPLOT(request,id):
    bookplot = BookPlot.objects.filter(id=id)
    cust_id = Customer.objects.all()   
    plot_no = AddPlot.objects.all()  
    context = {
        'bookplot': bookplot,
        'plot_no':plot_no,
        'cust_id':cust_id
        
    }
    return render(request, 'HOD/editbookplot.html', context)


def UPDATE_CUSTOMER(request):
    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        cust_id = request.POST.get("cust_id")
        # cust_id = request.POST.get('cust_id')
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        mob_no = request.POST.get('mob_no')

        # customer =  Customer(customer_id=cust_id,customer_name=name,cust_father_name=father_name,cust_mobileno=mob_no)
        customer = Customer.objects.get(owner=customer_id)
        customer.customer_id = cust_id
        customer.customer_name = name
        customer.cust_father_name = father_name
        customer.cust_mobileno = mob_no
        customer.save()
        messages.success(request, "Record Updated Add Successfully")
        return redirect('customer_view')
    return render(request,"HOD/customer_edit.html")



def DELETE_CUSTOMER(request,id):
    
    customer = Customer.objects.get(id=id)
    # customer = CustomUser.objects.get(id=admin)
    customer.delete()
    messages.success(request,"Record are Successfully Deleted")
    return redirect('customer_view')


def Print(request,id):

    plot = BookPlot.objects.get(id=id)
    context = {
        'plot_no':plot

        
    }
    # customer = CustomUser.objects.get(id=admin)
    
    
    # messages.success(request,"Record are Successfully Deleted")
    return render(request, 'HOD/print.html', context)
def Print0(request,id):

    plot = BookPlot.objects.get(id=id)
    context = {
        'plot_no':plot

        
    }
    # customer = CustomUser.objects.get(id=admin)
    
    
    # messages.success(request,"Record are Successfully Deleted")
    return render(request, 'HOD/Print92.html', context)
def Print1(request,id):

    plot = Installment.objects.get(id=id)
    context = {
        'plot_no':plot

        
    }
    # customer = CustomUser.objects.get(id=admin)
    
    
    # messages.success(request,"Record are Successfully Deleted")
    return render(request, 'HOD/Print1.html', context)


def PHASE(request):
    if request.method == "POST":
        phse = request.POST.get('phase')
        
        if phase.objects.filter(phase = phse).exists():
            messages.warning(request, "Phase Name is already Taken")
            return redirect('phase')
        phse = phase.objects.create(phase=phse)
        phse.save()
        messages.success(request,"Record are Successfully Added")
        return redirect('phase')
    return render(request,'HOD/phase.html')

def PHASE_VIEW(request):
    phse = phase.objects.all()
    return render(request,"HOD/view_phase.html",{'phase':phse})

def EDIT_PHASE(request,id):
    phse = phase.objects.filter(id=id)
    return render(request,'HOD/phase_view.html',{'phse':phse})

def UPDATE_PHASE(request):
    if request.method == "POST":
        phase_id = request.POST.get('phase_id')
        phase_name = request.POST.get("phase")
        phse = phase.objects.get(id=phase_id)
        phse.phase = phase_name 
        phse.save()
        messages.success(request, "Record Updated Add Successfully")
        return redirect('phase_view')
    return render(request,"HOD/phase_view.html")

def DELETE_PHASE(request,id):
    
    phse = phase.objects.get(id=id)
    # customer = CustomUser.objects.get(id=admin)
    phse.delete()
    messages.success(request,"Record are Successfully Deleted")
    return redirect('phase_view')

    
def DELETE_PLOT(request,id):

    plot = BookPlot.objects.get(id=id)
    
    # customer = CustomUser.objects.get(id=admin)
    
    plot.delete()
    messages.success(request,"Record are Successfully Deleted")
    return redirect('approvedplote')


def SEARCH_BAR(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = AddPlot.objects.filter(id__icontains=searched)

        return render(request, 'search.html',{'searched':searched,'venues':venues})
    else:
        return render(request, 'search.html',{})




def UPDATE_BOOKPLOT(request):
    if request.method == "POST":
        bookplot_id = request.POST.get('bookplot_id')
        print(bookplot_id)
        ref_id = request.POST.get('ref_id')
        user_id = request.POST.get('user_id')
       
        plot_number = request.POST.get('plot_number')
        amount = request.POST.get('amount')
        Mnthly_Installment = request.POST.get('Mnthly_installment')
        no_Installment = request.POST.get('no_Installment')
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        mobile_number = request.POST.get('mobile_number')
        payment_mode = request.POST.get('payment_mode')
        remarks = request.POST.get('remarks')
        receipt = request.FILES.get('receipt')
        print(ref_id)
        # print(f"ref id= {ref_id}, plot_number = {plot_number},  ")
        # print(f"reference Id = {ref_id}, Plot No = {plot_number}, amount = {amount} name = {name}, father name = {father_name}, Mobile No = {mobile_number} payment mode = {payment_mode}, remars = {remarks}, receipt = {receipt} ")  

        # book_plot = BookPlot(ref_id= ref_id,user_id=user_id,plot_number = plot_number, Payable_amout = amount,Mnthly_Installment = Mnthly_Installment, number_of_Installment = no_Installment, name = name,father_name = father_name , mobile_no = mobile_number, payment_mode = payment_mode ,remarks=remarks,receipt=receipt )
        # book_plot.save()
        # messages.success(request,"Booking Plot Successfully")

        bookplot = BookPlot.objects.get(id=bookplot_id)
       
       
        # user.save()

        bookplot.plot_number = plot_number
        bookplot.Payable_amout = amount
        bookplot.Mnthly_Installment = Mnthly_Installment
        bookplot.number_of_Installment = no_Installment
        bookplot.name = name
        bookplot.father_name = father_name
        bookplot.mobile_no = mobile_number
        bookplot.payment_mode = payment_mode
        bookplot.remarks = remarks
        bookplot.receipt = receipt
        bookplot.save()
        messages.success(request, "Record Are Successfully Updated")
        return redirect('approvedplote')

        
    return render(request, 'HOD/edit_student.html')    



    
def  fundtransfer(request):
    selected_customer_id = None
    selected_plot_no = None
    customer_Id = Customer.objects.all()
    plot_no = AddPlot.objects.all()
    current_user = request.user
    code = current_user.user_id
    
    rank = current_user.rank
   

    Funddetails1 = FundDetails.objects.all()

    context = {
        'Funddetails1': Funddetails1,
        'code' : code,
        'rank':rank,
        # 'plot_number':plot_number,
        # 'cus_id':cus_id,
        'customer_Id':customer_Id,
        'selected_customer_id':selected_customer_id,
        # 'plot_num':plot_num,
        'plot_no':plot_no,
        'selected_plot_no':selected_plot_no

    }
    return render(request, 'HOD/fundtransfer.html',context)
def previewfunds(request):
    booking_data = BookPlot.objects.all()
    # downpayment_data = Installment.objects.all()

   

    context = {
        'booking_data': booking_data,
        # 'downpayment_data': downpayment_data
        
        
        # 'code' : code

    }
    # approval = BookPlot.objects.all()#.order_by('uname')
    # return render(request,'show.html',)
    

    

    return render(request, 'HOD/previewfunds.html',context)
def previewfunds1(request):
    booking_data = Installment.objects.all()
    # downpayment_data = Installment.objects.all()

   

    context = {
        'booking_data': booking_data,
        # 'downpayment_data': downpayment_data
        
        
        # 'code' : code

    }
    # approval = BookPlot.objects.all()#.order_by('uname')
    # return render(request,'show.html',)
    

    

    return render(request, 'HOD/previewfunds1.html',context)

def  viewfunds1(request,id):
    

    ref_idd = Installment.objects.filter(id=id)
    matchid=FundDetails.objects.all()
    match_id=str(matchid[0:])
    # print("check 22")
    # print(matchid)
    # print("ref idd")
    # print(len(matchid))
    # print(ref_idd)
    ref_id=str(ref_idd[0])
    ref_id=ref_id.split(' ')
    # print(ref_id)
    # print(ref_iid)
    
    useriddd=(ref_id[0])
    # print("useriddd is")
    # print(useriddd)
    amounttt=(ref_id[1])
    # print(amounttt)
    plotno=(ref_id[3])
    # print("Plot no is")
    # print(plotno)
    date=ref_id[4]
    time=ref_id[5]
    dateandtime=date+' '+time
    # print(dateandtime)
    total_amount=int((ref_id[2]))
    # print(total_amount)
    booking_amount_percentage=int((int(amounttt)/(int(total_amount)))*100)
    # print(booking_amount_percentage)

    conn = MySQLdb.connect  (user='root',
                              host='127.0.0.1',
                              database='ssrbrokerProject')
    # conn = MySQLdb.connect  (user='root', password='root',
    #                           host='127.0.0.1',
    #                           database='ssrbrokerProject')

    
    useridd=useriddd
    # print("user id is")
    check=ref_id[0:]
    
    check[0:]=[' '.join(check[0:])]
    
    
    # check1=match_id[0:]
    # print(check1)
    z=0
    x=[]
    while z< len(matchid):
        # print("z is")
        a=str(matchid[z])
        # print(a)
        x.append(a)
        z=z+1
    # print(check)
    # print("x is")
    # print(x)
    # set1 = set(check)
    # set2 = set(x)
    # is_subset = set1.issubset(set2)
    # if is_subset==True:
    #     messages.success(request,"Fund of this rows are already been transferred.")
    # else:
    #     print("False")

    
    amount=int(amounttt)
    if useridd==1:
        pass
    else:
        set1 = set(check)
        set2 = set(x)
        is_subset = set1.issubset(set2)
        if is_subset==True:
            messages.success(request,"Fund of this rows are already been transferred.")
        else:
            print("False")
            myTable69=[]
            
                
            cur = conn.cursor()
            cur.execute('''SELECT plot_number FROM matrixapp_funddetails''')
                # cur.execute(f'''SELECT o.user_id, o.rank FROM matrixapp_customuser i.created_at, i.reference_id FROM matrixapp_superagent FROM matrixapp_customuser o LEFT JOIN matrixapp_superagent i on o.id = i.admin_id where user_id=%s''',{useridd2})            
            Data = cur.fetchall()
                # print(Data)
            myTable69.append(Data)
                
                
            # print("my table is")
            # print(myTable69)
            myTablex691=sum(myTable69,(()))
            myTablex69=sum(myTablex691,(()))
            myTable6969=list(myTablex69)
            # print(myTable6969)
            exist_count = myTable6969.count(plotno)
    
            # checking if it is more then 0
            if exist_count > 0:
                plottable=[(('Total amount', 'Plot no', 'Recievedamount'),)]
                cur = conn.cursor()
                cur.execute(f'''SELECT Total_amount,plot_number,amount from matrixapp_funddetails WHERE plot_number=%s''',(plotno,))

                refID = cur.fetchall()
                plottable.append(refID)
                plottable1=sum(plottable,())
                plottable2=list(plottable1)
                print(plottable2)

                j=1
                totalrecieved=0
                while j<len(plottable2):
                    recieved=plottable2[j]
                    k=(recieved[2])
                    l=float(k)
                    totalrecieved=totalrecieved+l
                    j=j+1
                
                print(totalrecieved)
                total_commission1=plottable2[1]
                total_commission=total_commission1[0]
                print(total_commission)
                total_commission=float(total_commission)
                print(type(total_commission))
                difference=total_commission-totalrecieved
                difference=float(difference)
                if totalrecieved<total_commission:
                    def getuserid():
                        cur = conn.cursor()
                        cur.execute('''SELECT user_id FROM matrixapp_customuser''')
                        User_ID = cur.fetchall()
                        
                        i = 0
                        j = 0
                        l = []
                        for index in User_ID:
                            b = User_ID[i]
                            k = (b[j])
                            i += 1
                            l.append(k)
                        return l 

                        
                    userid = getuserid()
                    # print("userid is")
                    # print(userid)
                    useridd1=useridd
                    # print("useridd1 is")
                    # print(useridd1)
                    i=0
                    p = [useridd1]
                    # print("p is")
                    # print(p)
                    
                    while i<len(userid) :

                        if str(useridd1) == userid[i]:
                            cur = conn.cursor()
                            cur.execute(f'''SELECT matrixapp_superagent.reference_id FROM matrixapp_superagent JOIN matrixapp_customuser ON matrixapp_superagent.admin_id=matrixapp_customuser.id WHERE user_id=%s''',(useridd1,))
                            refID = cur.fetchall()
                            print("ref id is")
                            print(refID)
                            if refID==():
                                messages.success(request,"This booking is done by admin and all fund register into his account")
                                i=i+1
                            else:
                                i = 0
                                j = 0
                                l = []
                                for index in refID:
                                    b = refID[i]
                                    k = (b[j])
                                    i += 1
                                    l.append(k)
                                # print("l is")
                                # print(l)
                                refidd= l[0]
                                # print(refidd)
                                useridd1=refidd
                                i=i+1
                                p.append(useridd1)
                        else:
                            pass
                            i=i+1
                        useridd = useridd1
                    # print("p is")
                    # print(p)
                    j=0
                    myTable1=[(('User_ID', 'Name', 'Rank', 'Ref_ID', 'Admin_ID'),)]
                    # print(myTable1)
                    while j<len(p) :
                        useridd2=p[j]
                        # print(useridd2)
                        #print(useridd2)
                        cur = conn.cursor()
                        cur.execute(f'''SELECT matrixapp_customuser.user_id,matrixapp_customuser.username,matrixapp_customuser.rank, matrixapp_superagent.reference_id,matrixapp_customuser.id FROM matrixapp_superagent JOIN matrixapp_customuser ON matrixapp_superagent.admin_id=matrixapp_customuser.id WHERE user_id=%s''',{useridd2})
                        # cur.execute(f'''SELECT o.user_id, o.rank FROM matrixapp_customuser i.created_at, i.reference_id FROM matrixapp_superagent FROM matrixapp_customuser o LEFT JOIN matrixapp_superagent i on o.id = i.admin_id where user_id=%s''',{useridd2})            
                        Data = cur.fetchall()
                        # print(Data)
                        myTable1.append(Data)
                        
                        j=j+1
                    # print("my table is")
                    # print(myTable1)
                    myTablex=sum(myTable1,())
                    myTable=list(myTablex)
                    # print((myTable))



                    


                    
                    i = 1
                    namelist = []
                    while i < len(myTable):
                        z = (myTable[i])
                        # print("z is")
                        # print(z)
                        list1 = list(z)
                        # print(list1)
                        c = (list1[1])
                        namelist.append(c)

                        i += 1
                    # print("namelist is")
                    # print(namelist)
                    i = 1
                    UserIdList = []
                    while i < len(myTable):
                        z = (myTable[i])
                        # print(z)
                        list1 = list(z)
                        c = (list1[0])
                        UserIdList.append(c)

                        i += 1
                    # print(UserIdList)

                    i = 1
                    RefIdlist = []
                    while i < len(myTable):
                        z = (myTable[i])
                        # print(z)
                        list1 = list(z)
                        c = (list1[3])
                        RefIdlist.append(c)

                        i += 1
                    # print(RefIdlist)

                    i = 1
                    Ownerid = []
                    while i < len(myTable):
                        z = (myTable[i])
                        # print("z is")
                        # print(z)
                        list1 = list(z)
                        # print(list1)
                        c = (list1[4])
                        Ownerid.append(c)

                        i += 1

                    print('Owner id is')
                    print(Ownerid)


                    j = 1
                    ranklist1 = []
                    while j < len(myTable):
                        z = (myTable[j])
                        list1 = list(z)
                        c = (list1[2])
                        ranklist1.append(c)
                        j += 1
                    # print(ranklist1)
                    ranklist=list(reversed(ranklist1))





                        # brokrage_transfer=[]
                        # if booking_amount_percentage in range(0,60):
                        #     # print("yes")
                        #     Brokrageamount=5/3*booking_amount_percentage
                        #     brokrage_transfer.append(Brokrageamount)


                        # elif booking_amount_percentage in range(60,100):
                        #     # print("no")
                        #     Brokrageamount=(int(Rank)/100)*int(total_amount)
                        #     brokrage_transfer.append(Brokrageamount)

                        # print(brokrage_transfer)









                    k = 0
                    l = 1
                    finalpercentage1 = []
                    while k < len(ranklist):
                        if k != (len(ranklist) - 1):
                            m = int(int(ranklist[k]) - int(ranklist[l]))
                            finalpercentage1.append(abs(m))
                            k += 1
                            l += 1
                        else:
                            n = (int(ranklist[k]))
                            finalpercentage1.append(abs(n))
                            k += 1
                    finalpercentage=list(reversed(finalpercentage1))
                    print("final percentage is")
                    print(finalpercentage)
                    # print('Final percentage')




                    k=0
                    # l=1
                    finalpercentage2 = []
                    while k < len(finalpercentage):
                        if booking_amount_percentage in range(0,60):
                            a=(finalpercentage[k])
                            v=(((5/3)*booking_amount_percentage)*a)/100
                            print(v)
                            finalpercentage2.append(v)
                            k=k+1
                        else:
                            a=(finalpercentage[k])
                            v=a
                            print(v)
                            finalpercentage2.append(v)
                        # if k != (len(finalpercentage) - 1):
                        #     m = int(int(finalpercentage[k]) - int(finalpercentage[l]))
                        #     finalpercentage2.append(abs(m))
                            k += 1
                            # l += 1
                        # elif booking_amount_percentage in range(60,100):
                        #     v=
                        #     # n = (int(finalpercentage[k]))
                        #     # finalpercentage2.append(abs(n))
                        #     k += 1
                    finalpercentage3=list(finalpercentage2)
                    print("final percentage list 3 is")
                    print(finalpercentage3)





                    a = 0
                    while a < len(finalpercentage3):
                        distamount = str((finalpercentage3[a] * total_amount) / 100)
                        totalamount=str((finalpercentage[a] * total_amount) / 100)
                        print(type(difference))
                        print(type(distamount))
                        distamount=float(distamount)
                        if distamount<difference:
                            distamount=str(distamount)
                            bina=(namelist[a] + ' whose User ID is '+UserIdList[a] + ' and Reference ID is '+RefIdlist[a] + ' will get ' + "Rs." + distamount)
                            messages.success(request,bina)
                            
                            # fundetail = FundDetails.objects.get(id=user_id)
                            fundetail = FundDetails.objects.all()
                    
                    
                            # user.save()
                            fundetail = FundDetails(user_id= UserIdList[a],ref_id=RefIdlist[a],amount = distamount, user_name = namelist[a],plot_number=plotno,Total_amount= totalamount, Payable_amout=total_amount,payment_amount=amounttt,joinig_date=dateandtime)
                            # book_plot.save()
                            owner=fundetail.owner=Ownerid[a]
                            fundetail.owner = owner
                            
                            fundetail.save()
                            a += 1
                        
                        elif distamount>difference or distamount==difference:
                            distamount=str(distamount)
                            difference=str(difference)
                            bina=(namelist[a] + ' whose User ID is '+UserIdList[a] + ' and Reference ID is '+RefIdlist[a] + ' will get ' + "Rs." + difference)
                            messages.success(request,bina)
                            
                            # fundetail = FundDetails.objects.get(id=user_id)
                            fundetail = FundDetails.objects.all()
                    
                    
                            # user.save()
                            fundetail = FundDetails(user_id= UserIdList[a],ref_id=RefIdlist[a],amount = distamount, user_name = namelist[a],plot_number=plotno,Total_amount= totalamount, Payable_amout=total_amount,payment_amount=amounttt,joinig_date=dateandtime)
                            # book_plot.save()
                            owner=fundetail.owner=Ownerid[a]
                            fundetail.owner = owner
                            
                            fundetail.save()
                            a += 1
                        else:
                            messages.success(request,"All the comission has been already transfered.")
                else:
                    messages.success(request,"All the comission has been already transfered.")

                context={
                    "user_id":useriddd
                }

                return render(request, 'HOD/viewfunds.html',context)


            
            else:
                print("No, plotno does not exists in list")


                def getuserid():
                    cur = conn.cursor()
                    cur.execute('''SELECT user_id FROM matrixapp_customuser''')
                    User_ID = cur.fetchall()
                    
                    i = 0
                    j = 0
                    l = []
                    for index in User_ID:
                        b = User_ID[i]
                        k = (b[j])
                        i += 1
                        l.append(k)
                    return l 

                    
                userid = getuserid()
                # print("userid is")
                # print(userid)
                useridd1=useridd
                # print("useridd1 is")
                # print(useridd1)
                i=0
                p = [useridd1]
                # print("p is")
                # print(p)
                
                while i<len(userid) :

                    if str(useridd1) == userid[i]:
                        cur = conn.cursor()
                        cur.execute(f'''SELECT matrixapp_superagent.reference_id FROM matrixapp_superagent JOIN matrixapp_customuser ON matrixapp_superagent.admin_id=matrixapp_customuser.id WHERE user_id=%s''',(useridd1,))
                        refID = cur.fetchall()
                        print("ref id is")
                        print(refID)
                        if refID==():
                            messages.success(request,"This booking is done by admin and all fund register into his account")
                            i=i+1
                        else:
                            i = 0
                            j = 0
                            l = []
                            for index in refID:
                                b = refID[i]
                                k = (b[j])
                                i += 1
                                l.append(k)
                            # print("l is")
                            # print(l)
                            refidd= l[0]
                            # print(refidd)
                            useridd1=refidd
                            i=i+1
                            p.append(useridd1)
                    else:
                        pass
                        i=i+1
                    useridd = useridd1
                # print("p is")
                # print(p)
                j=0
                myTable1=[(('User_ID', 'Name', 'Rank', 'Ref_ID', 'Admin_ID'),)]
                # print(myTable1)
                while j<len(p) :
                    useridd2=p[j]
                    # print(useridd2)
                    #print(useridd2)
                    cur = conn.cursor()
                    cur.execute(f'''SELECT matrixapp_customuser.user_id,matrixapp_customuser.username,matrixapp_customuser.rank, matrixapp_superagent.reference_id,matrixapp_customuser.id FROM matrixapp_superagent JOIN matrixapp_customuser ON matrixapp_superagent.admin_id=matrixapp_customuser.id WHERE user_id=%s''',{useridd2})
                    # cur.execute(f'''SELECT o.user_id, o.rank FROM matrixapp_customuser i.created_at, i.reference_id FROM matrixapp_superagent FROM matrixapp_customuser o LEFT JOIN matrixapp_superagent i on o.id = i.admin_id where user_id=%s''',{useridd2})            
                    Data = cur.fetchall()
                    # print(Data)
                    myTable1.append(Data)
                    
                    j=j+1
                # print("my table is")
                # print(myTable1)
                myTablex=sum(myTable1,())
                myTable=list(myTablex)
                # print((myTable))



                


                
                i = 1
                namelist = []
                while i < len(myTable):
                    z = (myTable[i])
                    # print("z is")
                    # print(z)
                    list1 = list(z)
                    # print(list1)
                    c = (list1[1])
                    namelist.append(c)

                    i += 1
                # print("namelist is")
                # print(namelist)
                i = 1
                UserIdList = []
                while i < len(myTable):
                    z = (myTable[i])
                    # print(z)
                    list1 = list(z)
                    c = (list1[0])
                    UserIdList.append(c)

                    i += 1
                # print(UserIdList)

                i = 1
                RefIdlist = []
                while i < len(myTable):
                    z = (myTable[i])
                    # print(z)
                    list1 = list(z)
                    c = (list1[3])
                    RefIdlist.append(c)

                    i += 1
                # print(RefIdlist)

                i = 1
                Ownerid = []
                while i < len(myTable):
                    z = (myTable[i])
                    # print("z is")
                    # print(z)
                    list1 = list(z)
                    # print(list1)
                    c = (list1[4])
                    Ownerid.append(c)

                    i += 1

                print('Owner id is')
                print(Ownerid)


                j = 1
                ranklist1 = []
                while j < len(myTable):
                    z = (myTable[j])
                    list1 = list(z)
                    c = (list1[2])
                    ranklist1.append(c)
                    j += 1
                # print(ranklist1)
                ranklist=list(reversed(ranklist1))





                    # brokrage_transfer=[]
                    # if booking_amount_percentage in range(0,60):
                    #     # print("yes")
                    #     Brokrageamount=5/3*booking_amount_percentage
                    #     brokrage_transfer.append(Brokrageamount)


                    # elif booking_amount_percentage in range(60,100):
                    #     # print("no")
                    #     Brokrageamount=(int(Rank)/100)*int(total_amount)
                    #     brokrage_transfer.append(Brokrageamount)

                    # print(brokrage_transfer)









                k = 0
                l = 1
                finalpercentage1 = []
                while k < len(ranklist):
                    if k != (len(ranklist) - 1):
                        m = int(int(ranklist[k]) - int(ranklist[l]))
                        finalpercentage1.append(abs(m))
                        k += 1
                        l += 1
                    else:
                        n = (int(ranklist[k]))
                        finalpercentage1.append(abs(n))
                        k += 1
                finalpercentage=list(reversed(finalpercentage1))
                print("final percentage is")
                print(finalpercentage)
                # print('Final percentage')




                k=0
                # l=1
                finalpercentage2 = []
                while k < len(finalpercentage):
                    if booking_amount_percentage in range(0,60):
                        a=(finalpercentage[k])
                        v=(((5/3)*booking_amount_percentage)*a)/100
                        print(v)
                        finalpercentage2.append(v)
                        k=k+1
                    else:
                        a=(finalpercentage[k])
                        v=a
                        print(v)
                        finalpercentage2.append(v)
                    # if k != (len(finalpercentage) - 1):
                    #     m = int(int(finalpercentage[k]) - int(finalpercentage[l]))
                    #     finalpercentage2.append(abs(m))
                        k += 1
                        # l += 1
                    # elif booking_amount_percentage in range(60,100):
                    #     v=
                    #     # n = (int(finalpercentage[k]))
                    #     # finalpercentage2.append(abs(n))
                    #     k += 1
                finalpercentage3=list(finalpercentage2)
                print("final percentage list 3 is")
                print(finalpercentage3)






                a = 0
                while a < len(finalpercentage3):
                    distamount = str((finalpercentage3[a] * total_amount) / 100)
                    totalamount=str((finalpercentage[a] * total_amount) / 100)
                    bina=(namelist[a] + ' whose User ID is '+UserIdList[a] + ' and Reference ID is '+RefIdlist[a] + ' will get ' + "Rs." + distamount)
                    messages.success(request,bina)
                    
                    # fundetail = FundDetails.objects.get(id=user_id)
                    fundetail = FundDetails.objects.all()
            
            
                    # user.save()
                    fundetail = FundDetails(user_id= UserIdList[a],ref_id=RefIdlist[a],amount = distamount, user_name = namelist[a],plot_number=plotno,Total_amount= totalamount, Payable_amout=total_amount,payment_amount=amounttt,joinig_date=dateandtime)
                    # book_plot.save()
                    owner=fundetail.owner=Ownerid[a]
                    fundetail.owner = owner
                    
                    fundetail.save()
                    a += 1
        context={
            "user_id":useriddd
        }
        # ref_idd.()
        return render(request, 'HOD/viewfunds.html',context)

def  viewfunds(request,id):
    
    # Funddetails1 = FundDetails.objects.filter(owner=request.user.id)
    # ref_id = Installment.objects.filter(id=id)
    ref_idd = BookPlot.objects.filter(id=id)
    # ref_iid= BookPlot.ref_id
    
    print("ref idd")
    print(ref_idd)
    ref_id=str(ref_idd[0])
    ref_id=ref_id.split(' ')
    print(ref_id)
    # print(ref_iid)
    
    useriddd=(ref_id[0])
    print("useriddd is")
    print(useriddd)
    amounttt=(ref_id[1])
    print(amounttt)
    total_amount=int((ref_id[2]))
    print(total_amount)
    booking_amount_percentage=int((int(amounttt)/(int(total_amount)))*100)
    print(booking_amount_percentage)

    conn = MySQLdb.connect  (user='root',
                              host='127.0.0.1',
                              database='ssrbrokerProject')
    # conn = MySQLdb.connect  (user='root', password='Manish@1999',
    #                           host='127.0.0.1',
    #                           database='ssrbrokerProject')

    
    useridd=useriddd
    
    amount=int(amounttt)
    if useridd==1:
        pass
    else:
        def getuserid():
            cur = conn.cursor()
            cur.execute('''SELECT user_id FROM matrixapp_customuser''')
            User_ID = cur.fetchall()
            
            i = 0
            j = 0
            l = []
            for index in User_ID:
                b = User_ID[i]
                k = (b[j])
                i += 1
                l.append(k)
            return l 

            
        userid = getuserid()
        # print("userid is")
        # print(userid)
        useridd1=useridd
        # print("useridd1 is")
        # print(useridd1)
        i=0
        p = [useridd1]
        # print("p is")
        # print(p)
        
        while i<len(userid) :

            if str(useridd1) == userid[i]:
                cur = conn.cursor()
                cur.execute(f'''SELECT matrixapp_superagent.reference_id FROM matrixapp_superagent JOIN matrixapp_customuser ON matrixapp_superagent.admin_id=matrixapp_customuser.id WHERE user_id=%s''',(useridd1,))
                refID = cur.fetchall()
                print("ref id is")
                print(refID)
                if refID==():
                    messages.success(request,"This booking is done by admin and all fund register into his account")
                    i=i+1
                else:
                    i = 0
                    j = 0
                    l = []
                    for index in refID:
                        b = refID[i]
                        k = (b[j])
                        i += 1
                        l.append(k)
                    # print("l is")
                    # print(l)
                    refidd= l[0]
                    # print(refidd)
                    useridd1=refidd
                    i=i+1
                    p.append(useridd1)
            else:
                pass
                i=i+1
            useridd = useridd1
        # print("p is")
        # print(p)
        j=0
        myTable1=[(('User_ID', 'Name', 'Rank', 'Ref_ID', 'Admin_ID'),)]
        # print(myTable1)
        while j<len(p) :
            useridd2=p[j]
            # print(useridd2)
            #print(useridd2)
            cur = conn.cursor()
            cur.execute(f'''SELECT matrixapp_customuser.user_id,matrixapp_customuser.username,matrixapp_customuser.rank, matrixapp_superagent.reference_id,matrixapp_customuser.id FROM matrixapp_superagent JOIN matrixapp_customuser ON matrixapp_superagent.admin_id=matrixapp_customuser.id WHERE user_id=%s''',{useridd2})
            # cur.execute(f'''SELECT o.user_id, o.rank FROM matrixapp_customuser i.created_at, i.reference_id FROM matrixapp_superagent FROM matrixapp_customuser o LEFT JOIN matrixapp_superagent i on o.id = i.admin_id where user_id=%s''',{useridd2})            
            Data = cur.fetchall()
            # print(Data)
            myTable1.append(Data)
            
            j=j+1
        # print("my table is")
        # print(myTable1)
        myTablex=sum(myTable1,())
        myTable=list(myTablex)
        print((myTable))
        
        i = 1
        namelist = []
        while i < len(myTable):
            z = (myTable[i])
            # print("z is")
            # print(z)
            list1 = list(z)
            # print(list1)
            c = (list1[1])
            namelist.append(c)

            i += 1
        # print("namelist is")
        # print(namelist)
        i = 1
        Ownerid = []
        while i < len(myTable):
            z = (myTable[i])
            # print("z is")
            # print(z)
            list1 = list(z)
            # print(list1)
            c = (list1[4])
            Ownerid.append(c)

            i += 1

        print('Owner id is')
        print(Ownerid)
        i = 1
        UserIdList = []
        while i < len(myTable):
            z = (myTable[i])
            # print(z)
            list1 = list(z)
            c = (list1[0])
            UserIdList.append(c)

            i += 1
        # print(UserIdList)

        i = 1
        RefIdlist = []
        while i < len(myTable):
            z = (myTable[i])
            # print(z)
            list1 = list(z)
            c = (list1[3])
            RefIdlist.append(c)

            i += 1
        # print(RefIdlist)


        j = 1
        ranklist1 = []
        while j < len(myTable):
            z = (myTable[j])
            list1 = list(z)
            c = (list1[2])
            ranklist1.append(c)
            j += 1
        # print(ranklist1)
        ranklist=list(reversed(ranklist1))





            # brokrage_transfer=[]
            # if booking_amount_percentage in range(0,60):
            #     # print("yes")
            #     Brokrageamount=5/3*booking_amount_percentage
            #     brokrage_transfer.append(Brokrageamount)


            # elif booking_amount_percentage in range(60,100):
            #     # print("no")
            #     Brokrageamount=(int(Rank)/100)*int(total_amount)
            #     brokrage_transfer.append(Brokrageamount)

            # print(brokrage_transfer)









        k = 0
        l = 1
        finalpercentage1 = []
        while k < len(ranklist):
            if k != (len(ranklist) - 1):
                m = int(int(ranklist[k]) - int(ranklist[l]))
                finalpercentage1.append(abs(m))
                k += 1
                l += 1
            else:
                n = (int(ranklist[k]))
                finalpercentage1.append(abs(n))
                k += 1
        finalpercentage=list(reversed(finalpercentage1))
        print("final percentage is")
        print(finalpercentage)
        # print('Final percentage')




        k=0
        # l=1
        finalpercentage2 = []
        while k < len(finalpercentage):
            if booking_amount_percentage in range(0,60):
                a=(finalpercentage[k])
                v=(((5/3)*booking_amount_percentage)*a)/100
                print(v)
                finalpercentage2.append(v)
                k=k+1
            else:
                a=(finalpercentage[k])
                v=a
                print(v)
                finalpercentage2.append(v)
            # if k != (len(finalpercentage) - 1):
            #     m = int(int(finalpercentage[k]) - int(finalpercentage[l]))
            #     finalpercentage2.append(abs(m))
                k += 1
                # l += 1
            # elif booking_amount_percentage in range(60,100):
            #     v=
            #     # n = (int(finalpercentage[k]))
            #     # finalpercentage2.append(abs(n))
            #     k += 1
        finalpercentage3=list(finalpercentage2)
        print("final percentage list 3 is")
        print(finalpercentage3)






        a = 0
        while a < len(finalpercentage3):
            distamount = str((finalpercentage3[a] * total_amount) / 100)
            bina=(namelist[a] + ' whose User ID is '+UserIdList[a] + ' and Reference ID is '+RefIdlist[a] + ' will get ' + "Rs." + distamount)
            messages.success(request,bina)
            
            # fundetail = FundDetails.objects.get(id=user_id)
            fundetail = FundDetails.objects.all()
       
       
            # user.save()
            fundetail = FundDetails(user_id= UserIdList[a],ref_id=RefIdlist[a],amount = distamount, user_name = namelist[a]  )
            # book_plot.save()
            owner=fundetail.owner=Ownerid[a]
            fundetail.owner = owner
            
            fundetail.save()
            a += 1

    context={
        "user_id":useriddd
    }

    return render(request, 'HOD/viewfunds.html',context)

def  approvedkyc(request):
   
    kycdetails = Kyc.objects.all()
    context = {
        'kycdetails' : kycdetails
    }

    return render(request,'HOD/approvedkyc.html',context)

def  approvedkyc(request):
   
    kycdetails = Kyc.objects.all()
    context = {
        'kycdetails' : kycdetails
    }

    return render(request,'HOD/approvedkyc.html',context)
def  approvedkyc(request):
   
    kycdetails = Kyc.objects.all()
    context = {
        'kycdetails' : kycdetails
    }

    return render(request,'HOD/approvedkyc.html',context)

def  approvedkyc(request):
   
    kycdetails = Kyc.objects.all()
    context = {
        'kycdetails' : kycdetails
    }

    return render(request,'HOD/approvedkyc.html',context)

    
def  kyc(request):
    
    customer_id = Customer.objects.all()

    context = {
        'cust_id':customer_id, 

    }
    if request.method =="POST":
        cust_id = request.POST.get('cust_id')
        accountname = request.POST.get('accountname')
        accountno=request.POST.get('accountno')
        IFSCno = request.POST.get('IFSCno')
        Pancardno = request.POST.get('Pancardno')
        print(Pancardno)
        
        kyc = Kyc(cust_id=cust_id, accountname=accountname,accountno=accountno,IFSCno=IFSCno, Pancardno=Pancardno)
        kyc.save()
        messages.success(request,"KYC Updated Successfully")  

    return render(request, 'HOD/kyc.html', context)

def EDIT_KYC(request,id):

    kyc = Kyc.objects.filter(id=id)
    cust_id = Customer.objects.all()   
    plot_no = AddPlot.objects.all()  
    context = {
        'bookplot': bookplot,
        'plot_no':plot_no,
        'cust_id':cust_id,
        'kyc':kyc
        
    }
    return render(request, 'HOD/editkyc.html', context)

def UPDATE_KYC(request):

    if request.method =="POST":
        kyc_id = request.POST.get('kyc_id')
        cust_id = request.POST.get('cust_id')
        accountname = request.POST.get('accountname')
        accountno=request.POST.get('accountno')
        IFSCno = request.POST.get('IFSCno')
        Pancardno = request.POST.get('Pancardno')
        # print(Pancardno)
        kyc = Kyc.objects.get(id=kyc_id)
        kyc.cust_id = cust_id
        kyc.accountname = accountname
        kyc.accountno = accountno
        kyc.IFSCno = IFSCno
        kyc.Pancardno = Pancardno
        
        # kyc = Kyc(cust_id=cust_id, accountname=accountname,accountno=accountno,IFSCno=IFSCno, Pancardno=Pancardno)
        kyc.save()
        messages.success(request,"KYC Updated Successfully")  
        return redirect('approvedkyc')
    return render(request,'edit_kyc')


def DELETE_KYC(request,id):

    kyc = Kyc.objects.get(id=id)
    
    # customer = CustomUser.objects.get(id=admin)
    
    kyc.delete()
    messages.success(request,"Record are Successfully Deleted")
    return redirect('approvedkyc')


def KYC_export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    # response['Content-Disposition'] = 'attachment; filename="Approve Po.csv"'
    response['Content-Disposition'] = 'attachment; filename= ALL KYC DETAILS' + str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Customer ID', 'Account Name', "Account No", 'IFSC Code','Pan Card No'])
    kyc = Kyc.objects.all()
    for approve in kyc:
        print(approve)
    
        writer.writerow(
                    [approve.cust_id, 
				approve.accountname, 
				approve.accountno, 
				approve.IFSCno,
                approve.Pancardno])
           

    return response



    
def  pendingkyc(request):
    return render(request, 'HOD/pendingkyc.html')
def  rejectedkyc(request):
    return render(request, 'HOD/rejectedkyc.html')
    
def  memberlist(request):
    all_user = SuperAgent.objects.all()
    # firstname = all_user.username
    # print(firstname)
    context = {
        'all_user':all_user
    }
    return render(request, 'HOD/memberlist.html',context)


def memberlistEdit(request,staff_id):
    staff = SuperAgent.objects.get(admin=staff_id)
    
    
    return render(request, 'HOD/member_edit.html',{'staff':staff,"id":staff_id})





def UPDATE_MEMBER(request):
    '''
    UPDATE_CUSTOMER1 function comes in role after customer_edit1 function and saves all the detail of AGENT/customer_edit1.html page in Customer table.
    This function is used for updating customer's common details.
    '''

    if request.method == "POST":

        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("lname")
        email=request.POST.get("email")
        username=request.POST.get("username")
        rank=request.POST.get("percentage")
        reference_id=request.POST.get("reference_id")
        change_psw=request.POST.get("change_psw")
        mobile_no=request.POST.get("mob")

       
        customuser = CustomUser.objects.get(id=staff_id)

        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.email = email
        customuser.username=username
        customuser.rank=rank
        #   customuser.password = password
        
        if change_psw != None and change_psw !="":
            customuser.set_password(change_psw)
        
       
        customuser.save()

        staff_model=SuperAgent.objects.get(admin=staff_id)
        staff_model.reference_id = reference_id
        staff_model.mobile_no = mobile_no
        if change_psw != None and change_psw !="":
            staff_model.password = change_psw
        
        staff_model.save()
        messages.success(request, "Your Profile Updated Successfully !!")
        return HttpResponseRedirect(reverse("memberlist"))
        # redirect('/')
        
       
        
        
        
    return render(request,"HOD/memberlist.html")



def DELETE_MEMBER(request,id):
    
    # agent = SuperAgent.objects.get(admin=id)
    agent = CustomUser.objects.get(id=id)
    agent.delete()
    messages.success(request,"Record are Successfully Deleted")
    return redirect('memberlist')

def memberList_export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    # response['Content-Disposition'] = 'attachment; filename="Approve Po.csv"'
    response['Content-Disposition'] = 'attachment; filename= memberlist'+ str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['User Id', 'User Name', 'Mobile No', 'Email', 'Sponsor ID', 'Rank'])
    member_list = SuperAgent.objects.all()
    for approve in member_list:
        print(approve)
        writer.writerow(
            [approve.admin.user_id,
            approve.admin.username,
            '',         
            approve.admin.email,
            approve.reference_id,
            approve.admin.rank],
        )
    
        # writer.writerow(
        #             [approve.name, 
		# 		approve.father_name, 
		# 		approve.plot_number, 
		# 		approve.Payable_amout, 
		# 		approve.payment_mode, 
		# 		approve.mobile_no, 
		# 		approve.ref_id, 
		# 		approve.joinig_date, 
		# 		approve.remarks])
           

    return response


def  payplotinstallment(request):
    booking_data = Installment.objects.all()
   

    context = {
        'booking_data': booking_data,
        
        
        # 'code' : code

    }
    # approval = BookPlot.objects.all()#.order_by('uname')
    # return render(request,'show.html',)
    

    # return render(request, 'HOD/approvedplote.html', context)

    return render(request, 'HOD/payplotinstallment.html',context)
def  updateplotinstallment(request):
    return render(request, 'HOD/updateplotinstallment.html')
def  updatebookingdate(request):
    return render(request, 'HOD/updatebookingdate.html')
def  deleteplotinstallment(request):
    return render(request, 'HOD/deleteplotinstallment.html')
def  updateplotrate(request):
    return render(request, 'HOD/updateplotrate.html')
def  blockassociate(request):
    return render(request, 'HOD/blockassociate.html')
def  blockassociatelist(request):
    return render(request, 'HOD/blockassociatelist.html')
def  tokenslip(request):
    return render(request, 'HOD/tokenslip.html')
def  pendingPlot(request):
    return render(request, 'HOD/pendingplot.html')
def  updatekyc(request):
    return render(request, 'HOD/updatekyc.html')


def  ADDInstallment(request):
    
    # selected_customer_id = None
    # selected_plot_no = None
    # customer_Id = Customer.objects.all()
    # plot_no = Installment.objects.all()
    current_user = request.user
    code = current_user.user_id
    
    rank = current_user.rank
   
    # plot_number = AddPlot.objects.all()

    if request.method =="POST":
        if 'newsletter_sub' in request.POST:
            searched = request.POST['searched']
            venues = BookPlot.objects.filter(plot_number__contains=searched)
            return render(request, 'HOD/add_installment.html',{'searched':searched,'venues':venues})
        

        # else:
        #     return render(request, 'add_installment.html',{})
        
            # selected_customer_id = request.POST.get("user_id")
            # customer_Id = customer_Id.filter(customer_id=selected_customer_id)

            # selected_plot_no = request.POST.get("plot_no")
            # plot_no = plot_no.filter(plot_number=selected_plot_no)
            # return render(request, 'HOD/bookplot.html',context)
            

        
        if 'demo' in request.POST:

        
            ref_id = request.POST.get('ref_id')
        
            user_id = request.POST.get('user_id')
        
            plot_number = request.POST.get('plot_number')
            amount = request.POST.get('amount')
            # booking_amount = int(request.POST.get('booking_amount'))
            remaining_amount = int(request.POST.get('remaining_amt'))
            payment_amt = int(request.POST.get('payment_amount'))
            remaining_amount = remaining_amount-payment_amt
            rem = remaining_amount
            # print("ddddddddddddddddddddddddd",remaining_amount)
            no_Installment = request.POST.get('no_Installment')
            name = request.POST.get('name')
           
            mobile_number = request.POST.get('mobile_number')
            payment_mode = request.POST.get('payment_mode')
            remarks = request.POST.get('remarks')
            receipt = request.FILES.get('receipt')
            plot_size = request.POST.get('plot_size')
            mail = request.POST.get('mail')
            addresss = request.POST.get('addresss')
            # print(ref_id)
            if rem>=0:
                isntallment = Installment(plot_size=plot_size,mail=mail,addresss=addresss,ref_id= ref_id,user_id=user_id,plot_number = plot_number, Payable_amout = amount,remaining_amount=remaining_amount,payment_amount = payment_amt, name = name, mobile_no = mobile_number, payment_mode = payment_mode ,remarks=remarks,receipt=receipt )
                    
                owner=isntallment.owner=request.user
                # print("heloooooo",owner)
                isntallment.owner = owner          
                isntallment.save()
                messages.success(request,"Installment Add Successfully")
                return redirect('add_installment')
               
               
                
            else:
                messages.warning(request, "No more Remaining Amount")
                return redirect('add_installment')
                


           
           
        else:
            return render(request, 'HOD/add_installment.html',{})
    # cus_id = Customer.objects.order_by('customer_id').values_list('customer_id', flat=True)
    # plot_num = Installment.objects.order_by('plot_number').values_list('plot_number', flat=True)
        

    context = {
    'code':code,
    'rank':rank,
    # 'plot_number':plot_number,
    # 'cus_id':cus_id,
    # 'customer_Id':customer_Id,
    # 'selected_customer_id':selected_customer_id,

    # 'plot_num':plot_num,
    # 'plot_no':plot_no,
    # 'selected_plot_no':selected_plot_no
    
    # 'customer_id':customer_Id,
    

    }
    

    return render(request, 'HOD/add_installment.html',context)

def VIEWInstallment(request):
    isntallment = Installment.objects.all()
   
    approve = BookPlot.objects.all()
   
    return render(request,'HOD/view_installment.html',{'installment':isntallment,'approve':approve})

def Sec_Installment(request):

    selected_customer_id = None
    selected_plot_no = None
    customer_Id = Customer.objects.all()
    plot_no = Installment.objects.all()
    current_user = request.user
    code = current_user.user_id
    
    rank = current_user.rank
   
    plot_number = AddPlot.objects.all()

    if request.method =="POST":
        if 'newsletter_sub' in request.POST:
        
            selected_customer_id = request.POST.get("user_id")
            customer_Id = customer_Id.filter(customer_id=selected_customer_id)

            selected_plot_no = request.POST.get("plot_number")
            plot_no = plot_no.filter(plot_number=selected_plot_no)
            # return render(request, 'HOD/bookplot.html',context)
            

        
        if 'demo' in request.POST:

        
            ref_id = request.POST.get('ref_id')
        
            user_id = request.POST.get('user_id')
        
            plot_number = request.POST.get('plot_number')
            amount = request.POST.get('amount')
            # booking_amount = int(request.POST.get('booking_amount'))
            remaining_amount = int(request.POST.get('remaining_amt'))
            payment_amt = int(request.POST.get('payment_amount'))
            remaining_amount = remaining_amount-payment_amt
            # print("ddddddddddddddddddddddddd",remaining_amount)
            no_Installment = request.POST.get('no_Installment')
            name = request.POST.get('name')
           
            mobile_number = request.POST.get('mobile_number')
            payment_mode = request.POST.get('payment_mode')
            remarks = request.POST.get('remarks')
            receipt = request.FILES.get('receipt')
            # print(ref_id)

            isntallment = Installment(ref_id= ref_id,user_id=user_id,plot_number = plot_number, Payable_amout = amount,remaining_amount=remaining_amount,payment_amount = payment_amt, name = name, mobile_no = mobile_number, payment_mode = payment_mode ,remarks=remarks,receipt=receipt )
            owner=isntallment.owner=request.user
            # print("heloooooo",owner)
            isntallment.owner = owner
            

            
            isntallment.save()
            messages.success(request,"Booking Plot Successfully")
            return redirect('add_installment')
    cus_id = Customer.objects.order_by('customer_id').values_list('customer_id', flat=True)
    plot_num = BookPlot.objects.order_by('plot_number').values_list('plot_number', flat=True)
        

    context = {
    'code':code,
    'rank':rank,
    'plot_number':plot_number,
    'cus_id':cus_id,
    'customer_Id':customer_Id,
    'selected_customer_id':selected_customer_id,

    'plot_num':plot_num,
    'plot_no':plot_no,
    'selected_plot_no':selected_plot_no
    
    # 'customer_id':customer_Id,
    

    }
    

    return render(request,'HOD/sec_installment.html',context)
def VIEWInstallment(request):
    isntallment = Installment.objects.all()
    approve = BookPlot.objects.all()
    
    return render(request,'HOD/view_installment.html',{'installment':isntallment,'approve':approve})    

def  installmentdetail(request):
    # Installment_data = BookPlot.objects.all()
    # context = {
    #     'Installment' : Installment_data
    # }
    return render(request, 'HOD\installmentdetail.html')
def  supportsystem(request):
    return render(request, 'HOD/supportsystem.html')
# def  userdashboard(request):
#     return render(request, 'HOD/installmentdetail.html')    



def installment_export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    # response['Content-Disposition'] = 'attachment; filename="Approve Po.csv"'
    response['Content-Disposition'] = 'attachment; filename= Installment Details'+ str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Customer Name','Customer ID', 'Mobile No','Plot No', 'Plot Rate','Payment Amount' "Remaining Amount",'Payment Mode','Remarks','Date','Ref Id' ])
    installment = Installment.objects.all()
    for approve in installment:
        print(approve)
    
        writer.writerow(
                    [approve.name, 
				approve.user_id, 
				approve.mobile_no, 
				approve.plot_number, 
				approve.Payable_amout, 
				approve.remaining_amount, 
				approve.payment_amount, 
				approve.remarks, 
				approve.joinig_date, 
				approve.ref_id])
           

    return response
def fund_export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    # response['Content-Disposition'] = 'attachment; filename="Approve Po.csv"'
    response['Content-Disposition'] = 'attachment; filename= Fund Details'+ str(datetime.datetime.now())+'.csv'
    member_list = FundDetails.objects.all()
    writer = csv.writer(response)
    writer.writerow(['User Id', 'Ref ID', 'User Name', 'Amount'])
    
    for approve in member_list:
        print(approve)
    
        writer.writerow(
                    [approve.user_id, 
				approve.ref_id, 
				approve.user_name, 
				# approve.amount, 
				# approve.Payable_amout, 
				# approve.payment_amount, 
				# approve.remaining_amount, 
				# approve.payment_mode, 
				# approve.remarks,
                # approve.joinig_date, 
                approve.amount])
           

    return response


def TOKEN(request):

    booking_data = BookPlot.objects.all()
   

    context = {
        'booking_data': booking_data,
        
        
        # 'code' : code

    }
    return render(request,'HOD/token.html',context)

def TOKEN_APPROVE(request,id):
    approve = BookPlot.objects.get(id=id)
    approve.status = 1
    ins = Installment.objects.filter(id=id)
    ins.status = 1
    for object in ins:
        object.save()
    # ins.save()
    approve.save()
    # bookplot = BookPlot.objects.filter(id=id)
    # print("eeeeeeeeeeeeeeeeeeeeeeee",bookplot)
    # ins = Installment.objects.filter(id=id)
    # print("insssssssssssssss",ins)
    # ins.status = 1
    # ins.save()
    
    # ins.status = 1  
    # ins.save()
    return redirect('token')
    


def TOKEN_DISAPPROVE(request,id):
    reject = BookPlot.objects.get(id=id)
    reject.status = 2
    reject.save()
    return redirect('token')
    

def TOKEN_DELETE(request,id):
    plot = BookPlot.objects.get(id=id)
    plot.delete()
    messages.success(request,"Record are Successfully Deleted")
    return redirect('token')