from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Sale
from .serializers import SaleSerializer


class SaleListCreateView(APIView):
    """
    API view to list all sales or create a new sale.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all sales.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing a list of serialized sale objects.
                      Each sale includes its ID, date, total amount, cashier, and details.
                      Status code 200 OK on success.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new sale with details and update inventory accordingly.

        Parameters:
            request (Request): The HTTP request object containing the sale data in JSON format.
                              Expected fields:
                              - details (list): A list of sale detail objects, each containing:
                                - item (int): The ID of the item (required).
                                - quantity (int): The quantity sold (required, positive integer).
                                - unit_price (decimal): The unit price of the item (optional, max 10 digits, 2 decimal places; defaults to item's unit price).

        Returns:
            Response: A JSON response containing the serialized sale object on success with status code 201 Created.
                      If the input data is invalid or inventory is insufficient, returns errors with status code 400 Bad Request.

        Authentication:
            Requires a valid authentication token in the Authorization header.

        Notes:
            - The cashier is automatically set to the authenticated user.
            - The total_amount and date are calculated server-side and are read-only.
            - Inventory quantities are updated automatically, and the request will fail if stock is insufficient.
        """
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cashier=request.user)  # Set cashier to current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaleDetailView(APIView):
    """
    API view to retrieve a specific sale.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to retrieve a sale by its primary key.

        Parameters:
            pk (int): The primary key of the sale.

        Returns:
            Sale: The sale object if found, otherwise None.
        """
        try:
            return Sale.objects.get(pk=pk)
        except Sale.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve details of a specific sale by ID.

        Parameters:
            request (Request): The HTTP request object.
            pk (int): The primary key of the sale to retrieve.

        Returns:
            Response: A JSON response containing the serialized sale object with status code 200 OK.
                      Includes the sale's ID, date, total amount, cashier, and details.
                      If the sale is not found, returns status code 404 Not Found.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        sale = self.get_object(pk)
        if sale is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SaleSerializer(sale)
        return Response(serializer.data)