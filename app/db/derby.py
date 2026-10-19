import os
import jaydebeapi

JAR_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "lib")
JARS = [
    os.path.join(JAR_DIR, "derby.jar"),
    os.path.join(JAR_DIR, "derbyshared.jar"),
    os.path.join(JAR_DIR, "derbytools.jar"),
]

JDBC_URL = "jdbc:derby:tareas_db;create=true"
DRIVER = "org.apache.derby.jdbc.EmbeddedDriver"

_connection = None

def get_connection():
    global _connection
    if _connection is None:
        _connection = jaydebeapi.connect(
            DRIVER,
            JDBC_URL,
            jars=JARS,
            driver_args={},
        )
    return _connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM SYS.SYSTABLES WHERE TABLENAME = 'TAREAS'
    """)
    exists = cursor.fetchone()[0]
    if not exists:
        cursor.execute("""
            CREATE TABLE tareas (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                titulo VARCHAR(100) NOT NULL,
                descripcion VARCHAR(500),
                responsable VARCHAR(50) NOT NULL,
                estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
                fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
    cursor.close()
    conn.commit()
