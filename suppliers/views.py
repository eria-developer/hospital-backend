from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Supplier
from .serializers import SupplierSerializer


class SupplierListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all suppliers.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing a list of serialized supplier objects.
                      Status code 200 OK on success.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new supplier.

        Parameters:
            request (Request): The HTTP request object containing the supplier data in JSON format.
                              Expected fields:
                              - name (str): The name of the supplier (required, max 100 characters).
                              - registration_number (str): A unique registration number for the supplier (required, max 30 characters).
                              - email (str): The email address of the supplier (required, valid email format).
                              - phone (str): The primary phone number of the supplier (required, max 15 characters).
                              - alternative_phone (str): An alternative phone number (optional, max 15 characters, nullable).
                              - address (str): The address of the supplier (optional, can be blank).
                              - description (str): A description of the supplier (optional, nullable).

        Returns:
            Response: A JSON response containing the serialized supplier object on success with status code 201 Created.
                      If the input data is invalid (e.g., duplicate registration_number), returns errors with status code 400 Bad Request.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to retrieve a supplier by its primary key.

        Parameters:
            pk (int): The primary key of the supplier.

        Returns:
            Supplier: The supplier object if found, otherwise None.
        """
        try:
            return Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a supplier by its ID.

        Parameters:
            request (Request): The HTTP request object.
            pk (int): The primary key of the supplier to retrieve.

        Returns:
            Response: A JSON response containing the serialized supplier object with status code 200 OK.
                      If the supplier is not found, returns status code 404 Not Found.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        supplier = self.get_object(pk)
        if supplier is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a supplier by its ID.

        Parameters:
            request (Request): The HTTP request object containing the updated supplier data in JSON format.
                              Expected fields (partial updates allowed):
                              - name (str): The name of the supplier (max 100 characters).
                              - registration_number (str): A unique registration number for the supplier (max 30 characters).
                              - email (str): The email address of the supplier (valid email format).
                              - phone (str): The primary phone number of the supplier (max 15 characters).
                              - alternative_phone (str): An alternative phone number (max 15 characters, nullable).
                              - address (str): The address of the supplier (can be blank).
                              - description (str): A description of the supplier (nullable).
            pk (int): The primary key of the supplier to update.

        Returns:
            Response: A JSON response containing the updated serialized supplier object on success with status code 200 OK.
                      If the supplier is not found, returns status code 404 Not Found.
                      If the input data is invalid (e.g., duplicate registration_number), returns errors with status code 400 Bad Request.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        supplier = self.get_object(pk)
        if supplier is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a supplier by its ID.

        Parameters:
            request (Request): The HTTP request object.
            pk (int): The primary key of the supplier to delete.

        Returns:
            Response: A response with status code 204 No Content on successful deletion.
                      If the supplier is not found, returns status code 404 Not Found.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        supplier = self.get_object(pk)
        if supplier is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)