import codecs

with codecs.open('d:/citywatch/reports/templates/reports/admin_report_detail.html', 'r', 'utf-8') as f:
    html = f.read()

target = """{% if report.latitude and report.longitude %}
<div class="bg-surface-container-lowest p-6 rounded-xl border border-outline-variant shadow-sm md:col-span-2">
<h3 class="text-xl font-semibold mb-4 text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-primary">map</span> Location</h3>
<p class="text-sm text-on-surface-variant">Lat: {{ report.latitude }}, Lng: {{ report.longitude }}</p>
</div>
{% endif %}"""

replacement = """{% if report.latitude and report.longitude %}
<div class="bg-surface-container-lowest p-6 rounded-xl border border-outline-variant shadow-sm md:col-span-2">
<div class="flex justify-between items-center mb-4">
  <h3 class="text-xl font-semibold text-on-surface flex items-center gap-2">
    <span class="material-symbols-outlined text-primary">map</span> Location</h3>
  <span class="text-xs text-on-surface-variant font-mono bg-surface-container px-2.5 py-1 rounded-full">Lat: {{ report.latitude|floatformat:4 }}, Lng: {{ report.longitude|floatformat:4 }}</span>
</div>
<div id="detailMap" class="w-full h-[350px] rounded-xl z-10 border border-outline-variant/50 shadow-inner"></div>
<script>
(function() {
    if (window.detailMapInst) {
        window.detailMapInst.remove();
        window.detailMapInst = null;
    }
    
    // Check if L exists (from admin_base.html)
    if (typeof L === 'undefined') return;

    const lat = {{ report.latitude|default:'null' }};
    const lng = {{ report.longitude|default:'null' }};
    
    if (lat && lng) {
        const map = L.map('detailMap', { zoomControl: false }).setView([lat, lng], 17);
        window.detailMapInst = map;
        
        L.tileLayer('https://api.maptiler.com/maps/openstreetmap/256/{z}/{x}/{y}.jpg?key=85AhB7OaKR8pWqppnXdS', {
            attribution: '&copy; <a href="https://www.maptiler.com/copyright/">MapTiler</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        }).addTo(map);
        
        L.control.zoom({ position: 'bottomright' }).addTo(map);

        let color = '#d97706';
        {% if report.status == 'resolved' %}color = '#166534';{% endif %}
        {% if report.status == 'in_progress' %}color = '#0ea5e9';{% endif %}
        
        const svgIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="32" height="32"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" fill="${color}" stroke="#ffffff" stroke-width="1.5"/></svg>`;
        
        const icon = L.divIcon({
            className: 'custom-leaflet-marker',
            html: svgIcon,
            iconSize: [32, 32],
            iconAnchor: [16, 32]
        });

        L.marker([lat, lng], { icon: icon }).addTo(map);
    }
})();
</script>
<style>
.custom-leaflet-marker {
    filter: drop-shadow(0 4px 3px rgb(0 0 0 / 0.2));
    transition: transform 0.2s;
}
.custom-leaflet-marker:hover {
    transform: scale(1.1) translateY(-4px) !important;
}
</style>
</div>
{% endif %}"""

if target in html:
    html = html.replace(target, replacement)
else:
    print("Target not found")

with codecs.open('d:/citywatch/reports/templates/reports/admin_report_detail.html', 'w', 'utf-8') as f:
    f.write(html)
