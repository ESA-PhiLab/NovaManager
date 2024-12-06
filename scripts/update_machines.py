import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vmmanager.settings")
django.setup()

from manager.models import Machine
from utils.openstack import AuthenticatedNovaClient

nc = AuthenticatedNovaClient().client
servers = nc.servers.list()

set_ids = set()
for server in servers:
    set_ids.add(server.id)
    Machine(uuid=server.id, name=server.human_id).save()

for machine in Machine.objects.all():
    if str(machine.uuid) not in set_ids:
        machine.delete()
