import codecs

# 1. Extract notification block from resident header
with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_header.html', 'r', 'utf-8') as f:
    resident_content = f.read()

start_marker = '<div class="relative" id="notification-dropdown-container">'
end_marker = '</script>'
start_idx = resident_content.find(start_marker)
end_idx = resident_content.find(end_marker, start_idx) + len(end_marker)

notification_html = resident_content[start_idx:end_idx]

# 2. Inject into admin_base.html
with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'r', 'utf-8') as f:
    admin_content = f.read()

target = '<div class="flex items-center gap-2 bg-surface-container px-3 py-1.5 rounded-full border border-outline-variant">'
replacement = notification_html + '\n\n' + target

admin_content = admin_content.replace(target, replacement)

with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'w', 'utf-8') as f:
    f.write(admin_content)

print("Injected notification bell to admin_base.html successfully")
