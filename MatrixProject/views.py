from asyncore import write
from multiprocessing import context
from operator import imod
from urllib import response
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from MatrixProject.SuperAgent_Views import Home
from matrixapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from matrixapp.models import CustomUser,HOD,SuperAgent,BookPlot,Customer,Installment
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import csv
import datetime

def home(request):
    return render(request,'infra/index.html')
def about(request):
    return render(request,'infra/about-us.html')
def contact(request):
    return render(request,'infra/contact.html')

def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    # response['Content-Disposition'] = 'attachment; filename="Approve Po.csv"'
    response['Content-Disposition'] = 'attachment; filename= Booking Details'+ str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Customer Id','Name', 'Father Name', 'Plot No', 'Amount', 'Payment Mode','A/c No','IFSC CODE','Check No', 'Mobile No', 'Ref Id', 'Date', 'Remarks'])
    approve_plot = BookPlot.objects.all()
    for approve in approve_plot:
        print(approve)
    
        writer.writerow(
                    [approve.user_id, 
                approve.name, 
				approve.father_name, 
				approve.plot_number, 
				approve.Payable_amout, 
				approve.payment_mode, 
				approve.account_no, 
				approve.ifsc_code, 
				approve.check_no, 
				approve.mobile_no, 
				approve.ref_id, 
				approve.joinig_date, 
				approve.remarks])
           

    return response


def BASE(request):
    return render(request, 'base.html')
def basee(request):
    return render(request, 'homepage/base.html')



def BASE1(request):
    return render(request, 'base1.html')




def pagelogin(request):
    return render(request, 'page-login.html')


def signup_admin(request):
    return render(request,"HOD/signup_admin_page.html")



def do_admin_signup(request):
    username=request.POST.get("username")
    fname=request.POST.get("fname")
    lname=request.POST.get("lname")
    email=request.POST.get("email")
    password=request.POST.get("password")
    rpt_password=request.POST.get("rpt_password")
    rank=request.POST.get("rank")
    

    if password != rpt_password:
        messages.error(request,"Password does not match")
        return redirect('signup_admin')

   
    user=CustomUser.objects.create_user(username=username,email=email,password=password,rank=rank,user_type=1)
    user.first_name = fname
    user.last_name = lname
    

        # if password != rpt_password:
        #     messages.error(request, "Password does not match Try Again " )
        #     return render('do_admin_signup')


    user.save()
    hod = HOD(
                admin = user,  
                # rank = rank                      
            )
    hod.save()
    
    
    messages.success(request,"Successfully Created Admin")
    return HttpResponseRedirect(reverse("login"))
    

@login_required
def dosuperAgent(request):
    current_user = request.user
    code = current_user.user_id
    rank = current_user.rank
  
  
    if request.method == "POST":
        username=request.POST.get("username")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        password1=request.POST.get("password1")        
        password2=request.POST.get("password2")
        Refrence_ID=request.POST.get("Refrence_ID")
        percentage=request.POST.get("percentage")
        mobile=request.POST.get("mob_no")
 
     
        # print(profile_pic,first_name,last_name,email,username,password,address,gender,course_id,session_year_id)

        # if CustomUser.objects.filter(email = email).exists():
        #     messages.warning(request, "Email is already Taken")
        #     return redirect('registeruser')

        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request, "Username is already Taken")
            return redirect('Agent_Home')
        
        else:
            user = CustomUser(
                first_name = fname,
                last_name = lname,
                username = username,
                email = email,               
                user_type = 2,
                rank = percentage,
               
                
                
            )
            if password1!=password2:

                messages.warning(request, "Password Does not match")
                return redirect('registeruser')
            
            user.set_password(password1)
            user.save()

            
            agent = SuperAgent(
                admin = user,
                # rank = rank,
                reference_id = Refrence_ID , 
                password = password1,         
                mobile_no = mobile,         
 
            )
            agent.save()
            messages.success(request, user.first_name + "  "+ user.last_name + ' Are Successfully Added !!' )
            return redirect('admin_home')
    context = {
        'code':code,
        'rank':rank
    }

    return render(request, 'register-user.html',context)
