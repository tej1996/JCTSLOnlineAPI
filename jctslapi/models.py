from __future__ import unicode_literals

from django.db import models
import qrcode
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your models here.
class AdminUser(models.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class Passengers(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=200)
    otpcode = models.IntegerField()
    status = models.CharField(max_length=10)
    wallet = models.FloatField(default=0.0)


class BusConductor(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    wallet = models.FloatField(default=2000.0)


class LiveConductorDetails(models.Model):
    username = models.CharField(max_length=200)
    busname = models.CharField(max_length=200)
    busnumber = models.CharField(max_length=20)


class BusRoute(models.Model):
    route_id = models.IntegerField()
    busname = models.CharField(max_length=200)
    startid = models.IntegerField()
    endid = models.IntegerField()


class BusStations(models.Model):
    def __unicode__(self):
       return 'Station: ' + self.stationname
    stationname = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()


class RouteSequence(models.Model):
    route_id = models.IntegerField()
    station_id = models.IntegerField()
    sequence = models.IntegerField()


class LiveBusDetails(models.Model):
    cusername = models.CharField(max_length=200)
    busname = models.CharField(max_length=200)
    busnumber = models.CharField(max_length=20)
    currstation = models.CharField(max_length=200)
    whichway = models.CharField(max_length=200)
    tripno = models.IntegerField()


class TicketTransactionsCond(models.Model):
    cusername = models.CharField(max_length=200)
    busname = models.CharField(max_length=200)
    busnumber = models.CharField(max_length=20)
    qty = models.IntegerField()
    sourcestation = models.CharField(max_length=200)
    deststation = models.CharField(max_length=200)
    totalfare = models.FloatField()
    datetime = models.DateTimeField(default=None, blank=True)
    status = models.CharField(max_length=20,default="active")


class TicketTransactionsUser(models.Model):
    passen_email = models.CharField(max_length=200)
    cusername = models.CharField(max_length=200)
    busname = models.CharField(max_length=200)
    busnumber = models.CharField(max_length=20)
    qty = models.IntegerField()
    sourcestation = models.CharField(max_length=200)
    deststation = models.CharField(max_length=200)
    totalfare = models.FloatField()
    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)
    datetime = models.DateTimeField(default=None, blank=True)
    tripno = models.IntegerField()
    status = models.CharField(max_length=20,default="active")

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )

        #str = "{\"busname\" : \"" + self.busname + "\" , \"busnumber\" : \"" +self.busnumber+"\" , \"tripno\" : \""+self.tripno+"\" , \"passen_email\" : \""+self.passen_email+"\" , \"cusername\" : \""+self.cusername+"\" , \"sourcestation\" : \""+self.sourcestation+"\", \"deststation\" : \""+self.deststation+"\", \"status\" : \""+self.status+"\", \"qty\" : \""+self.qty+"\" }"

        qr.add_data(self.busname+","+self.busnumber+","+str(self.tripno)+","+self.passen_email+","+self.cusername+","+self.sourcestation+","+self.deststation+","+self.qty+","+self.status)
        #qr.add_data(str)
        qr.make(fit=True)

        img = qr.make_image()

        buffer = StringIO.StringIO()
        img.save(buffer)
        filename = '%s.png' % (self.passen_email)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.len, None)
        self.qrcode.save(filename, filebuffer)

    def generate_qrcode_update(self):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=0,
            )

            #str = "{\"busname\" : \"" + self.busname + "\" , \"busnumber\" : \"" +self.busnumber+"\" , \"tripno\" : \""+self.tripno+"\" , \"passen_email\" : \""+self.passen_email+"\" , \"cusername\" : \""+self.cusername+"\" , \"sourcestation\" : \""+self.sourcestation+"\", \"deststation\" : \""+self.deststation+"\", \"status\" : \""+self.status+"\", \"qty\" : \""+self.qty+"\" }"
            qr.add_data(","+self.status)
            #qr.add_data(self.busname+","+self.busnumber+","+str(self.tripno)+","+self.passen_email+","+self.cusername+","+self.sourcestation+","+self.deststation+","+self.status+","+self.qty)
            #qr.add_data(str)
            qr.make(fit=True)

            img = qr.make_image()

            buffer = StringIO.StringIO()
            img.save(buffer)
            filename = '%s.png' % (self.passen_email)
            filebuffer = InMemoryUploadedFile(
                buffer, None, filename, 'image/png', buffer.len, None)
            self.qrcode.save(filename, filebuffer)


class StationsOnRoute(models.Model):
    station_id = models.IntegerField()
    route_id = models.IntegerField()