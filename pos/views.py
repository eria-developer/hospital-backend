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
        """
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new sale with details and update inventory accordingly.
        """
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cashier=request.user)  # Set cashier to the current authenticated user
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
        """
        try:
            return Sale.objects.get(pk=pk)
        except Sale.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve details of a specific sale by ID.
        """
        sale = self.get_object(pk)
        if sale is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SaleSerializer(sale)
        return Response(serializer.data)