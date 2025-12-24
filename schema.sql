-- Create table for Tasks
create table if not exists tareas (
  id uuid default gen_random_uuid() primary key,
  created_at timestamptz default now(),
  titulo text not null,
  descripcion text,
  estado text default 'Pendiente', -- 'Pendiente', 'Proceso', 'Ejecuta'
  fecha_ingreso timestamptz default now(),
  fecha_salida timestamptz,
  foto_url text,
  responsable text,
  frente text -- Ubicación del trabajo
);

-- Enable Row Level Security (RLS)
alter table tareas enable row level security;

-- Create policy to allow all actions for now (public access for simplicity as requested 'interactivo')
-- NOTE: In a production environment with auth, we would restrict this.
create policy "Allow all access to tareas"
on tareas for all
using (true)
with check (true);

-- Create Storage Bucket for Photos if it doesn't exist
-- Policy for storage must be set in the Supabase Dashboard > Storage > Policies
