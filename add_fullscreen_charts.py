import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Trend Line Chart
target1 = '''<!-- Trend Line Chart -->
<div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 mb-8 flex flex-col">
  <div class="flex items-center justify-between mb-4">
    <div>
      <h3 class="font-bold text-lg text-on-surface">Submission Trend</h3>
      <p class="text-xs font-medium text-on-surface-variant">Volume of incoming reports over time</p>
    </div>
    <span class="material-symbols-outlined text-on-surface-variant">trending_up</span>
  </div>'''

replacement1 = '''<!-- Trend Line Chart -->
<div class="chart-card bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 mb-8 flex flex-col transition-all duration-300">
  <div class="flex items-center justify-between mb-4">
    <div>
      <h3 class="font-bold text-lg text-on-surface">Submission Trend</h3>
      <p class="text-xs font-medium text-on-surface-variant">Volume of incoming reports over time</p>
    </div>
    <div class="flex items-center gap-2">
      <button type="button" onclick="const card = this.closest('.chart-card'); card.classList.toggle('fixed'); card.classList.toggle('inset-0'); card.classList.toggle('z-[100]'); card.classList.toggle('rounded-none'); card.classList.toggle('w-screen'); card.classList.toggle('h-screen'); this.querySelector('span').innerText = card.classList.contains('fixed') ? 'fullscreen_exit' : 'fullscreen'; setTimeout(() => window.dispatchEvent(new Event('resize')), 100);" class="text-on-surface-variant hover:text-primary transition-colors p-1 rounded-md hover:bg-surface-container-low flex items-center justify-center" title="Toggle Fullscreen">
        <span class="material-symbols-outlined text-[20px]">fullscreen</span>
      </button>
      <span class="material-symbols-outlined text-on-surface-variant">trending_up</span>
    </div>
  </div>'''

html = html.replace(target1, replacement1)

# 2. Status Chart
target2 = '''  <!-- Status Chart -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 flex flex-col">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-bold text-lg text-on-surface">Reports by Status</h3>
      <span class="material-symbols-outlined text-on-surface-variant">donut_large</span>
    </div>'''

replacement2 = '''  <!-- Status Chart -->
  <div class="chart-card bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 flex flex-col transition-all duration-300">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-bold text-lg text-on-surface">Reports by Status</h3>
      <div class="flex items-center gap-2">
        <button type="button" onclick="const card = this.closest('.chart-card'); card.classList.toggle('fixed'); card.classList.toggle('inset-0'); card.classList.toggle('z-[100]'); card.classList.toggle('rounded-none'); card.classList.toggle('w-screen'); card.classList.toggle('h-screen'); this.querySelector('span').innerText = card.classList.contains('fixed') ? 'fullscreen_exit' : 'fullscreen'; setTimeout(() => window.dispatchEvent(new Event('resize')), 100);" class="text-on-surface-variant hover:text-primary transition-colors p-1 rounded-md hover:bg-surface-container-low flex items-center justify-center" title="Toggle Fullscreen">
          <span class="material-symbols-outlined text-[20px]">fullscreen</span>
        </button>
        <span class="material-symbols-outlined text-on-surface-variant">donut_large</span>
      </div>
    </div>'''

html = html.replace(target2, replacement2)

# 3. Category Chart
target3 = '''  <!-- Category Chart -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 flex flex-col">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-bold text-lg text-on-surface">Reports by Category</h3>
      <span class="material-symbols-outlined text-on-surface-variant">pie_chart</span>
    </div>'''

replacement3 = '''  <!-- Category Chart -->
  <div class="chart-card bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 flex flex-col transition-all duration-300">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-bold text-lg text-on-surface">Reports by Category</h3>
      <div class="flex items-center gap-2">
        <button type="button" onclick="const card = this.closest('.chart-card'); card.classList.toggle('fixed'); card.classList.toggle('inset-0'); card.classList.toggle('z-[100]'); card.classList.toggle('rounded-none'); card.classList.toggle('w-screen'); card.classList.toggle('h-screen'); this.querySelector('span').innerText = card.classList.contains('fixed') ? 'fullscreen_exit' : 'fullscreen'; setTimeout(() => window.dispatchEvent(new Event('resize')), 100);" class="text-on-surface-variant hover:text-primary transition-colors p-1 rounded-md hover:bg-surface-container-low flex items-center justify-center" title="Toggle Fullscreen">
          <span class="material-symbols-outlined text-[20px]">fullscreen</span>
        </button>
        <span class="material-symbols-outlined text-on-surface-variant">pie_chart</span>
      </div>
    </div>'''

html = html.replace(target3, replacement3)

# 4. Barangay Chart
target4 = '''<!-- Barangay Breakdown -->
<div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 mb-8">
  <div class="flex items-center justify-between mb-6">
    <div>
      <h3 class="font-bold text-lg text-on-surface">Barangay Heatmap</h3>
      <p class="text-xs font-medium text-on-surface-variant">Distribution of incident reports across local regions</p>
    </div>
    <span class="material-symbols-outlined text-primary bg-primary-container p-2 rounded-xl">map</span>
  </div>'''

replacement4 = '''<!-- Barangay Breakdown -->
<div class="chart-card bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm p-6 mb-8 flex flex-col transition-all duration-300">
  <div class="flex items-center justify-between mb-6">
    <div>
      <h3 class="font-bold text-lg text-on-surface">Barangay Heatmap</h3>
      <p class="text-xs font-medium text-on-surface-variant">Distribution of incident reports across local regions</p>
    </div>
    <div class="flex items-center gap-3">
      <button type="button" onclick="const card = this.closest('.chart-card'); card.classList.toggle('fixed'); card.classList.toggle('inset-0'); card.classList.toggle('z-[100]'); card.classList.toggle('rounded-none'); card.classList.toggle('w-screen'); card.classList.toggle('h-screen'); this.querySelector('span').innerText = card.classList.contains('fixed') ? 'fullscreen_exit' : 'fullscreen'; setTimeout(() => window.dispatchEvent(new Event('resize')), 100);" class="text-on-surface-variant hover:text-primary transition-colors p-2 rounded-xl hover:bg-surface-container-low flex items-center justify-center" title="Toggle Fullscreen">
        <span class="material-symbols-outlined text-[24px]">fullscreen</span>
      </button>
      <span class="material-symbols-outlined text-primary bg-primary-container p-2 rounded-xl">map</span>
    </div>
  </div>'''

html = html.replace(target4, replacement4)

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'w', 'utf-8') as f:
    f.write(html)
