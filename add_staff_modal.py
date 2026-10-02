import codecs

with codecs.open('d:/citywatch/accounts/templates/accounts/user_list.html', 'r', 'utf-8') as f:
    html = f.read()

target_form_start = """              <form method="POST" action="{% url 'toggle_staff' u.id %}" class="inline-block" onsubmit="return confirm('Are you sure you want to change permissions for {{ u.username }}?');">"""
replacement_form_start = """              <form method="POST" action="{% url 'toggle_staff' u.id %}" class="inline-block" onsubmit="event.preventDefault(); window.openStaffModal(this, '{{ u.username|escapejs }}', {% if u.is_staff %}false{% else %}true{% endif %});">"""

html = html.replace(target_form_start, replacement_form_start)

target_endblock = """{% endblock %}"""
modal_and_js = """
<!-- Staff Confirmation Modal -->
<dialog id="confirm-staff-modal" class="bg-transparent p-0 backdrop:bg-black backdrop:bg-opacity-50 backdrop:backdrop-blur-sm m-auto fixed inset-0 z-50" onclick="if(event.target === this) this.close()">
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-2xl p-6 w-[90vw] max-w-md mx-auto" style="animation: modalScaleUp 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;">
    <h3 class="text-xl font-bold font-display text-on-surface flex items-center gap-2 mb-3" id="modal-staff-title">
      <span class="material-symbols-outlined text-primary text-2xl">security</span> Change Access Role?
    </h3>
    <p class="text-sm text-on-surface-variant mb-5 leading-relaxed" id="modal-staff-message">
      You are about to change the access permissions for this user.
    </p>
    
    <div class="p-4 rounded-xl border mb-6 flex items-start gap-3" id="modal-staff-warning-box">
      <span class="material-symbols-outlined text-[20px] mt-0.5" id="modal-staff-warning-icon">info</span>
      <p class="text-xs font-medium leading-relaxed" id="modal-staff-warning-text">Warning text here</p>
    </div>

    <div class="flex justify-end gap-3">
      <button type="button" class="px-4 py-2.5 rounded-xl font-bold text-on-surface hover:bg-surface-container transition-colors" onclick="document.getElementById('confirm-staff-modal').close()">Cancel</button>
      <button type="button" id="modal-staff-confirm-btn" class="px-5 py-2.5 rounded-xl font-bold text-white transition-colors shadow-sm flex items-center gap-2" onclick="window.confirmStaffAction()">Confirm</button>
    </div>
  </div>
</dialog>

<script>
  let pendingStaffForm = null;

  window.openStaffModal = function(form, username, isGranting) {
      pendingStaffForm = form;
      const modal = document.getElementById('confirm-staff-modal');
      const title = document.getElementById('modal-staff-title');
      const message = document.getElementById('modal-staff-message');
      const warningBox = document.getElementById('modal-staff-warning-box');
      const warningIcon = document.getElementById('modal-staff-warning-icon');
      const warningText = document.getElementById('modal-staff-warning-text');
      const confirmBtn = document.getElementById('modal-staff-confirm-btn');

      if (isGranting) {
          title.innerHTML = `<span class="material-symbols-outlined text-primary text-2xl">security</span> Grant Staff Access`;
          message.innerHTML = `You are about to promote <strong>${username}</strong> to a Staff/Admin role.`;
          
          warningBox.className = 'p-4 rounded-xl border mb-6 flex items-start gap-3 bg-primary-container/30 border-primary/20 text-primary';
          warningIcon.textContent = 'admin_panel_settings';
          warningText.innerHTML = `This user will gain access to the <strong>Admin Dashboard</strong>, allowing them to view analytics, update reports, and manage internal notes.`;
          
          confirmBtn.className = 'px-5 py-2.5 rounded-xl font-bold bg-primary hover:bg-primary-container text-on-primary transition-colors shadow-sm flex items-center gap-2';
          confirmBtn.innerHTML = `Grant Access`;
      } else {
          title.innerHTML = `<span class="material-symbols-outlined text-[#991b1b] text-2xl">person_off</span> Revoke Staff Access`;
          message.innerHTML = `You are about to revoke Staff privileges from <strong>${username}</strong>.`;
          
          warningBox.className = 'p-4 rounded-xl border mb-6 flex items-start gap-3 bg-[#fee2e2] border-[#fecaca] text-[#991b1b]';
          warningIcon.textContent = 'warning';
          warningText.innerHTML = `This user will be downgraded to a standard Resident. They will immediately lose access to the Admin Dashboard and all administrative tools.`;
          
          confirmBtn.className = 'px-5 py-2.5 rounded-xl font-bold bg-[#dc2626] hover:bg-[#b91c1c] text-white transition-colors shadow-sm flex items-center gap-2';
          confirmBtn.innerHTML = `Revoke Access`;
      }

      modal.showModal();
  };

  window.confirmStaffAction = function() {
      if (pendingStaffForm) {
          pendingStaffForm.submit();
      }
  };
</script>
<style>
@keyframes modalScaleUp {
    0% { opacity: 0; transform: scale(0.95) translateY(10px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
{% endblock %}"""

html = html.replace(target_endblock, modal_and_js)

with codecs.open('d:/citywatch/accounts/templates/accounts/user_list.html', 'w', 'utf-8') as f:
    f.write(html)
