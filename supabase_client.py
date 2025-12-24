import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_supabase() -> Client:
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Error connecting to Supabase: {e}")
        st.warning("Please make sure you have set SUPABASE_URL and SUPABASE_KEY in .streamlit/secrets.toml")
        return None
