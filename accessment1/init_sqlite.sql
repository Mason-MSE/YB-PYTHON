-- Core user authentication and roles
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    password TEXT,
    email TEXT,
    phone TEXT,
    status INTEGER,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_profile (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    street TEXT,
    city TEXT,
    state_name TEXT,
    zipcode TEXT,
    membership_type INTEGER,
    driver_license_id INTEGER,
    avatar_url TEXT,
    date_of_birth DATE,
    nationality TEXT,
    emergency_contact_name TEXT,
    emergency_contact_phone TEXT,
    preferred_language TEXT,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS driver_license (
    driver_license_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    license_pic TEXT,
    expire_date DATE,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS resource (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_name TEXT,
    resource_link TEXT,
    resource_method TEXT,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_role (
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    role_id INTEGER,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS role_resource (
    role_resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER,
    resource_id INTEGER,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

-- Car rental related tables
CREATE TABLE IF NOT EXISTS car_category (
    car_category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS location (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_name TEXT,
    street TEXT,
    zipcode TEXT,
    city TEXT,
    state_name TEXT,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS car (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    make TEXT,
    model TEXT,
    year INTEGER,
    mileage INTEGER,
    is_available BOOLEAN,
    min_rent_days INTEGER,
    max_rent_days INTEGER,
    license_plate TEXT,
    color TEXT,
    daily_rate DECIMAL(10,2),
    location_id INTEGER,
    category_id INTEGER,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS booking (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    car_id INTEGER,
    start_date DATETIME,
    end_date DATETIME,
    pickup_location TEXT,
    drop_location TEXT,
    status TEXT,
    notes TEXT,
    color TEXT,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS rent_fee (
    rent_fee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    base_amount DECIMAL(10,2),
    insurance_amount DECIMAL(10,2),
    late_fee DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    payment_status INTEGER,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS payment (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    rent_fee_id INTEGER,
    payment_amount DECIMAL(10,2),
    payment_date DATETIME,
    payment_method TEXT,
    transaction_id TEXT,
    payment_status INTEGER,
    reference_number TEXT,
    payer_name TEXT,
    notes TEXT,
    create_time DATETIME,
    modify_time DATETIME,
    is_deleted INTEGER DEFAULT 0
);