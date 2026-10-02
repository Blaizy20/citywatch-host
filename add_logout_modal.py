import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'r', 'utf-8') as f:
    html = f.read()

target_link = """<a href="{% url 'logout' %}" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-error hover:bg-error-container hover:text-on-error-container transition-all text-sm font-semibold">"""
replacement_link = """<a href="#" onclick="event.preventDefault(); document.getElementById('logout-modal').showModal();" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-error hover:bg-error-container hover:text-on-error-container transition-all text-sm font-semibold">"""

if target_link in html:
    html = html.replace(target_link, replacement_link)

modal_html = """
<!-- Logout Confirmation Modal -->
<dialog id="logout-modal" class="bg-transparent p-0 backdrop:bg-black backdrop:bg-opacity-50 backdrop:backdrop-blur-sm m-auto fixed inset-0 z-[100]" onclick="if(event.target === this) this.close()">
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-2xl p-6 w-[90vw] max-w-sm mx-auto" style="animation: modalScaleUp 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;">
    <div class="flex flex-col items-center text-center">
      <div class="w-16 h-16 rounded-full bg-[#fee2e2] text-[#991b1b] flex items-center justify-center mb-4 shadow-inner">
        <span class="material-symbols-outlined text-3xl">logout</span>
      </div>
      <h3 class="text-xl font-bold font-display text-on-surface mb-2">Ready to Leave?</h3>
      <p class="text-sm text-on-surface-variant mb-6 leading-relaxed">
        You are about to securely log out of your administrative session. You will need to re-enter your credentials to access the dashboard again.
      </p>
    </div>
    <div class="flex flex-col gap-3">
      <a href="{% url 'logout' %}" data-no-spa="true" class="w-full py-3 rounded-xl font-bold bg-[#dc2626] hover:bg-[#b91c1c] text-white transition-colors shadow-sm flex items-center justify-center gap-2">
        <span class="material-symbols-outlined text-[20px]">logout</span> Confirm Log Out
      </a>
      <button type="button" class="w-full py-3 rounded-xl font-bold text-on-surface-variant hover:bg-surface-container transition-colors" onclick="document.getElementById('logout-modal').close()">
        Cancel
      </button>
    </div>
  </div>
</dialog>
<style>
@keyframes modalScaleUp {
    0% { opacity: 0; transform: scale(0.95) translateY(10px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
</body>"""

if "</body>" in html:
    html = html.replace("</body>", modal_html)

with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'w', 'utf-8') as f:
    f.write(html)
