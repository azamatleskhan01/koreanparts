from rest_framework import serializers
from django.db import models
from .models import AutoPart, Review


# 🔹 Сериализатор для вложенных отзывов
class ReviewNestedSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'image_url', 'created_at']

    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        req = self.context.get('request')
        return req.build_absolute_uri(obj.image.url) if obj.image and req else None


# 🔹 Основной сериализатор отзывов с валидацией
class ReviewSerializer(serializers.ModelSerializer):
    auto_part = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'auto_part', 'user', 'rating', 'comment', 'image', 'image_url', 'created_at']
        read_only_fields = ['user', 'auto_part', 'created_at']

    def get_image_url(self, obj):
        req = self.context.get('request')
        return req.build_absolute_uri(obj.image.url) if obj.image and req else None

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value

    def validate_comment(self, value):
        if value and len(value) < 10:
            raise serializers.ValidationError('Comment must be at least 10 characters.')
        return value


# 🔹 Полный сериализатор для автозапчастей с вложенными отзывами
class AutoPartSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewNestedSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()

    class Meta:
        model = AutoPart
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'category', 'manufacturer',
            'image', 'image_url', 'display_price', 'is_in_stock', 'average_rating', 'reviews'
        ]

    def get_image_url(self, obj):
        req = self.context.get('request')
        return req.build_absolute_uri(obj.image.url) if obj.image and req else None

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0

    def get_is_in_stock(self, obj):
        return obj.is_in_stock


# 🔹 Упрощённый сериализатор (например, для списка)
class GenericAutoPartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_in_stock = serializers.SerializerMethodField()

    def get_is_in_stock(self, obj):
        return obj.is_in_stock
