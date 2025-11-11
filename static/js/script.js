// Input field templates
const inputTemplates = {
    url: `
        <div class="form-group">
            <label for="url"><i class="fas fa-link"></i> Website URL</label>
            <input type="text" id="url" name="url" placeholder="https://example.com" required>
        </div>
    `,
    text: `
        <div class="form-group">
            <label for="text"><i class="fas fa-file-alt"></i> Your Text</label>
            <textarea id="text" name="text" placeholder="Enter your text here..." required></textarea>
        </div>
    `,
    email: `
        <div class="form-group">
            <label for="email"><i class="fas fa-envelope"></i> Email Address</label>
            <input type="email" id="email" name="email" placeholder="example@email.com" required>
        </div>
        <div class="form-group">
            <label for="subject">Subject (Optional)</label>
            <input type="text" id="subject" name="subject" placeholder="Email subject">
        </div>
        <div class="form-group">
            <label for="message">Message (Optional)</label>
            <textarea id="message" name="message" placeholder="Email message"></textarea>
        </div>
    `,
    phone: `
        <div class="form-group">
            <label for="phone"><i class="fas fa-phone"></i> Phone Number</label>
            <input type="tel" id="phone" name="phone" placeholder="+1 (234) 567-8900" required>
        </div>
    `,
    location: `
        <div class="location-buttons">
            <button type="button" class="location-btn" id="currentLocationBtn">
                <i class="fas fa-crosshairs"></i>
                <span>Current Location</span>
            </button>
            <button type="button" class="location-btn active" id="customLocationBtn">
                <i class="fas fa-map-marked-alt"></i>
                <span>Custom Location</span>
            </button>
        </div>
        <div id="locationInputs">
            <div class="form-group">
                <label for="lat">Latitude</label>
                <input type="text" id="lat" name="lat" placeholder="40.7128" required>
            </div>
            <div class="form-group">
                <label for="lng">Longitude</label>
                <input type="text" id="lng" name="lng" placeholder="-74.0060" required>
            </div>
            <div class="form-group">
                <label>Map Type</label>
                <div class="location-type-selector">
                    <label class="location-type-option">
                        <input type="radio" name="locationType" value="geo" checked>
                        <span><i class="fas fa-map-marker-alt"></i> Generic</span>
                    </label>
                    <label class="location-type-option">
                        <input type="radio" name="locationType" value="google">
                        <span><i class="fab fa-google"></i> Google Maps</span>
                    </label>
                    <label class="location-type-option">
                        <input type="radio" name="locationType" value="apple">
                        <span><i class="fab fa-apple"></i> Apple Maps</span>
                    </label>
                    <label class="location-type-option">
                        <input type="radio" name="locationType" value="waze">
                        <span><i class="fab fa-waze"></i> Waze</span>
                    </label>
                </div>
            </div>
        </div>
    `,
    wifi: `
        <div class="form-group">
            <label for="ssid"><i class="fas fa-wifi"></i> Network Name (SSID)</label>
            <input type="text" id="ssid" name="ssid" placeholder="MyWiFi" required>
        </div>
        <div class="form-group">
            <label for="password"><i class="fas fa-lock"></i> Password</label>
            <input type="text" id="password" name="password" placeholder="WiFi password">
        </div>
        <div class="form-group">
            <label>Security Type</label>
            <div class="radio-group">
                <label class="radio-option">
                    <input type="radio" name="security" value="WPA" checked>
                    <span>WPA</span>
                </label>
                <label class="radio-option">
                    <input type="radio" name="security" value="WEP">
                    <span>WEP</span>
                </label>
                <label class="radio-option">
                    <input type="radio" name="security" value="nopass">
                    <span>None</span>
                </label>
            </div>
        </div>
    `
};

