class Menu {
  final int? id;
  final String name;
  final double price;
  final int? categoryId;
  final String? imageUrl;
  final bool isAvailable;
  final String? description;

  Menu({
    this.id,
    required this.name,
    required this.price,
    this.categoryId,
    this.imageUrl,
    this.isAvailable = true,
    this.description,
  });

  factory Menu.fromJson(Map<String, dynamic> json) {
    return Menu(
      id: json['id'] as int?,
      name: json['name'] as String,
      price: (json['price'] as num).toDouble(),
      categoryId: json['category_id'] as int?,
      imageUrl: json['image_url'] as String?,
      isAvailable: json['is_available'] as bool? ?? true,
      description: json['description'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'price': price,
      'category_id': categoryId,
      'image_url': imageUrl,
      'is_available': isAvailable,
      'description': description,
    };
  }
}