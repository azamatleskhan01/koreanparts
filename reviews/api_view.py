from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import AutoPart, Review
from .serializers import AutoPartSerializer, ReviewSerializer
from rest_framework import generics
from .models import AutoPart, Review
from .serializers import AutoPartSerializer, ReviewSerializer
from django.db.models import Avg, Prefetch
import time
class AutoPartListCreateAPIView(APIView):
    def get(self, request):
        parts = AutoPart.objects.all()
        serializer = AutoPartSerializer(parts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AutoPartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AutoPartDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(AutoPart, pk=pk)

    def get(self, request, pk):
        part = self.get_object(pk)
        serializer = AutoPartSerializer(part)
        return Response(serializer.data)

    def put(self, request, pk):
        part = self.get_object(pk)
        serializer = AutoPartSerializer(part, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        part = self.get_object(pk)
        part.delete()
        return Response(status=204)


class AutoPartSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({"error": "Query parameter 'q' is required."}, status=400)
        parts = AutoPart.objects.filter(
            Q(name__icontains=query) | Q(article_number__icontains=query)
        )
        serializer = AutoPartSerializer(parts, many=True)
        return Response(serializer.data)



class AutoPartReviewListAPIView(APIView):
    def get(self, request, pk):
        part = get_object_or_404(AutoPart, pk=pk)
        reviews = Review.objects.filter(auto_part=part)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class AutoPartReviewCreateAPIView(APIView):
    def post(self, request, pk):
        part = get_object_or_404(AutoPart, pk=pk)
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, auto_part=part)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ReviewListBlocked(APIView):
    def get(self, request):
        return Response({"detail": "List of all reviews is not allowed."}, status=405)


class ReviewDetailBlocked(APIView):
    def get(self, request, pk):
        return Response({"detail": "Detail view of a review is not allowed."}, status=405)


class ReviewCreateAPIView(APIView):
    def post(self, request):
        return Response({"detail": "Create via /parts/<id>/reviews/create only."}, status=405)


# Video5: Profiling Mixin
class ProfilingMixin:
    def initial(self, request, *args, **kwargs):
        request._start_time = time.time()
        return super().initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        elapsed = time.time() - getattr(request, '_start_time', time.time())
        if hasattr(response, 'data') and isinstance(response.data, dict):
            response.data.setdefault('_profiling', {})['time_ms'] = int(elapsed * 1000)
        return super().finalize_response(request, response, *args, **kwargs)

# Video6: Generic views with prefetch
class AutoPartListAPIView(ProfilingMixin, generics.ListAPIView):
    queryset = AutoPart.objects.annotate(average_rating=Avg('reviews__rating')).prefetch_related(
        Prefetch('reviews', queryset=Review.objects.select_related('user'))
    )
    serializer_class = AutoPartSerializer

class AutoPartDetailAPIView(ProfilingMixin, generics.RetrieveAPIView):
    queryset = AutoPart.objects.prefetch_related(
        Prefetch('reviews', queryset=Review.objects.select_related('user'))
    )
    serializer_class = AutoPartSerializer

class AutoPartListCreateAPIView(ProfilingMixin, generics.ListCreateAPIView):
    queryset = AutoPart.objects.all()
    serializer_class = AutoPartSerializer

class AutoPartReviewListAPIView(ProfilingMixin, generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(auto_part_id=self.kwargs['pk']).select_related('user')

class AutoPartReviewCreateAPIView(ProfilingMixin, generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        part = generics.get_object_or_404(AutoPart, pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, auto_part=part)