let currentQRImage = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    const inputFields = document.getElementById('inputFields');
    const qrTypeRadios = document.querySelectorAll('input[name="qrType"]');
    const generateBtn = document.getElementById('generateBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const boxSizeInput = document.getElementById('boxSize');
    const sizeValue = document.getElementById('sizeValue');
    const fgColorInput = document.getElementById('fgColor');
    const bgColorInput = document.getElementById('bgColor');
    const gradientColorInput = document.getElementById('gradientColor');
    const gradientRadios = document.querySelectorAll('input[name="gradientType"]');
    
    // Update input fields based on QR type
    function updateInputFields() {
        const selectedType = document.querySelector('input[name="qrType"]:checked').value;
        inputFields.innerHTML = inputTemplates[selectedType];
        
        if (selectedType === 'location') {
            setupLocationButtons();
        }
    }
    
    // Setup location buttons
    function setupLocationButtons() {
        const currentLocationBtn = document.getElementById('currentLocationBtn');
        const customLocationBtn = document.getElementById('customLocationBtn');
        
        currentLocationBtn.addEventListener('click', function() {
            currentLocationBtn.classList.add('active');
            customLocationBtn.classList.remove('active');
            
            if (navigator.geolocation) {
                generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Getting location...</span>';
                generateBtn.disabled = true;
                
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const lat = position.coords.latitude.toFixed(6);
                        const lng = position.coords.longitude.toFixed(6);
                        
                        document.getElementById('lat').value = lat;
                        document.getElementById('lng').value = lng;
                        
                        generateBtn.innerHTML = '<span class="btn-icon">✨</span><span>Generate QR Code</span>';
                        generateBtn.disabled = false;
                        
                        showNotification('✅ Location detected successfully!', 'success');
                    },
                    function(error) {
                        generateBtn.innerHTML = '<span class="btn-icon">✨</span><span>Generate QR Code</span>';
                        generateBtn.disabled = false;
                        showNotification('❌ Could not get location. Please enter manually.', 'error');
                        
                        currentLocationBtn.classList.remove('active');
                        customLocationBtn.classList.add('active');
                    }
                );
            } else {
                showNotification('❌ Geolocation is not supported by your browser.', 'error');
                currentLocationBtn.classList.remove('active');
                customLocationBtn.classList.add('active');
            }
        });
        
        customLocationBtn.addEventListener('click', function() {
            customLocationBtn.classList.add('active');
            currentLocationBtn.classList.remove('active');
        });
    }
    
    // Show/hide gradient color picker
    gradientRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const gradientSection = document.getElementById('gradientColorSection');
            if (this.value !== 'none') {
                gradientSection.style.display = 'block';
            } else {
                gradientSection.style.display = 'none';
            }
        });
    });
    
    // Initial load
    updateInputFields();
    
    // Listen for type changes
    qrTypeRadios.forEach(radio => {
        radio.addEventListener('change', updateInputFields);
    });
    
    // Update size value display
    boxSizeInput.addEventListener('input', function() {
        sizeValue.textContent = this.value;
    });
    
    // Update color hex displays
    fgColorInput.addEventListener('input', function() {
        this.nextElementSibling.textContent = this.value.toUpperCase();
    });
    
    bgColorInput.addEventListener('input', function() {
        this.nextElementSibling.textContent = this.value.toUpperCase();
    });
    
    gradientColorInput.addEventListener('input', function() {
        this.nextElementSibling.textContent = this.value.toUpperCase();
    });
    
    // Generate QR Code
    generateBtn.addEventListener('click', async function() {
        await generateQRCode();
    });
    
    // Download QR Code
    downloadBtn.addEventListener('click', function() {
        if (currentQRImage) {
            const link = document.createElement('a');
            link.href = currentQRImage;
            link.download = `qrcode-${Date.now()}.png`;
            link.click();
            showNotification('💾 QR Code downloaded!', 'success');
        }
    });
    
    // Copy to clipboard
    document.getElementById('copyBtn').addEventListener('click', async function() {
        if (currentQRImage) {
            try {
                const blob = await (await fetch(currentQRImage)).blob();
                await navigator.clipboard.write([
                    new ClipboardItem({ 'image/png': blob })
                ]);
                showNotification('📋 QR Code copied to clipboard!', 'success');
            } catch (err) {
                showNotification('❌ Failed to copy to clipboard', 'error');
            }
        }
    });
    
    // Share QR Code
    document.getElementById('shareBtn').addEventListener('click', async function() {
        if (currentQRImage && navigator.share) {
            try {
                const blob = await (await fetch(currentQRImage)).blob();
                const file = new File([blob], 'qrcode.png', { type: 'image/png' });
                await navigator.share({
                    files: [file],
                    title: 'QR Code',
                    text: 'Check out this QR code!'
                });
            } catch (err) {
                showNotification('❌ Sharing failed', 'error');
            }
        } else {
            showNotification('❌ Sharing not supported on this device', 'error');
        }
    });
    
    // History button
    document.getElementById('historyBtn').addEventListener('click', async function() {
        const modal = document.getElementById('historyModal');
        modal.classList.add('show');
        
        try {
            const response = await fetch('/history');
            const data = await response.json();
            const historyList = document.getElementById('historyList');
            
            if (data.history.length === 0) {
                historyList.innerHTML = '<p style="text-align: center; color: #6b7280;">No history yet</p>';
            } else {
                historyList.innerHTML = data.history.map(item => `
                    <div class="history-item" onclick="loadFromHistory('${item.image}')">
                        <img src="${item.image}" alt="QR Code">
                        <div class="history-item-type">${item.type}</div>
                        <div class="history-item-content">${item.content}</div>
                    </div>
                `).join('');
            }
        } catch (err) {
            showNotification('❌ Failed to load history', 'error');
        }
    });
    
    // Batch generate button
    document.getElementById('batchBtn').addEventListener('click', function() {
        document.getElementById('batchModal').classList.add('show');
    });
    
    document.getElementById('batchGenerateBtn').addEventListener('click', async function() {
        const input = document.getElementById('batchInput').value;
        const urls = input.split('\n').filter(url => url.trim());
        
        if (urls.length === 0) {
            showNotification('⚠️ Please enter at least one URL', 'error');
            return;
        }
        
        const resultsDiv = document.getElementById('batchResults');
        resultsDiv.innerHTML = '<p>Generating...</p>';
        
        const results = [];
        for (const url of urls) {
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        type: 'url',
                        url: url.trim(),
                        style: 'square',
                        errorCorrection: 'M',
                        fgColor: '#000000',
                        bgColor: '#FFFFFF',
                        boxSize: '10'
                    })
                });
                
                const result = await response.json();
                if (result.success) {
                    results.push({ url, image: result.image });
                }
            } catch (err) {
                console.error('Batch generation error:', err);
            }
        }
        
        resultsDiv.innerHTML = results.map((item, index) => `
            <div class="batch-result-item">
                <img src="${item.image}" alt="QR ${index + 1}">
                <a href="${item.image}" download="qrcode-${index + 1}.png" style="font-size: 0.75rem; color: #6366f1;">Download</a>
            </div>
        `).join('');
        
        showNotification(`✅ Generated ${results.length} QR codes!`, 'success');
    });
    
    // Templates button
    document.getElementById('templatesBtn').addEventListener('click', function() {
        document.getElementById('templatesModal').classList.add('show');
    });
    
    // Template selection
    document.querySelectorAll('.template-card').forEach(card => {
        card.addEventListener('click', function() {
            const template = this.dataset.template;
            applyTemplate(template);
            closeModal('templatesModal');
            showNotification('✨ Template applied!', 'success');
        });
    });
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(400px); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
});

