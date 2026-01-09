"""
Script para hacer la columna salt nullable
"""
import psycopg2

try:
    # Conectar a la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="espe_medsafe",
        user="postgres",
        password="admin"
    )
    
    cur = conn.cursor()
    
    # Modificar la columna salt para permitir NULL
    cur.execute("ALTER TABLE usuarios ALTER COLUMN salt DROP NOT NULL;")
    
    conn.commit()
    print("✅ Columna 'salt' modificada exitosamente - ahora permite valores NULL")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
