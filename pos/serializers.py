from rest_framework import serializers
from .models import Sale, SaleDetail
from inventory.models import Item


class SaleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for SaleDetail model, including nested item representation.
    Allows optional unit_price and subtotal in requests, recalculates them server-side.

    Fields:
        - id (int): The unique identifier of the sale detail (read-only).
        - item (int): The ID of the associated item (required).
        - quantity (int): The quantity sold (required, positive integer).
        - unit_price (decimal): The unit price of the item (optional, max 10 digits, 2 decimal places; defaults to item's unit price).
        - subtotal (decimal): The calculated subtotal (quantity * unit_price, read-only, max 10 digits, 2 decimal places).

    Usage:
        Validates and serializes sale detail data, ensuring unit_price and subtotal are calculated correctly.
    """
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, read_only=True)

    class Meta:
        model = SaleDetail
        fields = ['id', 'item', 'quantity', 'unit_price', 'subtotal']

    def validate(self, data):
        """
        Validate and recalculate unit_price and subtotal based on item data.

        Parameters:
            data (dict): The input data containing item, quantity, and optional unit_price.

        Returns:
            dict: The validated data with recalculated unit_price and subtotal.

        Raises:
            ValidationError: If the item or quantity is invalid.
        """
        item = data['item']
        quantity = data['quantity']

        # Use provided unit_price if given, otherwise fetch from item
        unit_price = data.get('unit_price', item.unit_price)

        # Recalculate subtotal regardless of provided value
        data['unit_price'] = unit_price
        data['subtotal'] = quantity * unit_price
        return data


class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer for Sale model, including nested sale details and inventory updates.

    Fields:
        - id (int): The unique identifier of the sale (read-only).
        - date (datetime): The date and time of the sale (read-only, set automatically).
        - total_amount (decimal): The total amount of the sale (read-only, calculated from details).
        - cashier (int): The ID of the user who created the sale (read-only, set automatically).
        - details (list): A list of SaleDetail objects (required, as defined in SaleDetailSerializer).

    Usage:
        Validates and serializes sale data, creates sale records, calculates total amount, and updates inventory quantities.
    """
    details = SaleDetailSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'date', 'total_amount', 'cashier', 'details']
        read_only_fields = ['date', 'total_amount']

    def create(self, validated_data):
        """
        Create a new sale, calculate total amount, and update inventory quantities.

        Parameters:
            validated_data (dict): Validated data containing cashier and details.

        Returns:
            Sale: The created sale instance.

        Raises:
            ValidationError: If there is insufficient stock for any item in the sale.
        """
        details_data = validated_data.pop('details')
        sale = Sale.objects.create(cashier=validated_data['cashier'])
        total_amount = 0

        for detail_data in details_data:
            item = detail_data['item']
            quantity = detail_data['quantity']
            unit_price = detail_data['unit_price']  # Already validated and set in SaleDetailSerializer
            subtotal = detail_data['subtotal']      # Already calculated

            total_amount += subtotal
            SaleDetail.objects.create(
                sale=sale,
                item=item,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )
            # Update inventory
            item.quantity -= quantity
            if item.quantity < 0:
                raise serializers.ValidationError(f"Insufficient stock for item {item.name}")
            item.save()

        sale.total_amount = total_amount
        sale.save()
        return sale