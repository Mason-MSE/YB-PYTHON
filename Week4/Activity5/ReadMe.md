# 📌 Project Name

**Clinic Database OOP + Generic ORM-Like Python CRUD Framework**

---

## 📍 Core Objective

Develop a general-purpose Python database access layer that:

- Supports multiple databases: **SQLite** & **MySQL**  
- Uses **OOP design** for data access abstraction  
- Implements a **clean layered architecture** for database operations  
- Provides entity models, generic repositories, transaction, and logging support  
- Demonstrates CRUD operations and business queries on clinic data  

---

## 🛠 Key Technologies and Architecture

### ⭐ 1. Python Standard Library

- `sqlite3` for SQLite local database operations  
- `datetime` for audit fields (`create_time`, `modify_time`)  
- `typing` for generic type support: `Generic`, `TypeVar`, `Type`  

---

### 🧱 2. Database Abstraction Layer

Implemented a unified `DBEngine` abstract base class:

- **SQLiteEngine**: using `sqlite3`  
- **MySQLEngine**: using third-party module `pymysql`  
- Standardized interface for: `execute`, `fetch`, `executescript`, `commit`, `rollback`, `close`  
- All SQL queries are **parameterized** to prevent SQL injection  

> Pluggable DB engines improve cross-database compatibility and maintainability

---

### 🧠 3. Generic Repository Design (Generic + OOP)

Implemented `Repository[T]` using Python generics:

- Supports any `BaseEntity` subclass  
- Automatically adapts SQL placeholders (`?` for SQLite, `%s` for MySQL)  
- Encapsulates common CRUD operations:  
  - `insert`, `select`, `select_by_id`  
  - `update_by_id`, `soft_delete`, `hard_delete`  
  - Supports pagination and LIKE queries  
- Recognizes primary key fields, auto-handles audit fields, and soft delete flags  

This design follows a **layered repository pattern** for maintainable and reusable database operations.

---

### 🧾 4. ORM-Like Entity Mapping

Entity classes inherit a base class:

- Includes audit fields: `create_time`, `modify_time`, `is_deleted`  
- Can declare primary key and field lists  
- Can easily convert objects to SQL field dictionaries  
- Repository layer maps objects to SQL parameters automatically

---

### 🔍 5. SQL Logging with AOP

Implemented `debug_sql` decorator:

- Automatically prints generated SQL for every execution  
- Formats parameters in color for clarity  
- Displays execution time for monitoring  

> Similar to SQL interceptors in enterprise frameworks

---

### 🧪 6. Core Business Implementation

Clinic scenario examples:

- List all **patients over 65 years old**  
- Count doctors specialized in **ophthalmology**  

All queries are implemented via the generic Repository and SQL combination.

---

### 🧩 Design Highlights

- ✔ Generic + base classes improve code reuse  
- ✔ Layered architecture for clean separation of concerns  
- ✔ Dynamic SQL placeholders for multi-database support  
- ✔ Automatic audit field handling  
- ✔ Pagination and fuzzy search support  
- ✔ SQL debug logging for observability

🖼 ER Diagram
![Clinic ER Diagram](https://github.com/Mason-MSE/YB-PYTHON/raw/main/Week4/Activity5/images/image.png)


### Vedio
![Clinic ER Diagram](
https://drive.google.com/file/d/1h6H4_wCPRobCQxig0jgBuJYZ055UOmSJ/view?usp=drive_link)
