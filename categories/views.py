from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer


class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all categories.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing a list of serialized category objects.
                      Status code 200 OK on success.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new category.

        Parameters:
            request (Request): The HTTP request object containing the category data in JSON format.
                              Expected fields:
                              - name (str): The name of the category (required, max 200 characters).
                              - description (str): The description of the category (required).

        Returns:
            Response: A JSON response containing the serialized category object on success with status code 201 Created.
                      If the input data is invalid, returns errors with status code 400 Bad Request.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to retrieve a category by its primary key.

        Parameters:
            pk (int): The primary key of the category.

        Returns:
            Category: The category object if found, otherwise None.
        """
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a category by its ID.

        Parameters:
            request (Request): The HTTP request object.
            pk (int): The primary key of the category to retrieve.

        Returns:
            Response: A JSON response containing the serialized category object with status code 200 OK.
                      If the category is not found, returns status code 404 Not Found.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        supplier = self.get_object(pk)
        if supplier is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(supplier)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a category by its ID.

        Parameters:
            request (Request): The HTTP request object containing the updated category data in JSON format.
                              Expected fields (partial updates allowed):
                              - name (str): The name of the category (max 200 characters).
                              - description (str): The description of the category.
            pk (int): The primary key of the category to update.

        Returns:
            Response: A JSON response containing the updated serialized category object on success with status code 200 OK.
                      If the category is not found, returns status code 404 Not Found.
                      If the input data is invalid, returns errors with status code 400 Bad Request.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        supplier = self.get_object(pk)
        if supplier is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a category by its ID.

        Parameters:
            request (Request): The HTTP request object.
            pk (int): The primary key of the category to delete.

        Returns:
            Response: A response with status code 204 No Content on successful deletion.
                      If the category is not found, returns status code 404 Not Found.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        supplier = self.get_object(pk)
        if supplier is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)