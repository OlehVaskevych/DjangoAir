from django.contrib import admin

from .models import (AirlineUser, Airplane, Baggage, BoardingPass, CheckIn,
                     Comfort, DietaryOption, Flight, Meal, Ticket)


class RoleBasedAdmin(admin.ModelAdmin):
    allowed_roles = []

    def has_module_permission(self, request):
        return request.user.is_authenticated and request.user.role in self.allowed_roles

    def has_view_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.role in self.allowed_roles:
            return True
        return (
            obj is not None
            and request.user.role == "passenger"
            and getattr(obj, "passenger", None) == request.user
        )

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.role in self.allowed_roles

    def has_add_permission(self, request):
        return request.user.is_authenticated and request.user.role in self.allowed_roles

    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.role in self.allowed_roles


class TicketAdmin(RoleBasedAdmin):
    allowed_roles = ["supervisor", "checkin_manager", "gate_manager"]

class CheckInManager(RoleBasedAdmin):
    allowed_roles = ["supervisor", "checkin_manager"]

class GateManager(RoleBasedAdmin):
    allowed_roles = ["supervisor", "gate_manager"]

class AirlineUserAdmin(RoleBasedAdmin):
    allowed_roles = ["supervisor"]

class AirplaneAdmin(RoleBasedAdmin):
    allowed_roles = ["supervisor"]

class FlightAdmin(RoleBasedAdmin):
    allowed_roles = ["supervisor"]


admin.site.register(AirlineUser, AirlineUserAdmin)
admin.site.register(Airplane, TicketAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Baggage, FlightAdmin)
admin.site.register(Comfort, FlightAdmin)
admin.site.register(DietaryOption, FlightAdmin)
admin.site.register(Meal, FlightAdmin)

admin.site.register(Ticket, TicketAdmin)
admin.site.register(CheckIn, CheckInManager)
admin.site.register(BoardingPass, GateManager)
