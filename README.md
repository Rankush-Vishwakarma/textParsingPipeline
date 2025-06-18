# textParsingPipeline
# Text Parsing Pipeline

A robust Python-based text extraction and processing pipeline that supports multiple file formats and integrates with Google Cloud Storage (GCS) for scalable document processing.

## Features

- **Multi-format Support**: Extract text from PDF, DOCX, HTML, and XML files
- **Cloud Integration**: Seamless integration with Google Cloud Storage
- **FastAPI Framework**: RESTful API endpoints for easy integration
- **Comprehensive Logging**: Detailed logging for monitoring and debugging
- **URL Processing**: Direct text extraction from web URLs
- **Error Handling**: Robust exception handling and logging

## Supported File Types

- **PDF**: Using PyMuPDF (fitz) for reliable text extraction
- **DOCX/DOC**: Microsoft Word documents using python-docx
- **HTML**: Web pages with BeautifulSoup for clean text extraction
- **XML**: XML documents using ElementTree
- **URLs**: Direct web content processing

## Prerequisites

### Python Dependencies

```bash
pip install google-cloud-storage
pip install nltk
pip install beautifulsoup4
pip install PyMuPDF
pip install python-docx
pip install fastapi
pip install requests
```

### Google Cloud Setup

1. Create a Google Cloud Project
2. Enable the Cloud Storage API
3. Create a service account and download the JSON key file
4. Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   ```

### NLTK Data

The pipeline automatically downloads required NLTK data:
- punkt (tokenizer)
- stopwords

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd text-parsing-pipeline
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Cloud credentials:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
   ```

4. Configure your GCS bucket name in the code:
   ```python
   GCS_BUCKET = "your-bucket-name"
   ```
## Configuration

### Environment Variables

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to GCS service account JSON file

### Pipeline Settings

- `GCS_BUCKET`: Your Google Cloud Storage bucket name
- `GCS_FOLDER`: Input folder path in GCS (default: "input")
- `SUPPORTED_TYPES`: List of supported file extensions

## API Endpoints

The FastAPI application provides RESTful endpoints for document processing:

- **POST /upload**: Upload and process files
- **POST /process-url**: Process content from URLs
- **GET /health**: Health check endpoint

## Logging

The pipeline includes comprehensive logging:

- **File Logging**: Saves to `pipeline_report.log`
- **Console Logging**: Real-time output
- **Function Decorators**: Automatic logging for all major functions
- **Error Tracking**: Detailed exception logging

## Error Handling

The pipeline handles various error scenarios:

- Unsupported file formats
- Network timeouts for URLs
- GCS authentication failures
- File parsing errors
- Missing files in GCS

## Performance Considerations

- Files are processed in memory using BytesIO streams
- Large files are handled efficiently through streaming
- Automatic cleanup of temporary resources
- Optimized text extraction for each file type

## Security

- Service account credentials for GCS access
- Input validation for file types and URLs
- Secure file handling without local storage
- Request timeouts to prevent hanging

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **Authentication Error**:
   - Verify GOOGLE_APPLICATION_CREDENTIALS is set correctly
   - Ensure service account has Storage Admin permissions

2. **Unsupported File Type**:
   - Check SUPPORTED_TYPES list
   - Verify file extension matches supported formats

3. **Network Timeouts**:
   - Increase timeout values for large URLs
   - Check internet connectivity

4. **Memory Issues**:
   - For very large files, consider implementing streaming
   - Monitor memory usage during processing

### Debug Mode

Enable debug logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

additional improvements - 
# Text Parsing Pipeline

This is a FastAPI-based text extraction pipeline that supports PDF, DOCX, XLSX, HTML, and XML. Files are uploaded or pulled from a URL, parsed, and saved to Google Cloud Storage.

## 🧰 Features
- ✅ PDF, DOCX, XLSX, HTML, XML support
- ✅ Upload single file or URL
- ✅ Upload and parse multiple files in parallel
- ✅ Deduplication using file hash
- ✅ GCS integration
- ✅ Modular design

---

## 🚀 Run It Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```


---

## 📡 API Endpoints

### ➤ `POST /upload/`
**Upload a single file**
```bash
curl -F "file=@example.pdf" http://localhost:8000/upload/
```

### ➤ `POST /upload-url/`
**Upload content from a URL**
```bash
curl -X POST -F "url=https://example.com" http://localhost:8000/upload-url/
```

### ➤ `POST /upload-multiple/`
**Upload and process multiple files in parallel**
```bash
curl -X POST http://localhost:8000/upload-multiple/ \
  -F "files=@sample1.pdf" \
  -F "files=@sample2.docx" \
  -F "files=@sample3.xlsx"
```

---

## 📁 Output
Each processed file is saved in GCS under the `output/` folder with `.json` extension containing extracted text.

---

## 🔧 Configuration
Set your GCS bucket name and folders in `app/config.py`:
```python
GCS_BUCKET = "your-gcs-bucket"
GCS_INPUT_FOLDER = "input"
GCS_OUTPUT_FOLDER = "output"
```

---

## 📦 Supported File Types
- `.pdf`
- `.docx`, `.doc`
- `.xlsx`
- `.html`
- `.xml`

---

## 🔒 Deduplication
- Files are hashed (SHA-256) before upload.
- If the same file is uploaded again, it is not reprocessed.

