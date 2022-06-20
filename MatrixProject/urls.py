
from email.mime import base
from django.contrib import admin
from django.db import router
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from matrixapp import views
from matrixapp import API_Views
from .import views , HOD_Views,SuperAgent_Views
router = DefaultRouter()
router.register('Customer', API_Views.CustomerViewSet,basename="Customer")
router.register('Plot', API_Views.PlotViewSet,basename="Plot")
router.register('BookPlot', API_Views.BookPlotViewSet,basename="BookPlot")
router.register('Kyc', API_Views.KYCViewSet,basename="Kyc")
# router.register('HOD', API_Views.HODViewSet,basename="HOD")
router.register('User', API_Views.CustomUserViewSet,basename="User")
router.register('Agent', API_Views.AgentViewSet,basename="Agent")
# router.register('Login', API_Views.LoginViewSet.as_view(),basename="Login")
router.register('Installment', API_Views.InstallmentViewSet,basename="Installment")
router.register('fundTransfer', API_Views.FundDetailViewSet,basename="fundTransfer")
# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns



def trigger_error(request):
    division_by_zero = 1 / 0



urlpatterns = [
    
    # path('api/',API_View.Plot_list),
    # path('api/BookPlotList/',API_View.BookPlotList),
    # path('api/KYCList/',API_View.KYCList),
    # path('api-auth/', include('rest_framework.urls')),
    # path('sentry-debug/', trigger_error),

    
    path('admin/', admin.site.urls),
    
    path('api/Login/',API_Views.LoginViewSet.as_view()),
    path('api/',include(router.urls)),
    path('base', views.BASE, name='base') ,
    path('base1', views.BASE1, name='base1') ,
   
    #Login Path

    # path('', views.LOGIN, name='login') ,
    path('pagelogin', views.pagelogin, name='login') ,
    path('', views.home, name='home') ,
    path('about', views.about, name='about') ,
    path('contact', views.contact, name='contact') ,
    path('basee', views.basee, name='basee') ,

    path('doLogin', views.doLogin, name='doLogin'),
    path('doCustomerLogin', views.doCustomerLogin, name='doCustomerLogin'),
    path('Logout', views.doLogout,name="logout"),

    #profile update 

    path('profile/', views.profile,name="profile"),
    path('profile/update', views.Profile_Update,name="profile_update"),
    path('registeruser/', views.registeruser,name="registeruser"),
    path('registeruserr/', views.registeruserr,name="registeruserr"),
    path('do_superAgent_signup',views.dosuperAgent,name="do_superAgent_signup"),
    path('do_Agent_signup',views.doAgent,name="do_Agent_signup"),


    ################################## ADDING USER ######################
    
    path('HOD/add_user/',HOD_Views.ADD_USER,name="add_user"),
    path('HOD/customer_view/',HOD_Views.CUSTOMER_VIEW,name="customer_view"),
    path('HOD/customer_view/export_csv/',HOD_Views.customer_export_csv,name="customer_export-csv"),
    path('HOD/customer/Edit/<str:id>', HOD_Views.EDIT_CUSTOMER,name="edit_customer"),
    path('HOD/customer/Update/', HOD_Views.UPDATE_CUSTOMER,name="update_customer"),
    path('HOD/customer/Delete/<str:id>',HOD_Views.DELETE_CUSTOMER,name="delete_customer"),
    
    
    path('HOD/phase/',HOD_Views.PHASE,name="phase"),
    path('HOD/phase_view/',HOD_Views.PHASE_VIEW,name="phase_view"),
    path('HOD/phase/Edit/<str:id>', HOD_Views.EDIT_PHASE,name="edit_phase"),
    path('HOD/phase/Update/', HOD_Views.UPDATE_PHASE,name="update_phase"),
    path('HOD/phase/Delete/<str:id>',HOD_Views.DELETE_PHASE,name="delete_phase"),

    path('HOD/approvedplot/Print/<str:id>',HOD_Views.Print,name="Print"),
    path('HOD/approvedplot/Print Aggrement/<str:id>',HOD_Views.Print0,name="Print0"),

    path('HOD/view_installment/Print/<str:id>',HOD_Views.Print1,name="Print1"),
    path('Agent/approvedplot/Print/<str:id>',HOD_Views.Print,name="Print2"),
    path('Agent/view_installment1/Print/<str:id>',HOD_Views.Print1,name="Print3"),

    # path('HOD/add_user',HodViews.ADD_USER,name="add_user")

    
    # path('approvedplote/', views.approvedplote,name="approvedplote"),
    # path('edit_approvedplote/<str:staff_id>', HodViews.edit_staff,name="edit_staff"),
    # path('editApprovePlote/<int:id>/', views.editApprovePlote.as_view(), name='editApprovePlote'),

    path('cancelledplote/',HOD_Views.cancelledplote,name="cancelledplote"),
    path('bookingdetails/', HOD_Views.bookingdetails,name="bookingdetails"),
    
    path('agrrement/', HOD_Views.agrrement,name="agrrement"),
    path('fundtransfer/', HOD_Views.fundtransfer,name="fundtransfer"),
    path('viewfunds/<str:id>', HOD_Views.viewfunds,name="viewfunds"),
    path('previewfunds/', HOD_Views.previewfunds,name="previewfunds"),
    path('previewfunds1/', HOD_Views.previewfunds1,name="previewfunds1"),
    path('viewfunds1/<str:id>', HOD_Views.viewfunds1,name="viewfunds1"),



    
    path('kyc/', HOD_Views.kyc,name="kyc"),
    path('approvedkyc/', HOD_Views.approvedkyc,name="approvedkyc"),
    path('approvedkyc/export_csv/',HOD_Views.KYC_export_csv,name="kyc_export-csv"),
    path('HOD/kyc/Edit/<str:id>', HOD_Views.EDIT_KYC,name="edit_kyc"),
    path('HOD/kyc/Update/', HOD_Views.UPDATE_KYC,name="update_kyc"),
    path('HOD/kyc/Delete/<str:id>',HOD_Views.DELETE_KYC,name="delete_kyc"),
     

    
    path('pendingkyc/', HOD_Views.pendingkyc,name="pendingkyc"),
    path('rejectedkyc/', HOD_Views.rejectedkyc,name="rejectedkyc"),
    path('memberlist/', HOD_Views.memberlist,name="memberlist"),
    path('HOD/memberlist/Edit/<str:staff_id>', HOD_Views.memberlistEdit,name="memberlistEdit"),
    path('HOD/member/Update/', HOD_Views.UPDATE_MEMBER,name="update_member"),
    path('HOD/member/Delete/<str:id>', HOD_Views.DELETE_MEMBER,name="delete_member"),
    path('memberlist/export_csv/',HOD_Views.memberList_export_csv,name="memberlist_export-csv"),
    
    path('payplotinstallment/', HOD_Views.payplotinstallment,name="payplotinstallment"),
    path('updateplotinstallment/', HOD_Views.updateplotinstallment,name="updateplotinstallment"),
    path('updatebookingdate/', HOD_Views.updatebookingdate,name="updatebookingdate"),
    
    path('deleteplotinstallment/', HOD_Views.deleteplotinstallment,name="deleteplotinstallment"),
    path('updateplotrate/', HOD_Views.updateplotrate,name="updateplotrate"),
    
    path('blockassociate/', HOD_Views.blockassociate,name="blockassociate"),
    
    path('blockassociatelist/', views.blockassociatelist,name="blockassociatelist"),
    path('tokenslip/', views.tokenslip,name="tokenslip"),
    path('pendingPlot/', views.pendingPlot,name="pendingPlot"),
    path('updatekyc/', views.updatekyc,name="updatekyc"),
    path('installmentdetail/', views.installmentdetail,name="installmentdetail"),
    path('supportsystem/', views.supportsystem,name="supportsystem"),

    # Plot Path 

    
    path('addplot/', HOD_Views.addplot,name="addplot"),
    path('plotno/View-plotno', HOD_Views.VIEWPlotNo,name="view_plotno"),
    path('HOD/View-plotno/export_csv/',HOD_Views.PLOTDETAILS_export_csv,name="plot_export-csv"),
    path('plotno/Edit<str:id>', HOD_Views.EDIT_PlotNo,name="edit_plotno"),
    path('plotno/UPDATE', HOD_Views.UPDATE_PlotNo,name="update_plotno"),
    path('plotno/DELETE<str:id>', HOD_Views.DELETE_PlotNo,name="delete_plotno"),
   
     
    
   
    path('HOD/approvedplote/', HOD_Views.approvedplote,name="approvedplote"),
    path('HOD/bookplot/', HOD_Views.bookplot,name="bookplot"),
    path('HOD/bookplot/Edit/<str:id>', HOD_Views.EDIT_BOOKPLOT,name="edit_bookplot"),
    path('HOD/bookplot/Update/', HOD_Views.UPDATE_BOOKPLOT,name="update_bookplot"),
    path('HOD/bookplot/Delete/<str:id>',HOD_Views.DELETE_PLOT,name="delete_plot"),
    path('HOD/searchbar/',HOD_Views.SEARCH_BAR,name="searchbar"),
   

    path('export_csv/', views.export_csv,name="export-csv"),
    path('pendingPlot/', views.pendingPlot,name="pendingPlot"),
    

    # Hod Panel 
    path('signup_admin/',views.signup_admin,name="signup_admin"),
    path('do_admin_signup',views.do_admin_signup,name="do_admin_signup"),
    path('HOD/Home', HOD_Views.HOME, name='admin_home'),
    path('HOD/Token', HOD_Views.TOKEN, name='token'),
    path('HOD/Token/approve/<str:id>', HOD_Views.TOKEN_APPROVE, name='token_approve'),
    path('HOD/Token/disapprove/<str:id>', HOD_Views.TOKEN_DISAPPROVE, name='token_disapprove'),
    path('HOD/Delete/Token/<str:id>', HOD_Views.TOKEN_DELETE, name='token_delete'),


    
    # path("signup/", views.signup_view,name="signup-view"),
    

    ############## hod Installment ######################

    path('HOD/add_installment', HOD_Views.ADDInstallment, name='add_installment'),
    # path('HOD/Sec_installment', HOD_Views.Sec_Installment, name='Sec_Installment'),
    path('HOD/View_installment', HOD_Views.VIEWInstallment, name='view_installment'),
    path('HOD/View_installment/export_csv/', HOD_Views.installment_export_csv, name='installment_export_csv'),
    path('HOD/previewfunds1/export_csv/', HOD_Views.fund_export_csv, name='fund_export_csv'),


     ########################## define for user url ############################

    path('Agent/Home', SuperAgent_Views.Home, name='Agent_Home') ,
    path('Agent/add_user/',SuperAgent_Views.AgentADD_USER,name="agentadd_user"),
    path('Agent/customer_view1/',SuperAgent_Views.customer_view1,name="customer_view1"),
    path('Agent/customer_view1/export_csv/',SuperAgent_Views.customer_export_csv1,name="customer_export-csv1"),
    path('Agent/customer_view1/approvedplot/',SuperAgent_Views.approved_export_csv1,name="approved_export-csv1"),
    path('Agent/View_installment1/approvedplot/',SuperAgent_Views.View_installment1_export_csv1,name="View_installment1_export-csv1"),
    path('AGENT/customer/Edit/<str:id>', SuperAgent_Views.customer_edit1,name="customer_edit1"),
    path('Agent/customer/Update/', SuperAgent_Views.UPDATE_CUSTOMER1,name="update_customer1"),
    path('Agent/customer/Delete/<str:id>',SuperAgent_Views.DELETE_CUSTOMER1,name="delete_customer1"),
    path('Agent/Agent_bookplot', SuperAgent_Views.Agent_bookplot, name='Agent_bookplot') ,
    path('Agent/installment_detail', SuperAgent_Views.installment_detail, name='installment_detail') ,
    path('Agent/update_account', SuperAgent_Views.update_account, name='update_account') ,
    path('Agent/editagentdata', SuperAgent_Views.editagentdata, name='editagentdata') ,
    path('Agent/update_password', SuperAgent_Views.update_password, name='update_password') ,
    path('Agent/update_bank_details', SuperAgent_Views.update_bank_details, name='update_bank_details') ,
    path('Agent/wallet_history', SuperAgent_Views.wallet_history, name='wallet_history') ,
    path('Agent/wallet_history/export_csv?', SuperAgent_Views.wallet_history_export_csv1, name='wallet_history_export_csv1') ,
    path('Agent/income_details', SuperAgent_Views.income_details, name='income_details') ,
    path('Agent/level_income', SuperAgent_Views.level_income, name='level_income') ,
    path('Agent/get_in_touch', SuperAgent_Views.get_in_touch, name='get_in_touch') ,
    path('Agent/agent_profile', SuperAgent_Views.agent_profile, name='agent_profile') ,
    path('Agent/approvedplot', SuperAgent_Views.agent_approvedplot, name='agent_approvedplot') ,
    path('Agent/approvedplot/Edit/<str:id>', SuperAgent_Views.edit_bookplot1,name="edit_bookplot1"),
    path('Agent/approvedplot/Update/', SuperAgent_Views.update_bookplot1,name="update_bookplot1"),
    path('Agent/approvedplot/Delete/<str:id>',SuperAgent_Views.delete_plot1,name="delete_plot1"),
    path('plotno/View-plotno1', SuperAgent_Views.VIEWPlotNo1,name="view_plotno1"),
    path('memberlist1/', SuperAgent_Views.memberlist1,name="memberlist1"),

    
    path('Agent/add_installment1', SuperAgent_Views.ADDInstallment1, name='add_installment1'),
    # path('HOD/Sec_installment', HOD_Views.Sec_Installment, name='Sec_Installment'),
    path('Agent/View_installment1', SuperAgent_Views.VIEWInstallment1, name='view_installment1'),
    
    
    path('Agent/memberlist', SuperAgent_Views.VIEW_MEMBERLIST, name='view_agentmemberlist'),




    ################ customer #########################
    path('customer/',views.customer,name="customer")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)



if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
         path('__debug__/', include('debug_toolbar.urls')),

    ]+urlpatterns

# urlpatterns += staticfiles_urlpatterns()
   