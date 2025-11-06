class Customer {
  final int? id;
  final String name;
  final String? phoneNumber;
  final String? email;

  Customer({
    this.id,
    required this.name,
    this.phoneNumber,
    this.email,
  });

  factory Customer.fromJson(Map<String, dynamic> json) {
    return Customer(
      id: json['id'] as int?,
      name: json['name'] as String,
      phoneNumber: json['phone_number'] as String?,
      email: json['email'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'phone_number': phoneNumber,
      'email': email,
    };
  }
}