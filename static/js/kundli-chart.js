/**
 * Kundli Chart Visualization
 * Uses D3.js to create a visual representation of a Vedic astrology chart
 */

function createKundliChart(data, containerId, transitData = null) {
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
    
    // Create a tooltip div for displaying information
    const tooltip = d3.select('body').append('div')
        .attr('class', 'chart-tooltip')
        .style('opacity', 0)
        .style('position', 'absolute')
        .style('background-color', 'white')
        .style('border', '1px solid #ddd')
        .style('border-radius', '4px')
        .style('padding', '8px')
        .style('box-shadow', '0 2px 4px rgba(0,0,0,0.1)')
        .style('pointer-events', 'none')
        .style('max-width', '250px')
        .style('z-index', 1000);
    
    // Create a details panel for showing more information
    const detailsPanel = d3.select(`#${containerId}`)
        .append('div')
        .attr('class', 'chart-details-panel')
        .style('display', 'none');
    
    // Add a close button to the details panel
    detailsPanel.append('button')
        .attr('class', 'btn-close')
        .attr('type', 'button')
        .attr('aria-label', 'Close')
        .style('position', 'absolute')
        .style('top', '5px')
        .style('right', '5px')
        .on('click', function() {
            detailsPanel.style('display', 'none');
        });
    
    // Add a content div to the details panel
    const detailsContent = detailsPanel.append('div')
        .attr('class', 'details-content');
    
    // Function to show house details
    function showHouseDetails(house, i) {
        const houseNumber = i + 1;
        const signName = house.sign;
        
        let content = `<div class="tooltip-content">
            <h5>House ${houseNumber}</h5>
            <p><strong>Sign:</strong> ${signName}</p>`;
        
        // Add house significations
        const houseSignifications = getHouseSignifications(houseNumber);
        content += `<p><strong>Signifies:</strong> ${houseSignifications}</p>`;
        
        // List planets in this house
        const planetsInHouse = planetsArray.filter(p => p.house === houseNumber);
        if (planetsInHouse.length > 0) {
            content += `<p><strong>Planets:</strong> ${planetsInHouse.map(p => p.name).join(', ')}</p>`;
        }
        
        content += `</div>`;
        
        tooltip.html(content)
            .style('opacity', 1)
            .style('left', (d3.event.pageX + 10) + 'px')
            .style('top', (d3.event.pageY - 10) + 'px');
    }
    
    // Function to hide tooltip
    function hideTooltip() {
        tooltip.style('opacity', 0);
    }
    
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
            
            // Create clickable house areas
            const houseArea = svg.append('path')
                .attr('d', d3.arc()
                    .innerRadius(innerRadius)
                    .outerRadius(outerRadius)
                    .startAngle(radians - Math.PI/12)
                    .endAngle(radians + Math.PI/12))
                .attr('fill', 'transparent')
                .attr('stroke', 'none')
                .attr('class', 'house-area')
                .style('cursor', 'pointer');
                
            // Add interactivity to house areas
            houseArea.on('mouseover', function() {
                d3.select(this).attr('fill', 'rgba(200, 200, 200, 0.2)');
                if (houses[i]) {
                    showHouseDetails(houses[i], i);
                }
            })
            .on('mouseout', function() {
                d3.select(this).attr('fill', 'transparent');
                hideTooltip();
            })
            .on('click', function() {
                // Show detailed house information in a modal or panel
                if (houses[i]) {
                    showHouseDetailsPanel(houses[i], i + 1);
                }
            });
            
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
        } else {
            // Convert object to array
            for (const [name, details] of Object.entries(data.planets)) {
                planetsArray.push({
                    name: name,
                    ...details
                });
            }
        }
    }
    
    // Function to calculate planet position in the chart
    function calculatePlanetPosition(planet, isTransit = false) {
        // Calculate position based on longitude
        const longitude = planet.longitude;
        const angle = longitude * (360 / 360); // Convert to degrees
        const radians = (angle - 90) * Math.PI / 180;
        
        // Different radius for natal vs transit planets
        let planetRadius;
        if (isTransit) {
            planetRadius = outerRadius * 0.65; // Transit planets closer to outer edge
        } else {
            planetRadius = outerRadius * 0.55; // Natal planets closer to center
        }
        
        const x = planetRadius * Math.cos(radians);
        const y = planetRadius * Math.sin(radians);
        
        return { x, y };
    }
    
    // Draw planets
    planetsArray.forEach((planet, index) => {
        const { x, y } = calculatePlanetPosition(planet);
        
        // Determine color based on dignity
        let color = '#333'; // Default color
        if (planet.dignity && dignityColors[planet.dignity.toLowerCase()]) {
            color = dignityColors[planet.dignity.toLowerCase()];
        }
        
        // Create planet circle
        const planetCircle = svg.append('circle')
            .attr('cx', x)
            .attr('cy', y)
            .attr('r', 12)
            .attr('fill', color)
            .attr('stroke', '#fff')
            .attr('stroke-width', 1)
            .attr('class', 'planet')
            .style('cursor', 'pointer');
        
        // Add planet symbol
        const symbol = planetSymbols[planet.name] || planet.name.charAt(0);
        svg.append('text')
            .attr('x', x)
            .attr('y', y)
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .attr('font-size', '12px')
            .attr('fill', 'white')
            .attr('pointer-events', 'none')
            .text(symbol);
        
        // Add retrograde indicator if applicable
        if (planet.retrograde) {
            svg.append('text')
                .attr('x', x + 14)
                .attr('y', y - 14)
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline', 'middle')
                .attr('font-size', '12px')
                .attr('fill', '#d63031')
                .attr('pointer-events', 'none')
                .text('℞');
        }
        
        // Add interactivity
        planetCircle.on('mouseover', function() {
            d3.select(this).attr('r', 14);
            
            // Show tooltip with planet information
            let content = `<div class="tooltip-content">
                <h5>${planet.name}</h5>
                <p><strong>Sign:</strong> ${planet.sign}</p>
                <p><strong>House:</strong> ${planet.house}</p>
                <p><strong>Position:</strong> ${formatDMS(planet.longitude % 30)}°</p>`;
            
            if (planet.retrograde) {
                content += `<p><strong>Motion:</strong> <span class="retrograde">Retrograde</span></p>`;
            }
            
            if (planet.dignity) {
                content += `<p><strong>Dignity:</strong> ${planet.dignity}</p>`;
            }
            
            content += `</div>`;
            
            tooltip.html(content)
                .style('opacity', 1)
                .style('left', (d3.event.pageX + 10) + 'px')
                .style('top', (d3.event.pageY - 10) + 'px');
        })
        .on('mouseout', function() {
            d3.select(this).attr('r', 12);
            hideTooltip();
        })
        .on('click', function() {
            showPlanetDetailsPanel(planet);
        });
    });
    
    // Draw transit planets if transit data is provided
    if (transitData && transitData.transits) {
        // Process transit planets data
        let transitPlanetsArray = [];
        
        for (const [name, details] of Object.entries(transitData.transits)) {
            transitPlanetsArray.push({
                name: name,
                ...details
            });
        }
        
        // Draw transit planets
        transitPlanetsArray.forEach((planet, index) => {
            const { x, y } = calculatePlanetPosition(planet, true);
            
            // Create transit planet circle (with dashed stroke to distinguish from natal planets)
            const transitPlanetCircle = svg.append('circle')
                .attr('cx', x)
                .attr('cy', y)
                .attr('r', 10)
                .attr('fill', 'white')
                .attr('stroke', '#333')
                .attr('stroke-width', 2)
                .attr('stroke-dasharray', '3,2')
                .attr('class', 'transit-planet')
                .style('cursor', 'pointer');
            
            // Add planet symbol
            const symbol = planetSymbols[planet.name] || planet.name.charAt(0);
            svg.append('text')
                .attr('x', x)
                .attr('y', y)
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline', 'middle')
                .attr('font-size', '10px')
                .attr('fill', '#333')
                .attr('pointer-events', 'none')
                .text(symbol);
            
            // Add retrograde indicator if applicable
            if (planet.retrograde) {
                svg.append('text')
                    .attr('x', x + 12)
                    .attr('y', y - 12)
                    .attr('text-anchor', 'middle')
                    .attr('dominant-baseline', 'middle')
                    .attr('font-size', '10px')
                    .attr('fill', '#d63031')
                    .attr('pointer-events', 'none')
                    .text('℞');
            }
            
            // Add interactivity
            transitPlanetCircle.on('mouseover', function() {
                d3.select(this).attr('r', 12);
                
                // Show tooltip with transit planet information
                let content = `<div class="tooltip-content">
                    <h5>${planet.name} (Transit)</h5>
                    <p><strong>Sign:</strong> ${planet.sign}</p>
                    <p><strong>House:</strong> ${planet.house}</p>
                    <p><strong>Position:</strong> ${formatDMS(planet.longitude % 30)}°</p>`;
                
                if (planet.retrograde) {
                    content += `<p><strong>Motion:</strong> <span class="retrograde">Retrograde</span></p>`;
                }
                
                content += `</div>`;
                
                tooltip.html(content)
                    .style('opacity', 1)
                    .style('left', (d3.event.pageX + 10) + 'px')
                    .style('top', (d3.event.pageY - 10) + 'px');
            })
            .on('mouseout', function() {
                d3.select(this).attr('r', 10);
                hideTooltip();
            })
            .on('click', function() {
                showTransitPlanetDetailsPanel(planet);
            });
        });
        
        // Add a legend for the chart
        const legendY = height / 2 - 20;
        
        // Natal planet legend
        svg.append('circle')
            .attr('cx', -width/2 + 20)
            .attr('cy', legendY)
            .attr('r', 6)
            .attr('fill', '#333')
            .attr('stroke', '#fff')
            .attr('stroke-width', 1);
            
        svg.append('text')
            .attr('x', -width/2 + 35)
            .attr('y', legendY)
            .attr('dominant-baseline', 'middle')
            .attr('font-size', '12px')
            .text('Natal Planets');
            
        // Transit planet legend
        svg.append('circle')
            .attr('cx', -width/2 + 20)
            .attr('cy', legendY + 20)
            .attr('r', 6)
            .attr('fill', 'white')
            .attr('stroke', '#333')
            .attr('stroke-width', 2)
            .attr('stroke-dasharray', '3,2');
            
        svg.append('text')
            .attr('x', -width/2 + 35)
            .attr('y', legendY + 20)
            .attr('dominant-baseline', 'middle')
            .attr('font-size', '12px')
            .text('Transit Planets');
    }
}