# def dosuperAgent(request):


#     # user_code = AdminHOD.objects.get(id = request.user.id)
#     # print('user_cod''''''''')
#     username=request.POST.get("username")
#     fname=request.POST.get("fname")
#     lname=request.POST.get("lname")
#     email=request.POST.get("email")
#     password1=request.POST.get("password1")
#     password2=request.POST.get("password2")

#     try:
#         user=CustomUser.objects.create_user(username, email, password1,user_type=2)
#         # user=CustomUser.objects.create_user(username=username,email=email,password=password1,user_type=2)
#         user.first_name = fname
#         user.last_name = lname
#         user.save()
#         messages.success(request,"Successfully Created Admin")
#         return HttpResponseRedirect(reverse("registeruser"))
#     except:
#         messages.error(request,"Failed to Create Admin")
#         # return HttpResponseRedirect(reverse("login"))
   
#     return(request, 'register-user.html' )


def doAgent(request):
    current_user = request.user
    code = current_user.user_id
    rank = current_user.rank
  
  
    if request.method == "POST":
        username=request.POST.get("username")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        password1=request.POST.get("password1")        
        password2=request.POST.get("password2")
        Refrence_ID=request.POST.get("Refrence_ID")
        percentage=request.POST.get("percentage")
        mobile=request.POST.get("mob_no")
        
 
     
        # print(profile_pic,first_name,last_name,email,username,password,address,gender,course_id,session_year_id)

        if CustomUser.objects.filter(email = email).exists():
            messages.warning(request, "Email is already Taken")
            return redirect('registeruserr')

        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request, "Username is already Taken")
            return redirect('registeruserr')
        
        else:
            user = CustomUser(
                first_name = fname,
                last_name = lname,
                username = username,
                email = email,               
                user_type = 2,
                rank = percentage,
                
                
            )
            if password1!=password2:

                messages.warning(request, "Password Does not match")
                return redirect('registeruserr')
            
            user.set_password(password1)
            user.save()

            
            agent = SuperAgent(
                admin = user,
                # rank = rank,
                reference_id = Refrence_ID              
 
            )
            agent.save()
            messages.success(request, user.first_name + "  "+ user.last_name + ' Are Successfully Added !!' )
            return redirect('Agent_Home')
    context = {
        'code':code,
        'rank':rank
    }

    return render(request, 'register-userr.html',context)
      



def doLogin(request):
    if request.method == "POST":
        # print(request.POST.get('email'))
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password = request.POST.get('password'))
        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_home')
                # return HttpResponseRedirect('/HOD/Home')
                # return render(request, "page-login.html")
                # return HttpResponse("This is admin panel")
                
            elif user_type == '2':
                
                return redirect('Agent_Home')
        
            elif user_type == '3':
                pass
            else:
                
                #Message
                return HttpResponse("This is Agent panel")
        else:
            messages.error(request,"Invalid Login Or Password!!")
            #Message
            
            return redirect('login')
        
    return render(request, 'page-login.html')

def doCustomerLogin(request):
    if request.method == "POST":
        # print(request.POST.get('email'))
        
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password = request.POST.get('password'))
        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '3':
                return redirect('customer')
        else:
            messages.error(request,"Invalid Login Or Password!!")
            
    return render(request, 'homepage/index.html')

def doLogout(request):
    logout(request)
    return redirect("login")



def profile(request):
    current_user = request.user
    code = current_user.user_id
    rank = current_user.rank
   
    context = {
        'code': code,
        'rank':rank,
    }
    return render(request, 'profile.html',context)

def Profile_Update(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(profile_pic)
        # print(profile_pic,first_name,last_name,email,username,password)

        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.profile_pic = profile_pic
            if password != None and password !="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Your Profile Updated Successfully !!")
            return HttpResponseRedirect(reverse("profile"))
            # redirect('/')
            
            
        except :
            messages.error(request, "Failed to Update Your Profile")
            
        
    return render(request, 'profile.html')


