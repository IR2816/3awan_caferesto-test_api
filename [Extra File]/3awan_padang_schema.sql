
-- =========================================================
-- 3AWAN PADANG CAFE & RESTO DATABASE SCHEMA (PostgreSQL)
-- =========================================================

-- Drop existing tables (for clean import)
DROP TABLE IF EXISTS order_status_history, reviews, discounts, payments, order_items, orders, carts, menu_addons, menus, categories, customers, users CASCADE;

-- ======================
-- USERS (Admin/Petugas)
-- ======================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ======================
-- CUSTOMERS (Pelanggan)
-- ======================
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100)
);

-- ======================
-- CATEGORIES (Jenis Menu)
-- ======================
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- ======================
-- MENUS (Daftar Menu)
-- ======================
CREATE TABLE menus (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    image_url TEXT,
    description TEXT,
    is_available BOOLEAN DEFAULT TRUE,
    average_rating NUMERIC(3,2) DEFAULT 0
);

-- ======================
-- MENU ADDONS (Tambahan)
-- ======================
CREATE TABLE menu_addons (
    id SERIAL PRIMARY KEY,
    menu_id INTEGER REFERENCES menus(id) ON DELETE CASCADE,
    name VARCHAR(100),
    price NUMERIC(10,2)
);

-- ======================
-- CARTS (Keranjang Belanja)
-- ======================
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    menu_id INTEGER REFERENCES menus(id),
    quantity INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ======================
-- ORDERS (Pesanan)
-- ======================
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE SET NULL,
    discount_id INTEGER,
    total_after_discount NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT NOW(),
    current_status VARCHAR(50) DEFAULT 'pending'
);

-- ======================
-- ORDER ITEMS (Rincian Pesanan)
-- ======================
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    menu_id INTEGER REFERENCES menus(id),
    quantity INTEGER DEFAULT 1,
    subtotal NUMERIC(10,2)
);

-- ======================
-- PAYMENTS (Pembayaran)
-- ======================
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    amount NUMERIC(10,2),
    payment_method VARCHAR(50),
    payment_status VARCHAR(50) DEFAULT 'pending',
    paid_at TIMESTAMP
);

-- ======================
-- DISCOUNTS (Diskon)
-- ======================
CREATE TABLE discounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    percentage NUMERIC(5,2) CHECK (percentage BETWEEN 0 AND 100),
    valid_until DATE
);

-- ======================
-- REVIEWS (Ulasan Pelanggan)
-- ======================
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    menu_id INTEGER REFERENCES menus(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ======================
-- ORDER STATUS HISTORY
-- ======================
CREATE TABLE order_status_history (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    status VARCHAR(50),
    note TEXT,
    changed_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- SAMPLE DATA (Cita Rasa Padang)
-- =========================================
INSERT INTO categories (name) VALUES
('Makanan'), ('Minuman');

INSERT INTO menus (name, price, category_id, image_url, description, is_available)
VALUES
('Rendang Daging Sapi', 35000, 1, 'https://example.com/rendang.jpg', 'Rendang khas Padang dengan bumbu rempah melimpah.', TRUE),
('Ayam Pop', 28000, 1, 'https://example.com/ayam_pop.jpg', 'Ayam pop khas Padang, gurih dan lembut.', TRUE),
('Dendeng Balado', 32000, 1, 'https://example.com/dendeng.jpg', 'Dendeng kering dengan sambal balado pedas.', TRUE),
('Teh Talua', 12000, 2, 'https://example.com/teh_talua.jpg', 'Teh telur khas Minang, manis dan hangat.', TRUE),
('Es Cendol Padang', 10000, 2, 'https://example.com/es_cendol.jpg', 'Cendol segar dengan santan dan gula aren.', TRUE);

INSERT INTO menu_addons (menu_id, name, price) VALUES
(1, 'Tambah Sambal Ijo', 3000),
(2, 'Tambah Nasi', 5000),
(3, 'Tambah Kerupuk Kulit', 4000);

INSERT INTO customers (name, phone_number, email) VALUES
('Andi Saputra', '081234567890', 'andi@example.com'),
('Siti Nurhaliza', '089876543210', 'siti@example.com');

INSERT INTO users (name, email, password, role) VALUES
('Admin Padang', 'admin@3awanpadang.com', 'hashed_password', 'admin');