// Function to show detailed planet information in a panel
function showPlanetDetailsPanel(planet) {
    // Get or create the details panel
    let detailsPanel = document.getElementById('chart-details-panel');
    if (!detailsPanel) {
        detailsPanel = document.createElement('div');
        detailsPanel.id = 'chart-details-panel';
        detailsPanel.className = 'chart-details-panel';
        document.getElementById('chart').appendChild(detailsPanel);
        
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.className = 'btn-close';
        closeBtn.setAttribute('aria-label', 'Close');
        closeBtn.onclick = function() {
            detailsPanel.style.display = 'none';
        };
        detailsPanel.appendChild(closeBtn);
    }
    
    // Create content container
    const contentDiv = document.createElement('div');
    contentDiv.className = 'details-content';
    
    // Create header
    const header = document.createElement('h4');
    header.textContent = planet.name;
    contentDiv.appendChild(header);
    
    // Create table for planet details
    const table = document.createElement('table');
    table.className = 'table table-sm';
    
    // Add rows for each property
    const properties = [
        { label: 'Sign', value: planet.sign },
        { label: 'House', value: planet.house },
        { label: 'Degree', value: formatDMS(planet.degree_precise || planet.degree) },
        { label: 'Dignity', value: planet.dignity },
        { label: 'Motion', value: planet.isRetrograde ? 'Retrograde' : 'Direct' },
        { label: 'Nakshatra', value: planet.nakshatra },
        { label: 'Nakshatra Lord', value: planet.nakshatra_lord }
    ];
    
    // Add relationships if available
    if (planet.relationships) {
        const relationshipStr = Object.entries(planet.relationships)
            .map(([planet, relation]) => `${planet}: ${relation}`)
            .join(', ');
        properties.push({ label: 'Relationships', value: relationshipStr });
    }
    
    // Create table body
    const tbody = document.createElement('tbody');
    properties.forEach(prop => {
        if (prop.value) {
            const row = document.createElement('tr');
            
            const labelCell = document.createElement('td');
            labelCell.className = 'fw-bold';
            labelCell.textContent = prop.label;
            row.appendChild(labelCell);
            
            const valueCell = document.createElement('td');
            valueCell.textContent = prop.value;
            
            // Apply color to dignity
            if (prop.label === 'Dignity') {
                const dignityColors = {
                    'exalted': '#1a9850',
                    'own': '#66bd63',
                    'friend': '#a6d96a',
                    'neutral': '#ffffbf',
                    'enemy': '#fdae61',
                    'debilitated': '#d73027'
                };
                valueCell.style.color = dignityColors[prop.value.toLowerCase()] || 'inherit';
            }
            
            row.appendChild(valueCell);
            tbody.appendChild(row);
        }
    });
    
    table.appendChild(tbody);
    contentDiv.appendChild(table);
    
    // Clear previous content and add new content
    detailsPanel.innerHTML = '';
    detailsPanel.appendChild(contentDiv);
    
    // Add close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'btn-close position-absolute top-0 end-0 m-2';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.onclick = function() {
        detailsPanel.style.display = 'none';
    };
    detailsPanel.appendChild(closeBtn);
    
    // Show the panel
    detailsPanel.style.display = 'block';
}

