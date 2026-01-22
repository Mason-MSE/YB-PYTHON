from datetime import datetime
from DB.DBEngine import *
from typing import Type, List, Generic, TypeVar,Union
from Entities.BaseEntity import *
from Log import *

# T must be a subclass of BaseEntity
T = TypeVar("T", bound=BaseEntity)

class Repository(Generic[T]):
    

    def __init__(self, db: DBEngine, table_name: str, entity_class: Type[T]):
        self.db = db
        self.table = table_name
        self.entity_class = entity_class

    def insert(self, entity: T):
        pk_name = getattr(entity, "__id_field__", None)
        auto_inc = getattr(entity, "__auto_increment__", True)
        data = {}
        for field in getattr(entity, "__fields__", entity.__dict__.keys()):
            value = getattr(entity, field, None)
            if value is None and field == pk_name and auto_inc:
                continue
            if value is not None:
                data[field] = value

        if not data:
            raise ValueError("No data to insert")
        keys = ", ".join(data.keys())
        placeholders = ", ".join([self._placeholder() for _ in data])
        values = tuple(data.values())
        sql = f"INSERT INTO {self.table} ({keys}) VALUES ({placeholders})"
        self.db.execute(sql, values)
        return self.db.cursor.lastrowid

    def soft_delete(self, conditions: dict):
        sql = f"UPDATE {self.table} SET is_deleted=1, modify_time="
        if self.db.__class__.__name__ == "SQLiteEngine":
            sql += "?"
            values = [datetime.now()]
        else:
            sql += "%s"
            values = [datetime.now()]

        if conditions:
            where_clause = " AND ".join([f"{k}={self._placeholder()}" for k in conditions])
            sql += " WHERE " + where_clause
            values += list(conditions.values())

        self.db.execute(sql, tuple(values))
    # ---------------- SELECT ----------------
    def select(self, conditions: dict = None, include_deleted=False,like_conditions: dict = None,
               page: int = None, page_size: int = None) -> List[T]:
        #Select entities with optional conditions and pagination"""
        sql = f"SELECT * FROM {self.table}"
        values: tuple = ()
        clauses = []

        if conditions:
            clauses += [f"{k}={self._placeholder()}" 
                        for k in conditions]
            values += tuple(conditions.values())

        # LIKE conditions
        if like_conditions:
            for k, v in like_conditions.items():
                clauses.append(f"{k} LIKE {self._placeholder()}")
                values.append(f"%{v}%")

        if not include_deleted:
            clauses.append("is_deleted=0")

        if clauses:
            sql += " WHERE " + " AND ".join(clauses)

        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            sql += f" LIMIT {self._placeholder} OFFSET {self._placeholder}"
            values += (page_size, offset)

        rows = self.db.fetch(sql, values)
        return [self.entity_class(**dict(row)) for row in rows]

    def select_by_id(self, id_value: Union[int, str]) -> Union[T, None]:
        """Select a single entity by primary key"""
        pk_name = getattr(self.entity_class, "id_field", None) or f"{self.entity_class.__name__.lower()}_id"
        sql = f"SELECT * FROM {self.table} WHERE {pk_name}={ self._placeholder()} AND is_deleted=0"
        row = self.db.fetch(sql, (id_value,))
        if row:
            return self.entity_class(**dict(row[0]))
        return None

    # ---------------- UPDATE ----------------
    def update_by_id(self, entity: T) -> int:
        """Update entity based on its primary key"""
        # Determine primary key
        pk_name = "id" if hasattr(entity, "id") else f"{self.entity_class.__name__.lower()}_id"
        pk_value = getattr(entity, pk_name)
        if pk_value is None:
            raise ValueError("Entity ID cannot be None")

        entity.modify_time = datetime.now()
        data = {k: v for k, v in entity.__dict__.items() if k not in (pk_name, "is_deleted")}

        set_clause = ", ".join([f"{k}={self._placeholder()}" for k in data])

        sql = f"UPDATE {self.table} SET {set_clause} WHERE {pk_name}={self._placeholder()}"
        values = tuple(data.values()) + (pk_value,)
        self.db.execute(sql, values)
        return pk_value

    def batch_update(self, entities: List[T]):
        #Batch update multiple entities by their IDs
        for entity in entities:
            self.update_by_id(entity)

    # ---------------- DELETE ----------------
    def soft_delete_by_id(self, id_value: Union[int, str]):
        #Soft delete entity by ID
        pk_name = f"{self.entity_class.__name__.lower()}_id"
        sql = f"UPDATE {self.table} SET is_deleted=1, modify_time={ self._placeholder() } WHERE {pk_name}={ '?' if self.db.__class__.__name__ == 'SQLiteEngine' else '%s' }"
        values = (datetime.now(), id_value)
        self.db.execute(sql, values)

    def soft_delete(self, conditions: dict):
        #Soft delete entities by conditions
        sql = f"UPDATE {self.table} SET is_deleted=1, modify_time="
        values = [datetime.now()]
        sql += self._placeholder()

        if conditions:
            where_clause = " AND ".join([f"{k}={self._placeholder()}" 
                                         for k in conditions])
            sql += " WHERE " + where_clause
            values += list(conditions.values())

        self.db.execute(sql, tuple(values))
    
    # ---------------- HARD DELETE ----------------
    def hard_delete_by_id(self, id_value: Union[int, str]):
        #Physically remove a row by primary key
        pk_name = f"{self.entity_class.__name__.lower()}_id"
        sql = f"DELETE FROM {self.table} WHERE {pk_name}={ self._placeholder()}"
        self.db.execute(sql, (id_value,))

    def hard_delete(self, conditions: dict):
        #Physically remove rows matching conditions
        if not conditions:
            raise ValueError("Conditions required for hard delete to prevent full table deletion")
        where_clause = " AND ".join([f"{k}={self._placeholder()}" 
                                     for k in conditions])
        sql = f"DELETE FROM {self.table} WHERE {where_clause}"
        values = tuple(conditions.values())
        self.db.execute(sql, values)

    def _placeholder(self) -> str:
        # Return SQL placeholder depending on DB type.
        # SQLite  -> ?
        # MySQL/PG -> %s
        return "?" if self.db.__class__.__name__ == "SQLiteEngine" else "%s"
