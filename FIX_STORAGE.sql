-- Permitir SUBIR archivos al bucket 'mantto_photos' para todos (público)
create policy "Permitir Subir Fotos"
on storage.objects for insert
with check ( bucket_id = 'mantto_photos' );

-- Permitir VER archivos del bucket 'mantto_photos' para todos
create policy "Permitir Ver Fotos"
on storage.objects for select
using ( bucket_id = 'mantto_photos' );

-- Permitir ACTUALIZAR archivos (opcional, por si acaso)
create policy "Permitir Actualizar Fotos"
on storage.objects for update
with check ( bucket_id = 'mantto_photos' );
