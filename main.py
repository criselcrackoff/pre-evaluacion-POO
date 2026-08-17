from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Factura(BaseModel):
    id: int
    numero_factura: int
    fecha: str
    cliente: str
    total: int

class FacturaCreate(BaseModel):
    numero_factura: int
    fecha: str
    cliente: str
    total: int    

@app.get("/")
async def root():
    return { "Estado": "Servidor en línea"}

# Endpoint 1
# GET /facturas
@app.get("/facturas")
def obtener_facturas():
    conexion = sqlite3.connect("master.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    respuesta = cursor.execute("SELECT id, numero_factura, fecha, cliente, total FROM facturas ORDER BY fecha DESC")
    
    return [dict(factura) for factura in respuesta]

# Endpoint 2
# GET /facturas/{id}
@app.get("/facturas/{id}")
def obtener_factura(id: int):
    conexion = sqlite3.connect("master.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    respuesta = cursor.execute("SELECT id, numero_factura, fecha, cliente, total FROM facturas WHERE id = ?", (id,)).fetchone()
    return dict(respuesta)

# Endpoint 3
# POST /facturas
@app.post("/facturas")
def crear_factura(factura: FacturaCreate):
    conexion =  sqlite3.connect("master.db")

    cursor = conexion.cursor()

    respuesta = cursor.execute("INSERT INTO facturas (numero_factura,fecha,cliente,total) VALUES (?, ?, ?, ?)", 
                          (factura.numero_factura,factura.fecha,factura.cliente,factura.total))

    conexion.commit()

    nuevo_id = cursor.lastrowid

    conexion.close()

    return {
        "mensaje": "Factura creada correctamente",
        "id": nuevo_id,
        "numero_factura": factura.numero_factura,
        "fecha": factura.fecha,
        "cliente": factura.cliente,
        "total": factura.total
    }