from rest_framework import serializers
from .models import (
    Data,
    Domain,
    SubDomain
)


class SubDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDomain
        fields = "__all__"


class DomainSerializer(serializers.ModelSerializer):
    sub_domain = SubDomainSerializer(read_only=True, many=True)

    class Meta:
        model = Domain
        fields = "__all__"


class DataSerializer(serializers.ModelSerializer):
    """
    Basic model serializer for Data objects.
    """
    domain_name = serializers.CharField(max_length=200, write_only=True)
    sub_domain_name = serializers.CharField(max_length=200, write_only=True)
    domain = DomainSerializer(read_only=True)

    class Meta:
        model = Data
        fields = ("name", "file", "domain_name", 'sub_domain_name', "domain", "sub_domain")
        read_only_fields = ["domain", "sub_domain"]

    def create(self, validated_data):
        """
        Create method for the Data Serializer.
        We try to find domain and sub domain objects from the name given, if found we use that instance,
        else we create new domain and sub domain objects.
        :param validated_data: The validated data received from the serializer
        :return: Serialized data
        """
        name = validated_data.get('name', False)
        file = validated_data.get('file', False)
        domain_name = validated_data.get('domain_name', False)
        sub_domain_name = validated_data.get('sub_domain_name', False)

        try:
            domain_obj = Domain.objects.get(name=domain_name)
        except Domain.DoesNotExist:
            domain_obj = Domain.objects.create(name=domain_name)
        try:
            sub_domain_obj = SubDomain.objects.get(name=sub_domain_name)
            domain_obj.sub_domain.add(sub_domain_obj)
        except SubDomain.DoesNotExist:
            sub_domain_obj = SubDomain.objects.create(name=sub_domain_name)
            domain_obj.sub_domain.add(sub_domain_obj)

        data_obj = Data.objects.create(
            name=name,
            file=file,
            domain=domain_obj,
            sub_domain=sub_domain_obj
        )
        return data_obj
