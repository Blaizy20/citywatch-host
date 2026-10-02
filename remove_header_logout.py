import codecs
import re

with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_header.html', 'r', 'utf-8') as f:
    header_html = f.read()

pattern = re.compile(r'<div class="h-px bg-outline-variant/30 my-1 mx-2"></div>\s*<a href="#" onclick="window\.openLogoutModal\(event\)".*?Logout\s*</a>', re.DOTALL)
header_html = pattern.sub('', header_html)

with codecs.open('d:/citywatch/reports/templates/reports/partials/resident_header.html', 'w', 'utf-8') as f:
    f.write(header_html)
