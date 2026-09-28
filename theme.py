# -*- coding: utf-8 -*-
"""
theme.py
Paleta de colores y tipografias extraidas del diseno de Figma (src/index.css).
No modifiques los valores si quieres que el diseno se vea identico.
"""
import os
from kivy.core.text import LabelBase

# ---------------------------------------------------------------- utilidades
def rgba(hex_color, alpha=1.0):
    """Convierte '#5C7E8F' -> (0.36, 0.49, 0.56, alpha) que es lo que usa Kivy."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b, alpha)


# ------------------------------------------------------------------- colores
PRIMARY        = '#5C7E8F'   # --color-hr-primary
PRIMARY_LIGHT  = '#7A9BAC'   # --color-hr-primary-light
PRIMARY_DARK   = '#3E5E6E'   # --color-hr-primary-dark
SECONDARY      = '#A2A2A2'   # --color-hr-secondary (texto gris)
BG             = '#D4DDE2'   # --color-hr-bg (fondo)
SURFACE        = '#FFFFFF'   # --color-hr-surface
MUTED          = '#EEF2F5'   # --color-hr-muted
TEXT           = '#2C3E47'   # --color-hr-text
ORANGE         = '#F97316'   # badge "Urgente"
ORANGE_BG      = '#FFF3E8'
ORANGE_DOT     = '#FB923C'
EMERALD        = '#059669'   # "Disponibles sin conexion"
EMERALD_BG     = '#ECFDF5'
EMERALD_BORDER = '#A7F3D0'

C_PRIMARY       = rgba(PRIMARY)
C_PRIMARY_DARK  = rgba(PRIMARY_DARK)
C_PRIMARY_LIGHT = rgba(PRIMARY_LIGHT)
C_SECONDARY     = rgba(SECONDARY)
C_TEXT          = rgba(TEXT)
C_BG            = rgba(BG)
C_WHITE         = (1, 1, 1, 1)

# Vidrio (glassmorphism): Kivy no tiene backdrop-blur, se simula con
# blanco semitransparente + borde claro + sombra suave.
C_GLASS         = (1, 1, 1, 0.62)          # .glass-card
C_GLASS_BORDER  = (1, 1, 1, 0.45)
C_GLASS_MODAL   = (1, 1, 1, 0.94)          # .glass-modal
C_GLASS_DARK    = rgba(PRIMARY, 0.18)      # .glass-card-dark
C_SHADOW        = rgba(PRIMARY, 1.0)       # se usa con alpha variable
C_DIVIDER       = rgba(BG, 0.85)           # border-[#D4DDE2]/60
C_TINT_10       = rgba(PRIMARY, 0.10)      # bg-[#5C7E8F]/10
C_TINT_20       = rgba(PRIMARY, 0.20)

# ------------------------------------------------------------------- fuentes
# El diseno usa 'DM Sans' (texto) y 'JetBrains Mono' (el campo del RUT).
# Si colocas los .ttf en assets/fonts/ se usan; si no, Kivy usa Roboto.
_HERE = os.path.dirname(os.path.abspath(__file__))
_FONTS = os.path.join(_HERE, 'assets', 'fonts')

FONT = 'Roboto'
FONT_MONO = 'RobotoMono'


def _try_register(name, regular, bold=None, medium=None):
    reg = os.path.join(_FONTS, regular)
    if not os.path.exists(reg):
        return None
    kwargs = {'fn_regular': reg}
    for key, fname in (('fn_bold', bold), ('fn_italic', None)):
        if fname:
            path = os.path.join(_FONTS, fname)
            if os.path.exists(path):
                kwargs[key] = path
    LabelBase.register(name=name, **kwargs)
    return name


_dm = _try_register('DMSans', 'DMSans_18pt-Regular.ttf', bold='DMSans_18pt-Bold.ttf')
if _dm:
    FONT = _dm

_mono = _try_register('JetBrainsMono', 'JetBrainsMono-Regular.ttf')
if _mono:
    FONT_MONO = _mono
else:
    FONT_MONO = FONT
