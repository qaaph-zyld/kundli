/**
 * Kundli Chart Visualization
 * Uses D3.js to create a visual representation of a Vedic astrology chart
 */

function createKundliChart(data, containerId) {
    // Clear previous chart
    d3.select(`#${containerId}`).html('');
    
    // Chart dimensions
    const width = 500;
    const height = 500;
    const margin = 20;
    const chartSize = Math.min(width, height) - 2 * margin;
    
    // Create SVG container
    const svg = d3.select(`#${containerId}`)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width/2}, ${height/2})`);
    
    // Chart parameters
    const outerRadius = chartSize / 2;
    const innerRadius = outerRadius * 0.4; // For the inner square
    
    // Draw outer circle
    svg.append('circle')
        .attr('r', outerRadius)
        .attr('fill', 'none')
        .attr('stroke', '#333')
        .attr('stroke-width', 1);
    
    // Draw inner square (rashi chart)
    const squareSize = innerRadius * Math.sqrt(2);
    const square = svg.append('rect')
        .attr('x', -squareSize/2)
        .attr('y', -squareSize/2)
        .attr('width', squareSize)
        .attr('height', squareSize)
        .attr('fill', 'none')
        .attr('stroke', '#333')
        .attr('stroke-width', 1);
    
    // Draw house divisions (12 houses)
    const houses = data.houses || [];
    const houseAngle = 360 / 12;
    
    for (let i = 0; i < 12; i++) {
        const angle = i * houseAngle;
        const radians = (angle - 90) * Math.PI / 180;
        const x2 = outerRadius * Math.cos(radians);
        const y2 = outerRadius * Math.sin(radians);
        
        // Draw house lines from center to outer circle
        svg.append('line')
            .attr('x1', 0)
            .attr('y1', 0)
            .attr('x2', x2)
            .attr('y2', y2)
            .attr('stroke', '#333')
            .attr('stroke-width', 1);
        
        // Add house numbers
        const textRadius = outerRadius * 0.9;
        const textX = textRadius * Math.cos(radians);
        const textY = textRadius * Math.sin(radians);
        
        svg.append('text')
            .attr('x', textX)
            .attr('y', textY)
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .attr('font-size', '12px')
            .text((i + 1).toString());
        
        // Add zodiac signs
        if (houses[i]) {
            const signRadius = outerRadius * 0.8;
            const signX = signRadius * Math.cos(radians);
            const signY = signRadius * Math.sin(radians);
            
            svg.append('text')
                .attr('x', signX)
                .attr('y', signY)
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline', 'middle')
                .attr('font-size', '14px')
                .attr('class', 'zodiac-symbol')
                .text(getZodiacSymbol(houses[i].sign));
        }
    }
    
    // Planet colors based on dignity
    const dignityColors = {
        'exalted': '#1a9850',      // Green
        'own': '#66bd63',          // Light green
        'friend': '#a6d96a',       // Yellow-green
        'neutral': '#ffffbf',      // Light yellow
        'enemy': '#fdae61',        // Orange
        'debilitated': '#d73027'   // Red
    };
    
    // Planet symbols
    const planetSymbols = {
        'Sun': '☉',
        'Moon': '☽',
        'Mercury': '☿',
        'Venus': '♀',
        'Mars': '♂',
        'Jupiter': '♃',
        'Saturn': '♄',
        'Rahu': '☊',
        'Ketu': '☋',
        'Uranus': '♅',
        'Neptune': '♆',
        'Pluto': '♇'
    };
    
    // Process planets data - handle both array and object formats
    let planetsArray = [];
    
    if (data.planets) {
        if (Array.isArray(data.planets)) {
            planetsArray = data.planets;
        } else if (typeof data.planets === 'object') {
            // Convert object to array
            planetsArray = Object.entries(data.planets).map(([name, planet]) => {
                return {
                    name: name,
                    ...planet
                };
            });
        }
    }
    
    // Place planets in their houses
    planetsArray.forEach((planet, index) => {
        if (!planet.house) return;
        
        const houseIndex = planet.house - 1;
        const baseAngle = houseIndex * houseAngle;
        
        // Calculate position within the house
        const offset = (index % 3) * (houseAngle / 4) + houseAngle / 8;
        const planetAngle = baseAngle + offset;
        const radians = (planetAngle - 90) * Math.PI / 180;
        
        const planetRadius = outerRadius * 0.65;
        const x = planetRadius * Math.cos(radians);
        const y = planetRadius * Math.sin(radians);
        
        // Determine color based on dignity
        const color = planet.dignity ? dignityColors[planet.dignity.toLowerCase()] : '#333';
        
        // Draw planet circle
        svg.append('circle')
            .attr('cx', x)
            .attr('cy', y)
            .attr('r', 12)
            .attr('fill', 'white')
            .attr('stroke', color)
            .attr('stroke-width', 2);
        
        // Add planet symbol
        svg.append('text')
            .attr('x', x)
            .attr('y', y)
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .attr('font-size', '14px')
            .attr('fill', color)
            .text(planetSymbols[planet.name] || planet.name.charAt(0));
        
        // Add retrograde indicator
        if (planet.isRetrograde) {
            svg.append('text')
                .attr('x', x)
                .attr('y', y + 18)
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline', 'middle')
                .attr('font-size', '10px')
                .attr('fill', '#d73027')
                .text('R');
        }
    });
    
    // Add ascendant marker
    if (data.ascendant) {
        const ascHouse = 1; // Ascendant is always in the 1st house in Whole Sign system
        const ascAngle = (ascHouse - 1) * houseAngle;
        const ascRadians = (ascAngle - 90) * Math.PI / 180;
        const ascRadius = outerRadius * 0.95;
        const ascX = ascRadius * Math.cos(ascRadians);
        const ascY = ascRadius * Math.sin(ascRadians);
        
        svg.append('text')
            .attr('x', ascX)
            .attr('y', ascY)
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .attr('font-size', '14px')
            .attr('fill', '#d73027')
            .attr('font-weight', 'bold')
            .text('Asc');
    }
}

// Helper function to get zodiac symbols
function getZodiacSymbol(sign) {
    const symbols = {
        'Aries': '♈',
        'Taurus': '♉',
        'Gemini': '♊',
        'Cancer': '♋',
        'Leo': '♌',
        'Virgo': '♍',
        'Libra': '♎',
        'Scorpio': '♏',
        'Sagittarius': '♐',
        'Capricorn': '♑',
        'Aquarius': '♒',
        'Pisces': '♓'
    };
    
    return symbols[sign] || '';
}

// Format degrees, minutes, seconds
function formatDMS(degrees) {
    const d = Math.floor(degrees);
    const mFloat = (degrees - d) * 60;
    const m = Math.floor(mFloat);
    const s = Math.round((mFloat - m) * 60);
    
    return `${d}° ${m}' ${s}"`;
}

// Convert longitude to zodiac sign and degrees
function longitudeToZodiac(longitude) {
    const signs = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 
        'Leo', 'Virgo', 'Libra', 'Scorpio', 
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ];
    
    const signIndex = Math.floor(longitude / 30) % 12;
    const degrees = longitude % 30;
    
    return {
        sign: signs[signIndex],
        degrees: degrees
    };
}
