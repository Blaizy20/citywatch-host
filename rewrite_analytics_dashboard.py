import codecs

html = '''{% extends 'analytics/admin_base.html' %}
{% load static %}
{% block content %}

<div class="mx-auto max-w-7xl px-4 py-2 sm:px-6 lg:px-8 w-full">

  <!-- Header Area -->
  <div class="mb-8 flex flex-wrap items-end justify-between gap-3">
    <div>
      <h1 class="text-3xl font-bold font-display text-on-surface tracking-tight flex items-center gap-2">
        <span class="material-symbols-outlined text-primary text-[32px]">dashboard</span>
        Dashboard Overview
      </h1>
      <p class="mt-1 max-w-2xl text-sm text-on-surface-variant font-medium">Real-time status of community reports across Baliwag City.</p>
    </div>
  </div>

  <!-- Metric Cards -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    
    <!-- Total Reports -->
    <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between group relative overflow-hidden">
      <div class="absolute -right-6 -top-6 w-24 h-24 bg-primary/5 rounded-full blur-2xl group-hover:bg-primary/10 transition-colors"></div>
      <div class="flex justify-between items-start relative z-10">
        <span class="text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.15em] mb-2">Total Reports</span>
        <div class="w-10 h-10 rounded-xl bg-primary-container text-on-primary-container flex items-center justify-center shadow-inner">
          <span class="material-symbols-outlined text-[20px]">monitoring</span>
        </div>
      </div>
      <div class="mt-4 relative z-10">
        <span class="text-5xl font-display font-bold text-on-surface leading-none tracking-tight">{{ total_reports }}</span>
      </div>
    </div>

    <!-- Pending -->
    <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between group relative overflow-hidden">
      <div class="absolute -right-6 -top-6 w-24 h-24 bg-[#d97706]/5 rounded-full blur-2xl group-hover:bg-[#d97706]/10 transition-colors"></div>
      <div class="flex justify-between items-start relative z-10">
        <span class="text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.15em] mb-2">Pending</span>
        <div class="w-10 h-10 rounded-xl bg-[#fef3c7] text-[#d97706] flex items-center justify-center shadow-inner">
          <span class="material-symbols-outlined text-[20px]">pending_actions</span>
        </div>
      </div>
      <div class="mt-4 relative z-10">
        <span class="text-5xl font-display font-bold text-on-surface leading-none tracking-tight">{{ pending_count }}</span>
        <p class="text-xs font-semibold text-[#d97706] mt-1.5 flex items-center gap-1"><span class="material-symbols-outlined text-[12px]">warning</span> Requires triage</p>
      </div>
    </div>

    <!-- In Progress -->
    <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between group relative overflow-hidden">
      <div class="absolute -right-6 -top-6 w-24 h-24 bg-primary/5 rounded-full blur-2xl group-hover:bg-primary/10 transition-colors"></div>
      <div class="flex justify-between items-start relative z-10">
        <span class="text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.15em] mb-2">In Progress</span>
        <div class="w-10 h-10 rounded-xl bg-primary-container text-primary flex items-center justify-center shadow-inner">
          <span class="material-symbols-outlined text-[20px]">engineering</span>
        </div>
      </div>
      <div class="mt-4 relative z-10">
        <span class="text-5xl font-display font-bold text-on-surface leading-none tracking-tight">{{ in_progress_count }}</span>
        <p class="text-xs font-semibold text-primary mt-1.5 flex items-center gap-1"><span class="material-symbols-outlined text-[12px]">cycle</span> Active interventions</p>
      </div>
    </div>

    <!-- Resolved -->
    <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between group relative overflow-hidden">
      <div class="absolute -right-6 -top-6 w-24 h-24 bg-secondary/5 rounded-full blur-2xl group-hover:bg-secondary/10 transition-colors"></div>
      <div class="flex justify-between items-start relative z-10">
        <span class="text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.15em] mb-2">Resolved</span>
        <div class="w-10 h-10 rounded-xl bg-secondary-container text-secondary flex items-center justify-center shadow-inner">
          <span class="material-symbols-outlined text-[20px]">check_circle</span>
        </div>
      </div>
      <div class="mt-4 relative z-10">
        <span class="text-5xl font-display font-bold text-on-surface leading-none tracking-tight">{{ resolved_count }}</span>
        {% if avg_resolution_days %}<p class="text-xs font-semibold text-secondary mt-1.5 flex items-center gap-1"><span class="material-symbols-outlined text-[12px]">schedule</span> Avg resolution: {{ avg_resolution_days }} days</p>{% endif %}
      </div>
    </div>
  </div>

  <!-- Recent Reports Table -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm overflow-hidden flex flex-col">
    <div class="p-6 border-b border-outline-variant flex justify-between items-center bg-surface-container-low/50">
      <div>
        <h3 class="font-bold text-lg text-on-surface">Recent Reports</h3>
        <p class="text-xs font-medium text-on-surface-variant">Latest community submissions</p>
      </div>
      <a href="{% url 'admin_report_list' %}" class="inline-flex items-center gap-1.5 bg-surface hover:bg-surface-container border border-outline-variant text-on-surface-variant text-xs font-bold uppercase tracking-wider py-2 px-3 rounded-xl transition-colors shadow-sm">
        View All <span class="material-symbols-outlined text-[16px]">arrow_forward</span>
      </a>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-surface">
            <th class="p-4 pl-6 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">ID</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Category</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Location</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Date</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Status</th>
            <th class="p-4 pr-6 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant text-right">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-outline-variant">
          {% for report in recent_reports %}
          <tr class="hover:bg-surface-container-low transition-colors group">
            <td class="p-4 pl-6 text-sm text-on-surface font-bold">#CW-{{ report.id }}</td>
            <td class="p-4">
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-lg bg-surface flex items-center justify-center border border-outline-variant/50 shrink-0">
                  <span class="material-symbols-outlined text-[16px] text-on-surface-variant">
                    {% if report.category == 'infrastructure' %}construction
                    {% elif report.category == 'safety' %}security
                    {% elif report.category == 'sanitation' %}cleaning_services
                    {% elif report.category == 'noise' %}volume_up
                    {% else %}report{% endif %}
                  </span>
                </div>
                <span class="text-sm font-semibold text-on-surface">{{ report.get_category_display }}</span>
              </div>
            </td>
            <td class="p-4 text-sm font-medium text-on-surface-variant flex items-center gap-1.5"><span class="material-symbols-outlined text-[14px] opacity-70">location_on</span> {{ report.barangay }}</td>
            <td class="p-4 text-sm font-medium text-on-surface-variant">{{ report.date_submitted|date:"M d, Y" }}</td>
            <td class="p-4">
              {% if report.status == 'pending' %}
              <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold bg-[#fef3c7] text-[#92400e] border border-[#fde68a] uppercase tracking-wide">
                <span class="material-symbols-outlined text-[14px]">pending_actions</span> Pending
              </span>
              {% elif report.status == 'acknowledged' %}
              <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold bg-[#e0f2fe] text-[#075985] border border-[#bae6fd] uppercase tracking-wide">
                <span class="material-symbols-outlined text-[14px]">visibility</span> Acknowledged
              </span>
              {% elif report.status == 'in_progress' %}
              <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold bg-[#dbeafe] text-[#1e40af] border border-[#bfdbfe] uppercase tracking-wide">
                <span class="material-symbols-outlined text-[14px]">engineering</span> In Progress
              </span>
              {% elif report.status == 'resolved' %}
              <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold bg-[#dcfce7] text-[#166534] border border-[#bbf7d0] uppercase tracking-wide">
                <span class="material-symbols-outlined text-[14px]">check_circle</span> Resolved
              </span>
              {% else %}
              <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold bg-surface-container text-on-surface-variant border border-outline-variant uppercase tracking-wide">
                <span class="material-symbols-outlined text-[14px]">close</span> Closed
              </span>
              {% endif %}
            </td>
            <td class="p-4 pr-6 text-right">
              <a href="{% url 'admin_report_detail' report.id %}" class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-surface hover:bg-primary hover:text-on-primary text-on-surface-variant border border-outline-variant hover:border-primary transition-colors group-hover:shadow-sm">
                <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
              </a>
            </td>
          </tr>
          {% empty %}
          <tr><td colspan="6" class="p-12 text-center text-on-surface-variant font-medium bg-surface-container-lowest">No reports have been submitted yet.</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

</div>

{% endblock %}
'''

with codecs.open('d:/citywatch/analytics/templates/analytics/dashboard.html', 'w', 'utf-8') as f:
    f.write(html)
