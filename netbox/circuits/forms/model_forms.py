from django.utils.translation import gettext as _

from circuits.models import *
from dcim.models import Site
from ipam.models import ASN
from netbox.forms import NetBoxModelForm
from tenancy.forms import TenancyForm
from utilities.forms import (
    CommentField, DatePicker, DynamicModelChoiceField, DynamicModelMultipleChoiceField, SelectSpeedWidget, SlugField,
)

__all__ = (
    'CircuitForm',
    'CircuitTerminationForm',
    'CircuitTypeForm',
    'ProviderForm',
    'ProviderNetworkForm',
)


class ProviderForm(NetBoxModelForm):
    slug = SlugField()
    asns = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        label=_('ASNs'),
        required=False
    )
    comments = CommentField()

    fieldsets = (
        ('Provider', ('name', 'slug', 'asns', 'description', 'tags')),
        ('Support Info', ('account',)),
    )

    class Meta:
        model = Provider
        fields = [
            'name', 'slug', 'account', 'asns', 'description', 'comments', 'tags',
        ]


class ProviderNetworkForm(NetBoxModelForm):
    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all()
    )
    comments = CommentField()

    fieldsets = (
        ('Provider Network', ('provider', 'name', 'service_id', 'description', 'tags')),
    )

    class Meta:
        model = ProviderNetwork
        fields = [
            'provider', 'name', 'service_id', 'description', 'comments', 'tags',
        ]


class CircuitTypeForm(NetBoxModelForm):
    slug = SlugField()

    fieldsets = (
        ('Circuit Type', (
            'name', 'slug', 'description', 'tags',
        )),
    )

    class Meta:
        model = CircuitType
        fields = [
            'name', 'slug', 'description', 'tags',
        ]


class CircuitForm(TenancyForm, NetBoxModelForm):
    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all()
    )
    type = DynamicModelChoiceField(
        queryset=CircuitType.objects.all()
    )
    comments = CommentField()

    fieldsets = (
        ('Circuit', ('provider', 'cid', 'type', 'status', 'description', 'tags')),
        ('Service Parameters', ('install_date', 'termination_date', 'commit_rate')),
        ('Tenancy', ('tenant_group', 'tenant')),
    )

    class Meta:
        model = Circuit
        fields = [
            'cid', 'type', 'provider', 'status', 'install_date', 'termination_date', 'commit_rate', 'description',
            'tenant_group', 'tenant', 'comments', 'tags',
        ]
        widgets = {
            'install_date': DatePicker(),
            'termination_date': DatePicker(),
            'commit_rate': SelectSpeedWidget(),
        }


class CircuitTerminationForm(NetBoxModelForm):
    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        initial_params={
            'circuits': '$circuit'
        }
    )
    circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        query_params={
            'provider_id': '$provider',
        },
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        selector=True
    )
    provider_network = DynamicModelChoiceField(
        queryset=ProviderNetwork.objects.all(),
        required=False,
        selector=True
    )

    class Meta:
        model = CircuitTermination
        fields = [
            'provider', 'circuit', 'term_side', 'site', 'provider_network', 'mark_connected', 'port_speed',
            'upstream_speed', 'xconnect_id', 'pp_info', 'description', 'tags',
        ]
        widgets = {
            'port_speed': SelectSpeedWidget(),
            'upstream_speed': SelectSpeedWidget(),
        }
