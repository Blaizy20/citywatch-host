import re

with open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update aside tag
content = re.sub(
    r'<aside class="hidden lg:flex bg-surface-container-lowest border-r border-outline-variant flex-col sticky top-0 h-screen z-50 flex-shrink-0 w-64 overflow-hidden">',
    r'<aside id="admin-sidebar" data-collapsed="false" class="hidden lg:flex bg-surface-container-lowest border-r border-outline-variant flex-col sticky top-0 h-screen z-50 flex-shrink-0 transition-all duration-300 w-64 data-[collapsed=true]:w-20 overflow-hidden group/sidebar">',
    content
)

# 2. Update sidebar header
old_sidebar_header = """<div class="p-3 border-b border-outline-variant flex items-center min-h-[65px]">
<a class="flex items-center gap-2 text-xl font-bold text-primary" href="{% url 'landing' %}">
<span class="material-symbols-outlined shrink-0 text-3xl">location_city</span>
<span class="whitespace-nowrap font-display">CityWatch Admin</span>
</a>
</div>"""
new_sidebar_header = """<div class="p-3 border-b border-outline-variant flex group-data-[collapsed=false]/sidebar:items-center group-data-[collapsed=false]/sidebar:justify-between group-data-[collapsed=true]/sidebar:flex-col group-data-[collapsed=true]/sidebar:items-center group-data-[collapsed=true]/sidebar:gap-4 min-h-[65px] transition-all duration-300">
<a class="flex items-center gap-2 text-xl font-bold text-primary overflow-hidden" href="{% url 'landing' %}">
<span class="material-symbols-outlined shrink-0 text-3xl">location_city</span>
<span class="transition-opacity duration-200 whitespace-nowrap font-display group-data-[collapsed=true]/sidebar:opacity-0 group-data-[collapsed=true]/sidebar:hidden">Admin</span>
</a>
<button id="sidebar-toggle" class="text-on-surface-variant hover:text-primary transition-colors flex items-center justify-center p-1 rounded-md hover:bg-surface-container-low shrink-0" title="Collapse/Expand">
<span class="material-symbols-outlined text-[22px] group-data-[collapsed=true]/sidebar:rotate-180 transition-transform duration-300">menu_open</span>
</button>
</div>"""
content = content.replace(old_sidebar_header, new_sidebar_header)

# 3. Update nav tag
content = content.replace(
    '<nav class="flex-grow p-2 flex flex-col gap-1" aria-label="Admin navigation">',
    '<nav class="flex-grow p-2 flex flex-col gap-1 relative" aria-label="Admin navigation">\n<div id="nav-active-pill" class="absolute top-0 left-2 right-2 rounded-lg bg-primary-container/70 backdrop-blur-md transition-all duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)] z-0 hidden border border-white/40 shadow-sm"></div>'
)

# 4. Update links
content = re.sub(
    r'class="flex items-center gap-3 px-3 py-2\.5 rounded-lg transition-all text-sm font-semibold [^"]*"',
    r'class="group flex items-center gap-3 px-3 py-2.5 rounded-lg text-on-surface-variant hover:bg-surface-container-low transition-all text-sm font-semibold relative z-10"', 
    content
)
content = re.sub(
    r'<span class="material-symbols-outlined shrink-0">([^<]+)</span>\s*([^<]+)</a>',
    r'<span class="material-symbols-outlined shrink-0 group-hover:scale-110 transition-transform">\1</span><span class="transition-opacity duration-200 whitespace-nowrap group-data-[collapsed=true]/sidebar:opacity-0 group-data-[collapsed=true]/sidebar:hidden">\2</span></a>', 
    content
)

# 5. Update header
old_header = """<header class="flex justify-between items-center w-full px-5 h-[65px] sticky top-0 z-40 bg-surface-container-lowest border-b border-outline-variant lg:bg-background lg:border-none">
<div class="lg:hidden flex items-center gap-2 text-primary font-bold font-display"><span class="material-symbols-outlined">location_city</span> CityWatch Admin</div>
<div class="flex items-center gap-4 ml-auto">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-on-surface-variant">account_circle</span>
<span class="text-sm font-semibold text-on-surface hidden sm:block">{{ request.user.username }}</span>
</div>
</div>
</header>"""

new_header = """<header class="border-b border-outline-variant bg-surface-container-lowest sticky top-0 z-40 w-full" style="height: 56px; min-height: 56px;">
<div class="max-w-7xl mx-auto w-full px-4 sm:px-5 lg:px-8 flex items-center justify-between h-full">
<div class="flex items-center lg:hidden mr-auto">
  <a class="flex items-center gap-1 text-lg font-bold text-primary font-display" href="{% url 'landing' %}">
    <span class="material-symbols-outlined text-[20px]">location_city</span>Admin
  </a>
</div>
<div class="flex items-center gap-4 justify-end flex-grow ml-auto">
<div class="flex items-center gap-2 bg-surface-container px-3 py-1.5 rounded-full border border-outline-variant">
<span class="material-symbols-outlined text-on-surface-variant text-[20px]">account_circle</span>
<span class="text-sm font-semibold text-on-surface">{{ request.user.username }}</span>
</div>
</div>
</div>
</header>"""
content = content.replace(old_header, new_header)

