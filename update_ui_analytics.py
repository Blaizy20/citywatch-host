import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Update dropdown filter and add Custom Date pickers
target_filter = '''<div class="flex items-center gap-4">
  <form method="GET" class="flex items-center gap-2" id="timeframe-form">
    <label for="timeframe" class="text-sm font-bold text-on-surface-variant">Timeframe:</label>
    <select name="timeframe" id="timeframe" class="text-sm font-semibold text-primary bg-surface-container-low border border-outline-variant rounded-lg px-3 py-1.5 focus:ring-primary focus:border-primary cursor-pointer" onchange="this.form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }))">
      <option value="7" {% if timeframe == '7' %}selected{% endif %}>Last 7 Days</option>
      <option value="30" {% if timeframe == '30' %}selected{% endif %}>Last 30 Days</option>
      <option value="90" {% if timeframe == '90' %}selected{% endif %}>Last 90 Days</option>
      <option value="all" {% if timeframe == 'all' %}selected{% endif %}>All Time</option>
    </select>
  </form>'''

replacement_filter = '''<div class="flex items-center gap-4">
  <form method="GET" class="flex items-center gap-2" id="timeframe-form">
    <label for="timeframe" class="text-sm font-bold text-on-surface-variant">Timeframe:</label>
    <select name="timeframe" id="timeframe" class="text-sm font-semibold text-primary bg-surface-container-low border border-outline-variant rounded-lg pl-3 pr-8 py-1.5 focus:ring-primary focus:border-primary cursor-pointer" onchange="this.form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }))">
      <option value="7" {% if timeframe == '7' %}selected{% endif %}>Last 7 Days</option>
      <option value="30" {% if timeframe == '30' %}selected{% endif %}>Last 30 Days</option>
      <option value="90" {% if timeframe == '90' %}selected{% endif %}>Last 90 Days</option>
      <option value="all" {% if timeframe == 'all' %}selected{% endif %}>All Time</option>
      <option value="custom" {% if timeframe == 'custom' %}selected{% endif %}>Custom Date</option>
    </select>
    
    {% if timeframe == 'custom' %}
      <div class="flex items-center gap-2 ml-2">
        <input type="date" name="custom_start" value="{{ custom_start }}" class="text-sm font-semibold text-primary bg-surface-container-low border border-outline-variant rounded-lg px-2 py-1.5 focus:ring-primary focus:border-primary cursor-pointer" onchange="this.form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }))">
        <span class="text-sm font-bold text-on-surface-variant">to</span>
        <input type="date" name="custom_end" value="{{ custom_end }}" class="text-sm font-semibold text-primary bg-surface-container-low border border-outline-variant rounded-lg px-2 py-1.5 focus:ring-primary focus:border-primary cursor-pointer" onchange="this.form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }))">
      </div>
    {% endif %}
  </form>'''

html = html.replace(target_filter, replacement_filter)

# 2. Add detailed resolution indicator
target_resolution = '''  <!-- Resolution Time -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex items-center gap-4 relative overflow-hidden group lg:col-span-1">
    <div class="absolute right-0 top-0 w-full h-full bg-gradient-to-l from-secondary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
    <span class="material-symbols-outlined text-secondary bg-secondary-container p-3 rounded-xl text-[24px] shrink-0">timer</span>
    <div class="flex flex-col relative z-10">
      <p class="text-[10px] font-bold text-on-surface-variant uppercase tracking-wider mb-1">Resolution Time</p>
      <div class="flex items-baseline gap-1">
        <h3 class="text-3xl font-display font-bold text-on-surface">{% if avg_resolution_days %}{{ avg_resolution_days }}{% else %}0{% endif %}</h3>
        <span class="text-xs font-semibold text-on-surface-variant">days avg</span>
      </div>
    </div>
  </div>'''

replacement_resolution = '''  <!-- Resolution Time -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex items-center gap-4 relative overflow-hidden group lg:col-span-1">
    <div class="absolute right-0 top-0 w-full h-full bg-gradient-to-l from-secondary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
    <span class="material-symbols-outlined text-secondary bg-secondary-container p-3 rounded-xl text-[24px] shrink-0">timer</span>
    <div class="flex flex-col relative z-10 w-full">
      <p class="text-[10px] font-bold text-on-surface-variant uppercase tracking-wider mb-1">Resolution Time</p>
      <div class="flex items-baseline gap-1">
        <h3 class="text-3xl font-display font-bold text-on-surface">{% if avg_resolution_days %}{{ avg_resolution_days }}{% else %}0{% endif %}</h3>
        <span class="text-xs font-semibold text-on-surface-variant">days avg</span>
      </div>
      {% if avg_res_detailed %}
        <p class="text-[10px] font-semibold text-secondary bg-secondary/10 px-2 py-0.5 rounded max-w-max mt-1 whitespace-nowrap">{{ avg_res_detailed }} exact average</p>
      {% endif %}
    </div>
  </div>'''

html = html.replace(target_resolution, replacement_resolution)

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'w', 'utf-8') as f:
    f.write(html)
