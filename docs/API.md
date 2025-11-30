# Forensic AI Tool API Documentation

This document provides detailed information about the API endpoints available in the Forensic AI Tool.

## Base URL

```
http://localhost:12000
```

## Authentication

Currently, the API does not require authentication. For production deployments, it is recommended to implement appropriate authentication mechanisms.

## Endpoints

### System Status

#### GET /status

Check the main system status.

**Response:**
```json
{
    "status": "ok",
    "message": "System operational"
}
```

---

#### GET /util-status

Check the utility components status.

**Response:**
```json
{
    "status": "ok",
    "details": "All utilities loaded"
}
```

---

### APK Analysis

#### POST /upload

Upload an APK file for analysis.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` - The APK file to upload

**Response:**
Redirects to the dashboard with analysis results.

---

#### POST /analyze-apk

Analyze an uploaded APK file.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `apk` - The APK file

**Response:**
```json
{
    "analysis": {
        "apk_path": "/path/to/file.apk",
        "permissions": ["android.permission.INTERNET"]
    },
    "apk_path": "/tmp/file.apk"
}
```

---

### Permissions

#### POST /summarize-permissions

Get a summary of Android permissions.

**Request:**
```json
{
    "permissions": [
        "android.permission.INTERNET",
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.CAMERA"
    ]
}
```

**Response:**
```json
{
    "summary": "APK requests 3 permissions. Location access: 1 permissions. Primary permission: android.permission.INTERNET"
}
```

---

### Voice Commands

#### POST /voice-command

Process a voice command.

**Request:**
```json
{
    "transcript": "check system status"
}
```

**Response:**
```json
{
    "response": "Processed: check system status"
}
```

---

### Web Scraping

#### POST /scrape-website

Scrape a website for downloadable files.

**Request:**
```json
{
    "url": "https://example.com"
}
```

**Response:**
```json
{
    "file_links": [
        "https://example.com/file.apk",
        "https://example.com/document.pdf"
    ],
    "status": "Scraping Complete"
}
```

---

#### POST /download-and-analyze

Download a file from URL and analyze it.

**Request:**
```json
{
    "file_url": "https://example.com/file.apk"
}
```

**Response:**
```json
{
    "analysis": {
        "file_path": "/tmp/file.apk",
        "info": "Downloaded and analyzed"
    },
    "local_path": "/tmp/file.apk"
}
```

---

#### GET /run-scraper

Start the background web scraper.

**Response:**
```
Web scraper started! Check output.json for results.
```

---

### Emulator

#### GET /start-emulator

Start the Android emulator stream.

**Response:**
```json
{
    "emulator_started": true
}
```

---

### Logs

#### GET /logs

Get all scan logs.

**Response:**
```json
{
    "model_logs": [...],
    "utils_logs": [...]
}
```

---

#### GET /log-feed

Get the live log feed.

**Response:**
```json
{
    "status": "Idle",
    "file_links": [],
    "api_calls": ["/scrape-website", "/voice-command"],
    "transcripts": ["check status"]
}
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Missing or invalid parameters |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

Error responses include a JSON body:
```json
{
    "error": "Error description"
}
```

---

## Rate Limiting

No rate limiting is currently implemented. For production deployments, consider implementing rate limiting to prevent abuse.

---

## Examples

### Python

```python
import requests

# Check system status
response = requests.get('http://localhost:12000/status')
print(response.json())

# Analyze permissions
permissions = [
    "android.permission.INTERNET",
    "android.permission.READ_SMS"
]
response = requests.post(
    'http://localhost:12000/summarize-permissions',
    json={'permissions': permissions}
)
print(response.json())

# Upload APK for analysis
with open('app.apk', 'rb') as f:
    files = {'apk': f}
    response = requests.post(
        'http://localhost:12000/analyze-apk',
        files=files
    )
print(response.json())
```

### cURL

```bash
# Check status
curl http://localhost:12000/status

# Summarize permissions
curl -X POST http://localhost:12000/summarize-permissions \
    -H "Content-Type: application/json" \
    -d '{"permissions": ["android.permission.INTERNET"]}'

# Scrape website
curl -X POST http://localhost:12000/scrape-website \
    -H "Content-Type: application/json" \
    -d '{"url": "https://example.com"}'
```

### JavaScript

```javascript
// Check system status
fetch('http://localhost:12000/status')
    .then(response => response.json())
    .then(data => console.log(data));

// Summarize permissions
fetch('http://localhost:12000/summarize-permissions', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        permissions: [
            'android.permission.INTERNET',
            'android.permission.CAMERA'
        ]
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Websocket Support

Currently, the API does not support WebSocket connections. Real-time updates can be obtained by polling the `/log-feed` endpoint.

---

## Changelog

### Version 1.0.0
- Initial API release
- Core endpoints for APK analysis
- Web scraping functionality
- Voice command processing
- Emulator integration
