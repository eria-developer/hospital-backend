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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new sale with details, update inventory, and associate with a patient (optional).
        """
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cashier=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaleDetailView(APIView):
    """
    API view to retrieve or update a specific sale.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Retrieve a sale by its primary key.
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
            return Response({"error": "Sale not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SaleSerializer(sale)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """
        Update the status or payment method of a sale.
        """
        sale = self.get_object(pk)
        if sale is None:
            return Response({"error": "Sale not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Only allow updating status and payment_method
        allowed_fields = {'status', 'payment_method'}
        if not set(request.data.keys()).issubset(allowed_fields):
            return Response(
                {"error": "Only status and payment_method can be updated"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = SaleSerializer(sale, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)