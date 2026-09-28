# Fundamentación UX/UI — FirmApp (Interfaz de Recursos Humanos)

**Asignatura:** TINF1119 — Desarrollo Móvil (A+S)  
**Institución:** Instituto Tecnológico UC Temuco  
**Proyecto:** FirmApp (Maqueta Funcional en Kivy / KivyMD)  
**Integrantes:** `zikness`  

---

## 1. Metodología de Investigación de Usuarios (Subcriterio A1 — 5 pts)

Para el diseño centrado en el usuario de **FirmApp**, se aplicó un instrumento cuantitativo-cualitativo mediante un **formulario de diagnóstico en Google Forms** enfocado en el contexto del socio comunitario y la comunidad universitaria/laboral.

### Ficha Técnica de la Muestra
* **Total de participantes:** 11 respuestas completas.
* **Distribución por Rol Actual:**
  * **Otro:** 45,5 % (5 participantes)
  * **Estudiante (con ayudantía, pasantía o trabajo externo):** 27,3 % (3 participantes)
  * **Personal Administrativo / Profesional UCT:** 18,2 % (2 participantes)
  * **Docente / Académico(a) UCT:** 9,1 % (1 participante)
* **Tamaño de Organización de los Participantes:**
  * **Grande (más de 50 personas):** 36,4 % (4 participantes)
  * **No aplica / Independiente:** 27,3 % (3 participantes)
  * **Equipo pequeño (1 a 10 personas):** 18,2 % (2 participantes)
  * **Mediano (11 a 50 personas):** 18,2 % (2 participantes)

---

## 2. Resultados Principales con Evidencia (Subcriterio A2 — 10 pts)

A partir del análisis de las 11 respuestas recolectadas, se identificaron los siguientes hallazgos y evidencias clave:

1. **Alta Insatisfacción con el Proceso Actual:**
   * El **54,6 %** de los encuestados califica la rapidez y facilidad de su proceso actual como insatisfactorio (evaluado con notas **1 o 2** en escala de 1 a 5, con un **36,4 % evaluando con la nota mínima 1**).
2. **Fragmentación de Medios de Gestión:**
   * Un **50 % (5 de 10)** usa intranet o sistemas institucionales, pero coexiste con medios tradicionales: un **40 % (4 de 10)** gestiona en **papel impreso y firmando a mano** y otro **40 % (4 de 10)** mediante **archivos PDF por correo electrónico**.
3. **Puntos de Dolor y Frustraciones Principales:**
   * **36,4 % (4 encuestados):** Le frena tener que encender el computador sí o sí para realizar un trámite de RRHH.
   * **36,4 % (4 encuestados):** Se molesta por no recibir avisos ni notificaciones cuando hay documentos nuevos.
   * **27,3 % (3 encuestados):** Señala que las páginas web actuales no están optimizadas para la pantalla del teléfono celular.
   * **18,2 % (2 encuestados):** Manifiesta que los PDFs se pierden en el correo o que los documentos demoran mucho en ser firmados.
4. **Funcionalidades Más Demandadas para la App:**
   * **72,7 % (8 de 11 encuestados):** Exige **firmar contratos o liquidaciones de un toque desde el celular**.
   * **54,5 % (6 de 11 encuestados):** Requiere **pedir vacaciones o permisos administrativos en un par de clics**.
   * **45,5 % (5 de 11 encuestados):** Solicita **ver y descargar liquidaciones** y recibir **alertas/notificaciones push** al celular.
5. **Valoración de la Solución Móvil:**
   * El **54,5 % (6 de 11)** le asigna la máxima nota (**5/5**) a la utilidad de resolver estos trámites desde una app móvil en lugar de usar PC o ir presencialmente. Además, el **54,5 %** está dispuesto a probar la versión beta de la aplicación.

---

## 3. Matriz Hallazgo → Decisión de Diseño (UX/UI) (Subcriterio A3 — 10 pts)

La siguiente matriz conecta los resultados cuantitativos directos de la encuesta con las decisiones concretas implementadas en el código de **FirmApp** (Python + KivyMD):

