# Guía de Despliegue a Producción (Streamlit Cloud)

Para que tus supervisores puedan acceder desde cualquier lugar (internet), necesitas alojar tu código en la nube. La forma más fácil y gratuita es usar **Streamlit Community Cloud**.

## Paso 1: Subir tu código a GitHub

Streamlit Cloud toma el código directamente de GitHub.

1.  Crea una cuenta en [GitHub.com](https://github.com) si no tienes una.
2.  Crea un **Nuevo Repositorio** (ponle `Mantto2`).
3.  Sube los archivos de tu carpeta `d:\Antigravity\Mantto2` a ese repositorio.
    *   **IMPORTANTE**: NO subas la carpeta `.streamlit` ni el archivo `secrets.toml` por seguridad. (Git suele ignorarlos si hay un `.gitignore`, si no, simplemente no los subas manualmente).
    *   Asegúrate de que `requirements.txt` esté subido.

## Paso 2: Conectar con Streamlit Cloud

1.  Ve a [share.streamlit.io](https://share.streamlit.io/).
2.  Inicia sesión con tu cuenta de GitHub.
3.  Haz clic en **"New app"**.
4.  Selecciona el repositorio `Mantto2` que acabas de crear.
5.  Branch: `main` (o master).
6.  Main file path: `app.py`.

## Paso 3: Configurar Secretos (Credenciales)

Como no subimos el archivo `secrets.toml` (porque tiene claves privadas), necesitas dárselas a Streamlit Cloud manualmente.

1.  Antes de darle a "Deploy", busca el botón o configuración de **"Advanced settings"** o **"Secrets"**.
2.  Te pedirá un cuadro de texto para llenar tus secretos. Copia y pega el contenido de tu archivo `secrets.toml` local:

```toml
SUPABASE_URL = "https://mmjtzzkxuqbdbhrgetdy.supabase.co"
SUPABASE_KEY = "sb_publishable_6IACz8NQyOXHr-D0DNMmaA_HmLdE_3G"
```

3.  Guarda.

## Paso 4: Desplegar

1.  Haz clic en **"Deploy!"**.
2.  Espera unos minutos mientras instalan las librerías.
3.  ¡Listo! Te darán una URL (ej. `https://mantto2.streamlit.app`) que puedes copiar y mandar por WhatsApp a tus supervisores.

## Notas Adicionales
-   **Base de Datos**: Como usamos Supabase, no necesitas hacer nada extra. La app en la nube se conectará a la misma base de datos que tu app local. Lo que registres aquí, se verá allá.
-   **Fotos**: Las fotos se guardan en el "Bucket" de Supabase, así que también serán visibles desde cualquier lado.