# 6. Add Footer
mobile_nav = """
<!-- Mobile Bottom Navigation -->
<nav class="lg:hidden fixed bottom-0 left-0 right-0 bg-surface-container-lowest border-t border-outline-variant flex justify-around items-center h-[64px] z-50 px-2 pb-safe shadow-[0_-4px_20px_rgba(0,0,0,0.05)]">
  <a href="{% url 'analytics_dashboard' %}" class="flex flex-col items-center justify-center w-16 h-full gap-1 text-on-surface-variant mobile-nav-link">
    <div class="px-4 py-1 rounded-full flex items-center justify-center transition-colors">
      <span class="material-symbols-outlined text-[24px]">dashboard</span>
    </div>
    <span class="text-[10px] font-medium leading-none">Home</span>
  </a>
  <a href="{% url 'admin_report_list' %}" class="flex flex-col items-center justify-center w-16 h-full gap-1 text-on-surface-variant mobile-nav-link">
    <div class="px-4 py-1 rounded-full flex items-center justify-center transition-colors">
      <span class="material-symbols-outlined text-[24px]">description</span>
    </div>
    <span class="text-[10px] font-medium leading-none">Reports</span>
  </a>
  <a href="{% url 'reports_analytics' %}" class="flex flex-col items-center justify-center w-16 h-full gap-1 text-on-surface-variant mobile-nav-link">
    <div class="px-4 py-1 rounded-full flex items-center justify-center transition-colors">
      <span class="material-symbols-outlined text-[24px]">analytics</span>
    </div>
    <span class="text-[10px] font-medium leading-none">Stats</span>
  </a>
  <a href="{% url 'map_view' %}" class="flex flex-col items-center justify-center w-16 h-full gap-1 text-on-surface-variant mobile-nav-link">
    <div class="px-4 py-1 rounded-full flex items-center justify-center transition-colors">
      <span class="material-symbols-outlined text-[24px]">map</span>
    </div>
    <span class="text-[10px] font-medium leading-none">Map</span>
  </a>
</nav>
"""
if "Mobile Bottom Navigation" not in content:
    content = content.replace('</body>', mobile_nav + '\n</body>')


# 7. JS Updates
old_js = """    function updateActiveLink(urlPath) {
        sidebarLinks.forEach(link => {
            const href = link.getAttribute('href');
            if ((urlPath.includes(href) && href !== '/') || (href === '/' && urlPath === '/')) {
                link.classList.add('bg-primary-container', 'text-on-primary-container');
                link.classList.remove('text-on-surface-variant', 'hover:bg-surface-container-low');
            } else {
                link.classList.remove('bg-primary-container', 'text-on-primary-container');
                link.classList.add('text-on-surface-variant', 'hover:bg-surface-container-low');
            }
        });
    }"""

new_js = """    const activePill = document.getElementById('nav-active-pill');
    
    function updateActiveLink(urlPath) {
        let activeFound = false;
        sidebarLinks.forEach(link => {
            const href = link.getAttribute('href');
            if ((urlPath.includes(href) && href !== '/') || (href === '/' && urlPath === '/')) {
                activeFound = true;
                if (activePill) {
                    activePill.classList.remove('hidden');
                    activePill.style.transform = `translateY(${link.offsetTop}px)`;
                    activePill.style.height = `${link.offsetHeight}px`;
                }
                link.classList.add('text-on-primary-container');
                link.classList.remove('text-on-surface-variant', 'hover:bg-surface-container-low');
            } else {
                link.classList.remove('text-on-primary-container');
                link.classList.add('text-on-surface-variant', 'hover:bg-surface-container-low');
            }
        });
        if (!activeFound && activePill) activePill.classList.add('hidden');
        
        // Mobile links
        document.querySelectorAll('.mobile-nav-link').forEach(link => {
            const href = link.getAttribute('href');
            if ((urlPath.includes(href) && href !== '/') || (href === '/' && urlPath === '/')) {
                link.classList.add('text-primary');
                link.classList.remove('text-on-surface-variant');
                link.querySelector('div').classList.add('bg-primary-container', 'text-on-primary-container');
            } else {
                link.classList.remove('text-primary');
                link.classList.add('text-on-surface-variant');
                link.querySelector('div').classList.remove('bg-primary-container', 'text-on-primary-container');
            }
        });
    }

    // Sidebar toggle logic
    const sidebar = document.getElementById('admin-sidebar');
    const toggle = document.getElementById('sidebar-toggle');
    if(localStorage.getItem('adminSidebarCollapsed') === 'true' && sidebar) sidebar.setAttribute('data-collapsed', 'true');
    if(toggle && sidebar) {
        toggle.addEventListener('click', () => {
            const state = sidebar.getAttribute('data-collapsed') === 'true' ? 'false' : 'true';
            sidebar.setAttribute('data-collapsed', state);
            localStorage.setItem('adminSidebarCollapsed', state);
            setTimeout(() => updateActiveLink(window.location.pathname), 300);
        });
    }
    
    window.addEventListener('resize', () => updateActiveLink(window.location.pathname));"""

content = content.replace(old_js, new_js)

with open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated admin_base.html with liquid glass effect, minimize button, mobile footer, and consistent header.")
