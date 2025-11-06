import 'package:flutter/material.dart';
import '../models/menu.dart';
import '../models/addon.dart';

class CartItem {
  final Menu menu;
  int quantity;
  final List<Addon> addons;
  double subtotal;

  CartItem({
    required this.menu,
    this.quantity = 1,
    List<Addon>? addons,
  })  : addons = addons ?? [],
        subtotal = _calcSubtotal(menu.price, quantity, addons ?? []);

  void recalc() {
    subtotal = _calcSubtotal(menu.price, quantity, addons);
  }

  static double _calcSubtotal(double price, int quantity, List<Addon> addons) {
    final addonsTotal = addons.fold<double>(0, (s, a) => s + a.price);
    return price * quantity + addonsTotal * quantity;
  }
}

class CartProvider extends ChangeNotifier {
  final List<CartItem> _items = [];

  List<CartItem> get items => List.unmodifiable(_items);

  double get total => _items.fold(0, (s, item) => s + item.subtotal);

  void addItem(Menu menu, {int quantity = 1, List<Addon>? addons}) {
    // try to find existing item with same menu and same addon ids
    CartItem? existing;
    for (final it in _items) {
      if (it.menu.id == menu.id && _sameAddonIds(it.addons, addons ?? [])) {
        existing = it;
        break;
      }
    }

    if (existing != null) {
      existing.quantity += quantity;
      existing.recalc();
    } else {
      final itm = CartItem(menu: menu, quantity: quantity, addons: addons);
      _items.add(itm);
    }

    notifyListeners();
  }

  void removeItem(CartItem item) {
    _items.remove(item);
    notifyListeners();
  }

  void updateQuantity(CartItem item, int quantity) {
    final idx = _items.indexOf(item);
    if (idx >= 0) {
      _items[idx].quantity = quantity;
      _items[idx].recalc();
      notifyListeners();
    }
  }

  void clear() {
    _items.clear();
    notifyListeners();
  }

  static bool _sameAddonIds(List<Addon> a, List<Addon> b) {
    final aIds = a.map((e) => e.id).toSet();
    final bIds = b.map((e) => e.id).toSet();
    return aIds.length == bIds.length && aIds.containsAll(bIds);
  }
}
