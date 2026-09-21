import io
import os
import shutil
import tempfile
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Mode,
    RectangleRounded,
    Text,
    add,
    export_stl,
    extrude,
    offset,
)

app = FastAPI(title="3D Text Banner Generator")

BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = BASE_DIR / "fonts"
FONTS_DIR.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def build_banner_stl(
    text: str,
    font_path: str,
    style: Literal["solid", "outline"],
    outline_width: float,
    font_size: float,
    text_relief: float,
    plate_thickness: float,
    padding_x: float,
    padding_y: float,
    corner_radius: float,
) -> bytes:
    """Generates an STL model in memory using build123d."""
    with BuildPart() as model:
        # 1. Measure text boundary
        with BuildSketch() as measure_sketch:
            Text(
                text,
                font_size=font_size,
                font_path=font_path,
                align=(Align.CENTER, Align.CENTER),
            )
        bbox = measure_sketch.sketch.bounding_box()
        plate_w = bbox.size.X + (padding_x * 2)
        plate_h = bbox.size.Y + (padding_y * 2)

        # 2. Backing baseplate
        with BuildSketch():
            if corner_radius > 0:
                # Constrain radius so it cannot exceed half the shortest dimension
                max_rad = min(plate_w, plate_h) / 2.1
                RectangleRounded(plate_w, plate_h, radius=min(corner_radius, max_rad))
            else:
                RectangleRounded(plate_w, plate_h, radius=0.0)
        extrude(amount=plate_thickness)

        # 3. Text on top face
        top_face = model.faces().sort_by(Axis.Z)[-1]
        with BuildSketch(top_face):
            if style == "solid":
                Text(
                    text,
                    font_size=font_size,
                    font_path=font_path,
                    align=(Align.CENTER, Align.CENTER),
                )
            elif style == "outline":
                with BuildSketch() as base_text:
                    Text(
                        text,
                        font_size=font_size,
                        font_path=font_path,
                        align=(Align.CENTER, Align.CENTER),
                    )
                offset(amount=outline_width, mode=Mode.ADD)
                add(base_text.sketch, mode=Mode.SUBTRACT)

        extrude(amount=text_relief)

    # 4. Export to STL via an in-memory buffer / temp file
    with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        export_stl(model.part, tmp_path)
        with open(tmp_path, "rb") as f:
            stl_data = f.read()
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return stl_data


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    built_in_fonts = [f.name for f in FONTS_DIR.glob("*.ttf")] + [f.name for f in FONTS_DIR.glob("*.otf")]
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"fonts": built_in_fonts}
    )

@app.post("/generate")
async def generate_stl(
    text: str = Form("SAMPLE"),
    style: Literal["solid", "outline"] = Form("solid"),
    outline_width: float = Form(1.2),
    font_size: float = Form(20.0),
    text_relief: float = Form(1.6),
    plate_thickness: float = Form(2.4),
    padding_x: float = Form(8.0),
    padding_y: float = Form(6.0),
    corner_radius: float = Form(3.0),
    selected_font: str = Form(""),
    custom_font_file: UploadFile = File(None),
):
    temp_font_path = None
    try:
        # Determine whether to use uploaded TTF or pre-installed font
        if custom_font_file and custom_font_file.filename:
            suffix = Path(custom_font_file.filename).suffix.lower()
            if suffix not in [".ttf", ".otf"]:
                raise HTTPException(status_code=400, detail="Only .ttf and .otf font files are supported.")
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
                temp_font_path = f.name
                shutil.copyfileobj(custom_font_file.file, f)
            font_path = temp_font_path
        elif selected_font:
            font_path = str(FONTS_DIR / selected_font)
            if not Path(font_path).exists():
                raise HTTPException(status_code=404, detail="Selected font does not exist.")
        else:
            raise HTTPException(status_code=400, detail="Please select a preset font or upload a TTF.")

        # Generate STL
        stl_bytes = build_banner_stl(
            text=text.strip(),
            font_path=font_path,
            style=style,
            outline_width=outline_width,
            font_size=font_size,
            text_relief=text_relief,
            plate_thickness=plate_thickness,
            padding_x=padding_x,
            padding_y=padding_y,
            corner_radius=corner_radius,
        )

        safe_filename = "".join(c for c in text if c.isalnum() or c in ("-", "_")).strip() or "banner"
        filename = f"{safe_filename}_{style}.stl"

        return Response(
            content=stl_bytes,
            media_type="model/stl",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    finally:
        if temp_font_path and os.path.exists(temp_font_path):
            os.remove(temp_font_path)



