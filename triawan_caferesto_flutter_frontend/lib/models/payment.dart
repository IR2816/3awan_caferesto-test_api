class Payment {
  final int? id;
  final int orderId;
  final double amount;
  final String? method;
  final String? status;
  final DateTime? paidAt;

  Payment({
    this.id,
    required this.orderId,
    required this.amount,
    this.method = 'cash',
    this.status,
    this.paidAt,
  });

  factory Payment.fromJson(Map<String, dynamic> json) {
    return Payment(
      id: json['id'] as int?,
      orderId: json['order_id'] as int,
      amount: (json['amount'] as num).toDouble(),
      method: json['method'] as String?,
      status: json['status'] as String?,
      paidAt: json['paid_at'] != null ? DateTime.parse(json['paid_at']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'order_id': orderId,
      'amount': amount,
      'method': method,
    };
  }
}