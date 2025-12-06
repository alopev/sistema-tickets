"""
Script para actualizar la visualización del estado en el chat
Agrega badges de "En línea" / "Desconectado"
"""

# Leer el archivo base.html
with open('app/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar y reemplazar la sección del chat
old_code = """          var unreadCount = unreadMessages[user.id] || 0;
          var badgeHtml = unreadCount > 0 ? '<span class="badge bg-danger rounded-pill ms-auto">' + unreadCount + '</span>' : '';

          userDiv.id = 'user-list-item-' + user.id;
          userDiv.innerHTML = '<div class="d-flex align-items-center" style="width: 100%;">' +
            '<img src="/static/' + user.profile_picture + '" class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">' +
            '<div><strong>' + user.username + '</strong>' +
            '<small class="text-muted d-block">' + user.role + '</small></div>' + 
            badgeHtml + '</div>';"""

new_code = """          var unreadCount = unreadMessages[user.id] || 0;
          var badgeHtml = unreadCount > 0 ? '<span class="badge bg-danger rounded-pill ms-auto">' + unreadCount + '</span>' : '';
          
          // Status badge with text
          var statusBadge = user.is_online 
            ? '<span class="badge bg-success" style="font-size: 0.65em;">En línea</span>' 
            : '<span class="badge bg-secondary" style="font-size: 0.65em;">Desconectado</span>';

          userDiv.id = 'user-list-item-' + user.id;
          userDiv.innerHTML = '<div class="d-flex align-items-center" style="width: 100%;">' +
            '<img src="/static/' + user.profile_picture + '" class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">' +
            '<div style="flex-grow: 1;"><strong>' + user.username + '</strong>' +
            '<br>' + statusBadge + ' <small class="text-muted">' + user.role + '</small></div>' + 
            badgeHtml + '</div>';"""

if old_code in content:
    content = content.replace(old_code, new_code)
    
    # Guardar el archivo
    with open('app/templates/base.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Archivo actualizado exitosamente!")
    print("   Ahora el chat mostrará 'En línea' o 'Desconectado' para cada usuario")
    print("\n📝 Reinicia el servidor para ver los cambios:")
    print("   1. Presiona Ctrl + C")
    print("   2. Ejecuta: python run.py")
else:
    print("❌ No se encontró el código a reemplazar")
    print("   El archivo puede haber sido modificado manualmente")
