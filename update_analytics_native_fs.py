import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'r', 'utf-8') as f:
    html = f.read()

target = '''<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'''
html = html.replace(target, '')

# We also need to update the onclick logic for all 4 buttons to use native API
def replace_fullscreen_logic(html):
    old_onclick = '''const card = this.closest('.chart-card'); card.classList.toggle('fixed'); card.classList.toggle('inset-0'); card.classList.toggle('z-[100]'); card.classList.toggle('rounded-none'); card.classList.toggle('w-screen'); card.classList.toggle('h-screen'); this.querySelector('span').innerText = card.classList.contains('fixed') ? 'fullscreen_exit' : 'fullscreen'; setTimeout(() => window.dispatchEvent(new Event('resize')), 100);'''
    new_onclick = '''const card = this.closest('.chart-card'); if (!document.fullscreenElement) { card.requestFullscreen().catch(e => console.error(e)); } else { document.exitFullscreen(); }'''
    html = html.replace(old_onclick, new_onclick)
    
    # Add .btn-fullscreen class to the buttons so the global listener can find them
    old_class1 = '''class="text-on-surface-variant hover:text-primary transition-colors p-1 rounded-md hover:bg-surface-container-low flex items-center justify-center" title="Toggle Fullscreen"'''
    new_class1 = '''class="btn-fullscreen text-on-surface-variant hover:text-primary transition-colors p-1 rounded-md hover:bg-surface-container-low flex items-center justify-center" title="Toggle Fullscreen"'''
    html = html.replace(old_class1, new_class1)
    
    old_class2 = '''class="text-on-surface-variant hover:text-primary transition-colors p-2 rounded-xl hover:bg-surface-container-low flex items-center justify-center" title="Toggle Fullscreen"'''
    new_class2 = '''class="btn-fullscreen text-on-surface-variant hover:text-primary transition-colors p-2 rounded-xl hover:bg-surface-container-low flex items-center justify-center" title="Toggle Fullscreen"'''
    html = html.replace(old_class2, new_class2)
    
    return html

html = replace_fullscreen_logic(html)

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'w', 'utf-8') as f:
    f.write(html)
