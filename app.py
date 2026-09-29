from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image, ImageEnhance, ImageOps
try:
    from rembg import remove
    HAS_REMBG = True
except Exception:
    HAS_REMBG = False
    remove = None
import io

app = FastAPI(title="Photo Enhancer MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def enhance_image(img: Image.Image) -> Image.Image:
    # Auto contrast and subtle enhancements for product photos
    img = ImageOps.autocontrast(img, cutoff=1)
    
    # Slight brightness and color boost
    img = ImageEnhance.Brightness(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.12)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Sharpness(img).enhance(1.5)
    return img

def remove_bg_to_white(img: Image.Image) -> Image.Image:
    if not HAS_REMBG:
        # Fallback: just return original if rembg not available
        return img
    # Remove background, then composite on white
    # rembg returns RGBA with transparent background
    no_bg = remove(img)
    if no_bg.mode != "RGBA":
        no_bg = no_bg.convert("RGBA")
    
    white_bg = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, no_bg)
    return composited.convert("RGB")

@app.get("/")
def health():
    return {"status": "ok", "message": "Photo Enhancer MVP running"}

@app.post("/enhance")
async def enhance(file: UploadFile = File(...)):
    contents = await file.read()
    input_img = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # Step 1: white background
    white_img = remove_bg_to_white(input_img)
    # Step 2: enhance
    final_img = enhance_image(white_img)
    
    buf = io.BytesIO()
    final_img.save(buf, format="JPEG", quality=92)
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
