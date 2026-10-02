import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'r', 'utf-8') as f:
    admin_html = f.read()

target = "window.openLogoutModal(event)"
replacement = "event.preventDefault(); document.getElementById('logout-modal').showModal();"

if target in admin_html:
    admin_html = admin_html.replace(target, replacement)
    
    with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'w', 'utf-8') as f:
        f.write(admin_html)
    print('Fixed logout modal in admin profile dropdown')
else:
    print('Target not found')
