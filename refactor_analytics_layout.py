import codecs
import re

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'r', 'utf-8') as f:
    html = f.read()

# Extract Hero Card Content
hero_match = re.search(r'<!-- Hero Card: Total Reports -->(.*?)<!-- Resolution Time -->', html, re.DOTALL)
hero_content = hero_match.group(1).strip()
hero_content = re.sub(r'lg:col-span-2 lg:row-span-3', 'h-full', hero_content)

# Extract Resolution Time Content
res_match = re.search(r'<!-- Resolution Time -->(.*?)<!-- Pending Action -->', html, re.DOTALL)
res_content = res_match.group(1).strip()
res_content = re.sub(r'lg:col-span-1', 'flex-1', res_content)

# Extract Pending Action Content
pen_match = re.search(r'<!-- Pending Action -->(.*?)<!-- Top Category -->', html, re.DOTALL)
pen_content = pen_match.group(1).strip()
pen_content = re.sub(r'lg:col-span-1', 'flex-1', pen_content)

# Extract Top Category Content
cat_match = re.search(r'<!-- Top Category -->(.*?)</div>\s*<!-- Trend Line Chart -->', html, re.DOTALL)
cat_content = cat_match.group(1).strip()
cat_content = re.sub(r'lg:col-span-1', 'flex-1', cat_content)

# Extract Trend Chart Content
trend_match = re.search(r'<!-- Trend Line Chart -->(.*?)<!-- Charts Row -->', html, re.DOTALL)
trend_content = trend_match.group(1).strip()
trend_content = re.sub(r'mb-8', 'h-full', trend_content, count=1) # Remove mb-8 from trend chart card

# Extract Status Chart Content
status_match = re.search(r'<!-- Status Chart -->(.*?)<!-- Category Chart -->', html, re.DOTALL)
status_content = status_match.group(1).strip()

# Extract Category Chart Content
category_match = re.search(r'<!-- Category Chart -->(.*?)</div>\s*<!-- Barangay Breakdown -->', html, re.DOTALL)
category_content = category_match.group(1).strip()

# Extract Barangay Heatmap Content
barangay_match = re.search(r'<!-- Barangay Breakdown -->(.*?)</div>\s*<script>', html, re.DOTALL)
barangay_content = barangay_match.group(1).strip()
barangay_content = re.sub(r'mb-8', 'h-full', barangay_content, count=1)

new_layout = f'''<!-- Dashboard Master Grid Top Row -->
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8 items-stretch">
  
  <!-- Hero Card: Total Reports -->
  <div class="lg:col-span-4 flex flex-col h-full">
    <!-- Hero Card: Total Reports -->
    {hero_content}
  </div>

  <!-- Small Stats Stack -->
  <div class="lg:col-span-3 flex flex-col gap-6 justify-between h-full">
    <!-- Resolution Time -->
    {res_content}
    
    <!-- Pending Action -->
    {pen_content}
    
    <!-- Top Category -->
    {cat_content}
  </div>

  <!-- Trend Line Chart -->
  <div class="lg:col-span-5 flex flex-col h-full">
    <!-- Trend Line Chart -->
    {trend_content}
  </div>

</div>

<!-- Dashboard Master Grid Bottom Row -->
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8 items-stretch">
  <div class="lg:col-span-3 flex flex-col h-full">
    <!-- Status Chart -->
    {status_content}
  </div>
  
  <div class="lg:col-span-3 flex flex-col h-full">
    <!-- Category Chart -->
    {category_content}
  </div>
  
  <div class="lg:col-span-6 flex flex-col h-full">
    <!-- Barangay Breakdown -->
    {barangay_content}
  </div>
</div>
'''

# Replace everything from Overview Stats Cards down to the script tag
full_replacement = re.sub(r'<!-- Overview Stats Cards -->.*?(?=</div>\s*<script>)', new_layout, html, flags=re.DOTALL)

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'w', 'utf-8') as f:
    f.write(full_replacement)
