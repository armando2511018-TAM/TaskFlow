import sqlite3
from .modelos import Proyecto, Tarea
import os

DATABASE_NAME = 'tareas.db'

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS proyectos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        fecha_inicio TEXT,
        estado TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        fecha_creacion TEXT,
        fecha_limite TEXT,
        prioridad TEXT,
        estado TEXT,
        proyecto_id INTEGER,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
        """
    )

    try:
        cursor.execute(
            "INSERT INTO proyectos (id, nombre, descripcion, estado) VALUES (0, 'Tareas generales', 'Tareas sin clasificar', 'Activo')"
        )
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()

class DBManager:
    def __init__(self):
        crear_tabla()

    def crear_tarea(self, tarea: Tarea) -> Tarea:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tareas(titulo, descripcion, fecha_creacion, fecha_limite, prioridad, estado, proyecto_id)
            VALUES(?, ?, ?, ?, ?, ?, ? )
            """, (tarea._titulo, tarea._descripcion, tarea._fecha_creacion, tarea._fecha_limite, tarea._prioridad, tarea._estado, tarea._proyecto_id)
        )
        tarea.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return tarea

    def obtener_proyectos(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proyectos")
        filas = cursor.fetchall()

        conn.close()

        proyectos = [
            Proyecto(
                nombre=fila['nombre'],
                descripcion=fila['descripcion'] or "",
                id=fila['id'],
                estado=fila['estado']
            )
            for fila in filas
        ]
        return proyectos

    def obtener_tareas(self, estado=None):
        conn = get_connection()
        cursor = conn.cursor()
        consulta = "SELECT * FROM tareas"
        parametros = ()

        if estado:
            consulta += " WHERE estado = ?"
            parametros = (estado,)

        consulta += " ORDER BY fecha_limite IS NULL, fecha_limite ASC, id DESC"
        cursor.execute(consulta, parametros)
        filas = cursor.fetchall()
        conn.close()

        return [
            Tarea(
                id=fila['id'],
                titulo=fila['titulo'],
                descripcion=fila['descripcion'] or "",
                fecha_creacion=fila['fecha_creacion'],
                fecha_limite=fila['fecha_limite'],
                prioridad=fila['prioridad'],
                estado=fila['estado'],
                proyecto_id=fila['proyecto_id']
            )
            for fila in filas
        ]

    def completar_tarea(self, tarea_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tareas SET estado = 'Completada' WHERE id = ?",
            (tarea_id,)
        )
        conn.commit()
        conn.close()


if __name__ == '__main__':
    # Bloque de prueba para la clase
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print(f"Base de datos {DATABASE_NAME} eliminada.")

    crear_tabla()
    print("Base de datos y tablas inicializadas correctamente.")

    # Prueba del CRUD (CREATE)
    manager = DBManager()
    tarea_prueba = Tarea(
        titulo="Completar Ejercicio de CRUD",
        fecha_limite="2025-10-30",
        prioridad="Alta",
        proyecto_id=0,
        descripcion="Implementar el módulo database.py"
    )

    tarea_creada = manager.crear_tarea(tarea_prueba)
    print(f"Tarea creada y ID asignado: {tarea_creada.id}")