// Generate QR Code function
async function generateQRCode() {
    const selectedType = document.querySelector('input[name="qrType"]:checked').value;
    const styleRadio = document.querySelector('input[name="style"]:checked');
    const style = styleRadio ? styleRadio.value : 'square';
    const errorCorrectionRadio = document.querySelector('input[name="errorCorrection"]:checked');
    const errorCorrection = errorCorrectionRadio ? errorCorrectionRadio.value : 'M';
    const gradientRadio = document.querySelector('input[name="gradientType"]:checked');
    const gradientType = gradientRadio ? gradientRadio.value : 'none';
    const frameRadio = document.querySelector('input[name="frameStyle"]:checked');
    const frameStyle = frameRadio ? frameRadio.value : 'none';
    
    const data = {
        type: selectedType,
        style: style,
        errorCorrection: errorCorrection,
        fgColor: document.getElementById('fgColor').value || '#000000',
        bgColor: document.getElementById('bgColor').value || '#FFFFFF',
        gradientType: gradientType,
        gradientColor: document.getElementById('gradientColor').value || '#6366f1',
        frameStyle: frameStyle,
        labelText: document.getElementById('labelText').value || '',
        boxSize: document.getElementById('boxSize').value || '10'
    };
    
    const inputFields = document.getElementById('inputFields');
    const inputs = inputFields.querySelectorAll('input, textarea');
    let hasRequiredData = false;
    
    inputs.forEach(input => {
        if (input.type === 'radio') {
            if (input.checked) {
                data[input.name] = input.value;
            }
        } else if (input.type !== 'button') {
            const value = input.value ? input.value.trim() : '';
            data[input.name] = value;
            if (input.required && value) {
                hasRequiredData = true;
            }
        }
    });
    
    if (selectedType === 'wifi') {
        if (!data.ssid || data.ssid.trim() === '') {
            showNotification('⚠️ Please enter WiFi network name', 'error');
            return;
        }
        hasRequiredData = true;
    }
    
    if (!hasRequiredData) {
        showNotification('⚠️ Please fill in the required fields', 'error');
        return;
    }
    
    const generateBtn = document.getElementById('generateBtn');
    const originalContent = generateBtn.innerHTML;
    generateBtn.innerHTML = '<span class="btn-icon">⏳</span><span>Generating...</span>';
    generateBtn.disabled = true;
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            currentQRImage = result.image;
            document.getElementById('qrPreview').innerHTML = `<img src="${result.image}" alt="QR Code">`;
            document.getElementById('downloadOptions').style.display = 'flex';
            showNotification('✅ QR Code generated successfully!', 'success');
        } else {
            showNotification('❌ Error: ' + (result.error || 'Failed to generate QR code'), 'error');
        }
    } catch (error) {
        console.error('Generation error:', error);
        showNotification('❌ Failed to generate QR code. Please try again.', 'error');
    } finally {
        generateBtn.innerHTML = originalContent;
        generateBtn.disabled = false;
    }
}

