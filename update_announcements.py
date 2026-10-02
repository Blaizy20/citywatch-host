import codecs

html_content = """{% extends 'analytics/admin_base.html' %}
{% load static %}

{% block content %}
<div class="mx-auto max-w-7xl px-4 py-2 sm:px-6 lg:px-8 w-full">
<div class="mb-6 flex flex-wrap items-end justify-between gap-3">
<div>
<h1 class="text-3xl font-bold font-display text-on-surface tracking-tight">News &amp; Announcements</h1>
<p class="mt-1 max-w-2xl text-sm text-on-surface-variant font-medium">Publish updates, advisories, events, and schedules for residents.</p>
</div>
<a href="{% url 'analytics_dashboard' %}" data-no-spa="true" onclick="if(window.history.length > 1) { event.preventDefault(); this.querySelector('span').classList.add('-translate-x-4', 'opacity-0'); setTimeout(() => window.history.back(), 150); }" class="inline-flex items-center gap-1.5 text-sm font-bold text-on-surface-variant hover:text-primary transition-colors group p-2 hover:bg-surface-container-low rounded-full -mr-2"><span class="material-symbols-outlined text-[20px] transition-all duration-300 group-hover:-translate-x-1 group-active:scale-75">arrow_back</span> Dashboard</a>
</div>

{% if messages %}
<div class="mb-6 space-y-2">
{% for message in messages %}
<div class="rounded-lg border border-secondary border-opacity-20 bg-secondary-container bg-opacity-30 p-4 text-sm font-semibold text-on-surface flex items-center gap-3 shadow-sm" role="status">
<span class="material-symbols-outlined text-secondary">info</span> {{ message }}
</div>
{% endfor %}
</div>
{% endif %}

<div class="grid items-start gap-8 lg:grid-cols-[minmax(22rem,0.9fr)_minmax(0,1.1fr)]">

<!-- Form Section -->
<section class="rounded-2xl border border-outline-variant bg-surface-container-lowest shadow-sm overflow-hidden flex flex-col">
<div class="border-b border-outline-variant px-6 py-4 bg-surface-container-low flex justify-between items-center">
<div>
<h2 class="font-bold text-lg text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-primary">{% if editing_announcement %}edit_document{% else %}campaign{% endif %}</span>
{% if editing_announcement %}Edit Announcement{% else %}New Announcement{% endif %}
</h2>
<p class="mt-0.5 text-xs text-on-surface-variant font-medium">Published updates appear instantly on the resident dashboard.</p>
</div>
</div>

<form id="announcement-form" method="POST" enctype="multipart/form-data" class="space-y-5 p-6" action="{% if editing_announcement %}{% url 'admin_announcement_edit' form.instance.id %}{% else %}{% url 'admin_announcement_list' %}{% endif %}">
{% csrf_token %}
{% if form.non_field_errors %}<div class="rounded-lg border border-error border-opacity-30 bg-error-container p-3 text-sm text-error font-semibold">{{ form.non_field_errors }}</div>{% endif %}

<div class="space-y-1">
<label for="id_title" class="block text-sm font-bold text-on-surface">Title</label>
{{ form.title }}
{% if form.title.errors %}<p class="mt-1 text-xs font-semibold text-error">{{ form.title.errors|striptags }}</p>{% endif %}
</div>

<div class="space-y-1">
<label for="id_announcement_type" class="block text-sm font-bold text-on-surface">Type of Update</label>
{{ form.announcement_type }}
{% if form.announcement_type.errors %}<p class="mt-1 text-xs font-semibold text-error">{{ form.announcement_type.errors|striptags }}</p>{% endif %}
</div>

<div class="space-y-1">
<label for="id_content" class="block text-sm font-bold text-on-surface">Message Details</label>
{{ form.content }}
{% if form.content.errors %}<p class="mt-1 text-xs font-semibold text-error">{{ form.content.errors|striptags }}</p>{% endif %}
</div>

<div class="space-y-1">
<label for="id_event_date" class="block text-sm font-bold text-on-surface flex justify-between">Event Date <span class="font-normal text-on-surface-variant text-xs">(optional)</span></label>
{{ form.event_date }}
{% if form.event_date.errors %}<p class="mt-1 text-xs font-semibold text-error">{{ form.event_date.errors|striptags }}</p>{% endif %}
</div>

<div class="space-y-1">
<label for="id_image" class="block text-sm font-bold text-on-surface flex justify-between">Cover Image <span class="font-normal text-on-surface-variant text-xs">(optional, up to 5 MB)</span></label>
{{ form.image }}
{% if form.image.errors %}<p class="mt-1 text-xs font-semibold text-error">{{ form.image.errors|striptags }}</p>{% endif %}
</div>

<div class="pt-4 border-t border-outline-variant space-y-4">
<label class="flex cursor-pointer items-start gap-3 rounded-lg p-3 hover:bg-surface-container-low transition-colors border border-transparent hover:border-outline-variant">
{{ form.is_published }}
<div class="flex flex-col">
<span class="font-bold text-sm text-on-surface">Publish Immediately</span>
<span class="text-xs text-on-surface-variant font-medium mt-0.5">Leave unchecked to save this securely as a draft.</span>
</div>
</label>

<label class="flex cursor-pointer items-start gap-3 rounded-lg p-3 hover:bg-surface-container-low transition-colors border border-transparent hover:border-outline-variant">
{{ form.is_featured }}
<div class="flex flex-col">
<span class="font-bold text-sm text-on-surface">Feature this Update</span>
<span class="text-xs text-on-surface-variant font-medium mt-0.5">Pins it prominently above all other announcements.</span>
</div>
</label>
</div>

<div class="flex flex-col gap-3 pt-2">
<button type="submit" id="save-announcement-btn" class="inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-primary px-5 py-3 text-[15px] font-bold text-on-primary hover:bg-primary-container hover:text-on-primary-container shadow-sm hover:shadow-md transition-all">
<span class="material-symbols-outlined text-[20px]">publish</span>
{% if editing_announcement %}Update Announcement{% else %}Post Announcement{% endif %}
</button>
{% if editing_announcement %}
<a href="{% url 'admin_announcement_list' %}" class="inline-flex min-h-10 w-full items-center justify-center gap-2 rounded-xl bg-surface-container-low border border-outline-variant px-5 py-2 text-sm font-bold text-on-surface-variant hover:bg-surface-container transition-colors">Cancel Editing</a>
{% endif %}
</div>
</form>
</section>

<!-- List Section -->
<section class="min-w-0 flex flex-col gap-4">
<div class="flex items-center justify-between gap-3 px-1">
<h2 class="font-bold text-lg text-on-surface">Recent Updates</h2>
<span class="rounded-full bg-primary-container text-on-primary-container px-3 py-1 text-xs font-bold shadow-sm">{{ announcements|length }} Total</span>
</div>

<div id="announcement-list-container" class="flex flex-col gap-4">
{% for announcement in announcements %}
<article class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-5 shadow-sm hover:shadow-md transition-all flex flex-col sm:flex-row gap-5 relative group overflow-hidden">
{% if announcement.image %}
<div class="w-full sm:w-32 h-32 shrink-0 rounded-xl overflow-hidden relative bg-surface-container-low border border-outline-variant">
<img src="{{ announcement.image.url }}" alt="" class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105">
</div>
{% else %}
<div class="w-full sm:w-32 h-32 shrink-0 rounded-xl overflow-hidden relative bg-surface-container flex items-center justify-center border border-outline-variant border-dashed">
<span class="material-symbols-outlined text-4xl text-on-surface-variant opacity-30">newspaper</span>
</div>
{% endif %}

<div class="min-w-0 flex-1 flex flex-col">
<div class="flex flex-wrap items-center gap-2 mb-2">
<span class="px-2.5 py-0.5 rounded border border-outline-variant bg-surface-container-low text-[10px] font-bold uppercase tracking-wider text-secondary">{{ announcement.get_announcement_type_display }}</span>
{% if announcement.is_published %}
<span class="flex items-center gap-1 text-[11px] font-bold text-[#166534]"><span class="w-1.5 h-1.5 rounded-full bg-[#166534]"></span>Published</span>
{% else %}
<span class="flex items-center gap-1 text-[11px] font-bold text-[#92400e]"><span class="w-1.5 h-1.5 rounded-full bg-[#d97706]"></span>Draft</span>
{% endif %}
{% if announcement.is_featured %}
<span class="bg-primary text-on-primary px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider flex items-center gap-1"><span class="material-symbols-outlined text-[12px]">star</span>Featured</span>
{% endif %}
</div>

<h3 class="font-display font-bold text-lg text-on-surface leading-tight mb-1">{{ announcement.title }}</h3>
<p class="text-sm text-on-surface-variant line-clamp-2 leading-relaxed mb-3 flex-1">{{ announcement.content }}</p>

<div class="flex flex-wrap items-center justify-between gap-4 mt-auto pt-3 border-t border-outline-variant border-opacity-50">
<p class="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wide">
{% if announcement.event_date %}
<span class="text-primary flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">event</span>{{ announcement.event_date|date:'M d, g:i A' }}</span>
{% else %}
Created {{ announcement.date_created|date:'M d, Y' }}
{% endif %}
</p>

<div class="flex items-center gap-2">
<button type="button" onclick="openPreviewModal('{{ announcement.title|escapejs }}', '{{ announcement.content|escapejs }}', '{{ announcement.get_announcement_type_display|escapejs }}', '{% if announcement.image %}{{ announcement.image.url }}{% endif %}')" class="p-1.5 rounded-lg text-on-surface-variant hover:bg-surface-container hover:text-primary transition-colors flex items-center justify-center tooltip-trigger" title="Preview">
<span class="material-symbols-outlined text-[18px]">visibility</span>
</button>
<a href="{% url 'admin_announcement_edit' announcement.id %}" class="p-1.5 rounded-lg text-on-surface-variant hover:bg-surface-container hover:text-secondary transition-colors flex items-center justify-center tooltip-trigger" title="Edit">
<span class="material-symbols-outlined text-[18px]">edit</span>
</a>
<form method="POST" action="{% url 'admin_announcement_delete' announcement.id %}" class="delete-form m-0 p-0 flex">
{% csrf_token %}
<button type="button" class="delete-btn p-1.5 rounded-lg text-on-surface-variant hover:bg-error-container hover:text-error transition-colors flex items-center justify-center tooltip-trigger" title="Delete">
<span class="material-symbols-outlined text-[18px]">delete</span>
</button>
</form>
</div>
</div>
</div>
</article>
{% empty %}
<div class="rounded-2xl border border-outline-variant border-dashed bg-surface-container-lowest p-10 flex flex-col items-center justify-center text-center">
<div class="w-16 h-16 rounded-full bg-surface-container flex items-center justify-center mb-4"><span class="material-symbols-outlined text-3xl text-primary opacity-50">campaign</span></div>
<h3 class="font-bold text-lg text-on-surface mb-1">No Updates Yet</h3>
<p class="text-sm text-on-surface-variant max-w-sm">Create the first resident announcement to keep your community informed.</p>
</div>
{% endfor %}
</div>
</section>

</div>
</div>

<!-- Preview Modal -->
<dialog id="preview-modal" class="bg-transparent p-0 backdrop:bg-black backdrop:bg-opacity-50 backdrop:backdrop-blur-sm m-auto fixed inset-0 z-[70] w-full h-full" onclick="if(event.target === this) this.close()">
<div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-2xl w-[95vw] max-w-lg mx-auto flex flex-col relative overflow-hidden" style="animation: modalSlideIn 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;">
<div class="p-4 border-b border-outline-variant bg-surface-container flex justify-between items-center">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-primary">smartphone</span>
<span class="font-bold text-sm text-on-surface-variant uppercase tracking-wider">Resident View Preview</span>
</div>
<button type="button" onclick="document.getElementById('preview-modal').close()" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-surface-container-highest transition-colors">
<span class="material-symbols-outlined text-on-surface-variant">close</span>
</button>
</div>
<div class="p-5 overflow-y-auto max-h-[70vh] bg-surface">
<div class="bg-surface-container-lowest border border-outline-variant rounded-2xl overflow-hidden shadow-sm">
<img id="preview-image" src="" class="w-full h-48 object-cover hidden">
<div class="p-5">
<div class="flex items-center gap-2 mb-3">
<span id="preview-type" class="px-2.5 py-1 rounded-full bg-primary-container text-on-primary-container text-[10px] font-bold uppercase tracking-wider"></span>
<span class="text-xs font-semibold text-on-surface-variant">Just now</span>
</div>
<h3 id="preview-title" class="text-xl font-bold font-display text-on-surface mb-2"></h3>
<p id="preview-content" class="text-sm text-on-surface-variant leading-relaxed whitespace-pre-wrap"></p>
<button class="mt-4 w-full py-2.5 rounded-xl border border-outline-variant text-sm font-bold text-primary flex items-center justify-center gap-2 hover:bg-surface-container transition-colors pointer-events-none">
Acknowledge Notice
</button>
</div>
</div>
</div>
</div>
</dialog>

<!-- Delete Confirmation Modal -->
<dialog id="delete-modal" class="bg-transparent p-0 backdrop:bg-black backdrop:bg-opacity-50 backdrop:backdrop-blur-sm m-auto fixed inset-0 z-[60] w-full h-full">
<div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-2xl p-6 w-[90vw] max-w-sm mx-auto text-center" style="animation: modalSlideIn 0.25s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;">
<div class="w-16 h-16 rounded-full bg-error-container text-error flex items-center justify-center mx-auto mb-4">
<span class="material-symbols-outlined text-3xl">delete_forever</span>
</div>
<h3 class="text-xl font-bold font-display text-on-surface mb-2">Delete Announcement?</h3>
<p class="text-sm text-on-surface-variant mb-6 leading-relaxed">This action cannot be undone. This announcement will be permanently removed from the resident dashboard.</p>
<div class="flex justify-center gap-3">
<button type="button" class="px-5 py-2.5 rounded-xl font-bold text-on-surface hover:bg-surface-container transition-colors flex-1" onclick="document.getElementById('delete-modal').close()">Cancel</button>
<button type="button" id="confirm-delete-btn" class="px-5 py-2.5 rounded-xl font-bold bg-error text-on-error hover:bg-[#93000a] transition-colors shadow-sm flex items-center justify-center gap-2 flex-1">Delete</button>
</div>
</div>
</dialog>

<style>
@keyframes modalSlideIn {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
dialog::backdrop {
  animation: backdropFadeIn 0.3s ease forwards;
}
@keyframes backdropFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Ensure inputs are beautifully rounded */
input[type="text"], input[type="datetime-local"], select, textarea {
  width: 100%;
  border-radius: 0.5rem;
  border: 1px solid var(--tw-prose-body, #c4c6cf);
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  background-color: #fdfcff;
  transition: all 0.2s;
}
input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #156b3e;
  box-shadow: 0 0 0 2px rgba(21, 107, 62, 0.2);
}
input[type="file"] {
  width: 100%;
  border-radius: 0.5rem;
  border: 1px dashed #c4c6cf;
  padding: 0.5rem;
  font-size: 0.875rem;
  background-color: #f8f9fc;
}
input[type="checkbox"] {
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 0.25rem;
  border: 1.5px solid #c4c6cf;
  color: #156b3e;
  margin-top: 0.125rem;
}
</style>

<script src="https://unpkg.com/idiomorph/dist/idiomorph-ext.min.js"></script>
<script>
function openPreviewModal(title, content, type, imageUrl) {
    document.getElementById('preview-title').textContent = title;
    document.getElementById('preview-content').textContent = content;
    document.getElementById('preview-type').textContent = type;
    
    const imgEl = document.getElementById('preview-image');
    if (imageUrl) {
        imgEl.src = imageUrl;
        imgEl.classList.remove('hidden');
    } else {
        imgEl.classList.add('hidden');
        imgEl.src = '';
    }
    
    document.getElementById('preview-modal').showModal();
}

(function() {
    // 1. Initialize AutoAnimate
    const listContainer = document.getElementById('announcement-list-container');
    if (listContainer && window.autoAnimate) {
        window.autoAnimate(listContainer);
    } else {
        document.addEventListener('autoAnimateLoaded', () => {
            if (window.autoAnimate) window.autoAnimate(document.getElementById('announcement-list-container'));
        });
    }

    // 2. DOM Morphing Form Submission (Create/Edit)
    const form = document.getElementById('announcement-form');
    const saveBtn = document.getElementById('save-announcement-btn');
    
    if (form && saveBtn) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const originalHtml = saveBtn.innerHTML;
            saveBtn.innerHTML = '<span class="material-symbols-outlined animate-spin">refresh</span> Saving...';
            saveBtn.classList.add('opacity-80', 'pointer-events-none');
            
            try {
                const fd = new FormData(form);
                await fetch(form.action, { method: 'POST', body: fd, headers: {'X-Requested-With': 'XMLHttpRequest'} });
                
                saveBtn.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Saved!';
                saveBtn.classList.remove('bg-primary');
                saveBtn.classList.add('bg-secondary');
                
                await new Promise(r => setTimeout(r, 600));
                
                const res = await fetch("{% url 'admin_announcement_list' %}", { headers: {'X-Requested-With': 'XMLHttpRequest'} });
                const html = await res.text();
                const doc = new DOMParser().parseFromString(html, 'text/html');
                
                const newMain = doc.getElementById('admin-main-content');
                const oldMain = document.getElementById('admin-main-content');
                
                if (newMain && oldMain && window.Idiomorph) {
                    Idiomorph.morph(oldMain, newMain.innerHTML, { morphStyle: 'innerHTML' });
                    // Re-attach scripts
                    const scripts = oldMain.querySelectorAll('script');
                    scripts.forEach(oldScript => {
                        const newScript = document.createElement('script');
                        Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                        oldScript.parentNode.replaceChild(newScript, oldScript);
                    });
                    if (window.attachSPAListeners) window.attachSPAListeners(oldMain);
                }
            } catch (err) {
                console.error(err);
                saveBtn.innerHTML = originalHtml;
                saveBtn.classList.remove('opacity-80', 'pointer-events-none');
            }
        });
    }

    // 3. DOM Morphing Delete Logic
    const deleteModal = document.getElementById('delete-modal');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    let pendingDeleteForm = null;

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            pendingDeleteForm = btn.closest('form');
            deleteModal.showModal();
        });
    });

    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', async () => {
            if (!pendingDeleteForm) return;
            
            const originalHtml = confirmDeleteBtn.innerHTML;
            confirmDeleteBtn.innerHTML = '<span class="material-symbols-outlined animate-spin">refresh</span> Deleting...';
            confirmDeleteBtn.classList.add('opacity-80', 'pointer-events-none');
            
            try {
                const fd = new FormData(pendingDeleteForm);
                await fetch(pendingDeleteForm.action, { method: 'POST', body: fd, headers: {'X-Requested-With': 'XMLHttpRequest'} });
                
                confirmDeleteBtn.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Deleted!';
                confirmDeleteBtn.classList.remove('bg-error');
                confirmDeleteBtn.classList.add('bg-secondary');
                
                await new Promise(r => setTimeout(r, 600));
                deleteModal.close();
                
                const res = await fetch("{% url 'admin_announcement_list' %}", { headers: {'X-Requested-With': 'XMLHttpRequest'} });
                const html = await res.text();
                const doc = new DOMParser().parseFromString(html, 'text/html');
                
                const newMain = doc.getElementById('admin-main-content');
                const oldMain = document.getElementById('admin-main-content');
                
                if (newMain && oldMain && window.Idiomorph) {
                    Idiomorph.morph(oldMain, newMain.innerHTML, { morphStyle: 'innerHTML' });
                    // Re-attach scripts
                    const scripts = oldMain.querySelectorAll('script');
                    scripts.forEach(oldScript => {
                        const newScript = document.createElement('script');
                        Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                        oldScript.parentNode.replaceChild(newScript, oldScript);
                    });
                    if (window.attachSPAListeners) window.attachSPAListeners(oldMain);
                }
            } catch (err) {
                console.error(err);
                confirmDeleteBtn.innerHTML = originalHtml;
                confirmDeleteBtn.classList.remove('opacity-80', 'pointer-events-none', 'bg-secondary');
                confirmDeleteBtn.classList.add('bg-error');
                deleteModal.close();
            }
        });
    }
})();
</script>
{% endblock %}
"""

with codecs.open('d:/citywatch/reports/templates/reports/admin_announcement_list.html', 'w', 'utf-8') as f:
    f.write(html_content)
