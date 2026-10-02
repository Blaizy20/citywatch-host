import codecs

# 1. Add Chart.js to admin_base.html globally
with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'r', 'utf-8') as f:
    html = f.read()

target = '''<script src="https://unpkg.com/idiomorph/dist/idiomorph.min.js"></script>'''
replacement = '''<script src="https://unpkg.com/idiomorph/dist/idiomorph.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'''

html = html.replace(target, replacement)

# Add fullscreenchange listener globally
target_css = '''  #admin-main-content { 
    transition: opacity 0.25s ease, transform 0.25s ease;
    view-transition-name: main;
  }'''

replacement_css = '''  #admin-main-content { 
    transition: opacity 0.25s ease, transform 0.25s ease;
    view-transition-name: main;
  }
  .chart-card:fullscreen {
    padding: 2rem !important;
    background-color: #ffffff !important;
    border-radius: 0 !important;
  }'''

html = html.replace(target_css, replacement_css)

target_script = '''    window.attachSPAListeners = function attachSPAListeners(container) {'''

replacement_script = '''    document.addEventListener('fullscreenchange', () => {
        document.querySelectorAll('.chart-card').forEach(card => {
            const btn = card.querySelector('.btn-fullscreen span');
            if (btn) {
                btn.innerText = document.fullscreenElement === card ? 'fullscreen_exit' : 'fullscreen';
            }
        });
    });

    window.attachSPAListeners = function attachSPAListeners(container) {'''

html = html.replace(target_script, replacement_script)

with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'w', 'utf-8') as f:
    f.write(html)
