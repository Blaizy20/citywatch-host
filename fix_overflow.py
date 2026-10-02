import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'r', 'utf-8') as f:
    html = f.read()

target = 'class="chart-card bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 flex flex-col transition-all duration-300"'
replacement = 'class="chart-card bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 flex flex-col transition-all duration-300 overflow-hidden"'

html = html.replace(target, replacement)

target2 = 'class="chart-card bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 mb-8 flex flex-col transition-all duration-300"'
replacement2 = 'class="chart-card bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 mb-8 flex flex-col transition-all duration-300 overflow-hidden"'

html = html.replace(target2, replacement2)

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'w', 'utf-8') as f:
    f.write(html)
