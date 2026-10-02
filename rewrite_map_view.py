import codecs

html = '''{% extends 'analytics/admin_base.html' %}
{% load static %}
{% block content %}

<div class="mx-auto max-w-7xl px-4 py-2 sm:px-6 lg:px-8 w-full">

  <!-- Header Area -->
  <div class="mb-8 flex flex-wrap items-end justify-between gap-3">
    <div>
      <h1 class="text-3xl font-bold font-display text-on-surface tracking-tight flex items-center gap-2">
        <span class="material-symbols-outlined text-primary text-[32px]">public</span>
        Geospatial Analysis
      </h1>
      <p class="mt-1 max-w-2xl text-sm text-on-surface-variant font-medium">Interactive live map of reported incidents across local barangays.</p>
    </div>
    <div class="flex items-center gap-4">
      <a href="{% url 'analytics_dashboard' %}" data-no-spa="true" onclick="if(window.history.length > 1) { event.preventDefault(); this.querySelector('span').classList.add('-translate-x-4', 'opacity-0'); setTimeout(() => window.history.back(), 150); }" class="inline-flex items-center gap-1.5 text-sm font-bold text-on-surface-variant hover:text-primary transition-colors group p-2 hover:bg-surface-container-low rounded-full"><span class="material-symbols-outlined text-[20px] transition-all duration-300 group-hover:-translate-x-1 group-active:scale-75">arrow_back</span> Dashboard</a>
    </div>
  </div>

  <!-- Interactive Map Container -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-2 sm:p-4 shadow-sm mb-8">
    <div id="reportsMap" class="w-full h-[500px] sm:h-[650px] rounded-xl z-10 border border-outline-variant/50"></div>
  </div>

  <!-- Hotspots Reference Table -->
  <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm overflow-hidden">
    <div class="p-6 border-b border-outline-variant bg-surface-container-low/50">
      <h3 class="font-bold text-lg text-on-surface">Coordinate Reference</h3>
      <p class="text-xs font-medium text-on-surface-variant">Raw geospatial data for mapped incidents.</p>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-surface">
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Title</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Barangay</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Coordinates</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant">Status</th>
            <th class="p-4 text-[11px] font-bold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant text-right">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-outline-variant">
          {% for report in reports %}
          <tr class="hover:bg-surface-container-low transition-colors group">
            <td class="p-4 text-sm font-bold text-on-surface group-hover:text-primary transition-colors">{{ report.title }}</td>
            <td class="p-4 text-sm font-medium text-on-surface-variant"><span class="bg-surface-container px-2 py-1 rounded-md">{{ report.barangay }}</span></td>
            <td class="p-4 text-sm text-on-surface-variant font-mono text-xs">{{ report.latitude|floatformat:4 }}, {{ report.longitude|floatformat:4 }}</td>
            <td class="p-4 text-sm font-semibold">
              <span class="inline-flex items-center gap-1.5 {% if report.status == 'resolved' %}text-[#166534]{% elif report.status == 'in_progress' %}text-[#0ea5e9]{% else %}text-[#d97706]{% endif %}">
                <span class="w-1.5 h-1.5 rounded-full {% if report.status == 'resolved' %}bg-[#166534]{% elif report.status == 'in_progress' %}bg-[#0ea5e9]{% else %}bg-[#d97706]{% endif %}"></span>
                {{ report.get_status_display }}
              </span>
            </td>
            <td class="p-4 text-right">
              <a href="{% url 'admin_report_detail' report.id %}" class="inline-flex items-center justify-center text-primary bg-primary-container/50 hover:bg-primary-container px-3 py-1.5 rounded-lg text-xs font-bold tracking-wide transition-colors">Details</a>
            </td>
          </tr>
          {% empty %}
          <tr><td colspan="5" class="p-8 text-center text-on-surface-variant font-medium bg-surface-container-lowest">No geotagged reports yet. Reports need a location pin to appear here.</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

</div>

<script>
(function() {
    // If idiomorph re-evaluates, destroy old map instance to prevent "Map container is already initialized" error
    if (window.reportsMapInst) {
        window.reportsMapInst.remove();
        window.reportsMapInst = null;
    }

    // Default center (Baliuag, Bulacan coordinates roughly)
    const defaultCenter = [14.9540, 120.9000];
    
    // Extract map data from Django context
    const mapData = [
      {% for report in reports %}
      {
        id: {{ report.id }},
        lat: {{ report.latitude|default:"null" }},
        lng: {{ report.longitude|default:"null" }},
        title: '{{ report.title|escapejs }}',
        barangay: '{{ report.barangay|escapejs }}',
        status: '{{ report.get_status_display|escapejs }}',
        statusKey: '{{ report.status }}',
        url: '{% url "admin_report_detail" report.id %}'
      },
      {% endfor %}
    ].filter(d => d.lat !== null && d.lng !== null);

    // Initialize Map
    const map = L.map('reportsMap', {
        zoomControl: false // We'll add it in a better position
    }).setView(mapData.length > 0 ? [mapData[0].lat, mapData[0].lng] : defaultCenter, 13);
    
    window.reportsMapInst = map;

    // Premium CartoDB Positron tiles for a sleek, modern admin look
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Add zoom control to bottom right
    L.control.zoom({ position: 'bottomright' }).addTo(map);

    // Custom Icons based on status
    const getIcon = (statusKey) => {
        let color = '#d97706'; // pending orange
        if (statusKey === 'resolved') color = '#166534'; // green
        if (statusKey === 'in_progress') color = '#0ea5e9'; // blue
        
        // Use a simple SVG marker for ultimate crispness
        const svgIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="32" height="32"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" fill="${color}" stroke="#ffffff" stroke-width="1.5"/></svg>`;
        
        return L.divIcon({
            className: 'custom-leaflet-marker',
            html: svgIcon,
            iconSize: [32, 32],
            iconAnchor: [16, 32],
            popupAnchor: [0, -32]
        });
    };

    // Plot pins
    const bounds = L.latLngBounds();
    mapData.forEach(item => {
        const marker = L.marker([item.lat, item.lng], { icon: getIcon(item.statusKey) }).addTo(map);
        bounds.extend([item.lat, item.lng]);
        
        // Beautiful popup
        const popupContent = `
            <div style="font-family: 'DM Sans', sans-serif; padding: 4px;">
                <p style="margin: 0 0 4px 0; font-size: 10px; font-weight: bold; text-transform: uppercase; color: #74777f;">${item.barangay}</p>
                <h4 style="margin: 0 0 8px 0; font-size: 14px; font-weight: bold; color: #1a1c1e;">${item.title}</h4>
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px;">
                    <span style="font-size: 12px; font-weight: 600;">${item.status}</span>
                    <a href="${item.url}" style="font-size: 12px; font-weight: bold; color: #156b3e; text-decoration: none; background: #a0f3be; padding: 4px 10px; border-radius: 6px;">View</a>
                </div>
            </div>
        `;
        marker.bindPopup(popupContent, { className: 'premium-popup' });
    });

    // Auto fit bounds if we have pins
    if (mapData.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50], maxZoom: 16 });
    }
})();
</script>

<style>
/* Style the Leaflet popup to match our UI */
.premium-popup .leaflet-popup-content-wrapper {
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    border: 1px solid #e5e7eb;
}
.premium-popup .leaflet-popup-tip {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-top: none;
    border-left: none;
}
.custom-leaflet-marker {
    filter: drop-shadow(0 4px 3px rgb(0 0 0 / 0.2));
    transition: transform 0.2s;
}
.custom-leaflet-marker:hover {
    transform: scale(1.1) translateY(-4px) !important;
}
</style>

{% endblock %}
'''

with codecs.open('d:/citywatch/analytics/templates/analytics/map_view.html', 'w', 'utf-8') as f:
    f.write(html)
