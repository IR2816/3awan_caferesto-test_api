import 'order_item.dart';

class Order {
  final int? id;
  final int? customerId;
  final String? paymentMethod;
  final List<OrderItem> items;
  final String? status;
  final DateTime? createdAt;

  Order({
    this.id,
    this.customerId,
    this.paymentMethod = 'cash',
    required this.items,
    this.status,
    this.createdAt,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['id'] as int?,
      customerId: json['customer_id'] as int?,
      paymentMethod: json['payment_method'] as String?,
      items: (json['items'] as List<dynamic>)
          .map((item) => OrderItem.fromJson(item as Map<String, dynamic>))
          .toList(),
      status: json['status'] as String?,
      createdAt: json['created_at'] != null ? DateTime.parse(json['created_at']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'customer_id': customerId,
      'payment_method': paymentMethod,
      'items': items.map((item) => item.toJson()).toList(),
    };
  }

  double get total => items.fold(
        0,
        (sum, item) => sum + (item.subtotal ?? 0),
      );
}