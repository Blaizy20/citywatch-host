import codecs

with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_sidebar.html', 'r', 'utf-8') as f:
    html = f.read()

target = '</nav>'
replacement = """</nav>

<div class="p-3 border-t border-outline-variant">
  <a href="#" onclick="event.preventDefault(); document.getElementById('logout-modal').showModal();" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-error hover:bg-error-container hover:text-on-error-container transition-all text-sm font-semibold">
    <span class="material-symbols-outlined shrink-0 group-hover:scale-110 transition-transform">logout</span>
    <span class="transition-opacity duration-200 whitespace-nowrap group-data-[collapsed=true]/sidebar:opacity-0 group-data-[collapsed=true]/sidebar:hidden">Log Out</span>
  </a>
</div>"""

html = html.replace(target, replacement, 1)

with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_sidebar.html', 'w', 'utf-8') as f:
    f.write(html)
