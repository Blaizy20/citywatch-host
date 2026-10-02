import codecs

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'r', 'utf-8') as f:
    html = f.read()

target = '''    // Destroy existing charts to prevent SPA memory leaks / overlap
    if (window.trendChartInst) window.trendChartInst.destroy();
    if (window.statusChartInst) window.statusChartInst.destroy();
    if (window.categoryChartInst) window.categoryChartInst.destroy();
    if (window.barangayChartInst) window.barangayChartInst.destroy();

    Chart.defaults.font.family = "'DM Sans', sans-serif";
    Chart.defaults.color = '#43474e';

    // 0. Trend Line Chart
    const ctxTrend = document.getElementById('trendChart').getContext('2d');'''

replacement = '''    // Destroy existing charts to prevent SPA memory leaks / overlap
    if (window.trendChartInst) window.trendChartInst.destroy();
    if (window.statusChartInst) window.statusChartInst.destroy();
    if (window.categoryChartInst) window.categoryChartInst.destroy();
    if (window.barangayChartInst) window.barangayChartInst.destroy();

    // Helper to completely recreate the canvas. 
    // Idiomorph morphs DOM and can clash with Chart.js canvas mutations, causing freezes.
    function getFreshContext(id) {
        const oldCanvas = document.getElementById(id);
        if (!oldCanvas) return null;
        const newCanvas = document.createElement('canvas');
        newCanvas.id = id;
        oldCanvas.parentNode.replaceChild(newCanvas, oldCanvas);
        return newCanvas.getContext('2d');
    }

    Chart.defaults.font.family = "'DM Sans', sans-serif";
    Chart.defaults.color = '#43474e';

    // 0. Trend Line Chart
    const ctxTrend = getFreshContext('trendChart');'''

html = html.replace(target, replacement)

target2 = '''    // 1. Status Donut Chart
    const ctxStatus = document.getElementById('statusChart').getContext('2d');'''

replacement2 = '''    // 1. Status Donut Chart
    const ctxStatus = getFreshContext('statusChart');'''

html = html.replace(target2, replacement2)

target3 = '''    // 2. Category Pie Chart
    const ctxCategory = document.getElementById('categoryChart').getContext('2d');'''

replacement3 = '''    // 2. Category Pie Chart
    const ctxCategory = getFreshContext('categoryChart');'''

html = html.replace(target3, replacement3)

target4 = '''    // 3. Barangay Bar Chart
    const ctxBarangay = document.getElementById('barangayChart').getContext('2d');'''

replacement4 = '''    // 3. Barangay Bar Chart
    const ctxBarangay = getFreshContext('barangayChart');'''

html = html.replace(target4, replacement4)

with codecs.open('d:/citywatch/analytics/templates/analytics/reports_analytics.html', 'w', 'utf-8') as f:
    f.write(html)
