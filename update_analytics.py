import codecs

html_content = """{% extends 'analytics/admin_base.html' %}
{% load static %}

{% block extra_head %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
{% endblock %}

{% block content %}
<div class="mx-auto max-w-7xl px-4 py-2 sm:px-6 lg:px-8 w-full">

<!-- Header Area -->
<div class="mb-8 flex flex-wrap items-end justify-between gap-3">
<div>
<h1 class="text-3xl font-bold font-display text-on-surface tracking-tight flex items-center gap-2">
<span class="material-symbols-outlined text-primary text-[32px]">monitoring</span>
Analytics Hub
</h1>
<p class="mt-1 max-w-2xl text-sm text-on-surface-variant font-medium">Deep-dive into comprehensive statistics and reporting trends.</p>
</div>
<a href="{% url 'analytics_dashboard' %}" data-no-spa="true" onclick="if(window.history.length > 1) { event.preventDefault(); this.querySelector('span').classList.add('-translate-x-4', 'opacity-0'); setTimeout(() => window.history.back(), 150); }" class="inline-flex items-center gap-1.5 text-sm font-bold text-on-surface-variant hover:text-primary transition-colors group p-2 hover:bg-surface-container-low rounded-full -mr-2"><span class="material-symbols-outlined text-[20px] transition-all duration-300 group-hover:-translate-x-1 group-active:scale-75">arrow_back</span> Dashboard</a>
</div>

<!-- Overview Stats Cards -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between relative overflow-hidden group">
    <div class="absolute -right-4 -top-4 w-24 h-24 bg-primary opacity-[0.03] rounded-full group-hover:scale-150 transition-transform duration-500"></div>
    <div class="flex justify-between items-start mb-2">
      <p class="text-[11px] font-bold text-on-surface-variant uppercase tracking-wider">Total Reports</p>
      <span class="material-symbols-outlined text-primary bg-primary-container p-1.5 rounded-lg text-[20px]">assignment</span>
    </div>
    <div class="flex items-end gap-2 mt-2">
      <h3 class="text-4xl font-display font-bold text-on-surface counter" data-target="{{ total_reports }}">0</h3>
      <span class="text-xs font-semibold text-[#166534] mb-1.5 bg-[#166534]/10 px-1.5 py-0.5 rounded">All time</span>
    </div>
  </div>

  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between relative overflow-hidden group">
    <div class="absolute -right-4 -top-4 w-24 h-24 bg-secondary opacity-[0.03] rounded-full group-hover:scale-150 transition-transform duration-500"></div>
    <div class="flex justify-between items-start mb-2">
      <p class="text-[11px] font-bold text-on-surface-variant uppercase tracking-wider">Resolution Time</p>
      <span class="material-symbols-outlined text-secondary bg-secondary-container p-1.5 rounded-lg text-[20px]">timer</span>
    </div>
    <div class="flex items-end gap-2 mt-2">
      <h3 class="text-4xl font-display font-bold text-on-surface">{% if avg_resolution_days %}{{ avg_resolution_days }}{% else %}0{% endif %}</h3>
      <span class="text-sm font-semibold text-on-surface-variant mb-1.5">days avg</span>
    </div>
  </div>

  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between relative overflow-hidden group">
    <div class="absolute -right-4 -top-4 w-24 h-24 bg-[#d97706] opacity-[0.03] rounded-full group-hover:scale-150 transition-transform duration-500"></div>
    <div class="flex justify-between items-start mb-2">
      <p class="text-[11px] font-bold text-on-surface-variant uppercase tracking-wider">Pending Action</p>
      <span class="material-symbols-outlined text-[#d97706] bg-[#fef3c7] p-1.5 rounded-lg text-[20px]">pending_actions</span>
    </div>
    <div class="flex items-end gap-2 mt-2">
      {% for item in status_data %}
        {% if item.label == 'pending' %}
          <h3 class="text-4xl font-display font-bold text-on-surface counter" data-target="{{ item.count }}">0</h3>
          <span class="text-xs font-semibold text-[#d97706] mb-1.5 bg-[#fef3c7] px-1.5 py-0.5 rounded">Requires review</span>
        {% endif %}
      {% endfor %}
    </div>
  </div>

  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between relative overflow-hidden group">
    <div class="absolute -right-4 -top-4 w-24 h-24 bg-[#166534] opacity-[0.03] rounded-full group-hover:scale-150 transition-transform duration-500"></div>
    <div class="flex justify-between items-start mb-2">
      <p class="text-[11px] font-bold text-on-surface-variant uppercase tracking-wider">Top Category</p>
      <span class="material-symbols-outlined text-[#166534] bg-[#dcfce7] p-1.5 rounded-lg text-[20px]">category</span>
    </div>
    <div class="flex items-end gap-2 mt-2">
      {% if category_data %}
      <h3 class="text-xl font-display font-bold text-on-surface capitalize truncate">{{ category_data.0.label }}</h3>
      {% else %}
      <h3 class="text-xl font-display font-bold text-on-surface">None</h3>
      {% endif %}
    </div>
  </div>
</div>

<!-- Charts Row -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
  <!-- Status Chart -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 flex flex-col">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-bold text-lg text-on-surface">Reports by Status</h3>
      <span class="material-symbols-outlined text-on-surface-variant">donut_large</span>
    </div>
    <div class="relative w-full h-64 flex-1">
      <canvas id="statusChart"></canvas>
    </div>
  </div>

  <!-- Category Chart -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 flex flex-col">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-bold text-lg text-on-surface">Reports by Category</h3>
      <span class="material-symbols-outlined text-on-surface-variant">pie_chart</span>
    </div>
    <div class="relative w-full h-64 flex-1">
      <canvas id="categoryChart"></canvas>
    </div>
  </div>
</div>

<!-- Barangay Breakdown -->
<div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 mb-8">
  <div class="flex items-center justify-between mb-6">
    <div>
      <h3 class="font-bold text-lg text-on-surface">Barangay Heatmap</h3>
      <p class="text-xs font-medium text-on-surface-variant">Distribution of incident reports across local regions</p>
    </div>
    <span class="material-symbols-outlined text-primary bg-primary-container p-2 rounded-xl">map</span>
  </div>
  <div class="relative w-full h-96">
    <canvas id="barangayChart"></canvas>
  </div>
</div>

</div>

<script>
(function() {
    // Number Counter Animation
    const counters = document.querySelectorAll('.counter');
    const speed = 20; 
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const inc = Math.max(1, Math.ceil(target / speed));
            if (count < target) {
                counter.innerText = count + inc;
                setTimeout(updateCount, 40);
            } else {
                counter.innerText = target;
            }
        };
        updateCount();
    });

    // Chart.js Configuration
    const statusLabels = [{% for item in status_data %}'{{ item.label|title }}',{% endfor %}];
    const statusData = [{% for item in status_data %}{{ item.count }},{% endfor %}];
    
    const categoryLabels = [{% for item in category_data %}'{{ item.label|title }}',{% endfor %}];
    const categoryData = [{% for item in category_data %}{{ item.count }},{% endfor %}];
    
    const barangayLabels = [{% for item in barangay_data %}'{{ item.label }}',{% endfor %}];
    const barangayData = [{% for item in barangay_data %}{{ item.count }},{% endfor %}];

    // Destroy existing charts to prevent SPA memory leaks / overlap
    if (window.statusChartInst) window.statusChartInst.destroy();
    if (window.categoryChartInst) window.categoryChartInst.destroy();
    if (window.barangayChartInst) window.barangayChartInst.destroy();

    Chart.defaults.font.family = "'DM Sans', sans-serif";
    Chart.defaults.color = '#43474e';

    // 1. Status Donut Chart
    const ctxStatus = document.getElementById('statusChart').getContext('2d');
    window.statusChartInst = new Chart(ctxStatus, {
        type: 'doughnut',
        data: {
            labels: statusLabels,
            datasets: [{
                data: statusData,
                backgroundColor: ['#d97706', '#0ea5e9', '#166534'],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: { position: 'bottom', labels: { usePointStyle: true, padding: 20 } }
            }
        }
    });

    // 2. Category Pie Chart
    const ctxCategory = document.getElementById('categoryChart').getContext('2d');
    const categoryColors = [
        '#156b3e', '#004785', '#6366f1', '#eab308', '#ec4899', '#8b5cf6', '#14b8a6'
    ];
    window.categoryChartInst = new Chart(ctxCategory, {
        type: 'polarArea',
        data: {
            labels: categoryLabels,
            datasets: [{
                data: categoryData,
                backgroundColor: categoryColors.map(c => c + 'cc'),
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { usePointStyle: true, padding: 15 } }
            },
            scales: {
                r: { display: false }
            }
        }
    });

    // 3. Barangay Bar Chart
    const ctxBarangay = document.getElementById('barangayChart').getContext('2d');
    
    // Create gradient
    let gradient = ctxBarangay.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, '#156b3e');   
    gradient.addColorStop(1, '#a0f3be');

    window.barangayChartInst = new Chart(ctxBarangay, {
        type: 'bar',
        data: {
            labels: barangayLabels,
            datasets: [{
                label: 'Reports',
                data: barangayData,
                backgroundColor: gradient,
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
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
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            }
        }
    });
})();
</script>
{% endblock %}
"""

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'w', 'utf-8') as f:
    f.write(html_content)
