import codecs

with codecs.open('d:/citywatch/accounts/templates/accounts/user_list.html', 'r', 'utf-8') as f:
    html = f.read()

target_avatar = """{% else %}bg-surface-container-highest text-on-surface-variant{% endif %}">"""
replacement_avatar = """{% else %}bg-[#dcfce7] text-[#166534]{% endif %}">"""

if target_avatar in html:
    html = html.replace(target_avatar, replacement_avatar)

target_badge = """<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold bg-surface-container text-on-surface-variant border border-outline-variant uppercase tracking-wide">
                <span class="material-symbols-outlined text-[14px]">person</span> Resident
              </span>"""
replacement_badge = """<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold bg-[#dcfce7] text-[#166534] border border-[#bbf7d0] uppercase tracking-wide">
                <span class="material-symbols-outlined text-[14px]">person</span> Resident
              </span>"""

if target_badge in html:
    html = html.replace(target_badge, replacement_badge)

with codecs.open('d:/citywatch/accounts/templates/accounts/user_list.html', 'w', 'utf-8') as f:
    f.write(html)