// Function to show detailed transit planet information in a panel
function showTransitPlanetDetailsPanel(planet) {
    // Get or create the details panel
    let detailsPanel = document.getElementById('chart-details-panel');
    if (!detailsPanel) {
        detailsPanel = document.createElement('div');
        detailsPanel.id = 'chart-details-panel';
        detailsPanel.className = 'chart-details-panel';
        document.getElementById('chart').appendChild(detailsPanel);
        
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.className = 'btn-close';
        closeBtn.setAttribute('aria-label', 'Close');
        closeBtn.onclick = function() {
            detailsPanel.style.display = 'none';
        };
        detailsPanel.appendChild(closeBtn);
    }
    
    // Create content container
    const contentDiv = document.createElement('div');
    contentDiv.className = 'details-content';
    
    // Create header
    const header = document.createElement('h4');
    header.textContent = planet.name + ' (Transit)';
    contentDiv.appendChild(header);
    
    // Create table for planet details
    const table = document.createElement('table');
    table.className = 'table table-sm';
    
    // Add rows for each property
    const properties = [
        { label: 'Sign', value: planet.sign },
        { label: 'House', value: planet.house },
        { label: 'Degree', value: formatDMS(planet.longitude % 30) },
        { label: 'Motion', value: planet.retrograde ? 'Retrograde' : 'Direct' }
    ];
    
    // Create table body
    const tbody = document.createElement('tbody');
    properties.forEach(prop => {
        if (prop.value) {
            const row = document.createElement('tr');
            
            const labelCell = document.createElement('td');
            labelCell.className = 'fw-bold';
            labelCell.textContent = prop.label;
            row.appendChild(labelCell);
            
            const valueCell = document.createElement('td');
            valueCell.textContent = prop.value;
            
            row.appendChild(valueCell);
            tbody.appendChild(row);
        }
    });
    
    table.appendChild(tbody);
    contentDiv.appendChild(table);
    
    // Clear previous content and add new content
    detailsPanel.innerHTML = '';
    detailsPanel.appendChild(contentDiv);
    
    // Add close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'btn-close position-absolute top-0 end-0 m-2';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.onclick = function() {
        detailsPanel.style.display = 'none';
    };
    detailsPanel.appendChild(closeBtn);
    
    // Show the panel
    detailsPanel.style.display = 'block';
}

