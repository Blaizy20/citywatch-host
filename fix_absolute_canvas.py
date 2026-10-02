import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'r', 'utf-8') as f:
    html = f.read()

target1 = '<canvas id="trendChart"></canvas>'
replacement1 = '<canvas id="trendChart" class="absolute inset-0 w-full h-full"></canvas>'
html = html.replace(target1, replacement1)

target2 = '<canvas id="statusChart"></canvas>'
replacement2 = '<canvas id="statusChart" class="absolute inset-0 w-full h-full"></canvas>'
html = html.replace(target2, replacement2)

target3 = '<canvas id="categoryChart"></canvas>'
replacement3 = '<canvas id="categoryChart" class="absolute inset-0 w-full h-full"></canvas>'
html = html.replace(target3, replacement3)

target4 = '<canvas id="barangayChart"></canvas>'
replacement4 = '<canvas id="barangayChart" class="absolute inset-0 w-full h-full"></canvas>'
html = html.replace(target4, replacement4)

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'w', 'utf-8') as f:
    f.write(html)
