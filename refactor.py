import re
import os

base_html = """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta content="width=device-width, initial-scale=1.0" name="viewport">
<title>{% block title %}CityWatch Admin{% endblock %}</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<script>
tailwind.config = { 
  theme: { 
    extend: {
      fontFamily: {
        sans: ['"DM Sans"', 'sans-serif'],
        display: ['"Outfit"', 'sans-serif']
      },
      colors: {
        "primary": "#156b3e", "on-primary": "#ffffff", "primary-container": "#a0f3be",
        "on-primary-container": "#002111", "secondary": "#004785", "on-secondary": "#ffffff", "secondary-container": "#d6e3ff",
        "on-secondary-container": "#001b3f", "surface": "#fdfcff", "on-surface": "#1a1c1e",
        "on-surface-variant": "#43474e", "surface-container": "#f3f4f9", "surface-container-low": "#f8f9fc",
        "surface-container-lowest": "#ffffff", "outline": "#74777f", "outline-variant": "#c4c6cf",
        "error": "#ba1a1a", "error-container": "#ffdad6", "on-error-container": "#93000a",
        "background": "#f3f4f9", "on-background": "#1a1c1e",
        "tertiary-fixed": "#ffdeaa", "on-tertiary-fixed-variant": "#5f4100"
      },
      borderRadius: { xl: '0.5rem', full: '0.75rem' }
    }
  }
}
</script>
<style>
  .material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
</style>
{% block extra_head %}{% endblock %}
</head>
<body class="bg-background text-on-background font-sans antialiased flex flex-col min-h-screen">
<div class="flex min-h-screen w-full">

<aside class="hidden lg:flex bg-surface-container-lowest border-r border-outline-variant flex-col sticky top-0 h-screen z-50 flex-shrink-0 w-64 overflow-hidden">
<div class="p-3 border-b border-outline-variant flex items-center min-h-[65px]">
<a class="flex items-center gap-2 text-xl font-bold text-primary" href="{% url 'landing' %}">
<span class="material-symbols-outlined shrink-0 text-3xl">location_city</span>
<span class="whitespace-nowrap font-display">CityWatch Admin</span>
</a>
</div>
<nav class="flex-grow p-2 flex flex-col gap-1" aria-label="Admin navigation">
{% url 'analytics_dashboard' as url_dash %}
<a class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm font-semibold {% if request.path == url_dash %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:bg-surface-container-low{% endif %}" href="{{ url_dash }}">
<span class="material-symbols-outlined shrink-0">dashboard</span> Dashboard</a>

{% url 'admin_report_list' as url_reports %}
<a class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm font-semibold {% if request.path == url_reports %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:bg-surface-container-low{% endif %}" href="{{ url_reports }}">
<span class="material-symbols-outlined shrink-0">description</span> Reports</a>

{% url 'admin_announcement_list' as url_announcements %}
<a class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm font-semibold {% if request.path == url_announcements %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:bg-surface-container-low{% endif %}" href="{{ url_announcements }}">
<span class="material-symbols-outlined shrink-0">campaign</span> Announcements</a>

{% url 'reports_analytics' as url_analytics %}
<a class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm font-semibold {% if request.path == url_analytics %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:bg-surface-container-low{% endif %}" href="{{ url_analytics }}">
<span class="material-symbols-outlined shrink-0">analytics</span> Analytics</a>

{% url 'map_view' as url_map %}
<a class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm font-semibold {% if request.path == url_map %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:bg-surface-container-low{% endif %}" href="{{ url_map }}">
<span class="material-symbols-outlined shrink-0">map</span> Map View</a>

{% url 'user_list' as url_users %}
<a class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm font-semibold {% if request.path == url_users %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:bg-surface-container-low{% endif %}" href="{{ url_users }}">
<span class="material-symbols-outlined shrink-0">group</span> Users</a>

{% url 'department_list' as url_depts %}
<a class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm font-semibold {% if request.path == url_depts %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:bg-surface-container-low{% endif %}" href="{{ url_depts }}">
<span class="material-symbols-outlined shrink-0">settings</span> Settings</a>
</nav>
<div class="p-3 border-t border-outline-variant">
<a href="{% url 'logout' %}" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-error hover:bg-error-container hover:text-on-error-container transition-all text-sm font-semibold">
<span class="material-symbols-outlined shrink-0">logout</span> Log Out</a>
</div>
</aside>

<div class="flex-1 flex flex-col min-w-0">
<header class="flex justify-between items-center w-full px-5 h-[65px] sticky top-0 z-40 bg-surface-container-lowest border-b border-outline-variant lg:bg-background lg:border-none">
<div class="lg:hidden flex items-center gap-2 text-primary font-bold font-display"><span class="material-symbols-outlined">location_city</span> CityWatch Admin</div>
<div class="flex items-center gap-4 ml-auto">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-on-surface-variant">account_circle</span>
<span class="text-sm font-semibold text-on-surface hidden sm:block">{{ request.user.username }}</span>
</div>
</div>
</header>
<main class="w-full max-w-7xl px-4 sm:px-5 lg:px-8 py-5 lg:py-7 flex flex-col gap-7 relative self-center">
{% block content %}{% endblock %}
</main>
</div>
</div>
</body>
</html>
"""

