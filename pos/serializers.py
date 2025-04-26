from rest_framework import serializers
from .models import Sale, SaleDetail
from products.models import Product
from patients.models import Patients

class SaleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for SaleDetail model, handling serialization and validation of individual products in a sale.
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, read_only=True)

    class Meta:
        model = SaleDetail
        fields = ['id', 'product', 'quantity', 'unit_price', 'subtotal']

    def validate(self, data):
        """
        Validate and recalculate unit_price and subtotal, ensuring sufficient stock.
        """
        product = data['product']
        quantity = data['quantity']

        if quantity <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be a positive integer."})
        if product.stock_level < quantity:
            raise serializers.ValidationError(
                f"Insufficient stock for product {product.name}. Available: {product.stock_level}"
            )

        unit_price = data.get('unit_price', product.unit_price)
        from decimal import Decimal
        if isinstance(unit_price, str):
            unit_price = Decimal(unit_price)
        data['unit_price'] = unit_price
        data['subtotal'] = quantity * unit_price
        return data

class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer for Sale model, handling serialization, validation, and inventory updates.
    """
    details = SaleDetailSerializer(many=True)
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patients.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Sale
        fields = ['id', 'date', 'total_amount', 'discount', 'status', 'payment_method', 'cashier', 'patient', 'details']
        read_only_fields = ['date', 'total_amount', 'cashier']

    def validate(self, data):
        """
        Validate the sale data, ensuring details are provided and discount is non-negative.
        """
        if not data.get('details'):
            raise serializers.ValidationError({"details": "At least one sale detail is required."})
        if 'discount' in data and data['discount'] < 0:
            raise serializers.ValidationError({"discount": "Discount cannot be negative."})
        return data

    def create(self, validated_data):
        """
        Create a new sale, calculate total amount, and update inventory.
        """
        details_data = validated_data.pop('details')
        discount = validated_data.pop('discount', 0)
        sale = Sale.objects.create(
            cashier=validated_data['cashier'],
            patient=validated_data.get('patient'),
            discount=discount,
            status=validated_data.get('status', 'PENDING'),
            payment_method=validated_data.get('payment_method')
        )
        total_amount = 0

        for detail_data in details_data:
            product = detail_data['product']
            quantity = detail_data['quantity']
            unit_price = detail_data['unit_price']
            subtotal = detail_data['subtotal']

            SaleDetail.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )
            product.stock_level -= quantity
            if product.stock_level < 0:
                raise serializers.ValidationError(f"Insufficient stock for product {product.name}")
            product.save()

            total_amount += subtotal

        sale.total_amount = max(total_amount - discount, 0)
        sale.save()
        return sale