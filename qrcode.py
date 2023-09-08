#!/usr/bin/env python3
import segno

qrcode = segno.make("https://www.pythonwa.com", error="h")
qrcode.to_artistic(
    background="frontend/src/assets/pythonwa.png",
    target="pythonwa_qr_fancy.png",
    scale=20,
    border=0,
    dark="#295377",
)
qrcode.save(
    out="pythonwa_qr_simple.png",
    scale=20,
    border=0,
    dark="#295377",
    light="#FFFFFF",
    data_light="#ffe15f",
)
