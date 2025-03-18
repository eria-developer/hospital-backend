from rest_framework import serializers
from .models import Sale, SaleDetail
from inventory.models import Item
from inventory.serializers import ItemSerializer


class SaleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for SaleDetail model, including nested item representation.
    """
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )

    class Meta:
        model = SaleDetail
        fields = ['id', 'item', 'item_id', 'quantity', 'unit_price', 'subtotal']


class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer for Sale model, including nested sale details and inventory updates.
    """
    details = SaleDetailSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'date', 'total_amount', 'cashier', 'details']
        read_only_fields = ['date', 'total_amount']

    def create(self, validated_data):
        """
        Create a new sale, calculate total amount, and update inventory quantities.
        """
        details_data = validated_data.pop('details')
        sale = Sale.objects.create(cashier=validated_data['cashier'])
        total_amount = 0

        for detail_data in details_data:
            item = detail_data['item']
            quantity = detail_data['quantity']
            unit_price = item.unit_price  # Use the item's current unit price
            subtotal = quantity * unit_price
            total_amount += subtotal
            SaleDetail.objects.create(
                sale=sale,
                item=item,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )
            # Update inventory by reducing item quantity
            item.quantity -= quantity
            item.save()
        sale.total_amount = total_amount
        sale.save()
        return sale