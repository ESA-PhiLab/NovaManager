import time

import django_tables2 as tables
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from rest_framework.views import APIView

from manager.models import Machine
from manager.permissions import IsOwnerOrAdminUser
from manager.table import NovaTable
from utils.openstack import (
    OpenstackAuthenticator,
    AuthenticatedNovaClient,
    AuthenticatedGlanceClient,
)
from utils.utils import get_delta_to_now, get_hours_to_now


class MachinesView(tables.SingleTableView):
    table_class = NovaTable
    template_name = "manager/nova_list.html"

    def get_queryset(self):
        nc = AuthenticatedNovaClient().client
        servers = nc.servers.list()
        result = []
        for serv in servers:
            try:
                if (
                    self.request.user.is_staff
                    or Machine.objects.get(pk=serv.id)
                    .users.filter(id=self.request.user.id)
                    .exists()
                ):
                    serv_data = {
                        "name": serv.name,
                        "status": serv.status,
                        "id": serv.id,
                    }
                    ips = {}
                    for network in serv.networks:
                        if network == "eodata":
                            continue
                        else:
                            _ips = list(
                                filter(
                                    lambda x: not x.startswith("192"),
                                    serv.networks[network],
                                )
                            )
                            if _ips:
                                ips[network] = _ips
                                serv_data["networks"] = _ips

                    updated_time = "-"
                    last_restart = "-"
                    link = "Turn On"
                    if serv.status == "ACTIVE":
                        updated_time = get_delta_to_now(serv.updated)
                        last_restart = get_hours_to_now(serv.updated)
                        link = "Turn Off"
                    serv_data["link"] = link
                    serv_data["updated"] = updated_time
                    serv_data["last_restart"] = last_restart

                    result.append(serv_data)
            except ObjectDoesNotExist:
                continue
        return result


class TurnOnView(APIView):
    permission_classes = [IsOwnerOrAdminUser]

    def get(self, request, instance):
        authenticator = OpenstackAuthenticator.get_authenticator()
        nc = AuthenticatedNovaClient(authenticator).client
        gc = AuthenticatedGlanceClient(authenticator).client

        nc.servers.unshelve(instance)

        while True:
            time.sleep(3)
            server = nc.servers.get(instance)
            if "ACTIVE" in server.status:
                break
        self.delete_older_images(gc, server)

        return redirect("/")

    def delete_older_images(self, gc, server):
        images = [
            {"id": img["id"],
             "created_at": img["created_at"],
             "name": img["name"]}
            for img in gc.images.list()
            if server.human_id + "-shelved" in img.name
        ]
        images = sorted(images, key=lambda x: x["created_at"])
        if images:
            images.pop(-1)
            for img in images:
                gc.images.delete(img["id"])


class TurnOffView(APIView):
    permission_classes = [IsOwnerOrAdminUser]

    def get(self, request, instance):

        nc = AuthenticatedNovaClient().client

        nc.servers.shelve(instance)

        while True:
            time.sleep(3)
            server = nc.servers.get(instance)
            if "SHELVED" in server.status:
                break

        return redirect("/")
