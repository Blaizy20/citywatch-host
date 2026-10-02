import codecs

# 1. Update resident_sidebar.html
with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_sidebar.html', 'r', 'utf-8') as f:
    sidebar_html = f.read()

target1 = """<a href="#" onclick="event.preventDefault(); document.getElementById('logout-modal').showModal();" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-error hover:bg-error-container hover:text-on-error-container transition-all text-sm font-semibold">"""
replacement1 = """<a href="#" onclick="window.openLogoutModal(event)" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-error hover:bg-error-container hover:text-on-error-container transition-all text-sm font-semibold">"""

if target1 in sidebar_html:
    sidebar_html = sidebar_html.replace(target1, replacement1)

with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_sidebar.html', 'w', 'utf-8') as f:
    f.write(sidebar_html)


# 2. Update resident_header.html
with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_header.html', 'r', 'utf-8') as f:
    header_html = f.read()

target2 = """      <div class="h-px bg-outline-variant/30 my-1 mx-2"></div>
      <a href="#" onclick="window.openLogoutModal(event)" class="flex items-center gap-3 p-3 rounded-lg hover:bg-error-container/50 text-error transition-colors font-medium text-sm group">
        <span class="material-symbols-outlined text-[20px] group-hover:-translate-x-1 transition-transform">logout</span> Logout
      </a>"""

if target2 in header_html:
    header_html = header_html.replace(target2, "")
else:
    print('Header target not found')

with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_header.html', 'w', 'utf-8') as f:
    f.write(header_html)
