from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Category, Product
from .serializers import (
    CategorySerializer, 
    ProductSerializer,
    ProductStockUpdateSerializer
)


class ProductListCreateView(APIView):
    """
    API view for listing all products and creating new ones.
    
    GET: List all products
    POST: Create a new product
    """
    
    def get(self, request):
        """
        List all products with optional filtering.
        
        Supports query parameters:
        - category: Filter by category ID
        - needs_reorder: Filter products that need reordering (true/false)
        
        Args:
            request: HTTP request object
            
        Returns:
            Response: JSON response with filtered products
        """
        products = Product.objects.all()

        # Filter by category if provided
        category_id = request.query_params.get('category')
        if category_id:
            products = products.filter(category_id=category_id)
        
        # Filter by reorder status if provided
        needs_reorder = request.query_params.get('needs_reorder')
        if needs_reorder:
            if needs_reorder.lower() == 'true':
                products = [p for p in products if p.needs_reorder]
            elif needs_reorder.lower() == 'false':
                products = [p for p in products if not p.needs_reorder]
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new product.
        
        Args:
            request: HTTP request object with product data
            
        Returns:
            Response: JSON response with created product or error messages
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    


class ProductDetailView(APIView):
    """
    API view for retrieving, updating, and deleting a specific product.
    
    GET: Retrieve a product
    PUT: Update a product
    DELETE: Delete a product
    """
    
    def get_object(self, pk):
        """
        Helper method to get product object with given primary key.
        
        Args:
            pk: Primary key of the product
            
        Returns:
            Product: The product object
            
        Raises:
            Http404: If product does not exist
        """
        return get_object_or_404(Product, pk=pk)
    
    def get(self, request, pk):
        """
        Retrieve a product.
        
        Args:
            request: HTTP request object
            pk: Primary key of the product
            
        Returns:
            Response: JSON response with product data
        """
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Update a product.
        
        Args:
            request: HTTP request object with updated data
            pk: Primary key of the product
            
        Returns:
            Response: JSON response with updated product or error messages
        """
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        """
        Delete a product.
        
        Args:
            request: HTTP request object
            pk: Primary key of the product
            
        Returns:
            Response: Empty response with 204 status code
        """
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class ProductStockUpdateView(APIView):
    """
    API view for updating only the stock level of a product.
    
    PATCH: Update product stock level
    """
    
    def get_object(self, pk):
        """
        Helper method to get product object with given primary key.
        
        Args:
            pk: Primary key of the product
            
        Returns:
            Product: The product object
            
        Raises:
            Http404: If product does not exist
        """
        return get_object_or_404(Product, pk=pk)
    
    def patch(self, request, pk):
        """
        Update a product's stock level.
        
        Args:
            request: HTTP request object with stock level data
            pk: Primary key of the product
            
        Returns:
            Response: JSON response with updated product or error messages
        """
        product = self.get_object(pk)
        serializer = ProductStockUpdateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Return the full product data after update
            return Response(ProductSerializer(product).data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )