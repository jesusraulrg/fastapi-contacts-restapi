from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4 as uuid
import csv

app = FastAPI()

contactos = []

# clase Contacto
class Contacto(BaseModel):
    id_contacto: str
    nombre: str
    primer_apellido: str
    segundo_apellido: str
    email: str
    telefono: str

def cargar_datos_desde_csv():
    try:
        with open('contactos.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contactos.append(row)
    except FileNotFoundError:
        pass

def guardar_datos_en_csv():
    with open('contactos.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=contactos[0].keys() if contactos else [])
        writer.writeheader()
        for row in contactos:
            writer.writerow(row)

@app.on_event("startup")
async def startup_event():
    cargar_datos_desde_csv()

@app.get('/', description="Raíz de la API", summary="Raíz")
def root():
    return {"CONTACTOS" : "Esta es mi API Rest de Contactos"}

@app.get('/contactos', description="Obtener la lista de contactos", summary="Obtener contactos")
def obtener_contactos():
    return contactos

@app.post('/contactos', description="Crear un nuevo contacto", summary="Crear contacto", status_code=201)
def crear_contacto(post: Contacto):
    post.id_contacto = str(uuid())
    contactos.append(post.dict())
    guardar_datos_en_csv()
    return contactos[-1]

@app.get('/contactos/{contacto_id}', description="Obtener un contacto por ID", summary="Obtener contacto por ID")
def obtener_contacto(contacto_id: str):
    for post in contactos:
        if post['id_contacto'] == contacto_id:
            return post
    raise HTTPException(status_code=404, detail="Contacto No Encontrado")

@app.delete('/contactos/{contacto_id}', description="Eliminar un contacto por ID", summary="Eliminar contacto por ID", status_code=204)
def eliminar_contacto(contacto_id: str):
    for index, post in enumerate(contactos):
        if post['id_contacto'] == contacto_id:
            contactos.pop(index)
            guardar_datos_en_csv()
            return {"message" : "El contacto ha sido eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Contacto No Encontrado")

@app.put('/contactos/{contacto_id}', description="Actualizar un contacto por ID", summary="Actualizar contacto por ID")
def actualizar_contacto(contacto_id: str, contactoActualizado: Contacto):
    for index, post in enumerate(contactos):
        if post['id_contacto'] == contacto_id:
            contactos[index].update(contactoActualizado.dict())
            guardar_datos_en_csv()
            return {"message" : "Contacto Actualizado Correctamente"}
    raise HTTPException(status_code=404, detail="Contacto No Encontrado")
