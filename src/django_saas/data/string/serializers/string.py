from rest_framework import serializers

from django_saas.models.string import String


class StringSerializer(serializers.ModelSerializer):
    class Meta:
        model = String
        fields = [
            "id",
            "texto",
        ]
