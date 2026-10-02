import codecs

html = '''{% extends 'analytics/admin_base.html' %}
{% load static %}
{% block content %}

<div class="mx-auto max-w-7xl px-4 py-2 sm:px-6 lg:px-8 w-full">

  <!-- Header Area -->
  <div class="mb-8 flex flex-wrap items-end justify-between gap-3">
    <div>
      <h1 class="text-3xl font-bold font-display text-on-surface tracking-tight flex items-center gap-2">
        <span class="material-symbols-outlined text-primary text-[32px]">group</span>
        User Management
      </h1>
      <p class="mt-1 max-w-2xl text-sm text-on-surface-variant font-medium">Manage residents, assign department staff, and oversee platform access.</p>
    </div>
    <div class="flex items-center gap-4">
      <a href="{% url 'analytics_dashboard' %}" data-no-spa="true" onclick="if(window.history.length > 1) { event.preventDefault(); this.querySelector('span').classList.add('-translate-x-4', 'opacity-0'); setTimeout(() => window.history.back(), 150); }" class="inline-flex items-center gap-1.5 text-sm font-bold text-on-surface-variant hover:text-primary transition-colors group p-2 hover:bg-surface-container-low rounded-full"><span class="material-symbols-outlined text-[20px] transition-all duration-300 group-hover:-translate-x-1 group-active:scale-75">arrow_back</span> Dashboard</a>
    </div>
  </div>

  {% if messages %}
  <div class="mb-6 flex flex-col gap-2">
    {% for message in messages %}
    <div class="p-4 rounded-xl flex items-center gap-3 shadow-sm font-semibold text-sm animate-fade-in
        {% if message.tags == 'success' %}bg-[#dcfce7] text-[#166534] border border-[#bbf7d0]
        {% elif message.tags == 'error' %}bg-[#fee2e2] text-[#991b1b] border border-[#fecaca]
        {% else %}bg-secondary-container text-on-secondary-container border border-outline-variant{% endif %}">
      <span class="material-symbols-outlined text-[20px]">{% if message.tags == 'success' %}check_circle{% elif message.tags == 'error' %}error{% else %}info{% endif %}</span>
      {{ message }}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Users Table Card -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm overflow-hidden">
    <div class="p-6 border-b border-outline-variant bg-surface-container-low/50 flex justify-between items-center">
      <div>
        <h3 class="font-bold text-lg text-on-surface">Registered Accounts</h3>
        <p class="text-xs font-medium text-on-surface-variant">Complete directory of all system users.</p>
      </div>
      <div class="flex items-center gap-2 text-sm font-bold text-on-surface-variant bg-surface-container px-3 py-1.5 rounded-lg border border-outline-variant">
        <span class="material-symbols-outlined text-[18px]">group</span>
        {{ users|length }} Total Users
      </div>
    </div>
    
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-surface">
            <th class="p-4 pl-6 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">User Profile</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Contact / Location</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Access Role</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Joined</th>
            <th class="p-4 pr-6 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant text-right">Permissions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-outline-variant">
          {% for u in users %}
          <tr class="hover:bg-surface-container-low transition-colors group">
            
            <td class="p-4 pl-6">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg shrink-0 shadow-sm
                  {% if u.is_superuser %}bg-[#4f46e5] text-white
                  {% elif u.is_staff %}bg-primary text-on-primary
                  {% else %}bg-surface-container-highest text-on-surface-variant{% endif %}">
                  {{ u.username.0|upper }}
                </div>
                <div class="flex flex-col">
                  <span class="text-sm font-bold text-on-surface">{{ u.username }}</span>
                  <span class="text-xs font-medium text-on-surface-variant">{% if u.get_full_name %}{{ u.get_full_name }}{% else %}No Name Set{% endif %}</span>
                </div>
              </div>
            </td>
            
            <td class="p-4">
              <div class="flex flex-col gap-1">
                <div class="flex items-center gap-1.5 text-sm text-on-surface-variant font-medium">
                  <span class="material-symbols-outlined text-[14px]">mail</span> {{ u.email|default:"—" }}
                </div>
                <div class="flex items-center gap-1.5 text-xs text-on-surface-variant">
                  <span class="material-symbols-outlined text-[14px]">location_on</span> {{ u.profile.barangay|default:"No Barangay Selected" }}
                </div>
              </div>
            </td>
            
            <td class="p-4">
              {% if u.is_superuser %}
              <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold bg-[#e0e7ff] text-[#4338ca] border border-[#c7d2fe] uppercase tracking-wide">
                <span class="material-symbols-outlined text-[14px]">admin_panel_settings</span> Superuser
              </span>
              {% elif u.is_staff %}
              <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold bg-primary-container text-on-primary-container border border-primary/20 uppercase tracking-wide">
                <span class="material-symbols-outlined text-[14px]">shield_person</span> Staff / Admin
              </span>
              {% else %}
              <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold bg-surface-container text-on-surface-variant border border-outline-variant uppercase tracking-wide">
                <span class="material-symbols-outlined text-[14px]">person</span> Resident
              </span>
              {% endif %}
            </td>
            
            <td class="p-4 text-sm font-medium text-on-surface-variant">
              {{ u.date_joined|date:"M d, Y" }}
            </td>
            
            <td class="p-4 pr-6 text-right">
              {% if u != request.user and not u.is_superuser %}
              <form method="POST" action="{% url 'toggle_staff' u.id %}" class="inline-block" onsubmit="return confirm('Are you sure you want to change permissions for {{ u.username }}?');">
                {% csrf_token %}
                {% if u.is_staff %}
                <button type="submit" title="Revoke Staff Access" class="inline-flex items-center justify-center bg-surface hover:bg-[#fee2e2] text-[#991b1b] border border-outline-variant hover:border-[#fecaca] transition-colors p-2 rounded-lg group-hover:shadow-sm">
                  <span class="material-symbols-outlined text-[18px]">person_off</span>
                </button>
                {% else %}
                <button type="submit" title="Grant Staff Access" class="inline-flex items-center justify-center bg-surface hover:bg-primary-container text-primary border border-outline-variant hover:border-primary/30 transition-colors p-2 rounded-lg group-hover:shadow-sm">
                  <span class="material-symbols-outlined text-[18px]">person_add</span>
                </button>
                {% endif %}
              </form>
              {% else %}
              <span class="text-xs font-semibold text-on-surface-variant opacity-50 cursor-not-allowed" title="Cannot modify this account">Protected</span>
              {% endif %}
            </td>
            
          </tr>
          {% empty %}
          <tr><td colspan="5" class="p-8 text-center text-on-surface-variant font-medium bg-surface-container-lowest">No users registered in the system.</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

</div>

{% endblock %}
'''

with codecs.open('d:/citywatch/accounts/templates/accounts/user_list.html', 'w', 'utf-8') as f:
    f.write(html)
