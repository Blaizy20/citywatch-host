import os
import re

base_dir = r'd:\citywatch\reports\templates\reports'
notif_dir = r'd:\citywatch\notifications\templates\notifications'
out_file = os.path.join(base_dir, 'dashboard.html')

def get_main_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

dashboard_main = get_main_content(out_file)
report_list_main = get_main_content(os.path.join(base_dir, 'report_list.html'))
report_form_main = get_main_content(os.path.join(base_dir, 'report_form.html'))
# fix the form action
report_form_main = report_form_main.replace('<form method="POST"', '<form method="POST" action="{% url \'report_create\' %}"')

public_board_main = get_main_content(os.path.join(base_dir, 'public_board.html'))
announcements_main = get_main_content(os.path.join(base_dir, 'announcements.html'))
notifications_main = get_main_content(os.path.join(notif_dir, 'notification_list.html'))

with open(out_file, 'r', encoding='utf-8') as f:
    dash_full = f.read()

tabbed_main = f'''
<main class="flex-grow max-w-7xl mx-auto w-full px-5 md:px-16 py-8 md:py-12 flex flex-col gap-12 relative">
    <!-- Tab: Overview -->
    <div id="spa-overview" class="spa-tab block w-full transition-opacity duration-300">
        {dashboard_main}
    </div>
    <!-- Tab: Submit Report -->
    <div id="spa-submit" class="spa-tab hidden w-full transition-opacity duration-300">
        {report_form_main}
    </div>
    <!-- Tab: My Reports -->
    <div id="spa-my-reports" class="spa-tab hidden w-full transition-opacity duration-300">
        {report_list_main}
    </div>
    <!-- Tab: Public Board -->
    <div id="spa-public-board" class="spa-tab hidden w-full transition-opacity duration-300">
        {public_board_main}
    </div>
    <!-- Tab: Announcements -->
    <div id="spa-announcements" class="spa-tab hidden w-full transition-opacity duration-300">
        {announcements_main}
    </div>
    <!-- Tab: Notifications -->
    <div id="spa-notifications" class="spa-tab hidden w-full transition-opacity duration-300">
        {notifications_main}
    </div>
</main>

<script>
function navigateSpa() {{
    const hash = window.location.hash || '#spa-overview';
    const tabs = document.querySelectorAll('.spa-tab');
    const links = document.querySelectorAll('.spa-link');
    
    tabs.forEach(tab => {{
        tab.classList.remove('block');
        tab.classList.add('hidden');
    }});
    
    const activeTab = document.querySelector(hash);
    if (activeTab) {{
        activeTab.classList.remove('hidden');
        activeTab.classList.add('block');
    }} else {{
        document.getElementById('spa-overview').classList.remove('hidden');
        document.getElementById('spa-overview').classList.add('block');
    }}
    
    links.forEach(link => {{
        if (link.getAttribute('href') === hash || (hash === '#spa-overview' && link.getAttribute('href') === '#spa-overview')) {{
            link.classList.add('bg-primary-container', 'text-on-primary-container');
            link.classList.remove('text-on-surface-variant', 'hover:bg-surface-container-low', 'text-primary');
            // for mobile
            if (link.querySelector('div')) link.querySelector('div').classList.add('bg-primary-container', 'text-on-primary-container');
            link.classList.add('text-primary');
            link.classList.remove('text-on-surface-variant');
        }} else {{
            link.classList.remove('bg-primary-container', 'text-on-primary-container', 'text-primary');
            link.classList.add('text-on-surface-variant', 'hover:bg-surface-container-low');
            // for mobile
            if (link.querySelector('div')) link.querySelector('div').classList.remove('bg-primary-container', 'text-on-primary-container');
            link.classList.add('text-on-surface-variant');
        }}
    }});
}}

window.addEventListener('hashchange', navigateSpa);
document.addEventListener('DOMContentLoaded', navigateSpa);
</script>
'''

new_dash = re.sub(r'<main[^>]*>.*?</main>', tabbed_main, dash_full, flags=re.DOTALL | re.IGNORECASE)
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(new_dash)
print('Dashboard merged!')