// Helper functions
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed; top: 20px; right: 20px; padding: 16px 24px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #10b981, #059669)' : 'linear-gradient(135deg, #ef4444, #dc2626)'};
        color: white; border-radius: 12px; font-weight: 600;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); z-index: 1000;
        animation: slideInRight 0.5s ease;
    `;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

function loadFromHistory(image) {
    currentQRImage = image;
    document.getElementById('qrPreview').innerHTML = `<img src="${image}" alt="QR Code">`;
    document.getElementById('downloadOptions').style.display = 'flex';
    closeModal('historyModal');
    showNotification('✅ Loaded from history!', 'success');
}

function applyTemplate(template) {
    const templates = {
        business: { fg: '#667eea', bg: '#FFFFFF', gradient: 'linear', gradientColor: '#764ba2', style: 'rounded' },
        social: { fg: '#f093fb', bg: '#FFFFFF', gradient: 'radial', gradientColor: '#f5576c', style: 'circle' },
        minimal: { fg: '#000000', bg: '#FFFFFF', gradient: 'none', style: 'square' },
        modern: { fg: '#4facfe', bg: '#FFFFFF', gradient: 'linear', gradientColor: '#00f2fe', style: 'rounded' }
    };
    
    const t = templates[template];
    if (t) {
        document.getElementById('fgColor').value = t.fg;
        document.getElementById('bgColor').value = t.bg;
        document.querySelector(`input[name="style"][value="${t.style}"]`).checked = true;
        document.querySelector(`input[name="gradientType"][value="${t.gradient}"]`).checked = true;
        
        if (t.gradient !== 'none') {
            document.getElementById('gradientColor').value = t.gradientColor;
            document.getElementById('gradientColorSection').style.display = 'block';
        }
    }
}
