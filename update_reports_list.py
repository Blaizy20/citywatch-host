import codecs

html_content = """{% extends 'analytics/admin_base.html' %}

{% block content %}
<div class="flex flex-col gap-5 w-full">

<div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
<div>
<h1 class="text-4xl font-bold font-display tracking-tight text-on-surface mb-2">Community Reports Log</h1>
<p class="text-lg text-on-surface-variant leading-relaxed mt-1">Review, track, and manage incoming civic reports.</p>
</div>
<form id="admin-reports-form" method="GET" data-no-spa="true" class="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
<input type="hidden" name="view" value="{{ view_mode }}">
<div class="relative flex-grow sm:max-w-xs">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
<input name="q" value="{{ search_query }}" class="w-full pl-10 pr-4 py-2 border border-outline-variant rounded-lg bg-surface-container-lowest focus:outline-none focus:border-primary h-[44px]" placeholder="Search reports..." type="search">
</div>
<select name="status" class="px-4 py-2 border border-outline-variant rounded-lg bg-surface-container-lowest h-[44px]">
<option value="">All Status</option>
<option value="pending" {% if status_filter == 'pending' %}selected{% endif %}>Pending</option>
<option value="acknowledged" {% if status_filter == 'acknowledged' %}selected{% endif %}>Acknowledged</option>
<option value="in_progress" {% if status_filter == 'in_progress' %}selected{% endif %}>In Progress</option>
<option value="resolved" {% if status_filter == 'resolved' %}selected{% endif %}>Resolved</option>
</select>
<select name="category" class="px-4 py-2 border border-outline-variant rounded-lg bg-surface-container-lowest h-[44px]">
<option value="">All Categories</option>
{% for value, label in category_choices %}<option value="{{ value }}" {% if category_filter == value %}selected{% endif %}>{{ label }}</option>{% endfor %}
</select>
</form>
</div>

<!-- Removed animate-stagger from parent to avoid annoying flash -->
<div id="admin-reports-content" class="relative flex flex-col gap-6">
<div class="flex items-center justify-between">
<span class="text-xs font-bold text-on-surface-variant uppercase tracking-[0.1em] showing-count">Showing {{ reports|length }} entries</span>
<div class="flex items-center bg-surface-container-low p-1 rounded-lg border border-outline-variant">
<a href="?view=list{% if search_query %}&q={{ search_query|urlencode }}{% endif %}{% if status_filter %}&status={{ status_filter }}{% endif %}{% if category_filter %}&category={{ category_filter }}{% endif %}" data-no-spa="true" class="view-mode-link flex items-center gap-2 px-4 py-2 rounded-lg {% if view_mode == 'list' %}bg-primary text-on-primary{% else %}text-on-surface-variant hover:bg-surface-container-high{% endif %} text-sm font-semibold transition-colors"><span class="material-symbols-outlined text-[18px]">list</span>List View</a>
<a href="?view=visual{% if search_query %}&q={{ search_query|urlencode }}{% endif %}{% if status_filter %}&status={{ status_filter }}{% endif %}{% if category_filter %}&category={{ category_filter }}{% endif %}" data-no-spa="true" class="view-mode-link flex items-center gap-2 px-4 py-2 rounded-lg {% if view_mode == 'visual' %}bg-primary text-on-primary{% else %}text-on-surface-variant hover:bg-surface-container-high{% endif %} text-sm font-semibold transition-colors"><span class="material-symbols-outlined text-[18px]">grid_view</span>Visual View</a>
</div>
</div>

{% if view_mode == 'list' %}
<div class="bg-surface-container-lowest border border-outline-variant rounded-xl shadow-sm overflow-hidden">
<div class="overflow-x-auto">
<!-- Swapped <table> for a CSS Grid / Flex implementation to perfectly support AutoAnimate FLIP physics without stretching -->
<div class="w-full text-left min-w-[900px] flex flex-col">
<!-- Header Row -->
<div class="bg-surface-container-low border-b border-outline-variant text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.1em] grid grid-cols-[2.5fr_2fr_1.5fr_1.5fr_160px] gap-4">
<div class="py-4 px-6 text-[12px] uppercase tracking-wider font-bold">Report Info</div>
<div class="py-4 px-6 text-[12px] uppercase tracking-wider font-bold">Location</div>
<div class="py-4 px-6 text-[12px] uppercase tracking-wider font-bold">Date Submitted</div>
<div class="py-4 px-6 text-[12px] uppercase tracking-wider font-bold">Status</div>
<div class="py-4 px-6 text-[12px] uppercase tracking-wider font-bold text-right">Actions</div>
</div>
<!-- Body Rows -->
<!-- Removed overflow-hidden from here to prevent the button from being cut off! -->
<div id="auto-animate-target" class="divide-y divide-outline-variant animate-stagger flex flex-col relative w-full">
{% for report in reports %}
<div id="report-row-{{ report.id }}" class="hover:bg-surface-container-low transition-colors group item-node grid grid-cols-[2.5fr_2fr_1.5fr_1.5fr_160px] items-center w-full bg-surface-container-lowest gap-4">
<div class="py-4 px-6">
<div class="flex flex-col">
<span class="font-bold text-primary">{{ report.title }}</span>
<span class="text-xs text-on-surface-variant">Reported by: {{ report.resident.get_full_name|default:report.resident.username }}</span>
</div>
</div>
<div class="py-4 px-6">
<div class="flex items-start gap-2">
<span class="material-symbols-outlined text-secondary mt-0.5">location_on</span>
<span>{{ report.barangay }}</span>
</div>
</div>
<div class="py-4 px-6 text-on-surface-variant">{{ report.date_submitted|date:"M d, Y" }}</div>
<div class="py-4 px-6">
{% if report.status == 'pending' %}
<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs bg-[#FEF08A] text-[#854D0E] font-bold">Pending</span>
{% elif report.status == 'acknowledged' %}
<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs bg-blue-100 text-blue-800 font-bold">Acknowledged</span>
{% elif report.status == 'in_progress' %}
<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs bg-primary text-on-primary font-bold">In Progress</span>
{% elif report.status == 'resolved' %}
<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs bg-secondary text-on-secondary font-bold">Resolved</span>
{% else %}
<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs bg-gray-200 text-gray-800 font-bold">Closed</span>
{% endif %}
</div>
<div class="py-4 px-6 text-right">
<a href="{% url 'admin_report_detail' report.id %}" class="px-4 py-2 border border-outline rounded-lg text-primary hover:bg-primary-fixed hover:border-primary transition-colors text-sm font-bold whitespace-nowrap inline-block">
View Details</a>
</div>
</div>
{% empty %}
<div id="empty-state-row" class="p-6 text-center text-on-surface-variant empty-state w-full">No reports found.</div>
{% endfor %}
</div>
</div>
</div>
</div>
{% else %}
<!-- Added animate-stagger directly to grid -->
<div id="auto-animate-target" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 animate-stagger relative">
{% for report in reports %}
<article id="report-card-{{ report.id }}" class="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm flex flex-col hover:shadow-md transition-shadow item-node">
<div class="h-48 bg-surface-container-low flex items-center justify-center overflow-hidden relative">
{% if report.photo %}<img alt="{{ report.title }}" class="w-full h-full object-cover" src="{{ report.photo.url }}">{% else %}<span class="material-symbols-outlined text-6xl text-on-surface-variant opacity-20">image</span>{% endif %}
{% if report.status == 'pending' %}<span class="absolute top-3 right-3 rounded-full bg-[#FEF08A] text-[#854D0E] px-2.5 py-1 text-xs font-bold">Pending</span>{% elif report.status == 'in_progress' %}<span class="absolute top-3 right-3 rounded-full bg-primary-container text-on-primary-container px-2.5 py-1 text-xs font-bold">In Progress</span>{% elif report.status == 'resolved' %}<span class="absolute top-3 right-3 rounded-full bg-secondary text-on-secondary px-2.5 py-1 text-xs font-bold">Resolved</span>{% else %}<span class="absolute top-3 right-3 rounded-full bg-gray-200 text-gray-800 px-2.5 py-1 text-xs font-bold">{{ report.get_status_display }}</span>{% endif %}
</div>
<div class="p-4 flex flex-col gap-2 flex-1">
<div class="flex justify-between items-start gap-2"><h3 class="text-lg font-bold text-primary">{{ report.title }}</h3><span class="rounded bg-primary-fixed px-2 py-0.5 text-xs font-semibold text-primary">{{ report.get_category_display }}</span></div>
<p class="text-xs text-on-surface-variant">Rep: {{ report.resident.get_full_name|default:report.resident.username }}</p>
<div class="flex items-start gap-1 text-on-surface-variant mt-1"><span class="material-symbols-outlined text-[18px] text-secondary">location_on</span><span class="text-xs">{{ report.barangay }}</span></div>
<div class="mt-auto pt-4 flex items-center justify-between border-t border-outline-variant"><span class="text-xs text-on-surface-variant">{{ report.date_submitted|date:"M d, Y" }}</span><a href="{% url 'admin_report_detail' report.id %}" class="text-primary font-bold text-xs hover:underline">View Details</a></div>
</div>
</article>
{% empty %}<div id="empty-state-card" class="col-span-full bg-surface-container-lowest border border-outline-variant rounded-xl p-12 text-center text-on-surface-variant empty-state">No reports found.</div>{% endfor %}
</div>
{% endif %}
</div>
</div>
<script>
(function() {
    function attachLocalListeners() {
        const form = document.getElementById('admin-reports-form');
        const contentContainer = document.getElementById('admin-reports-content');
        
        if (!form || !contentContainer) return;
        
        // Custom AutoAnimate Plugin to completely prevent stretching/squishing!
        // This explicitly forbids AutoAnimate from animating width/height.
        const nonStretchingPlugin = (el, action, oldCoords, newCoords) => {
            let keyframes;
            // Exit early if missing coords for remain
            if (action === 'remain' && oldCoords && newCoords) {
                const deltaX = oldCoords.left - newCoords.left;
                const deltaY = oldCoords.top - newCoords.top;
                keyframes = [
                    { transform: `translate(${deltaX}px, ${deltaY}px)` },
                    { transform: 'translate(0, 0)' }
                ];
            } else if (action === 'add') {
                keyframes = [
                    { transform: 'scale(0.98)', opacity: 0 },
                    { transform: 'scale(1)', opacity: 1 }
                ];
            } else if (action === 'remove') {
                keyframes = [
                    { transform: 'scale(1)', opacity: 1 },
                    { transform: 'scale(0.98)', opacity: 0 }
                ];
            } else {
                return; // Fallback
            }
            return new KeyframeEffect(el, keyframes, { duration: 350, easing: 'cubic-bezier(0.2, 0.8, 0.2, 1)' });
        };
        
        // Initialize AutoAnimate robustly
        const targetContainer = document.getElementById('auto-animate-target');
        function initAutoAnimate() {
            if (targetContainer && window.autoAnimate) {
                window.autoAnimate(targetContainer, nonStretchingPlugin);
            }
        }
        if (window.autoAnimate) {
            initAutoAnimate();
        } else {
            window.addEventListener('autoAnimateLoaded', initAutoAnimate);
        }
        
        async function fetchUpdate(url, isViewSwitch = false) {
            try {
                const res = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
                const html = await res.text();
                const doc = new DOMParser().parseFromString(html, 'text/html');
                const newContent = doc.getElementById('admin-reports-content');
                
                if (!newContent) return;
                
                const oldTarget = contentContainer.querySelector('#auto-animate-target');
                const newTarget = newContent.querySelector('#auto-animate-target');
                
                if (!isViewSwitch && oldTarget && newTarget && oldTarget.tagName === newTarget.tagName) {
                    // Update content via DOM Morphing!
                    if (window.Idiomorph) {
                        Idiomorph.morph(oldTarget, newTarget.innerHTML, { morphStyle: 'innerHTML' });
                    } else {
                        oldTarget.innerHTML = newTarget.innerHTML;
                    }
                    
                    const oldCount = contentContainer.querySelector('.showing-count');
                    const newCount = newContent.querySelector('.showing-count');
                    if (oldCount && newCount) oldCount.innerHTML = newCount.innerHTML;
                    
                    document.querySelectorAll('.view-mode-link').forEach((link, idx) => {
                        const newLinks = newContent.querySelectorAll('.view-mode-link');
                        if (newLinks[idx]) {
                            link.href = newLinks[idx].href;
                            link.className = newLinks[idx].className;
                        }
                    });
                } else {
                    // View mode changed: replace entire container.
                    contentContainer.innerHTML = newContent.innerHTML;
                    
                    const oldViewInput = form.querySelector('input[name="view"]');
                    const newViewInput = doc.querySelector('form input[name="view"]');
                    if (oldViewInput && newViewInput) {
                        oldViewInput.value = newViewInput.value;
                    }
                    
                    attachViewLinks();
                    const nextTarget = document.getElementById('auto-animate-target');
                    if (nextTarget && window.autoAnimate) {
                        window.autoAnimate(nextTarget, nonStretchingPlugin);
                    }
                }
                
                window.history.replaceState({}, '', url);
            } catch (err) {
                console.error("Local SPA filter error:", err);
            }
        }

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const url = new URL(window.location.origin + window.location.pathname);
            const formData = new FormData(form);
            for (const pair of formData) {
                if (pair[1]) url.searchParams.set(pair[0], pair[1]);
            }
            fetchUpdate(url.toString(), false);
        });
        
        const selects = form.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', () => {
                form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
            });
        });

        const searchInput = form.querySelector('input[type="search"]');
        let debounceTimer;
        if (searchInput) {
            searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') e.preventDefault();
            });
            searchInput.addEventListener('input', () => {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
                }, 300);
            });
        }

        function attachViewLinks() {
            document.querySelectorAll('.view-mode-link').forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    let urlStr = link.getAttribute('href');
                    let targetUrl;
                    if (urlStr.startsWith('?')) {
                        targetUrl = window.location.pathname + urlStr;
                    } else {
                        targetUrl = urlStr;
                    }
                    fetchUpdate(targetUrl, true); // true = isViewSwitch
                });
            });
        }
        
        attachViewLinks();
    }
    
    attachLocalListeners();
})();
</script>
{% endblock %}
"""

with codecs.open('d:/citywatch/reports/templates/reports/admin_report_list.html', 'w', 'utf-8') as f:
    f.write(html_content)
