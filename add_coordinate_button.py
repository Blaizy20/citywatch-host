import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/map_view.html', 'r', 'utf-8') as f:
    html = f.read()

target = '<td class="p-4 text-sm text-on-surface-variant font-mono text-xs">{{ report.latitude|floatformat:4 }}, {{ report.longitude|floatformat:4 }}</td>'

replacement = '''<td class="p-4 text-sm text-on-surface-variant font-mono text-xs">
  <button type="button" title="Pinpoint on map" class="inline-flex items-center gap-1.5 bg-surface-container hover:bg-primary-container hover:text-primary transition-colors px-2 py-1 rounded border border-outline-variant hover:border-primary group-hover:bg-primary-container group-hover:text-primary" onclick="event.stopPropagation(); focusMapOn({{ report.latitude|default_if_none:'null' }}, {{ report.longitude|default_if_none:'null' }}, {{ report.id }})">
    <span class="material-symbols-outlined text-[16px]">my_location</span>
    <span>{{ report.latitude|floatformat:4 }}, {{ report.longitude|floatformat:4 }}</span>
  </button>
</td>'''

if target in html:
    html = html.replace(target, replacement)
    
    tr_target = '<tr class="hover:bg-surface-container-low transition-colors group cursor-pointer" onclick="focusMapOn({{ report.latitude|default_if_none:\'null\' }}, {{ report.longitude|default_if_none:\'null\' }}, {{ report.id }})">'
    tr_replacement = '<tr class="hover:bg-surface-container-low transition-colors group">'
    html = html.replace(tr_target, tr_replacement)

    with codecs.open('d:/citywatch/analytics/templates/analytics/map_view.html', 'w', 'utf-8') as f:
        f.write(html)
    print('Success')
else:
    print('Target not found')
