# Django Backend - Document Download API Example
# Add this to your core/views.py

from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import os
from pathlib import Path

# Directory where documents are stored
DOCUMENTS_DIR = Path('media/documents')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_documents(request):
    """
    List all documents for the authenticated user
    Query params: year (optional) - e.g., "2024-2025"
    """
    user = request.user
    year = request.GET.get('year', '2024-2025')
    
    # TODO: Filter documents by user and year from database
    # Example query:
    # documents = Document.objects.filter(user=user, financial_year=year)
    
    # Demo response
    documents = [
        {
            'id': 1,
            'date': '04 July 2024',
            'title': 'Form 16',
            'fileName': 'form16_2024.pdf',
            'downloadUrl': f'/api/documents/download/form16_2024.pdf'
        },
        {
            'id': 2,
            'date': '15 June 2024',
            'title': 'Salary Certificate',
            'fileName': 'salary_certificate_june_2024.pdf',
            'downloadUrl': f'/api/documents/download/salary_certificate_june_2024.pdf'
        },
        {
            'id': 3,
            'date': '01 April 2024',
            'title': 'Investment Declaration',
            'fileName': 'investment_declaration_2024.pdf',
            'downloadUrl': f'/api/documents/download/investment_declaration_2024.pdf'
        }
    ]
    
    return Response(documents)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_document(request, filename):
    """
    Download a specific document
    URL: /api/documents/download/<filename>
    """
    user = request.user
    
    # Security: Verify user has access to this document
    # TODO: Check if document belongs to user
    # document = Document.objects.filter(user=user, file_name=filename).first()
    # if not document:
    #     return Response({'error': 'Document not found'}, status=404)
    
    # Construct file path
    file_path = DOCUMENTS_DIR / filename
    
    # Check if file exists
    if not file_path.exists():
        return Response({'error': 'File not found'}, status=404)
    
    # Security: Prevent directory traversal attacks
    if not str(file_path.resolve()).startswith(str(DOCUMENTS_DIR.resolve())):
        return Response({'error': 'Invalid file path'}, status=400)
    
    # Open and return file
    try:
        response = FileResponse(
            open(file_path, 'rb'),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=500)


# Alternative: If you want to serve from S3 or cloud storage
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_document_from_s3(request, filename):
    """
    Generate a pre-signed URL for downloading from S3
    """
    import boto3
    from botocore.exceptions import ClientError
    
    user = request.user
    
    # TODO: Verify user has access to this document
    
    try:
        s3_client = boto3.client('s3')
        bucket_name = 'your-bucket-name'
        object_key = f'documents/{user.id}/{filename}'
        
        # Generate pre-signed URL (valid for 1 hour)
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key
            },
            ExpiresIn=3600
        )
        
        return Response({'downloadUrl': url})
    except ClientError as e:
        return Response({'error': str(e)}, status=500)


# Add to core/urls.py:
"""
from django.urls import path
from . import views

urlpatterns = [
    # ... existing patterns ...
    path('api/documents/', views.list_documents, name='list_documents'),
    path('api/documents/download/<str:filename>', views.download_document, name='download_document'),
]
"""
