from django.contrib import admin
from .models import BusRoute,LiveConductorDetails,BusStations,RouteSequence,BusConductor,StationsOnRoute,LiveBusDetails,TicketTransactionsCond,TicketTransactionsUser,AdminUser

# Register your models here.
admin.site.register(BusRoute)
admin.site.register(LiveConductorDetails)
admin.site.register(BusStations)
admin.site.register(RouteSequence)
admin.site.register(BusConductor)
admin.site.register(StationsOnRoute)
admin.site.register(LiveBusDetails)
admin.site.register(TicketTransactionsCond)
admin.site.register(TicketTransactionsUser)
admin.site.register(AdminUser)