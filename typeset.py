import re
import os

files_to_update = [
    'd:/citywatch/analytics/templates/analytics/dashboard.html',
    'd:/citywatch/reports/templates/reports/admin_report_list.html',
    'd:/citywatch/reports/templates/reports/admin_announcement_list.html',
    'd:/citywatch/analytics/templates/analytics/reports_analytics.html',
    'd:/citywatch/analytics/templates/analytics/map_view.html',
    'd:/citywatch/accounts/templates/accounts/user_list.html',
    'd:/citywatch/assignments/templates/assignments/department_list.html'
]

for fpath in files_to_update:
    if not os.path.exists(fpath): continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Typesetting Hierarchy Adjustments
    
    # 1. Page Titles (h1/h2) - Increase size to 4xl, use tracking-tight, and make it text-on-surface for higher contrast instead of colored
    content = re.sub(r'class="([^"]*)text-3xl font-bold font-display text-primary([^"]*)"', 
                     r'class="\1text-4xl font-bold font-display tracking-tight text-on-surface\2"', content)
    content = re.sub(r'class="([^"]*)text-3xl font-bold font-display([^"]*)"', 
                     r'class="\1text-4xl font-bold font-display tracking-tight text-on-surface\2"', content)
    
    # 2. Secondary section titles (h2/h3) - Make them 2xl, tracking-tight, text-on-surface
    content = re.sub(r'class="([^"]*)text-xl font-semibold text-primary([^"]*)"', 
                     r'class="\1text-2xl font-display font-semibold text-on-surface tracking-tight\2"', content)

    # 3. Subtitles / Lead paragraphs - Increase to text-lg, relaxed leading
    content = re.sub(r'<p class="text-on-surface-variant">([^<]*?)</p>', 
                     r'<p class="text-lg text-on-surface-variant leading-relaxed mt-1">\1</p>', content)
    content = re.sub(r'<p class="text-base text-on-surface-variant">([^<]*?)</p>', 
                     r'<p class="text-lg text-on-surface-variant leading-relaxed mt-1">\1</p>', content)

    # 4. Big Stat Numbers - text-5xl, leading-none, tracking-tight
    content = re.sub(r'class="([^"]*)text-4xl font-bold text-on-surface([^"]*)"', 
                     r'class="\1text-5xl font-display font-bold text-on-surface leading-none tracking-tight\2"', content)

    # 5. Overlines / Labels (e.g. "Total Reports") - Extra tracking, bold
    content = re.sub(r'class="([^"]*)text-xs font-semibold text-on-surface-variant uppercase tracking-wider([^"]*)"', 
                     r'class="\1text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.15em] mb-2\2"', content)

    # 6. Table Headers - Bold, uppercase, extra tracking
    content = re.sub(r'class="([^"]*)text-xs text-on-surface-variant font-medium([^"]*)"', 
                     r'class="\1text-[11px] font-bold text-on-surface-variant uppercase tracking-wider\2"', content)
    content = re.sub(r'class="([^"]*)text-xs text-on-surface-variant uppercase tracking-wider([^"]*)"', 
                     r'class="\1text-[11px] font-bold text-on-surface-variant uppercase tracking-[0.1em]\2"', content)

    # 7. List table th text sizes
    content = re.sub(r'<th class="([^"]*)py-4 px-6 font-semibold([^"]*)">',
                     r'<th class="\1py-4 px-6 text-[12px] uppercase tracking-wider font-bold\2">', content)

    # 8. Action Links - Slightly smaller, bold, tracking-wide
    content = re.sub(r'class="([^"]*)text-primary text-sm font-semibold hover:underline([^"]*)"', 
                     r'class="\1text-primary text-[14px] font-bold tracking-wide hover:underline\2"', content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {fpath}")
