from rest_framework import serializers
from .models import Passengers,LiveConductorDetails,TicketTransactionsUser,BusStations


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passengers
        fields = ('name', 'email', 'phone_number', 'password','otpcode','status')


class LiveConductorDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LiveConductorDetails
        fields = ('username', 'busname', 'busnumber')


class TicketTransactionsUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketTransactionsUser
        fields = ('passen_email','cusername','busname', 'busnumber','qty','sourcestation','deststation','totalfare','qrcode','datetime','tripno')

class BusStationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusStations
        fields = "__all__"