# Declaración de uso de IA

Este documento registra el uso de inteligencia artificial en el desarrollo de
**FirmApp**, tal como lo pide el instrumento de evaluación **E2 — TINF1119
(Desarrollo Móvil A+S)**: "README.md con... declaración de uso de IA (si
aplica)".

- **Herramienta:** Claude Code (Anthropic), modelos Claude Opus 5.5 y Claude
  Sonnet 5, en una sesión de ejecución en la nube sobre este repositorio.
- **Fecha:** 28 de septiembre de 2026.
- **Conversación de referencia:** el estudiante compartió además un enlace a
  un chat previo de Claude sobre este mismo tema
  (`https://claude.ai/share/00e8712d-cca6-41f9-8cd7-cee73b506069`); el
  contenido de esa conversación no pudo recuperarse desde esta sesión (el
  enlace no expuso su contenido a una herramienta automática de lectura), por
  lo que este documento registra lo efectivamente pedido y hecho **en esta
  sesión**, que es la que realizó los cambios de código.
- **Sesión de esta ejecución (trazabilidad técnica):**
  `https://claude.ai/code/session_01KBjmqzBqPJ2Hs1HFW63rQu`

## Qué se le pidió a la IA (en orden)

1. **"Analiza el proyecto entero."** Revisión completa del repositorio
   (`main.py`, `widgets.py`, `theme.py`, `icons.py`, `interfazrrhh.kv`,
   `README.md`, `requirements.txt`), incluyendo ejecutar la app en un entorno
   sin pantalla (Xvfb) para verificar comportamiento real, no solo lectura de
   código.
2. **Aplicar las correcciones propuestas en ese análisis**, además de:
   - agregar esta declaración de uso de IA (`uso_ia.md`),
   - identificar si el proyecto usa `ScreenManager`,
   - revisar la rúbrica de evaluación (`.docx` adjunto) y hacer los cambios
     necesarios para cumplir sus requisitos.

## Qué encontró el análisis inicial

- El repositorio tenía versionado el entorno virtual `.venv/` completo (de
  Windows, 130 MB, 5.276 de los 5.291 archivos del repo), `__pycache__/` y
  dos `.zip` de fuentes redundantes; no existía `.gitignore`.
- `requirements.txt` solo tenía `kivy>=2.3.0` y le faltaba `kivymd`, pese a
  que toda la app depende de KivyMD 1.2.0.
- `theme.py` buscaba `DMSans-Regular.ttf` / `DMSans-Bold.ttf`, pero los
  archivos reales en `assets/fonts/` se llaman
  `DMSans_18pt-Regular.ttf` / `DMSans_18pt-Bold.ttf` → la app nunca cargaba
  DM Sans y usaba Roboto en silencio.
- Al cambiar de pestaña (RUT ↔ Dibujar Firma) y volver, el botón "Firmar con
  1 toque" quedaba habilitado aunque el campo/lienzo estuviera vacío de
  nuevo (el estado `_rut_valid` / `_has_signature` no se reiniciaba).
- `Pressable` (`widgets.py`) hacía `Window.bind(mouse_pos=...)` sin
  desconectarlo nunca: cada apertura del modal de firma dejaba listeners
  colgados en memoria.
- Al firmar, la pantalla de éxito solo ponía `opacity = 0` a la cabecera y
  las pestañas del modal, pero esos botones seguían recibiendo toques
  (invisibles pero clicables) detrás del mensaje de éxito.
- **No existía `ScreenManager`**: toda la app era una sola pantalla
  (`RootScreen`) con un modal (`ModalOverlay` + `SignatureModal`) superpuesto
  mediante `add_widget`/`remove_widget`, no navegación real entre pantallas.
- El botón "Firmar sin sesión" de `FooterCard`/`DesktopCtaCard` asumía que
  `PENDING` nunca estaría vacía (`PENDING[0]` sin verificar longitud).

## Qué se cambió en el código

### Limpieza de repositorio
- Se creó `.gitignore` (`.venv/`, `__pycache__/`, `*.pyc`, `*.zip`, etc.).
- Se quitaron del control de versiones y del disco `.venv/`, `__pycache__/`
  y los `.zip` de fuentes ya redundantes con los `.ttf` extraídos.
- `requirements.txt` ahora fija `kivy==2.3.1` y `kivymd==1.2.0` (las
  versiones que el propio `.kv` y el `README` exigen).

