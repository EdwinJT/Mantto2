import streamlit as st
import pandas as pd
from datetime import datetime
import time
from supabase_client import init_supabase

st.set_page_config(page_title="Gestión de Mantenimiento", page_icon="🛠️", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .status-card {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        border: 1px solid #ddd;
    }
    .status-pendiente { background-color: #ffeeba; color: #856404; }
    .status-proceso { background-color: #b8daff; color: #004085; }
    .status-ejecuta { background-color: #c3e6cb; color: #155724; }
</style>
""", unsafe_allow_html=True)

# Initialize Supabase
supabase = init_supabase()

if not supabase:
    st.stop()

# --- Autenticación Simple ---
def check_password():
    """Returns `True` if the user had the correct password."""
    
    # Si no hay contraseña configurada en secrets, permitir acceso (modo desarrollo)
    # OJO: En producción SIEMPRE debe haber contraseña
    if "APP_PASSWORD" not in st.secrets:
        st.warning("⚠️ No se ha configurado contraseña (APP_PASSWORD). El acceso es libre.")
        return True

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "🔑 Ingrese la contraseña de acceso:", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password view, incorrect password.
        st.text_input(
            "🔑 Ingrese la contraseña de acceso:", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Contraseña incorrecta")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()

# --- Funciones Helper ---

def get_tasks(frente_filter=None):
    query = supabase.table("tareas").select("*").order("created_at", desc=True)
    if frente_filter and frente_filter != "Todos":
        query = query.eq("frente", frente_filter)
    response = query.execute()
    return response.data

def create_task(titulo, descripcion, responsable, frente, foto_file):
    foto_url = None
    if foto_file:
        try:
            file_path = f"task_photos/{datetime.now().strftime('%Y%m%d%H%M%S')}_{foto_file.name}"
            supabase.storage.from_("mantto_photos").upload(
                file_path, 
                foto_file.getvalue(), 
                {"content-type": foto_file.type}
            )
            # Get public URL
            foto_url = supabase.storage.from_("mantto_photos").get_public_url(file_path)
        except Exception as e:
            st.error(f"Error subiendo foto: {e}")

    data = {
        "titulo": titulo,
        "descripcion": descripcion,
        "responsable": responsable,
        "frente": frente,
        "foto_url": foto_url,
        "fecha_ingreso": datetime.now().isoformat(),
        "estado": "Pendiente"
    }
    supabase.table("tareas").insert(data).execute()

def update_status(task_id, new_status):
    update_data = {"estado": new_status}
    if new_status == "Ejecuta":
        update_data["fecha_salida"] = datetime.now().isoformat()
    
    supabase.table("tareas").update(update_data).eq("id", task_id).execute()

def update_task_details(task_id, titulo, descripcion, responsable, frente):
    data = {
        "titulo": titulo,
        "descripcion": descripcion,
        "responsable": responsable,
        "frente": frente
    }
    supabase.table("tareas").update(data).eq("id", task_id).execute()

# --- Sidebar: Nueva Tarea ---
with st.sidebar:
    st.header("➕ Nueva Tarea")
    with st.form("new_task_form", clear_on_submit=True):
        new_frente = st.selectbox("Frente / Ubicación", ["Frente 1", "Frente 2", "Taller", "Campo", "Oficina"], key="new_frente")
        new_titulo = st.text_input("Título")
        new_desc = st.text_area("Descripción")
        new_resp = st.text_input("Responsable")
        new_foto = st.file_uploader("Foto (Opcional)", type=['png', 'jpg', 'jpeg'])
        
        submitted = st.form_submit_button("Registrar Tarea")
        if submitted:
            if new_titulo:
                with st.spinner("Registrando..."):
                    create_task(new_titulo, new_desc, new_resp, new_frente, new_foto)
                st.success("Tarea registrada!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("El título es obligatorio.")

# --- Main App ---
st.title("🛠️ Control de Mantenimiento - Mantto2")

# Filtros
col_filter, col_refresh = st.columns([3, 1])
with col_filter:
    filter_frente = st.selectbox("📍 Filtrar por Frente:", ["Todos", "Frente 1", "Frente 2", "Taller", "Campo", "Oficina"])
with col_refresh:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Actualizar"):
        st.rerun()

tasks = get_tasks(filter_frente)

# Convert to DataFrame for easier handling if needed, but list of dicts is fine
if not tasks:
    st.info("No hay tareas registradas aun.")
else:
    # Kanban-like view
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔴 Pendientes")
        for task in tasks:
            if task['estado'] == 'Pendiente':
                with st.expander(f"**{task['titulo']}** ({task['frente']})", expanded=True):
                    st.markdown(f"_{task['descripcion']}_")
                    st.caption(f"👤 {task['responsable']} | 📅 {task['fecha_ingreso'][:10]}")
                    if task['foto_url']:
                        st.image(task['foto_url'], use_column_width=True)
                    
                    if st.button("▶️ Iniciar", key=f"start_{task['id']}"):
                        update_status(task['id'], "Proceso")
                        st.rerun()
                    
                    # Edit Logic (Simple approach via another expander or modal logic if desired, keeping it simple inline)
                    # For simplicity, let's keep edit in a consistent way or use a specialized "Edit" section if requested. 
                    # User asked for edits anywhere. Let's add a small "Edit" toggle.
                    if st.checkbox("Editar", key=f"edit_chk_{task['id']}"):
                         with st.form(key=f"edit_form_{task['id']}"):
                            ed_tit = st.text_input("Título", task['titulo'])
                            ed_desc = st.text_area("Desc", task['descripcion'])
                            ed_resp = st.text_input("Resp", task['responsable'])
                            ed_frente = st.selectbox("Frente", ["Frente 1", "Frente 2", "Taller", "Campo", "Oficina"], index=["Frente 1", "Frente 2", "Taller", "Campo", "Oficina"].index(task['frente']) if task['frente'] in ["Frente 1", "Frente 2", "Taller", "Campo", "Oficina"] else 0)
                            if st.form_submit_button("Guardar Cambios"):
                                update_task_details(task['id'], ed_tit, ed_desc, ed_resp, ed_frente)
                                st.success("Actualizado")
                                time.sleep(0.5)
                                st.rerun()

    with col2:
        st.markdown("### 🟡 En Proceso")
        for task in tasks:
            if task['estado'] == 'Proceso':
                with st.container(border=True): # New Streamlit container border
                    st.markdown(f"**{task['titulo']}**")
                    st.info(f"📍 {task['frente']}")
                    st.write(task['descripcion'])
                    st.caption(f"👤 {task['responsable']}")
                    if task['foto_url']:
                        st.image(task['foto_url'])
                    
                    if st.button("✅ Terminar", key=f"finish_{task['id']}"):
                        update_status(task['id'], "Ejecuta")
                        st.rerun()

    with col3:
        st.markdown("### 🟢 Ejecutado")
        for task in tasks:
            if task['estado'] == 'Ejecuta':
                with st.container(border=True):
                    st.markdown(f"~~{task['titulo']}~~")
                    st.caption(f"🏁 Finalizado: {task['fecha_salida'][:16] if task['fecha_salida'] else 'N/A'}")
                    st.write(f"_{task['descripcion']}_")
                    if task['foto_url']:
                        st.image(task['foto_url'])
