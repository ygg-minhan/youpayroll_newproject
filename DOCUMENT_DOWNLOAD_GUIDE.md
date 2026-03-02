# Document Download Implementation Guide

## ✅ What's Been Implemented

### Frontend (Documents.jsx)

The Documents page now has **full download functionality**:

1. **Download Handler** - `handleDownload(doc)` function that:
   - Fetches the document from the backend API
   - Creates a blob from the response
   - Triggers automatic download with proper filename
   - Falls back to opening in new tab if download fails

2. **Year Filtering** - Click the year selector to cycle through years:
   - 2024-2025
   - 2023-2024
   - 2022-2023

3. **Loading States** - Shows "Loading documents..." while fetching

4. **Empty States** - Shows message when no documents available

5. **Error Handling** - Gracefully handles download failures

## 🔧 How It Works

### Frontend Flow:

```javascript
1. User clicks download button
2. handleDownload() is called with document data
3. Fetch request sent to backend API
4. Backend returns file as blob
5. Blob converted to temporary URL
6. Temporary <a> element created and clicked
7. Browser downloads file
8. Cleanup: Remove element and revoke URL
```

### Backend Integration:

You need to create API endpoints in Django:

**Endpoint 1: List Documents**
```
GET /api/documents?year=2024-2025
```
Returns list of documents for the user

**Endpoint 2: Download Document**
```
GET /api/documents/download/<filename>
```
Returns the actual file

## 📝 Implementation Steps

### Step 1: Update Frontend API URL (if needed)

In `Documents.jsx`, update the API base URL:

```javascript
const fetchDocuments = async (year) => {
   const response = await fetch(`http://localhost:8000/api/documents?year=${year}`, {
      headers: {
         'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
   });
   const data = await response.json();
   setDocuments(data);
};
```

### Step 2: Create Django Models (if not exists)

```python
# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('FORM16', 'Form 16'),
        ('SALARY_CERT', 'Salary Certificate'),
        ('INVESTMENT', 'Investment Declaration'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/')
    financial_year = models.CharField(max_length=10)  # e.g., "2024-2025"
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
```

### Step 3: Add Backend Views

Copy the code from `DOCUMENT_DOWNLOAD_API.py` to your `core/views.py`

### Step 4: Add URL Routes

```python
# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... existing patterns ...
    path('api/documents/', views.list_documents, name='list_documents'),
    path('api/documents/download/<str:filename>', views.download_document, name='download_document'),
]
```

### Step 5: Create Media Directory

```bash
mkdir -p media/documents
```

### Step 6: Update Django Settings

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Step 7: Serve Media Files in Development

```python
# urls.py (main project)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your patterns ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 🔒 Security Considerations

The implementation includes:

1. **Authentication Required** - Only logged-in users can download
2. **User Verification** - Backend checks if document belongs to user
3. **Path Traversal Protection** - Prevents accessing files outside documents directory
4. **Token-based Auth** - Uses Bearer token for API requests

## 🎯 Testing the Download

### Option 1: Test with Demo Data (Current)

The frontend is already set up with demo data. Just click any download button to see the download flow (will fail at API call since backend isn't connected yet).

### Option 2: Test with Real Backend

1. Create some test documents in Django admin
2. Upload PDF files
3. Navigate to Documents page
4. Click download button
5. File should download automatically

## 📦 Alternative: Cloud Storage (S3)

If you want to store documents in AWS S3:

1. Install boto3: `pip install boto3`
2. Configure AWS credentials
3. Use the `download_document_from_s3()` function from the API example
4. Update frontend to handle pre-signed URLs

## 🎨 UI Features

### Current Features:
- ✅ Clean card-based layout
- ✅ Download button with hover effect
- ✅ Year selector dropdown
- ✅ Loading states
- ✅ Empty states
- ✅ Responsive design
- ✅ Back navigation

### Download Button States:
- **Normal**: Purple icon on light purple background
- **Hover**: Darker background, scales up slightly
- **Active**: Downloads file

## 🐛 Troubleshooting

### Issue: Download button doesn't work
**Solution**: Check browser console for errors. Make sure backend API is running.

### Issue: CORS errors
**Solution**: Add CORS headers in Django:
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
]
```

### Issue: File not found
**Solution**: Verify file exists in `media/documents/` directory

### Issue: Permission denied
**Solution**: Check file permissions: `chmod 644 media/documents/*`

## 📊 Database Schema

```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(200),
    document_type VARCHAR(20),
    file VARCHAR(255),
    financial_year VARCHAR(10),
    created_at TIMESTAMP
);
```

## 🚀 Next Steps

1. **Implement Backend API** - Use the provided code
2. **Test Download Flow** - Upload a test PDF and try downloading
3. **Add More Document Types** - Extend the DOCUMENT_TYPES choices
4. **Add Bulk Download** - Allow downloading multiple documents at once
5. **Add Document Preview** - Show PDF preview before download
6. **Add Search/Filter** - Filter by document type or date range

## 📱 Mobile Considerations

The download functionality works on mobile devices:
- iOS: Opens in new tab (Safari limitation)
- Android: Downloads to Downloads folder
- Desktop: Downloads to default download location

---

**Status**: Frontend is fully implemented and ready. Backend integration pending. ✅
