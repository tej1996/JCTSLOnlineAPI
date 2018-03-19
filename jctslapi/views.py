from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.views.generic import View
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import Passengers,BusConductor,LiveConductorDetails,BusRoute,RouteSequence,LiveBusDetails,TicketTransactionsCond,BusStations,TicketTransactionsUser,AdminUser
from .serializers import PassengerSerializer,LiveConductorDetailsSerializer,TicketTransactionsUserSerializer
from math import sin, cos, sqrt, atan2, radians
from django.db.models import Sum
import requests,json

# Create your views here.

class CreateUser(APIView):

    def post(self, request):
        serializer = PassengerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            num = request.POST['otpcode']
            send_mail("hello!  "+request.POST['name'], "Your verification code is : "+num, "laveshk3@gmail.com", [request.POST['email']])
            return Response({'flag':"true"})
        return Response({'flag':"false"})


class CheckIfAlready(APIView):

    def post(self, request):
        try:
            email = Passengers.objects.get(email=request.POST['email'])
        except Passengers.DoesNotExist:
            email = None
        try:
            phone = Passengers.objects.get(phone_number=request.POST['phone_number'])
        except Passengers.DoesNotExist:
            phone = None

        if email is None and phone is None:
            content = {'flag': "true"}
            return Response(content)
        else:
            content = {'flag': "false"}
            return Response(content)


class CheckLogin(APIView):

    def post(self, request):
        try:
            user = Passengers.objects.get(email=request.POST['email'])
            try:
                user = Passengers.objects.get(email=request.POST['email'],password= request.POST['password'])
                if user.status == "true":
                    return Response({'status':"success"})
                else:
                    return Response({'status':"verify"})
            except:
                return Response({'status': "You have entered wrong password"})
        except Passengers.DoesNotExist:
            return Response({'status':"You are not registered"})

class CheckOTP(APIView):

    def post(self,request):
        otp = request.POST['otpcode']
        email = request.POST['email']
        try:
            object = Passengers.objects.get(email=email,otpcode=otp)
            return Response({'flag':"true"})
        except Passengers.DoesNotExist:
            return Response({'flag':"false"})


class UpdateStatus(APIView):

    def post(self, request):
        email = request.POST['email']
        object = Passengers.objects.get(email=email)
        serializer = PassengerSerializer(object, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'flag':"success"})
        return Response({'flag':"failed"})


class SendForgotOtp(APIView):

    def post(self, request):
        email = request.POST['email']
        num = request.POST['otpcode']
        try:
            object = Passengers.objects.get(email=email)
            send_mail("hello"+request.POST['email'], "your verification code is"+num, "laveshk3@gmail.com", [request.POST['email']])
            return Response({'status':"otpsent"})
        except Passengers.DoesNotExist:
            return Response({'status':"You are not registered with us."})


class UpdatePassword(APIView):

    def post(self, request):
        email = request.POST['email']
        object = Passengers.objects.get(email=email)
        serializer = PassengerSerializer(object, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'flag':"sucess"})
        return Response({'flag':"failed"})

#ConductorDept
class CheckLoginConductor(APIView):

    def post(self, request):
        try:
            user = BusConductor.objects.get(username=request.POST['username'])
            try:
                user = BusConductor.objects.get(username=request.POST['username'],password= request.POST['password'])
                return Response({'status':"success"})
            except:
                return Response({'status': "You have entered wrong password"})
        except BusConductor.DoesNotExist:
            return Response({'status':"You are not registered"})


class AddConductorDetails(APIView):

    def post(self, request):
        try:
            user = BusConductor.objects.get(username=request.POST['username'])
            try:
                username = LiveConductorDetails.objects.get(username=request.POST['username'])
                username.delete()
            finally:
                try:
                    bus = BusRoute.objects.get(busname=request.POST['busname'])
                    serializer = LiveConductorDetailsSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'status':"conductordetailsadded",'wallet':user.wallet})
                except:
                    return Response({'status':"busnotfound"})
        except BusConductor.DoesNotExist:
            return Response({'status':"You are not registered"})


class BusRouteFetch(APIView):

    def post(self, request):
        bus = BusRoute.objects.get(busname=request.POST['busname'])
        rid = bus.route_id
        routestations = RouteSequence.objects.filter(route_id=rid).order_by("sequence")
        content = {}
        for stations in routestations:
            squery = BusStations.objects.get(id=stations.station_id)
            sname = squery.stationname
            content.update({str(stations.sequence):str(sname)})
        return Response(content)


