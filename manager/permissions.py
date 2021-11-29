from rest_framework import permissions

from manager.models import Machine


class IsOwnerOrAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        is_admin = request.user and request.user.is_staff
        if is_admin:
            return True

        machine = Machine.objects.get(pk=view.kwargs["instance"])
        return machine and machine.users.filter(id=request.user.id).exists()
