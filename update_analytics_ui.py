import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Add Filter Dropdown to Header
target_header = '''<div class="mb-8 flex flex-wrap items-end justify-between gap-3">
<div>
<h1 class="text-3xl font-bold font-display text-on-surface tracking-tight flex items-center gap-2">
<span class="material-symbols-outlined text-primary text-[32px]">monitoring</span>
Analytics Hub
</h1>
<p class="mt-1 max-w-2xl text-sm text-on-surface-variant font-medium">Deep-dive into comprehensive statistics and reporting trends.</p>
</div>
<a href="{% url 'analytics_dashboard' %}"'''

replacement_header = '''<div class="mb-8 flex flex-wrap items-end justify-between gap-3">
<div>
<h1 class="text-3xl font-bold font-display text-on-surface tracking-tight flex items-center gap-2">
<span class="material-symbols-outlined text-primary text-[32px]">monitoring</span>
Analytics Hub
</h1>
<p class="mt-1 max-w-2xl text-sm text-on-surface-variant font-medium">Deep-dive into comprehensive statistics and reporting trends.</p>
</div>
<div class="flex items-center gap-4">
  <form method="GET" class="flex items-center gap-2" id="timeframe-form">
    <label for="timeframe" class="text-sm font-bold text-on-surface-variant">Timeframe:</label>
    <select name="timeframe" id="timeframe" class="text-sm font-semibold text-primary bg-surface-container-low border border-outline-variant rounded-lg px-3 py-1.5 focus:ring-primary focus:border-primary cursor-pointer" onchange="this.form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }))">
      <option value="7" {% if timeframe == '7' %}selected{% endif %}>Last 7 Days</option>
      <option value="30" {% if timeframe == '30' %}selected{% endif %}>Last 30 Days</option>
      <option value="90" {% if timeframe == '90' %}selected{% endif %}>Last 90 Days</option>
      <option value="all" {% if timeframe == 'all' %}selected{% endif %}>All Time</option>
    </select>
  </form>
  <a href="{% url 'analytics_dashboard' %}"'''

html = html.replace(target_header, replacement_header)

# 2. Add Trend Chart before Charts Row
target_charts = '''<!-- Charts Row -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">'''

replacement_charts = '''<!-- Trend Line Chart -->
<div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 mb-8 flex flex-col">
  <div class="flex items-center justify-between mb-4">
    <div>
      <h3 class="font-bold text-lg text-on-surface">Submission Trend</h3>
      <p class="text-xs font-medium text-on-surface-variant">Volume of incoming reports over time</p>
    </div>
    <span class="material-symbols-outlined text-on-surface-variant">trending_up</span>
  </div>
  <div class="relative w-full h-72">
    <canvas id="trendChart"></canvas>
  </div>
</div>

<!-- Charts Row -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">'''

html = html.replace(target_charts, replacement_charts)

# 3. Add Trend Chart JS
target_js = '''    // Chart.js Configuration
    const statusLabels ='''

replacement_js = '''    // Chart.js Configuration
    const trendLabels = [{% for item in trend_data %}'{{ item.date }}',{% endfor %}];
    const trendData = [{% for item in trend_data %}{{ item.count }},{% endfor %}];

    const statusLabels ='''

html = html.replace(target_js, replacement_js)

target_js_destroy = '''    if (window.statusChartInst) window.statusChartInst.destroy();
    if (window.categoryChartInst) window.categoryChartInst.destroy();
    if (window.barangayChartInst) window.barangayChartInst.destroy();'''

replacement_js_destroy = '''    if (window.trendChartInst) window.trendChartInst.destroy();
    if (window.statusChartInst) window.statusChartInst.destroy();
    if (window.categoryChartInst) window.categoryChartInst.destroy();
    if (window.barangayChartInst) window.barangayChartInst.destroy();'''

html = html.replace(target_js_destroy, replacement_js_destroy)

target_js_init = '''    // 1. Status Donut Chart'''

replacement_js_init = '''    // 0. Trend Line Chart
    const ctxTrend = document.getElementById('trendChart').getContext('2d');
    let trendGradient = ctxTrend.createLinearGradient(0, 0, 0, 300);
    trendGradient.addColorStop(0, 'rgba(21, 107, 62, 0.25)'); // primary
    trendGradient.addColorStop(1, 'rgba(21, 107, 62, 0.0)');

    window.trendChartInst = new Chart(ctxTrend, {
        type: 'line',
        data: {
            labels: trendLabels,
            datasets: [{
                label: 'Reports Submitted',
                data: trendData,
                borderColor: '#156b3e',
                backgroundColor: trendGradient,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: '#156b3e',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#f3f4f9', drawBorder: false },
                    ticks: { precision: 0 }
                },
                x: {
                    grid: { display: false, drawBorder: false }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });

    // 1. Status Donut Chart'''

html = html.replace(target_js_init, replacement_js_init)

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'w', 'utf-8') as f:
    f.write(html)