// Function to show detailed house information in a panel
function showHouseDetailsPanel(house, houseNumber) {
    // Get or create the details panel
    let detailsPanel = document.getElementById('chart-details-panel');
    if (!detailsPanel) {
        detailsPanel = document.createElement('div');
        detailsPanel.id = 'chart-details-panel';
        detailsPanel.className = 'chart-details-panel';
        document.getElementById('chart').appendChild(detailsPanel);
    }
    
    // Create content container
    const contentDiv = document.createElement('div');
    contentDiv.className = 'details-content';
    
    // Create header
    const header = document.createElement('h4');
    header.textContent = `House ${houseNumber}`;
    contentDiv.appendChild(header);
    
    // Create table for house details
    const table = document.createElement('table');
    table.className = 'table table-sm';
    
    // Add rows for each property
    const tbody = document.createElement('tbody');
    
    // Sign information
    const signRow = document.createElement('tr');
    const signLabelCell = document.createElement('td');
    signLabelCell.className = 'fw-bold';
    signLabelCell.textContent = 'Sign';
    signRow.appendChild(signLabelCell);
    
    const signValueCell = document.createElement('td');
    signValueCell.textContent = house.sign;
    signRow.appendChild(signValueCell);
    tbody.appendChild(signRow);
    
    // House significations
    const signifRow = document.createElement('tr');
    const signifLabelCell = document.createElement('td');
    signifLabelCell.className = 'fw-bold';
    signifLabelCell.textContent = 'Significations';
    signifRow.appendChild(signifLabelCell);
    
    const signifValueCell = document.createElement('td');
    signifValueCell.textContent = getHouseSignifications(houseNumber);
    signifRow.appendChild(signifValueCell);
    tbody.appendChild(signifRow);
    
    table.appendChild(tbody);
    contentDiv.appendChild(table);
    
    // Clear previous content and add new content
    detailsPanel.innerHTML = '';
    detailsPanel.appendChild(contentDiv);
    
    // Add close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'btn-close position-absolute top-0 end-0 m-2';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.onclick = function() {
        detailsPanel.style.display = 'none';
    };
    detailsPanel.appendChild(closeBtn);
    
    // Show the panel
    detailsPanel.style.display = 'block';
}

