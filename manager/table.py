from django.urls import reverse
from django_tables2 import tables, Column


class NovaTable(tables.Table):
    name = tables.columns.TemplateColumn(
        template_code="""{{ record.name }}""", verbose_name="Name", orderable=False
    )
    ips = tables.columns.TemplateColumn(
        template_code="""{{ record.networks }}""", verbose_name="IPs", orderable=False
    )
    status = tables.columns.TemplateColumn(
        template_code="""{{ record.status }}""", verbose_name="Status", orderable=False
    )
    link = Column(
        verbose_name="Power Button",
        linkify=lambda record: reverse(
            record["link"].replace(" ", "_").lower(), kwargs={"instance": record["id"]}
        ),
        orderable=False,
    )
    updated = tables.columns.TemplateColumn(
        template_code="""{{ record.updated }}""",
        verbose_name="On Since",
        orderable=False,
    )
    last_restart = tables.columns.TemplateColumn(
        template_code="""{{ record.last_restart }}""",
        verbose_name="Last Start (hours passed)",
        orderable=False,
    )

    # volumes = tables.columns.TemplateColumn(template_code="""{{ record.updated }}""", orderable=True, verbose_name='Last Update')
    # project = tables.columns.TemplateColumn(template_code="""{{ record.updated }}""", orderable=True, verbose_name='Last Update')

    class Meta:
        attrs = {"id": "nova_table"}
        fields = ("name", "ips", "status", "link", "updated", "last_restart")
        sequence = fields
