import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'r', 'utf-8') as f:
    html = f.read()

target = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
replacement = '''<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'''

html = html.replace(target, replacement)

with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'w', 'utf-8') as f:
    f.write(html)