class LiveBusDetailAdd(APIView):

    def post(self, request):
        try:
            livebus = LiveBusDetails.objects.get(cusername=request.POST['cusername'])
            if request.POST['whichway']!=livebus.whichway:
                livebus.tripno = livebus.tripno + 1
            livebus.currstation = request.POST['currstation']
            livebus.whichway = request.POST['whichway']
            livebus.save()
        except LiveBusDetails.DoesNotExist:
            livebus = LiveBusDetails()
            livebus.cusername = request.POST['cusername']
            livebus.busname = request.POST['busname']
            livebus.busnumber = request.POST['busnumber']
            livebus.currstation = request.POST['currstation']
            livebus.whichway = request.POST['whichway']
            livebus.tripno = 1
            livebus.save()

        try:
            trans = TicketTransactionsCond.objects.filter(busnumber=livebus.busnumber,status="active")
            for tr in trans:
                if tr.deststation==livebus.currstation:
                    tr.status="expired"
                    tr.save()
            transuser = TicketTransactionsUser.objects.filter(busnumber=livebus.busnumber,status="active")
            for trs in transuser:
                if trs.deststation==livebus.currstation:
                    trs.status="expired"
                    trs.qrcode=""
                    trs.generate_qrcode_update()
                    trs.save()
        except:
            pass


        return Response({'status':"updatedlivebusdetails"})



class BookTicketConductor(APIView):

    def post(self, request):
        transaction = TicketTransactionsCond()
        transaction.cusername = request.POST['cusername']
        transaction.busname = request.POST['busname']
        transaction.busnumber = request.POST['busnumber']
        transaction.qty = request.POST['qty']
        livebus = LiveBusDetails.objects.get(cusername=request.POST['cusername'])
        transaction.sourcestation = livebus.currstation
        transaction.deststation = request.POST['deststation']
        transaction.totalfare = 10
        transaction.datetime = request.POST['datetime']
        busconductor = BusConductor.objects.get(username=transaction.cusername)
        busconductor.wallet = busconductor.wallet - transaction.totalfare
        transaction.save()
        busconductor.save()

        return Response({'status':"ticketbooked"})


class LogoutConductor(APIView):

    def post(self, request):
        try:
            cusername=request.POST['cusername']
            livecond = LiveConductorDetails.objects.get(username=cusername)
            livecond.delete()
            livebus = LiveBusDetails.objects.get(cusername=cusername)
            livebus.delete()
        except:
            pass
        return Response({'status':"success"})


class ListBusStations(APIView):

    def post(self, request):
        stations = BusStations.objects.all()
        content = {}
        i=0
        for stn in stations:
            content.update({str(i):stations.stationname})
            i=i+1
        return Response(content)

class ListBusStationsLocations(APIView):

    def post(self, request):
        busname = BusRoute.objects.get(busname=request.POST['busname'])
        stationid= RouteSequence.objects.get(route_id=busname.route_id)
        stations = BusStations.objects.filter(id=stationid)
        stationslist=[]
        for station in stations:
            dict = {'stationname': station.stationname, 'latitude': station.latitude, 'longitude': station.longitude}
            stationslist.append(dict)
        return Response(stationslist)

class SearchByLocation(APIView):

    def post(self, request):
        userlati = request.POST['latitude']
        userlongi = request.POST['longitude']
        userlati = radians(float(userlati))
        userlongi = radians(float(userlongi))

        srcstation = BusStations.objects.all()
        mindist = 9999999
        for st in srcstation:
            lati = radians(float(st.latitude))
            longi = radians(float(st.longitude))
            dlon = userlongi - longi
            dlat = userlati - lati
            R = 6373.0
            a = sin(dlat / 2)**2 + cos(lati) * cos(userlati) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            if distance<mindist:
                mindist = distance
                nearestdest = st

        return Response({'stationname':nearestdest.stationname})