def pendingPlot(request):
    return render(request,'HOD/pendingPlot.html')


def registeruser(request):
    # customuser = HOD.objects.get()
    current_user = request.user
    code = current_user.user_id
    rank = current_user.rank
   
    
    
    # user_profile = HOD.objects.get()
    # # user_profile = HOD.objects.get()
    # hod_code = user_profile
    # code = hod_code.user_id
    # # user_profile = HOD.objects.get(id=request.user.id)
    # print(code)
    context = {
        'code':code,
        'rank':rank
        

    }

    return render(request,'register-user.html',context)

def registeruserr(request):
    # customuser = SuperAgent.objects.get()
    # rank=SuperAgent.objects.get()
    current_user = request.user
    code = current_user.user_id
    rank1 = current_user.rank
    
    b=(str(rank1))
    print(b)
    f=(b[-2:])
    p=int(f)
    
    def decideranklist(admin_user):

        
        if admin_user == 1:
            messages.error(request, "Further User can't be made")

        else:

            ranklist = []

            for rank in range(admin_user):

                if admin_user == 1:
                    break
                ranklist.append(admin_user - 1)
                admin_user=admin_user-1
            return ranklist

            

    c= decideranklist(p)
    print(c)

    # if c==None:
    #         pass
    # elif c!=None:
    #         d=c[0]
    #         b= int(input("Enter Rank of new user: "))
    #         if d==1:
    #             messages.error(request, "Further User can't be made")
    #         elif b in c:
    #             print("Congratulations New user rank is ", b)

            
    

    # rank1=SuperAgent.objects.filter(rank=SuperAgent.rank).values()[0]
    # print(type(rank1))  
    # p=model_to_dict(SuperAgent)
    # print(p)
    
    
    context = {
        'code':code,
        'rank':c,
       
         
        

    }
    
    return render(request,'register-userr.html',context)
# def LOGIN(request):
#     return render(request, 'login.html')


# def signup_view(request):
    # profile_id = request.session.get('ref_profile')
    # print('profile id', profile_id)
    # # print('profile_id',profile_id)
    # form = UserCreationForm(request.POST or None)

    # # form = UserCreationForm(request.Post or None)
    # if form.is_valid():
    #     if profile_id is not None:
    #         recommended_by_profile = Profile.objects.get(id=profile_id)
    #         instance = form.save()
    #         registered_user = User.objects.get(id=instance.id)
    #         registered_profile = Profile.objects.get(user=registered_user)
    #         registered_profile.recommended_by = recommended_by_profile.user
    #         registered_profile.save()
    #     else:
    #         form.save()
    #     username = form.cleaned_data.get('username')
    #     password = form.cleaned_data.get('password1')
    #     user = authenticate(username=username, password=password)
    #     login(request,user)
    #     return redirect('main-view')
    
    # context = {'form': form}
    # # context = {}
    # return render(request, 'signup.html', context)



def  cancelledplote(request):
    return render(request, 'HOD/cancelledplote.html')

def  blockassociatelist(request):
    return render(request, 'HOD/blockassociatelist.html')
def  tokenslip(request):
    return render(request, 'HOD/tokenslip.html')
def  pendingPlot(request):
    return render(request, 'HOD/pendingplot.html')
def  updatekyc(request):
    return render(request, 'HOD/updatekyc.html')

def  installmentdetail(request):
    Installment_data = BookPlot.objects.all()
    context = {
        'Installment' : Installment_data
    }
    return render(request, 'HOD\installmentdetail.html', context)
def  supportsystem(request):
    return render(request, 'HOD/supportsystem.html')
def  userdashboard(request):
    return render(request, 'HOD/installmentdetail.html')


def customer(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched2 = request.POST['searched2']
        
        venues = Installment.objects.filter(user_id__contains=searched,plot_number__contains=searched2)

        return render(request, 'customer.html',{'searched':searched,'searched2':searched2,'venues':venues})
    else:
        return render(request, 'customer.html',{})
    # return render(request,'customer.html')