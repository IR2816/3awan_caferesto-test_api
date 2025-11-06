class OrderItem {
  final int? id;
  final int menuId;
  final int quantity;
  final double? subtotal;
  final List<int>? addonIds;

  OrderItem({
    this.id,
    required this.menuId,
    this.quantity = 1,
    this.subtotal,
    this.addonIds,
  });

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    return OrderItem(
      id: json['id'] as int?,
      menuId: json['menu_id'] as int,
      quantity: json['quantity'] as int? ?? 1,
      subtotal: json['subtotal'] != null ? (json['subtotal'] as num).toDouble() : null,
      addonIds: (json['addon_ids'] as List<dynamic>?)?.map((e) => e as int).toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'menu_id': menuId,
      'quantity': quantity,
      'subtotal': subtotal,
      'addon_ids': addonIds,
    };
  }
}