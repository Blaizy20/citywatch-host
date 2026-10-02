import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/map_view.html', 'r', 'utf-8') as f:
    html = f.read()

target = """L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);"""

replacement = """L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);"""

if target in html:
    html = html.replace(target, replacement)
else:
    print("Could not find target string")

with codecs.open('d:/citywatch/analytics/templates/analytics/map_view.html', 'w', 'utf-8') as f:
    f.write(html)
