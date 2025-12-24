# Instrucciones Finales para Despliegue en Streamlit Cloud

¡Genial! Tu código ya está en GitHub. Ahora solo falta conectarlo.

## Pasos para conectar:

1.  Ve a [share.streamlit.io](https://share.streamlit.io/).
2.  Haz clic en **"New app"**.
3.  Selecciona tu repositorio: `EdwinJT/Mantto2`.
4.  En "Main file path" escribe: `app.py`.
5.  **IMPORTANTE**: Antes de darle a "Deploy", haz clic en **"Advanced settings"**.
6.  En el cuadro de "Secrets", pega esto:

```toml
SUPABASE_URL = "https://mmjtzzkxuqbdbhrgetdy.supabase.co"
SUPABASE_KEY = "sb_publishable_6IACz8NQyOXHr-D0DNMmaA_HmLdE_3G"
```

7.  Haz clic en **"Deploy!"**.

---
Una vez termine de cargar, tendrás un link (ej. `https://mantto2.streamlit.app`) que puedes copiar y mandar por WhatsApp a todos tus supervisores. Funcionará desde cualquier celular o PC.
