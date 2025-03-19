# from rest_framework import serializers
# from .models import Sale, SaleDetail
# from inventory.models import Item
# from inventory.serializers import ItemSerializer


# class SaleDetailSerializer(serializers.ModelSerializer):
#     """
#     Serializer for SaleDetail model, including nested item representation.
#     """
#     item = ItemSerializer(read_only=True)
#     item_id = serializers.PrimaryKeyRelatedField(
#         queryset=Item.objects.all(), source='item', write_only=True
#     )

#     class Meta:
#         model = SaleDetail
#         fields = ['id', 'item', 'item_id', 'quantity', 'unit_price', 'subtotal']


# class SaleSerializer(serializers.ModelSerializer):
#     """
#     Serializer for Sale model, including nested sale details and inventory updates.
#     """
#     details = SaleDetailSerializer(many=True)

#     class Meta:
#         model = Sale
#         fields = ['id', 'date', 'total_amount', 'cashier', 'details']
#         read_only_fields = ['date', 'total_amount']

#     def create(self, validated_data):
#         """
#         Create a new sale, calculate total amount, and update inventory quantities.
#         """
#         details_data = validated_data.pop('details')
#         sale = Sale.objects.create(cashier=validated_data['cashier'])
#         total_amount = 0

#         for detail_data in details_data:
#             item = detail_data['item']
#             quantity = detail_data['quantity']
#             unit_price = item.unit_price  # Use the item's current unit price
#             subtotal = quantity * unit_price
#             total_amount += subtotal
#             SaleDetail.objects.create(
#                 sale=sale,
#                 item=item,
#                 quantity=quantity,
#                 unit_price=unit_price,
#                 subtotal=subtotal
#             )
#             # Update inventory by reducing item quantity
#             item.quantity -= quantity
#             item.save()
#         sale.total_amount = total_amount
#         sale.save()
#         return sale








from rest_framework import serializers
from .models import Sale, SaleDetail
from inventory.models import Item

class SaleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for SaleDetail model, including nested item representation.
    Allows optional unit_price and subtotal in requests, recalculates them server-side.
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