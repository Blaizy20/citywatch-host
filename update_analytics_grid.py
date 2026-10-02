import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'r', 'utf-8') as f:
    html = f.read()

target = '''<!-- Overview Stats Cards -->
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
</div>'''

replacement = '''<!-- Overview Stats Cards -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-8">
  
  <!-- Hero Card: Total Reports -->
  <div class="bg-primary text-on-primary rounded-[2rem] p-8 sm:p-10 shadow-lg hover:shadow-xl transition-all flex flex-col justify-center relative overflow-hidden group lg:col-span-2 lg:row-span-3 min-h-[300px]">
    <div class="absolute -right-20 -bottom-20 w-96 h-96 bg-white opacity-5 rounded-full group-hover:scale-110 transition-transform duration-700"></div>
    <div class="absolute -right-10 -top-10 w-48 h-48 bg-black opacity-10 rounded-full group-hover:scale-110 transition-transform duration-700 delay-75"></div>
    
    <div class="relative z-10 flex flex-col h-full justify-between">
      <div class="flex justify-between items-start">
        <span class="material-symbols-outlined text-[48px] opacity-90">assignment</span>
        <span class="bg-white/20 backdrop-blur-sm text-white px-3 py-1 rounded-full text-xs font-bold tracking-wider uppercase border border-white/20">System Volume</span>
      </div>
      
      <div class="mt-8">
        <p class="text-lg font-semibold text-primary-container mb-1">Total Reports Filed</p>
        <div class="flex items-baseline gap-3">
          <h3 class="text-[5rem] sm:text-[7rem] leading-none font-display font-bold counter" data-target="{{ total_reports }}">0</h3>
        </div>
        <p class="text-sm text-primary-container mt-4 max-w-sm leading-relaxed">Overall submission volume aggregated across all barangays and local agencies.</p>
      </div>
    </div>
  </div>

  <!-- Resolution Time -->
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
  </div>

  <!-- Pending Action -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex items-center gap-4 relative overflow-hidden group lg:col-span-1">
    <div class="absolute right-0 top-0 w-full h-full bg-gradient-to-l from-[#d97706]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
    <span class="material-symbols-outlined text-[#d97706] bg-[#fef3c7] p-3 rounded-xl text-[24px] shrink-0">pending_actions</span>
    <div class="flex flex-col relative z-10">
      <p class="text-[10px] font-bold text-on-surface-variant uppercase tracking-wider mb-1">Pending Action</p>
      <div class="flex items-baseline gap-2">
        {% for item in status_data %}
          {% if item.label == 'pending' %}
            <h3 class="text-3xl font-display font-bold text-on-surface counter" data-target="{{ item.count }}">0</h3>
            <span class="text-[10px] font-bold text-[#d97706] bg-[#fef3c7] px-1.5 py-0.5 rounded uppercase">Review</span>
          {% endif %}
        {% endfor %}
      </div>
    </div>
  </div>

  <!-- Top Category -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex items-center gap-4 relative overflow-hidden group lg:col-span-1">
    <div class="absolute right-0 top-0 w-full h-full bg-gradient-to-l from-[#166534]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
    <span class="material-symbols-outlined text-[#166534] bg-[#dcfce7] p-3 rounded-xl text-[24px] shrink-0">category</span>
    <div class="flex flex-col relative z-10 w-full overflow-hidden">
      <p class="text-[10px] font-bold text-on-surface-variant uppercase tracking-wider mb-1">Top Category</p>
      {% if category_data %}
      <h3 class="text-xl font-display font-bold text-on-surface capitalize truncate">{{ category_data.0.label }}</h3>
      {% else %}
      <h3 class="text-xl font-display font-bold text-on-surface">None</h3>
      {% endif %}
    </div>
  </div>
</div>'''

html = html.replace(target, replacement)

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'w', 'utf-8') as f:
    f.write(html)
