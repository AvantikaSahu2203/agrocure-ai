const fs = require('fs');
const http = require('http');

// Create a dummy image file
fs.writeFileSync('test_node_image.jpg', 'fake image content');

const boundary = '--------------------------123456789012345678901234';

const bodyParts = [
    `--${boundary}`,
    'Content-Disposition: form-data; name="crop_name"',
    '',
    'Tomato',
    `--${boundary}`,
    'Content-Disposition: form-data; name="image"; filename="test_node_image.jpg"',
    'Content-Type: image/jpeg',
    '',
    fs.readFileSync('test_node_image.jpg'),
    `--${boundary}--`
];

// Combine parts into a buffer
const buffer = Buffer.concat([
    Buffer.from(bodyParts[0] + '\r\n' + bodyParts[1] + '\r\n' + bodyParts[2] + '\r\n' + bodyParts[3] + '\r\n'),
    Buffer.from(bodyParts[4] + '\r\n' + bodyParts[5] + '\r\n' + bodyParts[6] + '\r\n' + bodyParts[7] + '\r\n'),
    fs.readFileSync('test_node_image.jpg'),
    Buffer.from('\r\n' + bodyParts[9])
]);

// Actually, constructing multipart manually is prone to error with newlines.
// A simpler way is to use 'fetch' if available (Node 18+) or 'axios' if installed.
// Since 'npm run dev' is running, 'node_modules' likely has 'next' dependencies but maybe not global fetch.
// Let's try to use the 'http' module with precise manual formatting or just check /health first.

const options = {
    hostname: 'localhost',
    port: 8000,
    path: '/api/v1/disease-ai/analyze',
    method: 'POST',
    headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': buffer.length
    }
};

// Start with a health check
const healthOptions = {
    hostname: 'localhost',
    port: 8000,
    path: '/health',
    method: 'GET'
};

const reqHealth = http.request(healthOptions, (res) => {
    console.log(`Health Status: ${res.statusCode}`);
    res.on('data', (d) => {
        process.stdout.write(d);
    });
});
reqHealth.on('error', (e) => {
    console.error(`Health Error: ${e.message}`);
});
reqHealth.end();

// Run analyze test after small delay
setTimeout(() => {
    console.log('\nTesting Analyze...');
    // We need to reconstruct the body properly.
    // Let's just create a simpler body for 'crop_name' only to see if we get 422 (validation error) instead of connection refused.
    // If we get 422, server is up and routing works.

    // BUT we want to pass validation. 
    // Let's try to use a boundary that works.

    // Just testing reachability first.
}, 1000);
