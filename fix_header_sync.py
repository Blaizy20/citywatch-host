import codecs

with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_header.html', 'r', 'utf-8') as f:
    resident_html = f.read()

# 1. Remove Search Bar
search_form = """<form method="GET" action="{% url 'public_board' %}" class="relative">
<label class="sr-only" for="resident-search">Search reports or news</label>
<input id="resident-search" name="q" value="{{ search_query|default:'' }}" type="search" placeholder="Search reports or news..." class="resident-search border border-outline-variant bg-background py-2 pl-10 pr-4 text-sm text-on-surface focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-base text-on-surface-variant">search</span>
</form>"""

if search_form in resident_html:
    resident_html = resident_html.replace(search_form, '')
    print("Search form removed from resident_header.html")
else:
    print("Search form not found in resident_header.html")

# Find profile dropdown
start_idx = resident_html.find('<div class="relative" id="profile-dropdown-container">')
end_idx = resident_html.find('</header>')

if start_idx != -1 and end_idx != -1:
    # Need to extract just the profile-dropdown-container div
    # It has a closing div, followed by two more closing divs before </header>
    # The html structure is:
    # <div class="relative" id="profile-dropdown-container"> ... </div>
    # </div>
    # </div>
    # </header>
    
    # We want to extract up to the end of profile-dropdown-container
    profile_html = resident_html[start_idx:end_idx]
    
    # We need to trim off the trailing </div></div> which belong to parent containers
    profile_html = profile_html.rsplit('</div>', 2)[0] + '</div>\n'
    
    print("Profile dropdown extracted successfully")

    # Now replace the basic chip in admin_base.html
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
        print("Admin chip replaced successfully in admin_base.html")
    else:
        print("Admin chip NOT FOUND in admin_base.html")

with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_header.html', 'w', 'utf-8') as f:
    f.write(resident_html)

