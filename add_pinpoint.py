import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/map_view.html', 'r', 'utf-8') as f:
    html = f.read()

target_row = '<tr class="hover:bg-surface-container-low transition-colors group">'
replacement_row = '<tr class="hover:bg-surface-container-low transition-colors group cursor-pointer" onclick="focusMapOn({{ report.latitude|default_if_none:\'null\' }}, {{ report.longitude|default_if_none:\'null\' }}, {{ report.id }})">'
html = html.replace(target_row, replacement_row)

target_js = '''    // Plot pins
    const bounds = L.latLngBounds();
    mapData.forEach(item => {
        const marker = L.marker([item.lat, item.lng], { icon: getIcon(item.statusKey) }).addTo(map);
        bounds.extend([item.lat, item.lng]);'''
        
replacement_js = '''    // Plot pins
    const bounds = L.latLngBounds();
    window.reportsMarkers = {}; // Store markers to open popups
    mapData.forEach(item => {
        const marker = L.marker([item.lat, item.lng], { icon: getIcon(item.statusKey) }).addTo(map);
        window.reportsMarkers[item.id] = marker;
        bounds.extend([item.lat, item.lng]);'''

html = html.replace(target_js, replacement_js)

target_js2 = '''    if (mapData.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50], maxZoom: 16 });
    }
})();'''

replacement_js2 = '''    if (mapData.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50], maxZoom: 16 });
    }
    
    // Global function to focus map
    window.focusMapOn = function(lat, lng, id) {
        if (!lat || !lng) return;
        map.flyTo([lat, lng], 18, {
            duration: 1.5,
            easeLinearity: 0.25
        });
        if (window.reportsMarkers && window.reportsMarkers[id]) {
            setTimeout(() => {
                window.reportsMarkers[id].openPopup();
            }, 1500); // Open popup after flyTo animation
        }
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };
})();'''

html = html.replace(target_js2, replacement_js2)

with codecs.open('d:/citywatch/analytics/templates/analytics/map_view.html', 'w', 'utf-8') as f:
    f.write(html)
