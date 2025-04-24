from rest_framework import serializers
from .models import Sale, SaleDetail
from products.models import Product


class SaleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the SaleDetail model, handling serialization and validation of individual products in a sale.

    Allows optional unit_price in requests, recalculates unit_price and subtotal server-side based on product data.

    Fields:
        - id (int): The unique identifier of the sale detail (read-only).
        - product (int): The ID of the associated product (required).
        - quantity (int): The quantity sold (required, positive integer).
        - unit_price (decimal): The unit price of the product (optional, max 10 digits, 2 decimal places; defaults to product's unit price).
        - subtotal (decimal): The calculated subtotal (quantity * unit_price, read-only, max 10 digits, 2 decimal places).

    Usage:
        Validates and serializes sale detail data, ensuring unit_price and subtotal are calculated correctly for each product in a sale.
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, read_only=True)

    class Meta:
        model = SaleDetail
        fields = ['id', 'product', 'quantity', 'unit_price', 'subtotal']

    def validate(self, data):
        """
        Validate and recalculate unit_price and subtotal based on product data.

        Parameters:
            data (dict): The input data containing product, quantity, and optional unit_price.

        Returns:
            dict: The validated data with recalculated unit_price and subtotal.

        Raises:
            ValidationError: If the product is invalid or quantity is not positive.
        """
        product = data['product']
        quantity = data['quantity']

        # Use provided unit_price if given, otherwise fetch from product
        unit_price = data.get('unit_price', product.unit_price)

        # Recalculate subtotal regardless of provided value
        data['unit_price'] = unit_price
        data['subtotal'] = quantity * unit_price
        return data


class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sale model, handling serialization, validation, and inventory updates.

    Includes nested sale details and supports associating a sale with a patient, defaulting to a Walk-in Customer if not specified.

    Fields:
        - id (int): The unique identifier of the sale (read-only).
        - date (datetime): The date and time of the sale (read-only, set automatically).
        - total_amount (decimal): The total amount of the sale (read-only, calculated from details, max 10 digits, 2 decimal places).
        - cashier (int): The ID of the user who created the sale (read-only, set automatically to the authenticated user).
        - patient (int): The ID of the associated patient (optional, defaults to Walk-in Customer if not provided).
        - details (list): A list of SaleDetail objects (required, as defined in SaleDetailSerializer).

    Usage:
        Validates and serializes sale data, creates sale records, calculates total amount, updates product inventory, and associates the sale with a patient (defaulting to Walk-in Customer if not specified).
    """
    details = SaleDetailSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'date', 'total_amount', 'cashier', 'patient', 'details']
        read_only_fields = ['date', 'total_amount', 'cashier']

    def create(self, validated_data):
        """
        Create a new sale, calculate total amount, associate with a patient (defaulting to Walk-in Customer if not provided), and update inventory quantities.

        Parameters:
            validated_data (dict): Validated data containing patient (optional), cashier, and details.

        Returns:
            Sale: The created sale instance.

        Raises:
            ValidationError: If there is insufficient stock for any product in the sale or if the patient ID is invalid.
        """
        details_data = validated_data.pop('details')
        # If patient is not provided, it will use the default from the model (Walk-in Customer)
        sale = Sale.objects.create(cashier=validated_data['cashier'], patient=validated_data.get('patient'))
        total_amount = 0

        for detail_data in details_data:
            product = detail_data['product']
            quantity = detail_data['quantity']
            unit_price = detail_data['unit_price']  # Already validated and set in SaleDetailSerializer
            subtotal = detail_data['subtotal']      # Already calculated

            total_amount += subtotal
            SaleDetail.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )
            # Update inventory
            product.stock_level -= quantity
            if product.stock_level < 0:
                raise serializers.ValidationError(f"Insufficient stock for product {product.name}")
            product.save()

        sale.total_amount = total_amount
        sale.save()
        return sale