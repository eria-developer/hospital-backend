from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer


class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all categories."""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new category."""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """Helper method to get a category by ID."""
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        """Retrieve a category by ID."""
        supplier = self.get_object(pk)
        if supplier is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(supplier)
        return Response(serializer.data)

    def put(self, request, pk):
        """Update a category by ID."""
        supplier = self.get_object(pk)
        if supplier is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a category by ID."""
        supplier = self.get_object(pk)
        if supplier is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)