// Function to get house significations
function getHouseSignifications(houseNumber) {
    const significations = {
        1: 'Self, personality, physical body, appearance, beginnings',
        2: 'Wealth, family, speech, resources, values',
        3: 'Siblings, courage, communication, short journeys',
        4: 'Home, mother, property, emotions, domestic happiness',
        5: 'Children, creativity, romance, intelligence, education',
        6: 'Enemies, obstacles, diseases, debts, service',
        7: 'Marriage, partnerships, business relationships, contracts',
        8: 'Death, transformation, occult, inheritance, joint resources',
        9: 'Higher learning, philosophy, religion, long journeys',
        10: 'Career, status, authority, father, government',
        11: 'Gains, income, friends, hopes, wishes',
        12: 'Losses, expenses, isolation, spirituality, foreign lands'
    };
    
    return significations[houseNumber] || '';
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
    
    return symbols[sign] || sign.charAt(0);
}

// Format degrees, minutes, seconds
function formatDMS(degrees) {
    if (typeof degrees !== 'number') return degrees;
    
    const d = Math.floor(degrees);
    const mFull = (degrees - d) * 60;
    const m = Math.floor(mFull);
    const s = Math.floor((mFull - m) * 60);
    
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
    const degree = longitude % 30;
    
    return {
        sign: signs[signIndex],
        degree: degree
    };
}
