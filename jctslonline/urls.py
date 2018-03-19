"""jctslonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from jctslapi.views import CreateUser,CheckIfAlready,CheckLogin,CheckOTP,UpdateStatus,SendForgotOtp,UpdatePassword,CheckLoginConductor,AddConductorDetails,BusRouteFetch,LiveBusDetailAdd,BookTicketConductor,ListBusStations,CheckForBus,BookTicketUser,FetchTicketTransactions,LogoutConductor,AdminLogin,AdminDashboard,AdminLogout,ListConductors,ListBusStationsLocations,SearchByLocation

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', CreateUser.as_view()),
    url(r'^check/', CheckIfAlready.as_view()),
    url(r'^checklogin/', CheckLogin.as_view()),
    url(r'^checkotp/', CheckOTP.as_view()),
    url(r'^updatestatus/', UpdateStatus.as_view()),
    url(r'^sendforgototp/', SendForgotOtp.as_view()),
    url(r'^updatepassword/', UpdatePassword.as_view()),
    url(r'^checkloginconductor/', CheckLoginConductor.as_view()),
    url(r'^addconductordetails/', AddConductorDetails.as_view()),
    url(r'^busroutefetch/', BusRouteFetch.as_view()),
    url(r'^livebusdetailadd/', LiveBusDetailAdd.as_view()),
    url(r'^bookticketconductor/', BookTicketConductor.as_view()),
    url(r'^listbusstation/', ListBusStations.as_view()),
    url(r'^checkforbus/', CheckForBus.as_view()),
    url(r'^bookticketuser/', BookTicketUser.as_view()),
    url(r'^fetchtickettransactions/', FetchTicketTransactions.as_view()),
    url(r'^logoutcond/', LogoutConductor.as_view()),
    url(r'^adminlogin/', AdminLogin.as_view(),name='adminlogin'),
    url(r'^admindashboard/', AdminDashboard.as_view(),name='admindashboard'),
    url(r'^adminlogout/', AdminLogout.as_view(),name='adminlogout'),
    url(r'^conductorslist/', ListConductors.as_view(),name='conductorslist'),
    url(r'^liststationlocations/', ListBusStationsLocations.as_view()),
    url(r'^searchbylocation/', SearchByLocation.as_view()),


]
