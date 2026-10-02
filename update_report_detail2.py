import codecs

html_content = """{% extends 'analytics/admin_base.html' %}

{% block content %}

<!-- Back Navigation header for SPA -->
<div class="flex items-center gap-4 mb-2">
<a href="{% url 'admin_report_list' %}" class="p-2 hover:bg-surface-container-low rounded-full transition-colors flex items-center justify-center text-on-surface-variant -ml-2" aria-label="Go back">
<span class="material-symbols-outlined">arrow_back</span></a>
<h1 class="text-2xl font-bold font-display text-on-surface tracking-tight">Report Management</h1>
</div>

{% if messages %}
<div class="w-full flex flex-col gap-2 mb-4">
{% for message in messages %}
<div class="p-3 rounded bg-secondary-container text-on-secondary-container text-sm shadow-sm">{{ message }}</div>
{% endfor %}
</div>
{% endif %}

<!-- ID added for morphing -->
<div id="report-detail-morph-target" class="flex flex-col xl:flex-row gap-6 w-full relative">

<div class="flex-1 flex flex-col gap-4">
<div class="bg-surface-container-lowest p-6 rounded-xl border border-outline-variant shadow-sm">
<div class="flex justify-between items-start mb-4 flex-wrap gap-3">
<div>
<div class="flex items-center gap-3 mb-2">
<span class="text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.15em]">Report #CW-{{ report.id }}</span>
<span class="px-2.5 py-0.5 rounded-full bg-primary-container text-on-primary-container text-[11px] font-bold uppercase tracking-wider">{{ report.get_urgency_display }} Priority</span>
</div>
<h2 class="text-4xl font-bold font-display tracking-tight text-on-surface mb-2 mt-1">{{ report.title }}</h2>
</div>
{% if report.status == 'pending' %}
<span class="px-3 py-1 rounded-full bg-[#fef3c7] text-[#92400e] font-semibold border border-[#fde68a] flex items-center gap-1.5 shadow-sm">
<span class="w-2 h-2 rounded-full bg-[#d97706]"></span> Pending</span>
{% elif report.status == 'in_progress' %}
<span class="px-3 py-1 rounded-full bg-primary text-on-primary font-semibold flex items-center gap-1.5 shadow-sm">In Progress</span>
{% elif report.status == 'resolved' %}
<span class="px-3 py-1 rounded-full bg-secondary text-on-secondary font-semibold flex items-center gap-1.5 shadow-sm">Resolved</span>
{% else %}
<span class="px-3 py-1 rounded-full bg-gray-200 text-gray-800 font-semibold flex items-center gap-1.5 shadow-sm">{{ report.get_status_display }}</span>
{% endif %}
</div>
<div class="flex flex-wrap gap-6 text-on-surface-variant">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-outline">calendar_today</span>
<span>{{ report.date_submitted|date:"M d, Y • h:i A" }}</span>
</div>
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-outline">location_on</span>
<span>{{ report.barangay }}</span>
</div>
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-outline">person</span>
<span>Reported by: {{ report.resident.get_full_name|default:report.resident.username }}</span>
</div>
</div>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
<div class="bg-surface-container-lowest p-6 rounded-xl border border-outline-variant shadow-sm md:col-span-2">
<h3 class="text-xl font-semibold mb-4 text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-primary">description</span> Description</h3>
<p class="text-lg text-on-surface-variant leading-relaxed">{{ report.description }}</p>
</div>

{% if report.photo %}
<div class="bg-surface-container-lowest p-6 rounded-xl border border-outline-variant shadow-sm md:col-span-2">
<div class="flex justify-between items-center mb-4">
<h3 class="text-xl font-semibold text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-primary">photo_library</span> Evidence</h3>
<span class="text-xs text-on-surface-variant bg-surface-container px-2.5 py-1 rounded-full font-semibold">Click image to enlarge</span>
</div>
<button type="button" class="w-full relative group overflow-hidden rounded-xl border border-outline-variant bg-surface-container-low focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2" onclick="document.getElementById('image-lightbox').showModal()">
<img src="{{ report.photo.url }}" class="w-full h-auto max-h-[500px] object-contain transition-transform duration-500 group-hover:scale-[1.01]">
<div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center pointer-events-none">
<div class="w-14 h-14 rounded-full bg-black bg-opacity-50 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 scale-75 group-hover:scale-100 transition-all duration-300 backdrop-blur-sm">
<span class="material-symbols-outlined text-3xl">zoom_in</span>
</div>
</div>
</button>
</div>
{% endif %}

{% if report.latitude and report.longitude %}
<div class="bg-surface-container-lowest p-6 rounded-xl border border-outline-variant shadow-sm md:col-span-2">
<h3 class="text-xl font-semibold mb-4 text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-primary">map</span> Location</h3>
<p class="text-sm text-on-surface-variant">Lat: {{ report.latitude }}, Lng: {{ report.longitude }}</p>
</div>
{% endif %}
</div>
</div>

<aside class="w-full xl:w-96 flex flex-col gap-4 shrink-0">

<div class="bg-surface-container-lowest p-6 rounded-xl border border-outline-variant shadow-sm">
<h3 class="text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.15em] mb-4">Status Management</h3>
<div class="flex flex-col gap-3" id="status-selection-group">
<button type="button" data-status="pending" class="status-btn w-full py-3 px-4 border rounded-lg text-sm flex justify-between items-center transition-all font-semibold {% if report.status == 'pending' %}border-secondary bg-secondary-container text-on-secondary-container{% else %}border-outline-variant text-on-surface hover:bg-surface-container{% endif %}">
Mark as Pending <span class="material-symbols-outlined">schedule</span>
</button>
<button type="button" data-status="in_progress" class="status-btn w-full py-3 px-4 border rounded-lg text-sm flex justify-between items-center transition-all font-semibold {% if report.status == 'in_progress' %}border-primary bg-primary text-on-primary{% else %}border-outline-variant text-on-surface hover:bg-surface-container{% endif %}">
Set to In Progress <span class="material-symbols-outlined">engineering</span>
</button>
<button type="button" data-status="resolved" class="status-btn w-full py-3 px-4 border rounded-lg text-sm flex justify-between items-center transition-all font-semibold {% if report.status == 'resolved' %}border-[#166534] bg-[#dcfce7] text-[#166534]{% else %}border-outline-variant text-on-surface hover:bg-surface-container{% endif %}">
Mark as Resolved <span class="material-symbols-outlined">check_circle</span>
</button>
</div>
</div>

<div class="bg-surface-container-lowest p-6 rounded-xl border border-outline-variant shadow-sm">
<h3 class="text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.15em] mb-4">Coordinate with Department</h3>
<div id="department-grid" class="grid grid-cols-2 gap-2">
{% for dept in departments %}
<button type="button" data-dept="{{ dept.id }}"
  class="dept-btn py-2.5 px-3 border rounded-lg flex flex-col items-center justify-center gap-2 transition-all font-semibold {% if forloop.counter > 4 %}hidden dept-extra{% endif %}
  {% if assignment.department_id == dept.id %}border-2 border-primary bg-primary-container text-on-primary-container{% else %}border-outline-variant text-on-surface hover:bg-surface-container{% endif %}">
<div class="w-10 h-10 rounded-full {% if assignment.department_id == dept.id %}bg-primary text-on-primary{% else %}bg-surface-container-highest text-on-surface-variant{% endif %} flex items-center justify-center transition-colors">
<span class="material-symbols-outlined">{% if dept.name == 'Fire' %}local_fire_department{% elif dept.name == 'Health' %}medical_services{% elif dept.name == 'DPWH' %}construction{% elif dept.name == 'Barangay Tanod' %}local_police{% else %}apartment{% endif %}</span>
</div>
<span class="text-xs text-center">{{ dept.name }}</span>
</button>
{% empty %}
<p class="text-sm text-on-surface-variant col-span-2">No departments yet.</p>
{% endfor %}
</div>
{% if departments|length > 4 %}<button type="button" id="toggle-departments" class="mt-3 text-sm font-semibold text-primary hover:underline">See More</button>{% endif %}
</div>

<!-- Sticky floating Apply Changes Button, appears only when changes are made -->
<div id="apply-changes-container" class="sticky bottom-4 z-10 transition-all duration-300 opacity-0 translate-y-4 pointer-events-none">
    <button id="apply-changes-btn" type="button" class="w-full py-4 bg-primary text-on-primary rounded-xl font-bold shadow-lg hover:bg-primary-container hover:shadow-xl transition-all flex items-center justify-center gap-2 text-lg">
        <span class="material-symbols-outlined">save</span> Apply Changes
    </button>
</div>

<div class="bg-surface-container-lowest p-6 rounded-xl border border-outline-variant shadow-sm flex-1 flex flex-col">
<h3 class="text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.15em] mb-4">Internal Notes &amp; Updates</h3>
<form id="note-form" method="POST" action="{% url 'add_note' report.id %}" class="flex flex-col flex-1">
{% csrf_token %}
<textarea name="note" class="w-full flex-1 min-h-[100px] rounded-lg border border-outline-variant p-3 text-sm focus:border-primary focus:ring-1 focus:ring-primary resize-none mb-3 bg-surface" placeholder="Add coordination notes for staff here..."></textarea>
<div class="flex justify-end">
<button type="submit" class="px-4 py-2 bg-primary text-on-primary rounded-lg text-sm font-semibold hover:bg-primary-container transition-colors shadow-sm flex items-center gap-2">
<span class="material-symbols-outlined text-[18px]">send</span> Post Update</button>
</div>
</form>

<div class="mt-6 pt-4 border-t border-outline-variant">
<h4 class="text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.15em] mb-3">Recent Activity</h4>
<div class="space-y-4 max-h-[300px] overflow-y-auto pr-2">
{% for log in status_logs %}
<div class="flex gap-3">
<div class="w-6 h-6 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center shrink-0 mt-0.5">
<span class="material-symbols-outlined text-[14px]">history</span>
</div>
<div>
<p class="text-sm text-on-surface">{{ log.notes|default:"Status updated" }}</p>
<p class="text-xs text-on-surface-variant mt-0.5">
{% if log.changed_by %}By {{ log.changed_by.username }}{% else %}By System{% endif %}
- {{ log.timestamp|date:"M d, Y h:i A" }}</p>
</div>
</div>
{% empty %}
<p class="text-sm text-on-surface-variant">No activity yet.</p>
{% endfor %}
</div>
</div>
</div>

</aside>
</div>

<!-- Modals -->
<dialog id="confirm-modal" class="bg-transparent p-0 backdrop:bg-black backdrop:bg-opacity-50 backdrop:backdrop-blur-sm m-auto fixed inset-0 z-50">
<div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-2xl p-6 w-[90vw] max-w-md mx-auto" style="animation: modalSlideIn 0.25s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;">
<h3 class="text-xl font-bold font-display text-on-surface flex items-center gap-2 mb-2">
<span class="material-symbols-outlined text-primary text-2xl">warning</span> Apply Changes?
</h3>
<p class="text-sm text-on-surface-variant mb-8 leading-relaxed">You are about to modify the status or department assignment of this report. This action may instantly notify the resident and the assigned department.</p>
<div class="flex justify-end gap-3">
<button type="button" class="px-4 py-2.5 rounded-xl font-bold text-on-surface hover:bg-surface-container transition-colors" onclick="document.getElementById('confirm-modal').close()">Cancel</button>
<button type="button" id="confirm-apply-btn" class="px-5 py-2.5 rounded-xl font-bold bg-primary text-on-primary hover:bg-primary-container transition-colors shadow-sm flex items-center gap-2">Confirm Update</button>
</div>
</div>
</dialog>

{% if report.photo %}
<dialog id="image-lightbox" class="bg-transparent p-0 backdrop:bg-black backdrop:bg-opacity-90 backdrop:backdrop-blur-md m-auto fixed inset-0 z-[60] w-full h-full" onclick="if(event.target === this) this.close()">
<div class="w-full h-full flex flex-col items-center justify-center p-4 md:p-12 relative pointer-events-none">
<button type="button" class="absolute top-6 right-6 w-12 h-12 bg-black bg-opacity-50 text-white rounded-full flex items-center justify-center hover:bg-opacity-80 transition-all backdrop-blur-sm border border-white border-opacity-20 z-10 pointer-events-auto" onclick="document.getElementById('image-lightbox').close()"><span class="material-symbols-outlined">close</span></button>
<img src="{{ report.photo.url }}" class="max-w-full max-h-full object-contain rounded-lg shadow-2xl pointer-events-auto" style="animation: modalScaleUp 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;" onclick="event.stopPropagation()">
</div>
</dialog>
{% endif %}

<style>
@keyframes modalSlideIn {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes modalScaleUp {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
dialog::backdrop {
  animation: backdropFadeIn 0.3s ease forwards;
}
@keyframes backdropFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>

<!-- Ensure Idiomorph is loaded for morphing updates -->
<script src="https://unpkg.com/idiomorph/dist/idiomorph-ext.min.js"></script>
<script>
(function() {
    // Initial server state
    const originalStatus = "{{ report.status }}";
    const originalDept = "{{ assignment.department_id|default:'' }}";
    
    // Mutable client state
    let selectedStatus = originalStatus;
    let selectedDept = originalDept;
    
    // UI Elements
    const statusBtns = document.querySelectorAll('.status-btn');
    const deptBtns = document.querySelectorAll('.dept-btn');
    const applyContainer = document.getElementById('apply-changes-container');
    const applyBtn = document.getElementById('apply-changes-btn');
    const toggleDepartments = document.getElementById('toggle-departments');
    
    // Update Apply Button Visibility
    function checkChanges() {
        const hasChanges = (selectedStatus !== originalStatus) || (selectedDept !== originalDept);
        if (hasChanges) {
            applyContainer.classList.remove('opacity-0', 'translate-y-4', 'pointer-events-none');
        } else {
            applyContainer.classList.add('opacity-0', 'translate-y-4', 'pointer-events-none');
        }
    }
    
    // Status Button Click Logic
    statusBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            selectedStatus = btn.getAttribute('data-status');
            
            // Reset visually
            statusBtns.forEach(b => {
                b.classList.remove('border-secondary', 'bg-secondary-container', 'text-on-secondary-container', 'border-primary', 'bg-primary', 'text-on-primary', 'border-[#166534]', 'bg-[#dcfce7]', 'text-[#166534]');
                b.classList.add('border-outline-variant', 'text-on-surface');
            });
            
            // Style active
            if (selectedStatus === 'pending') {
                btn.classList.remove('border-outline-variant', 'text-on-surface');
                btn.classList.add('border-secondary', 'bg-secondary-container', 'text-on-secondary-container');
            } else if (selectedStatus === 'in_progress') {
                btn.classList.remove('border-outline-variant', 'text-on-surface');
                btn.classList.add('border-primary', 'bg-primary', 'text-on-primary');
            } else if (selectedStatus === 'resolved') {
                btn.classList.remove('border-outline-variant', 'text-on-surface');
                btn.classList.add('border-[#166534]', 'bg-[#dcfce7]', 'text-[#166534]');
            }
            
            checkChanges();
        });
    });
    
    // Department Button Click Logic
    deptBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Toggle off if clicking the same one
            if (selectedDept === btn.getAttribute('data-dept')) {
                selectedDept = '';
            } else {
                selectedDept = btn.getAttribute('data-dept');
            }
            
            // Reset visually
            deptBtns.forEach(b => {
                b.classList.remove('border-2', 'border-primary', 'bg-primary-container', 'text-on-primary-container');
                b.classList.add('border-outline-variant', 'text-on-surface');
                const iconContainer = b.querySelector('div');
                iconContainer.classList.remove('bg-primary', 'text-on-primary');
                iconContainer.classList.add('bg-surface-container-highest', 'text-on-surface-variant');
            });
            
            // Style active
            if (selectedDept) {
                const activeBtn = document.querySelector(`.dept-btn[data-dept="${selectedDept}"]`);
                if (activeBtn) {
                    activeBtn.classList.remove('border-outline-variant', 'text-on-surface');
                    activeBtn.classList.add('border-2', 'border-primary', 'bg-primary-container', 'text-on-primary-container');
                    const iconContainer = activeBtn.querySelector('div');
                    iconContainer.classList.remove('bg-surface-container-highest', 'text-on-surface-variant');
                    iconContainer.classList.add('bg-primary', 'text-on-primary');
                }
            }
            
            checkChanges();
        });
    });
    
    // Apply Changes Submission via fetch
    if (applyBtn) {
        applyBtn.addEventListener('click', () => {
            document.getElementById('confirm-modal').showModal();
        });
        
        document.getElementById('confirm-apply-btn').addEventListener('click', async () => {
            document.getElementById('confirm-modal').close();
            
            applyBtn.innerHTML = '<span class="material-symbols-outlined animate-spin">refresh</span> Saving...';
            applyBtn.classList.add('opacity-80', 'pointer-events-none');
            
            try {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                
                // Submit Status if changed
                if (selectedStatus !== originalStatus) {
                    const fd = new FormData();
                    fd.append('csrfmiddlewaretoken', csrfToken);
                    fd.append('status', selectedStatus);
                    await fetch("{% url 'update_status' report.id %}", { method: 'POST', body: fd, headers: {'X-Requested-With': 'XMLHttpRequest'} });
                }
                
                // Submit Dept if changed
                if (selectedDept !== originalDept) {
                    const fd = new FormData();
                    fd.append('csrfmiddlewaretoken', csrfToken);
                    if (selectedDept) fd.append('department', selectedDept); // Might need logic if unassigning
                    await fetch("{% url 'assign_report' report.id %}", { method: 'POST', body: fd, headers: {'X-Requested-With': 'XMLHttpRequest'} });
                }
                
                // Fetch the updated page seamlessly and morph
                const res = await fetch(window.location.href, { headers: {'X-Requested-With': 'XMLHttpRequest'} });
                const html = await res.text();
                const doc = new DOMParser().parseFromString(html, 'text/html');
                
                const newMain = doc.getElementById('admin-main-content');
                const oldMain = document.getElementById('admin-main-content');
                
                if (newMain && oldMain && window.Idiomorph) {
                    Idiomorph.morph(oldMain, newMain.innerHTML, { morphStyle: 'innerHTML' });
                    // Scripts must be re-evaluated since we replaced everything inside main
                    const scripts = oldMain.querySelectorAll('script');
                    scripts.forEach(oldScript => {
                        const newScript = document.createElement('script');
                        Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                        oldScript.parentNode.replaceChild(newScript, oldScript);
                    });
                }
                
            } catch (err) {
                console.error('Error applying changes:', err);
                applyBtn.innerHTML = '<span class="material-symbols-outlined">error</span> Error';
            }
        });
    }
    
    // Notes submission seamless AJAX morph
    const noteForm = document.getElementById('note-form');
    if (noteForm) {
        noteForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = noteForm.querySelector('button[type="submit"]');
            const originalHtml = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="material-symbols-outlined animate-spin">refresh</span>...';
            submitBtn.classList.add('opacity-80', 'pointer-events-none');
            
            try {
                const fd = new FormData(noteForm);
                await fetch(noteForm.action, { method: 'POST', body: fd, headers: {'X-Requested-With': 'XMLHttpRequest'} });
                
                const res = await fetch(window.location.href, { headers: {'X-Requested-With': 'XMLHttpRequest'} });
                const html = await res.text();
                const doc = new DOMParser().parseFromString(html, 'text/html');
                
                const newMain = doc.getElementById('admin-main-content');
                const oldMain = document.getElementById('admin-main-content');
                
                if (newMain && oldMain && window.Idiomorph) {
                    Idiomorph.morph(oldMain, newMain.innerHTML, { morphStyle: 'innerHTML' });
                    const scripts = oldMain.querySelectorAll('script');
                    scripts.forEach(oldScript => {
                        const newScript = document.createElement('script');
                        Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                        oldScript.parentNode.replaceChild(newScript, oldScript);
                    });
                }
            } catch (err) {
                console.error(err);
                submitBtn.innerHTML = originalHtml;
                submitBtn.classList.remove('opacity-80', 'pointer-events-none');
            }
        });
    }

    if (toggleDepartments) {
        toggleDepartments.addEventListener('click', () => {
            document.querySelectorAll('.dept-extra').forEach((option) => option.classList.toggle('hidden'));
            toggleDepartments.textContent = toggleDepartments.textContent === 'See More' ? 'See Less' : 'See More';
        });
    }
})();
</script>
{% endblock %}
"""

with codecs.open('d:/citywatch/reports/templates/reports/admin_report_detail.html', 'w', 'utf-8') as f:
    f.write(html_content)
