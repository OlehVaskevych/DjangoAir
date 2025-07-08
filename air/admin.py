from django.contrib import admin

from .models import (AirlineUser, Airplane, Baggage, BoardingPass, CheckIn,
                     Comfort, DietaryOption, Flight, Meal, Ticket)


class TicketAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor", "checkin_manager", "gate_manager"]

    def has_view_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ["supervisor", "checkin_manager", "gate_manager"]:
            return True
        return (
            obj is not None
            and request.user.role == "passenger"
            and obj.passenger == request.user
        )

    def has_change_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role == "supervisor"

    def has_add_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role == "supervisor"

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role == "supervisor"


class CheckInManager(admin.ModelAdmin):
    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["checkin_manager", "supervisor"]

    def has_view_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ["supervisor", "checkin_manager"]:
            return True
        return (
            obj is not None
            and request.user.role == "passenger"
            and obj.passenger == request.user
        )

    def has_change_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor", "checkin_manager"]

    def has_add_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor", "checkin_manager"]

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor", "checkin_manager"]


class GateManager(admin.ModelAdmin):
    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["gate_manager", "supervisor"]

    def has_view_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ["supervisor", "gate_manager"]:
            return True
        return (
            obj is not None
            and request.user.role == "passenger"
            and obj.passenger == request.user
        )

    def has_change_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor", "gate_manager"]

    def has_add_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor", "gate_manager"]

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor", "gate_manager"]


class AirlineUserAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]

    def has_view_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ["supervisor"]:
            return True
        return (
            obj is not None
            and request.user.role == "passenger"
            and obj.passenger == request.user
        )

    def has_change_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]

    def has_add_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]


class AirplaneAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]

    def has_view_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ["supervisor"]:
            return True
        return (
            obj is not None
            and request.user.role == "passenger"
            and obj.passenger == request.user
        )

    def has_change_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]

    def has_add_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]


class FlightAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]

    def has_view_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ["supervisor"]:
            return True
        return (
            obj is not None
            and request.user.role == "passenger"
            and obj.passenger == request.user
        )

    def has_change_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]

    def has_add_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["supervisor"]


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
