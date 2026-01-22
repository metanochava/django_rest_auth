from rest_framework import serializers

from django_saas.models.input import Input


class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = [
            "id",
            "nome",
        ]