| ID | Hallazgo Cuantitativo (Evidencia) | Decisión de Interfaz (UI/UX) en FirmApp | Justificación Técnica de Diseño |
| :--- | :--- | :--- | :--- |
| **H1** | **72,7 %** exige firmar documentos "de un toque" desde el celular. | **Tarjetas de Acción Directa (`MDCard`):** Inclusión de botones prominentes en cada tarjeta para procesar o firmar solicitudes pendientes (`PENDING`) con una sola pulsación. | Elimina menús anidados y reduce la fricción, permitiendo completar la tarea principal en 1 paso táctil. |
| **H2** | **36,4 %** rechaza encender la PC y **27,3 %** critica webs no adaptadas a móviles. | **Diseño Mobile-First Nativo (`420x880` px):** Configuración del viewport en `main.py` ajustado a proporciones de teléfono móvil. | Garantiza una visualización limpia, elementos táctiles de tamaño adecuado e interfaz adaptada a pantallas verticales. |
| **H3** | **36,4 %** sufre por no recibir avisos ni saber si hay documentos nuevos. | **Sección Destacada de Pendientes (`PENDING`):** Carga dinámica en `main.py` que agrupa en la parte superior del Dashboard todas las tareas que requieren atención inmediata. | Proporciona visibilidad clara del estado del sistema sin obligar al usuario a buscar entre carpetas o correos. |
| **H4** | **54,5 %** solicita gestionar permisos y vacaciones en "un par de clics". | **Formulario Simplificado de Permisos (`interfazrrhh.kv`):** Estructura declarativa de inputs con `MDTextField` y botones de validación rápida. | Agiliza la solicitud de permisos administrativos eliminando campos innecesarios y guiando al usuario paso a paso. |
| **H5** | **40 %** aún depende del papel impreso o correos donde se pierden los PDFs. | **Historial Organizado (`RECENT`):** Categorización clara en el archivo KV entre documentos procesados recientemente y aquellos por tramitar. | Centraliza la documentación laboral en un solo lugar, evitando pérdidas en la bandeja de entrada del correo. |

---

## 4. Justificación de la Estructura de la App y Navegación (Subcriterio A4 — 3 pts)

La arquitectura de información de **FirmApp** responde a la necesidad de **rapidez e inmediatez** expresada por los usuarios (donde el 54,6 % calificó de difícil su sistema actual). La app se organiza mediante `ScreenManager` en un flujo ágil:

1. **Pantalla Principal / Dashboard (`PantallaInicio`):**
   * **Objetivo:** Mostrar de forma inmediata el listado de elementos `PENDING` (pendientes de firma o revisión) y `RECENT` (historial).
   * **Razón de UX:** Responde al **72,7 %** que busca firmar rápido y al **36,4 %** que necesita saber qué tiene pendiente apenas abre la aplicación.
2. **Pantalla de Detalle y Formulario (`PantallaFormulario`):**
   * **Objetivo:** Permitir la solicitud de permisos/vacaciones e ingreso de datos.
   * **Razón de UX:** Responde al **54,5 %** que desea pedir permisos en un par de clics mediante campos limpios de `MDTextField`.
3. **Pantalla de Confirmación / Estado (`PantallaEstado`):**
   * **Objetivo:** Mostrar la confirmación visual del trámite o la firma digital realizada.
   * **Razón de UX:** Da certeza al usuario de que el documento fue enviado/firmado correctamente, eliminando la incertidumbre del correo o papel.

---

## 5. Consideraciones de Diversidad y Accesibilidad (Subcriterio A5 — 2 pts)

Considerando que la muestra de usuarios incluye desde estudiantes con ayudantía hasta personal administrativo y docentes con variados niveles de familiaridad tecnológica y contextos de trabajo (desde independientes hasta organizaciones de más de 50 personas):

* **Claridad Tipográfica y Jerarquía Visual:** Se aplican las directrices de Material Design a través de KivyMD, utilizando contraste de color adecuado para lectura en dispositivos móviles en cualquier entorno laboral.
* **Blanqueo de Tecnology Gap (Brecha Digital):** Al diseñar botones amplios (`MDButton`) y tarjetas interactivas (`MDCard`), se facilita el toque para personas no familiarizadas con interfaces complejas de escritorio o intranets institucionales tradicionales.
* **Mensajes Claros y Directos:** Se evita el lenguaje burocrático, utilizando nomenclaturas cotidianas como *"Firmar"*, *"Pendientes"* y *"Permisos"*.