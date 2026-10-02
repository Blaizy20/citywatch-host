import codecs

html = '''{% extends 'analytics/admin_base.html' %}
{% load static %}
{% block content %}

<div class="mx-auto max-w-7xl px-4 py-2 sm:px-6 lg:px-8 w-full">

  <!-- Header Area -->
  <div class="mb-8 flex flex-wrap items-end justify-between gap-3">
    <div>
      <h1 class="text-3xl font-bold font-display text-on-surface tracking-tight flex items-center gap-2">
        <span class="material-symbols-outlined text-primary text-[32px]">settings</span>
        System Settings
      </h1>
      <p class="mt-1 max-w-2xl text-sm text-on-surface-variant font-medium">Manage operational departments and external agency integrations.</p>
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

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">

    <!-- Departments Table -->
    <div class="lg:col-span-2 bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm overflow-hidden">
      <div class="p-6 border-b border-outline-variant bg-surface-container-low/50 flex justify-between items-center">
        <div>
          <h3 class="font-bold text-lg text-on-surface">Registered Departments</h3>
          <p class="text-xs font-medium text-on-surface-variant">Agencies available for report coordination.</p>
        </div>
        <div class="flex items-center gap-2 text-sm font-bold text-on-surface-variant bg-surface-container px-3 py-1.5 rounded-lg border border-outline-variant">
          <span class="material-symbols-outlined text-[18px]">apartment</span>
          {{ departments|length }} Total
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-surface">
              <th class="p-4 pl-6 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant w-1/3">Agency Name</th>
              <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Description</th>
              <th class="p-4 pr-6 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant text-right w-24">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-outline-variant">
            {% for dept in departments %}
            <tr class="hover:bg-surface-container-low transition-colors group">
              <td class="p-4 pl-6">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center shrink-0 shadow-sm">
                    <span class="material-symbols-outlined text-[20px]">{% if dept.name == 'Fire' %}local_fire_department{% elif dept.name == 'Health' %}medical_services{% elif dept.name == 'DPWH' %}construction{% elif dept.name == 'Barangay Tanod' %}local_police{% else %}apartment{% endif %}</span>
                  </div>
                  <span class="font-bold text-on-surface text-sm">{{ dept.name }}</span>
                </div>
              </td>
              <td class="p-4 text-sm text-on-surface-variant leading-relaxed">
                {{ dept.description|default:"<span class='opacity-50 italic'>No description provided</span>"|safe }}
              </td>
              <td class="p-4 pr-6 text-right">
                <form method="POST" action="{% url 'department_delete' dept.id %}" class="inline-block" onsubmit="event.preventDefault(); window.openDeleteModal(this, '{{ dept.name|escapejs }}');">
                  {% csrf_token %}
                  <button type="submit" title="Remove Department" class="inline-flex items-center justify-center bg-surface hover:bg-[#fee2e2] text-[#991b1b] border border-outline-variant hover:border-[#fecaca] transition-colors p-2 rounded-lg group-hover:shadow-sm">
                    <span class="material-symbols-outlined text-[18px]">delete</span>
                  </button>
                </form>
              </td>
            </tr>
            {% empty %}
            <tr><td colspan="3" class="p-12 text-center text-on-surface-variant font-medium bg-surface-container-lowest">No departments configured yet.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add Department Form -->
    <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 shadow-sm sticky top-6">
      <div class="flex items-center gap-3 mb-6 pb-4 border-b border-outline-variant">
        <div class="w-10 h-10 rounded-xl bg-primary-container text-on-primary-container flex items-center justify-center shadow-inner">
          <span class="material-symbols-outlined">add_business</span>
        </div>
        <div>
          <h3 class="font-bold text-lg text-on-surface">Add Agency</h3>
          <p class="text-xs font-medium text-on-surface-variant">Register a new department</p>
        </div>
      </div>
      
      <form method="POST" class="flex flex-col gap-5">
        {% csrf_token %}
        <div class="group">
          <label class="block text-[11px] font-bold text-on-surface-variant uppercase tracking-wider mb-2">Department Name</label>
          <div class="relative">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px] opacity-50 group-focus-within:opacity-100 group-focus-within:text-primary transition-colors">domain</span>
            <input type="text" name="name" required class="w-full pl-10 pr-4 py-2.5 bg-surface text-on-surface border border-outline-variant rounded-xl focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all text-sm font-medium" placeholder="e.g., Public Works">
          </div>
        </div>
        
        <div class="group">
          <label class="block text-[11px] font-bold text-on-surface-variant uppercase tracking-wider mb-2">Description <span class="normal-case tracking-normal font-normal opacity-70">(Optional)</span></label>
          <textarea name="description" rows="3" class="w-full p-3 bg-surface text-on-surface border border-outline-variant rounded-xl focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all text-sm resize-none" placeholder="Briefly describe their responsibilities..."></textarea>
        </div>
        
        <button type="submit" class="w-full mt-2 bg-primary hover:bg-primary-container text-on-primary font-bold py-3 px-4 rounded-xl shadow-md hover:shadow-lg transition-all flex justify-center items-center gap-2">
          <span class="material-symbols-outlined text-[20px]">add</span> Register Department
        </button>
      </form>
    </div>

  </div>
</div>

<!-- Custom Delete Modal -->
<dialog id="delete-modal" class="bg-transparent p-0 backdrop:bg-black backdrop:bg-opacity-50 backdrop:backdrop-blur-sm m-auto fixed inset-0 z-50" onclick="if(event.target === this) this.close()">
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-2xl p-6 w-[90vw] max-w-md mx-auto" style="animation: modalScaleUp 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;">
    <h3 class="text-xl font-bold font-display text-on-surface flex items-center gap-2 mb-3">
      <span class="material-symbols-outlined text-[#991b1b] text-2xl">warning</span> Delete Department?
    </h3>
    <p class="text-sm text-on-surface-variant mb-5 leading-relaxed">
      You are about to permanently remove <strong id="modal-dept-name" class="text-on-surface"></strong>.
    </p>
    
    <div class="p-4 rounded-xl border mb-6 flex items-start gap-3 bg-[#fee2e2] border-[#fecaca] text-[#991b1b]">
      <span class="material-symbols-outlined text-[20px] mt-0.5">delete_forever</span>
      <p class="text-xs font-medium leading-relaxed">This action cannot be undone. Reports currently assigned to this department might lose their routing information.</p>
    </div>

    <div class="flex justify-end gap-3">
      <button type="button" class="px-4 py-2.5 rounded-xl font-bold text-on-surface hover:bg-surface-container transition-colors" onclick="document.getElementById('delete-modal').close()">Cancel</button>
      <button type="button" class="px-5 py-2.5 rounded-xl font-bold bg-[#dc2626] hover:bg-[#b91c1c] text-white transition-colors shadow-sm flex items-center gap-2" onclick="window.confirmDeleteAction()">Delete</button>
    </div>
  </div>
</dialog>

<script>
  let pendingDeleteForm = null;

  window.openDeleteModal = function(form, deptName) {
      pendingDeleteForm = form;
      document.getElementById('modal-dept-name').textContent = deptName;
      document.getElementById('delete-modal').showModal();
  };

  window.confirmDeleteAction = function() {
      if (pendingDeleteForm) {
          pendingDeleteForm.submit();
      }
  };
</script>

<style>
@keyframes modalScaleUp {
    0% { opacity: 0; transform: scale(0.95) translateY(10px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}
</style>

{% endblock %}
'''

with codecs.open('d:/citywatch/assignments/templates/assignments/department_list.html', 'w', 'utf-8') as f:
    f.write(html)
