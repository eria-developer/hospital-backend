from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer


class ItemListCreateView(APIView):
    """
    API view to list all inventory items or create a new item.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all inventory items.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing a list of serialized item objects.
                      Status code 200 OK on success.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new inventory item.

        Parameters:
            request (Request): The HTTP request object containing the item data in JSON format.
                              Expected fields:
                              - name (str): The name of the item (required, max 100 characters).
                              - description (str): The description of the item (optional).
                              - category (int): The ID of the associated category (optional, nullable).
                              - quantity (int): The quantity of the item (required, non-negative integer, default 0).
                              - unit_price (decimal): The unit price of the item (required, max 10 digits, 2 decimal places, default 0).
                              - supplier (int): The ID of the associated supplier (optional, nullable).
                              - expiration_date (date): The expiration date of the item in YYYY-MM-DD format (optional, nullable).

        Returns:
            Response: A JSON response containing the serialized item object on success with status code 201 Created.
                      If the input data is invalid, returns errors with status code 400 Bad Request.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailView(APIView):
    """
    API view to retrieve, update, or delete a specific inventory item.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to retrieve an item by its primary key.

        Parameters:
            pk (int): The primary key of the item.

        Returns:
            Item: The item object if found, otherwise None.
        """
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve details of a specific item by ID.

        Parameters:
            request (Request): The HTTP request object.
            pk (int): The primary key of the item to retrieve.

        Returns:
            Response: A JSON response containing the serialized item object with status code 200 OK.
                      If the item is not found, returns status code 404 Not Found.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        item = self.get_object(pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific item by ID.

        Parameters:
            request (Request): The HTTP request object containing the updated item data in JSON format.
                              Expected fields (partial updates allowed):
                              - name (str): The name of the item (max 100 characters).
                              - description (str): The description of the item.
                              - category (int): The ID of the associated category (nullable).
                              - quantity (int): The quantity of the item (non-negative integer).
                              - unit_price (decimal): The unit price of the item (max 10 digits, 2 decimal places).
                              - supplier (int): The ID of the associated supplier (nullable).
                              - expiration_date (date): The expiration date of the item in YYYY-MM-DD format (nullable).
            pk (int): The primary key of the item to update.

        Returns:
            Response: A JSON response containing the updated serialized item object on success with status code 200 OK.
                      If the item is not found, returns status code 404 Not Found.
                      If the input data is invalid, returns errors with status code 400 Bad Request.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        item = self.get_object(pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific item by ID.

        Parameters:
            request (Request): The HTTP request object.
            pk (int): The primary key of the item to delete.

        Returns:
            Response: A response with status code 204 No Content on successful deletion.
                      If the item is not found, returns status code 404 Not Found.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        item = self.get_object(pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)