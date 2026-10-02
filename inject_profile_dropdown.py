import codecs

with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_header.html', 'r', 'utf-8') as f:
    resident_html = f.read()

# Find the profile dropdown container in resident_header.html
start_idx = resident_html.find('<div class="relative" id="profile-dropdown-container">')

# To be completely safe, we'll find the last </header> and work backwards
# or just extract until the last </div></div></div>
end_idx = resident_html.rfind('</header>')

if start_idx != -1 and end_idx != -1:
    profile_html = resident_html[start_idx:end_idx]
    
    # Clean up trailing closing divs
    profile_html = profile_html.strip()
    while profile_html.endswith('</div>'):
        profile_html = profile_html[:-6].strip()
    profile_html += '\n</div>' # Add back the one for the container
    
    # We should also replace #spa-settings with # since admin might not have spa-settings
    profile_html = profile_html.replace('#spa-settings', '#')

    with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'r', 'utf-8') as f:
        admin_html = f.read()
    
    admin_chip = """<div class="flex items-center gap-2 bg-surface-container px-3 py-1.5 rounded-full border border-outline-variant">
<span class="material-symbols-outlined text-on-surface-variant text-[20px]">account_circle</span>
<span class="text-sm font-semibold text-on-surface">{{ request.user.username }}</span>
</div>"""
    
    if admin_chip in admin_html:
        admin_html = admin_html.replace(admin_chip, profile_html)
        with codecs.open('d:/citywatch/analytics/templates/analytics/admin_base.html', 'w', 'utf-8') as f:
            f.write(admin_html)
        print('Profile dropdown injected to admin_base.html successfully')
    else:
        print('Admin chip NOT FOUND in admin_base.html')
else:
    print('Profile dropdown NOT FOUND in resident_header.html')

