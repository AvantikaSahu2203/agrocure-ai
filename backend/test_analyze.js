const fs = require('fs');

async function testAnalyze() {
    try {
        const FormData = require('form-data'); // Might not be installed
        // If not installed, we can try native fetch (Node 18+)

        if (typeof fetch !== 'undefined') {
            const formData = new FormData();
            formData.append('crop_name', 'Tomato');
            // Mock file
            const blob = new Blob(['fake image'], { type: 'image/jpeg' });
            formData.append('image', blob, 'test.jpg');

            const res = await fetch('http://localhost:8000/api/v1/disease-ai/analyze', {
                method: 'POST',
                body: formData
            });
            console.log('Status:', res.status);
            const text = await res.text();
            console.log('Body:', text);
        } else {
            console.log('Fetch not available');
        }
    } catch (e) {
        console.error(e);
        // Fallback to manual http request if needed
    }
}

// Just checking if we can import 'form-data' or similar from node_modules if they exist in parent
// 'web' folder has node_modules.
// We are in 'backend'.