### Corrección de bugs
- `theme.py`: nombres de fuente corregidos a los archivos reales
  (`DMSans_18pt-Regular.ttf`, `DMSans_18pt-Bold.ttf`).
- `widgets.py` (`Pressable`): se agregó `on_parent()` para desconectar
  `Window.unbind(mouse_pos=...)` cuando el widget sale del árbol, evitando
  la fuga de memoria.
- `main.py` (`FooterCard`/`DesktopCtaCard.sign_pressed`): se agregó un
  chequeo de `PENDING` vacía antes de indexar `PENDING[0]`.

### Reestructuración a `ScreenManager` (requisito C2 de la rúbrica)
Se reemplazó el modal superpuesto por **3 pantallas navegables** con
`kivy.uix.screenmanager.ScreenManager`, creadas una sola vez en
`InterfazRRHHApp.build()`:

1. `HomeScreen` (`name='home'`) — envuelve el tablero existente
   (`RootScreen`) sin cambiar su lógica.
2. `SignScreen` (`name='sign'`) — aloja `SignPanel` (antes
   `SignatureModal`) con las pestañas RUT / Dibujar Firma.
3. `SuccessScreen` (`name='success'`) — pantalla de confirmación, con botón
   para volver a Inicio.

La navegación (`InterfazRRHHApp.go_to_sign`, `.go_to_success`, `.go_home`)
solo cambia `sm.current` con `SlideTransition`, sin crear ni destruir
widgets en cada viaje. Este cambio, además de cumplir el requisito técnico
de la evaluación, **corrigió de raíz** dos de los bugs encontrados:
- el estado de validación ya se reinicia explícitamente en
  `SignPanel.set_tab()` y en `SignPanel.reset_for()` (llamado cada vez que
  se entra a `SignScreen` con un documento nuevo);
- ya no queda ningún botón "invisible pero clicable" en la pantalla de
  éxito, porque ahora es una `Screen` distinta, no una superposición de
  opacidad sobre el mismo widget.

Se verificó el resultado ejecutando la app en un entorno sin pantalla
(Xvfb) con un script de prueba que recorre las 3 pantallas, fuerza el
cambio de pestañas, firma y vuelve a Inicio varias veces seguidas,
comprobando que el botón CTA se deshabilita correctamente al cambiar de
pestaña y que el número de listeners de `mouse_pos` no crece tras varios
ciclos de navegación. Se tomaron capturas reales de las 4 pantallas
(Inicio, Firmar-RUT, Firmar-Dibujo, Éxito) y se agregaron a
`assets/screenshots/` y al `README.md`.

### `README.md`
Se completó con las secciones que exige la rúbrica y que faltaban:
"Problema que resuelve", "Usuario objetivo", "Capturas de pantalla" y esta
"Declaración de uso de IA" (enlazando a este archivo). También se actualizó
la sección de estructura de archivos y se agregó la sección "Navegación
(ScreenManager)".

## Qué NO se generó con IA (y por qué)

La rúbrica exige además un documento `FUNDAMENTACION-UX-UI.md` con
metodología de investigación, hallazgos con **citas textuales reales** de
entrevistas/encuestas a usuarios, y una matriz hallazgo → decisión de
diseño. **Ese documento no fue creado en esta sesión**: requiere datos
primarios reales (entrevistas y encuestas que el estudiante debe haber
aplicado a su socio comunitario/usuarios), y no existe ese material en este
repositorio ni fue provisto en la conversación. Inventar citas o porcentajes
de usuarios inexistentes sería presentar evidencia falsa como si fuera
investigación real, algo que la IA no debe hacer. **Queda pendiente que el
estudiante complete `FUNDAMENTACION-UX-UI.md` con su propia investigación**
(criterio A de la rúbrica, 30 % de la nota).

## Qué revisó la IA de la rúbrica y no alcanzó a resolver

- Criterio A (Fundamentación UX/UI, 30 pts): pendiente, por el motivo
  anterior.
- Criterio D (presentación oral, 15 pts): no aplica a un cambio de código;
  es responsabilidad del estudiante al exponer.

## Cómo se usó el resultado

Todo el código generado por la IA fue revisado, ejecutado y probado en este
mismo proceso antes de darlo por válido (ver "Reestructuración a
`ScreenManager`" arriba). El estudiante es responsable de revisar el diff
final, entender los cambios y poder explicarlos en la presentación oral,
como exige la rúbrica (D2 — "Fundamentación al exponer").
