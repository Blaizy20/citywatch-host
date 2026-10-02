import codecs
import re

with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_header.html', 'r', 'utf-8') as f:
    resident_html = f.read()

# Find the profile dropdown container in resident_header.html
start_idx = resident_html.find('<div class="relative" id="profile-dropdown-container">')
end_idx = resident_html.rfind('</header>')

if start_idx != -1 and end_idx != -1:
    profile_html = resident_html[start_idx:end_idx].strip()
    while profile_html.endswith('</div>'):
        profile_html = profile_html[:-6].strip()
    profile_html += '\n</div>' 
    profile_html = profile_html.replace('#spa-settings', '#')
    # Use window.openLogoutModal
    # the replacement logic handles everything

    with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'r', 'utf-8') as f:
        admin_html = f.read()

    # Regex to match the admin chip robustly
    pattern = re.compile(r'<div class="flex items-center gap-2 bg-surface-container px-3 py-1\.5 rounded-full border border-outline-variant">\s*<span class="material-symbols-outlined text-on-surface-variant text-\[20px\]">account_circle</span>\s*<span class="text-sm font-semibold text-on-surface">{{ request\.user\.username }}</span>\s*</div>', re.DOTALL)
    
    if pattern.search(admin_html):
        # We need to escape backslashes if any, in profile_html for re.sub, or just use python string replace
        # We'll extract the exact match and do string replace to avoid regex sub issues
        match = pattern.search(admin_html).group(0)
        admin_html = admin_html.replace(match, profile_html)
        
        with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'w', 'utf-8') as f:
            f.write(admin_html)
        print('Profile dropdown injected to admin_base.html successfully')
    else:
        print('Admin chip NOT FOUND using regex')
else:
    print('Profile dropdown NOT FOUND in resident_header.html')
