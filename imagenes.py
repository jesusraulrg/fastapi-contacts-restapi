from fastapi import FastAPI, UploadFile, HTTPException
from PIL import Image, ImageOps
from fastapi.responses import JSONResponse
from datetime import datetime
import os

app = FastAPI()

@app.post('/imagenes')
async def guardar_imagen(image: UploadFile):
    extencion_imagen = image.filename.split(".")[-1]
    if extencion_imagen not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no válido")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ruta_imagen = os.path.join("imagenes", f"{timestamp}.{extencion_imagen}")

    with open(ruta_imagen, "wb") as image_file:
        image_file.write(image.file.read())

    return {"message": "Imagen guardada exitosamente", "image_id": timestamp}

@app.get('/imagenes')
async def obtener_imagenes():
    carpeta = "imagenes"
    imagenes = os.listdir(carpeta)
    return JSONResponse(content={"Imagenes": imagenes})



@app.post('/imagenes/{image_name}/crop')
async def crop_imagen(image_name: str, left: int, top: int, right: int, bottom: int):
    ruta_imagen = os.path.join("imagenes", image_name)

    if not os.path.exists(ruta_imagen):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    imagen = Image.open(ruta_imagen)
    imagen_recortada = imagen.crop((left, top, right, bottom))

    nuevo_nombre = f"copia_{image_name}"
    imagen_recortada.save(os.path.join("imagenes", nuevo_nombre))
    return {"message": "Imagen recortada y guardada exitosamente"}

@app.post('/imagenes/{image_name}/flip')
async def flip_imagen(image_name: str):
    ruta_imagen = os.path.join("imagenes", image_name)

    if not os.path.exists(ruta_imagen):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    imagen = Image.open(ruta_imagen)
    imagen_volteada = ImageOps.mirror(imagen)

    nuevo_nombre = f"copia_{image_name}"
    imagen_volteada.save(os.path.join("imagenes", nuevo_nombre))
    return {"message": "Imagen volteada y guardada exitosamente"}

@app.post('/imagenes/{image_name}/colorize')
async def colorize_imagen(image_name: str, color: str):
    ruta_imagen = os.path.join("imagenes", image_name)

    if not os.path.exists(ruta_imagen):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    imagen = Image.open(ruta_imagen)
    imagen_coloreada = ImageOps.colorize(imagen, "#000000", color)

    nuevo_nombre = f"copia_{image_name}"
    imagen_coloreada.save(os.path.join("imagenes", nuevo_nombre))
    return {"message": "Imagen coloreads y guardada exitosamente"}
