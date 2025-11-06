class Addon {
  final int? id;
  final int menuId;
  final String name;
  final double price;

  Addon({
    this.id,
    required this.menuId,
    required this.name,
    required this.price,
  });

  factory Addon.fromJson(Map<String, dynamic> json) {
    return Addon(
      id: json['id'] as int?,
      menuId: json['menu_id'] as int,
      name: json['name'] as String,
      price: (json['price'] as num).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'menu_id': menuId,
      'name': name,
      'price': price,
    };
  }
}