os.makedirs('d:/citywatch/analytics/templates/analytics', exist_ok=True)
with open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'w', encoding='utf-8') as f:
    f.write(base_html)

files_to_update = [
    'd:/citywatch/analytics/templates/analytics/dashboard.html',
    'd:/citywatch/reports/templates/reports/admin_report_list.html',
    'd:/citywatch/reports/templates/reports/admin_announcement_list.html',
    'd:/citywatch/analytics/templates/analytics/reports_analytics.html',
    'd:/citywatch/analytics/templates/analytics/map_view.html',
    'd:/citywatch/accounts/templates/accounts/user_list.html',
    'd:/citywatch/assignments/templates/assignments/department_list.html'
]

for fpath in files_to_update:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    m = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL)
    if m:
        main_content = m.group(1)
        main_content = re.sub(r'<header.*?</header>', '', main_content, flags=re.DOTALL)
        
        main_content = re.sub(r'class="p-6 md:p-16 flex-1 max-w-7xl mx-auto w-full"', 'class="flex flex-col gap-5 w-full"', main_content)
        main_content = re.sub(r'class="px-6 md:px-16 py-8 max-w-7xl mx-auto"', 'class="flex flex-col gap-5 w-full"', main_content)
        main_content = re.sub(r'class="px-6 md:px-12 py-8 max-w-7xl mx-auto"', 'class="flex flex-col gap-5 w-full"', main_content)
        main_content = re.sub(r'class="p-6 md:p-12"', 'class="flex flex-col gap-5 w-full"', main_content)
        main_content = re.sub(r'class="p-6 md:p-10"', 'class="flex flex-col gap-5 w-full"', main_content)
        
        # Additional formatting updates to make it match the resident dashboard more closely
        # Change text-3xl font-semibold to text-3xl font-bold font-display
        main_content = re.sub(r'text-3xl font-semibold', 'text-3xl font-bold font-display', main_content)
        main_content = re.sub(r'text-2xl font-semibold', 'text-2xl font-bold font-display', main_content)
        main_content = re.sub(r'bg-white', 'bg-surface-container-lowest', main_content)
        
        load_static = "{% load static %}" if "{% load static %}" in content else ""
        
        # Remove any existing {% extends ... %} or {% block content %} to prevent nesting errors if the file was already updated
        main_content = main_content.replace("{% block content %}", "").replace("{% endblock %}", "")
        
        new_content = "{% extends 'analytics/admin_base.html' %}\n" + load_static + "\n{% block content %}\n" + main_content + "\n{% endblock %}\n"
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {fpath}")
    else:
        print(f"Could not find <main> in {fpath}")