class CheckForBus(APIView):

    def post(self, request):
        dest = request.POST['destination']
        userlati = 26.797006
        userlongi = 75.815468
        userlati = radians(float(userlati))
        userlongi = radians(float(userlongi))
        qty = request.POST['qty']

        srcstation = BusStations.objects.all()
        mindist = 9999999
        for st in srcstation:
            lati = radians(float(st.latitude))
            longi = radians(float(st.longitude))
            dlon = userlongi - longi
            dlat = userlati - lati
            R = 6373.0
            a = sin(dlat / 2)**2 + cos(lati) * cos(userlati) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            if distance<mindist:
                mindist = distance
                nearestsource = st

        srcstationid= nearestsource.id

        deststation = BusStations.objects.get(stationname=dest)
        chkroutes = RouteSequence.objects.filter(station_id=deststation.id).order_by("route_id")
        flag = 0

        difflist=[]
        for route in chkroutes:
            try:
                src = RouteSequence.objects.get(route_id=route.route_id,station_id=srcstationid)
                dest = RouteSequence.objects.get(route_id=route.route_id,station_id=deststation.id)
                bus = BusRoute.objects.get(route_id=route.route_id)

                if dest.sequence-src.sequence>0:
                    whichway="forward"
                else:
                    whichway="reverse"
                currstationbuses = LiveBusDetails.objects.filter(busname=bus.busname,whichway=whichway)

                stns = abs(dest.sequence-src.sequence)
                for currstationbus in currstationbuses:
                        currstation = currstationbus.currstation
                        currstationid = BusStations.objects.filter(stationname=currstation)
                        currstation_seq = RouteSequence.objects.get(route_id=route.route_id,station_id=currstationid[0].id)

                        diff = abs(currstation_seq.sequence-src.sequence)
                        d={'diff':diff,'currstationbus':currstationbus}
                        difflist.append(d)
                        flag=1

            except:
                pass

        if flag == 0:
            buses=[]
            return Response(buses)
            #return Response({'status':"notfound",'msg':"There is no direct route from your location to specified destination"})
        else:

            newdifflist = sorted(difflist, key=lambda k: k['diff'])
            buses=[]
            for i in range(0,3):
                try:
                    currstationbus=newdifflist[i]['currstationbus']
                    busname = currstationbus.busname
                    busnumber = currstationbus.busnumber
                    cusername = currstationbus.cusername
                    srcstationname = nearestsource.stationname
                    deststationname = deststation.stationname
                    totalfare = int(stns)*int(qty)*10

                    crowd="empty"
                    try:
                        activeticketsuser = TicketTransactionsUser.objects.filter(busnumber=busnumber,status="active")
                        activeticketscond = TicketTransactionsCond.objects.filter(busnumber=busnumber,status="active")
                        totalactive=activeticketsuser.count()+activeticketscond.count()

                        if totalactive<=2:
                            crowd="empty"
                        else:
                            if totalactive>=2 and totalactive<=6:
                                crowd="moderate"
                            else:
                                crowd="full"
                    except:
                        pass

                    buslocation = BusStations.objects.get(stationname=currstationbus.currstation)
                    userstoplocation = BusStations.objects.get(stationname=srcstationname)
                    API_KEY = "AIzaSyBLETfXXLxISfCy_x9Gy1ZNd6ae2B1KfPQ"

                    try:
                        #req = requests.get("https://maps.googleapis.com/maps/api/directions/json?origin=26.849193,75.784385&destination=26.781059,75.819699&transit_mode=bus&key=AIzaSyBLETfXXLxISfCy_x9Gy1ZNd6ae2B1KfPQ")
                        req = requests.get("https://maps.googleapis.com/maps/api/directions/json?origin="+str(buslocation.latitude)+","+str(buslocation.longitude)+"&destination="+str(userstoplocation.latitude)+","+str(userstoplocation.longitude)+"&transit_mode=bus&key="+API_KEY)
                        resjson = json.loads(req.text)
                        arrtime = str(resjson['routes'][0]['legs'][0]['duration']['text'])

                    except:
                        pass

                    dict = {'busname': busname, 'busnumber': busnumber, 'cusername': cusername,'srcstationname':srcstationname,'deststationname':deststationname,'totalfare':totalfare,'crowd':crowd,'arrtime': arrtime}
                    buses.append(dict)

                except:
                    pass

        return Response(buses)

class BookTicketUser(APIView):

    def post(self, request):
        transaction = TicketTransactionsUser()
        transaction.passen_email = request.POST['email']
        transaction.cusername = request.POST['cusername']
        transaction.busname = request.POST['busname']
        transaction.busnumber = request.POST['busnumber']

        bus = LiveBusDetails.objects.get(cusername=request.POST['cusername'])
        transaction.tripno = bus.tripno

        transaction.qty = request.POST['qty']
        transaction.sourcestation = request.POST['srcstation']
        transaction.deststation = request.POST['deststation']
        transaction.totalfare = request.POST['totalfare']
        transaction.datetime = request.POST['datetime']
        transaction.generate_qrcode()
        transaction.save()

        return Response({'status':"ticketbooked"})


class FetchTicketTransactions(APIView):

    def post(self, request):
        email = request.POST['email']
        tickets = TicketTransactionsUser.objects.filter(passen_email=email).order_by('-datetime')
        serializer = TicketTransactionsUserSerializer(tickets, many=True)
        return Response(serializer.data)


class AdminLogin(View):
    template_name = 'jctslapi/login.html'
    def get(self, request):
        if request.session.has_key('username'):
            return redirect('admindashboard')
        else:
            return render(request,self.template_name,None)

    def post(self, request):
        username = request.POST['adminusername']
        password = request.POST['password']
        try:
            obj = AdminUser.objects.get(username=username,password=password)
            request.session['username'] = username
            return redirect('admindashboard')
        except AdminUser.DoesNotExist:
            return render(request,self.template_name, None)

class AdminDashboard(View):
    template_name = 'jctslapi/dashboard.html'
    login_template = 'jctslapi/login.html'

    def get(self, request):

        if request.session.has_key('username'):
            transactions = TicketTransactionsCond.objects.values('busname','busnumber','cusername','totalfare').annotate(fare=Sum('totalfare')).order_by('-fare')
            return render(request, self.template_name, {'transactions':transactions})
        else:
            return render(request,self.login_template,None)


class AdminLogout(View):
    template_name = 'jctslapi/login.html'

    def get(self, request):
        try:
              del request.session['username']
        except:
              pass
        return redirect("/adminlogin/")

class ListConductors(View):
    template_name = 'jctslapi/conductors.html'
    login_template = 'jctslapi/login.html'

    def get(self, request):

        if request.session.has_key('username'):
            conductors = BusConductor.objects.values('username','phone_number','wallet')
            return render(request, self.template_name, {'conductors':conductors})
        else:
            return render(request,self.login_template,None)
