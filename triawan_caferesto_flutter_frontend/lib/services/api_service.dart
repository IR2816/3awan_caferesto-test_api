import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart' as foundation;
import '../models/category.dart';
import '../models/menu.dart';

import '../models/addon.dart';
import '../models/customer.dart';
import '../models/order.dart';
import '../models/payment.dart';

class ApiService {
  // Change this to your computer's local IP address when testing on physical devices
  // For example: 192.168.1.5 (you can find this using 'ipconfig' in command prompt)
  static const String deviceIp = '192.168.1.1'; // Replace with your actual IP

  static String get baseUrl {
    const debug = bool.fromEnvironment('DEBUG', defaultValue: true);
    if (debug) {
      // Development/Debug mode - for emulators and local testing
      if (foundation.kIsWeb) {
        return 'http://localhost:8000/api';
      } else if (foundation.defaultTargetPlatform == foundation.TargetPlatform.android) {
        return 'http://10.0.2.2:8000/api';
      } else if (foundation.defaultTargetPlatform == foundation.TargetPlatform.iOS) {
        return 'http://127.0.0.1:8000/api';
      } else {
        return 'http://localhost:8000/api';
      }
    } else {
      // Release mode - for physical devices
      return 'http://$deviceIp:8000/api';
    }
  }

  Future<List<Category>> getCategories() async {
    try {
      // debug logs - will be visible in debug builds
  // ignore: avoid_print
  foundation.debugPrint('Fetching categories from: $baseUrl/categories');
      final response = await http.get(
        Uri.parse('$baseUrl/categories'),
        headers: {'Content-Type': 'application/json'},
      );
  // ignore: avoid_print
  foundation.debugPrint('Categories Response Status: ${response.statusCode}');
      // do not log full body in production; useful temporarily
  // ignore: avoid_print
  foundation.debugPrint('Categories Response Body: ${response.body}');
      if (response.statusCode == 200) {
        List<dynamic> data = json.decode(response.body);
        return data.map((json) => Category.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load categories: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
  // ignore: avoid_print
  foundation.debugPrint('Error fetching categories: $e');
      rethrow;
    }
  }

  Future<List<Menu>> getMenus({int? categoryId}) async {
    try {
      final url = categoryId != null 
        ? '$baseUrl/menus?category_id=$categoryId'
        : '$baseUrl/menus';
      
  // ignore: avoid_print
  foundation.debugPrint('Fetching menus from: $url');
      final response = await http.get(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
      );
  // ignore: avoid_print
  foundation.debugPrint('Menus Response Status: ${response.statusCode}');
  // ignore: avoid_print
  foundation.debugPrint('Menus Response Body: ${response.body}');
      if (response.statusCode == 200) {
        List<dynamic> data = json.decode(response.body);
        return data.map((json) => Menu.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load menus: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
  // ignore: avoid_print
  foundation.debugPrint('Error fetching menus: $e');
      rethrow;
    }
  }

  Future<Menu> getMenu(int menuId) async {
    final response = await http.get(Uri.parse('$baseUrl/menus/$menuId'));
    
    if (response.statusCode == 200) {
      return Menu.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to load menu');
    }
  }

  // Customer Methods
  Future<Customer> createCustomer(Customer customer) async {
    final response = await http.post(
      Uri.parse('$baseUrl/customers'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(customer.toJson()),
    );
    
    if (response.statusCode == 201) {
      return Customer.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to create customer');
    }
  }

  // Addon Methods
  Future<List<Addon>> getAddons(int menuId) async {
    final response = await http.get(Uri.parse('$baseUrl/menus/$menuId/addons'));
    
    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);
      return data.map((json) => Addon.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load addons');
    }
  }

  // Order Methods
  Future<Order> createOrder(Order order) async {
    final response = await http.post(
      Uri.parse('$baseUrl/orders'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(order.toJson()),
    );
    
    if (response.statusCode == 201) {
      return Order.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to create order');
    }
  }

  // Payment Methods
  Future<Payment> createPayment(Payment payment) async {
    final response = await http.post(
      Uri.parse('$baseUrl/payments'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(payment.toJson()),
    );
    
    if (response.statusCode == 201) {
      return Payment.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to create payment');
    }
  }
}