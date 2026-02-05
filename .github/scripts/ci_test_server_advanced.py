"""
Advanced DocumentServer Tests with Logging
Tests real document conversion functionality and performance
"""
import pytest
import requests
import time
import base64
import logging
from datetime import datetime

# Configure logging with file and console output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_detailed.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_URL = "http://127.0.0.1:8200"
CONVERTER_URL = "http://127.0.0.1:8000/converter"  # Direct converter port
TIMEOUT = 60


@pytest.fixture(scope="session", autouse=True)
def test_session_info():
    """Log test session start and end times"""
    start_time = datetime.now()
    logger.info("=" * 80)
    logger.info(f"TEST SESSION STARTED: {start_time}")
    logger.info(f"Using converter at: {CONVERTER_URL}")
    logger.info("=" * 80)
    
    yield
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info("=" * 80)
    logger.info(f"TEST SESSION COMPLETED: {end_time}")
    logger.info(f"Total duration: {duration:.2f}s")
    logger.info("=" * 80)


class TestDocumentConversion:
    """Test document conversion with detailed logging"""
    
    def test_text_to_pdf_conversion(self):
        """Convert plain text to PDF format"""
        logger.info("Starting text to PDF conversion test")
        
        # Create simple text content
        text_content = "Hello ONLYOFFICE!\nThis is a test document."
        text_base64 = base64.b64encode(text_content.encode()).decode()
        
        # Prepare conversion request
        conversion_request = {
            "async": False,
            "filetype": "txt",
            "key": f"test_txt_pdf_{int(time.time())}",
            "outputtype": "pdf",
            "title": "test.txt",
            "url": f"data:text/plain;base64,{text_base64}"
        }
        
        logger.debug(f"Request payload: {conversion_request}")
        
        # Perform conversion with timing
        start = time.time()
        response = requests.post(
            CONVERTER_URL,
            json=conversion_request,
            timeout=TIMEOUT
        )
        duration = time.time() - start
        
        # Log response details
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response time: {duration:.3f}s")
        logger.debug(f"Response body: {response.text[:200]}")
        
        # Validate response
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        result = response.json()
        
        if "endConvert" in result:
            logger.info(f"✓ Conversion completed successfully")
            logger.debug(f"Result: {result}")
        
        assert "endConvert" in result or "fileUrl" in result
        logger.info("✓ Test PASSED")
    
    def test_csv_to_xlsx_conversion(self):
        """Convert CSV data to XLSX format"""
        logger.info("Starting CSV to XLSX conversion test")
        
        # Create sample CSV content
        csv_content = """Name,Age,City
John Doe,30,New York
Jane Smith,25,Los Angeles"""
        
        csv_base64 = base64.b64encode(csv_content.encode()).decode()
        
        logger.debug(f"CSV content size: {len(csv_content)} bytes")
        
        # Prepare conversion request
        conversion_request = {
            "async": False,
            "filetype": "csv",
            "key": f"test_csv_xlsx_{int(time.time())}",
            "outputtype": "xlsx",
            "title": "test.csv",
            "url": f"data:text/csv;base64,{csv_base64}"
        }
        
        start = time.time()
        try:
            response = requests.post(
                CONVERTER_URL,
                json=conversion_request,
                timeout=TIMEOUT
            )
            duration = time.time() - start
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response time: {duration:.3f}s")
            
            assert response.status_code == 200
            logger.info("✓ Test PASSED")
            
        except Exception as e:
            logger.error(f"✗ Test FAILED: {e}")
            raise
    
    def test_html_to_docx_conversion(self):
        """Convert HTML document to DOCX format"""
        logger.info("Starting HTML to DOCX conversion test")
        
        # Create HTML content with formatting
        html_content = """
        <html>
        <head><title>Test Document</title></head>
        <body>
            <h1>Test Header</h1>
            <p>This is a <b>test</b> paragraph with <i>formatting</i>.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </body>
        </html>
        """
        html_base64 = base64.b64encode(html_content.encode()).decode()
        
        conversion_request = {
            "async": False,
            "filetype": "html",
            "key": f"test_html_docx_{int(time.time())}",
            "outputtype": "docx",
            "title": "test.html",
            "url": f"data:text/html;base64,{html_base64}"
        }
        
        start = time.time()
        response = requests.post(
            CONVERTER_URL,
            json=conversion_request,
            timeout=TIMEOUT
        )
        duration = time.time() - start
        
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response time: {duration:.3f}s")
        
        assert response.status_code == 200
        logger.info("✓ HTML to DOCX conversion successful")


class TestEditorPages:
    """Test that editor pages load correctly"""
    
    def test_document_editor_page(self):
        """Verify document editor page loads"""
        logger.info("Testing document editor page")
        
        response = requests.get(
            f"{BASE_URL}/web-apps/apps/documenteditor/main/index.html",
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        content = response.text
        
        # Verify key content is present
        assert "documenteditor" in content.lower()
        assert len(content) > 1000
        
        logger.info(f"✓ Document editor page loaded ({len(content)} bytes)")
    
    def test_spreadsheet_editor_page(self):
        """Verify spreadsheet editor page loads"""
        logger.info("Testing spreadsheet editor page")
        
        response = requests.get(
            f"{BASE_URL}/web-apps/apps/spreadsheeteditor/main/index.html",
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        content = response.text
        assert "spreadsheeteditor" in content.lower()
        
        logger.info(f"✓ Spreadsheet editor page loaded ({len(content)} bytes)")
    
    def test_api_js_loads(self):
        """Verify main API JavaScript file loads"""
        logger.info("Testing API.js loading")
        
        response = requests.get(
            f"{BASE_URL}/web-apps/apps/api/documents/api.js",
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        content = response.text
        
        # Check for key API objects
        assert "DocsAPI" in content
        assert "DocEditor" in content
        
        logger.info(f"✓ API.js loaded ({len(content)} bytes)")
        logger.debug("API.js contains required DocsAPI objects")


class TestPerformance:
    """Performance tests with detailed metrics"""
    
    def test_multiple_conversions_with_metrics(self):
        """Run multiple conversions and measure performance"""
        logger.info("Starting performance test with 5 conversions")
        
        text_content = "Performance test document"
        text_base64 = base64.b64encode(text_content.encode()).decode()
        
        results = []
        
        # Perform 5 sequential conversions
        for i in range(5):
            logger.info(f"Conversion {i+1}/5...")
            
            conversion_request = {
                "async": False,
                "filetype": "txt",
                "key": f"perf_test_{i}_{int(time.time())}",
                "outputtype": "pdf",
                "title": f"perf_{i}.txt",
                "url": f"data:text/plain;base64,{text_base64}"
            }
            
            start = time.time()
            response = requests.post(
                CONVERTER_URL,
                json=conversion_request,
                timeout=TIMEOUT
            )
            duration = time.time() - start
            
            # Collect metrics for each conversion
            result_data = {
                "iteration": i + 1,
                "status": response.status_code,
                "duration": duration,
                "success": response.status_code == 200
            }
            results.append(result_data)
            
            logger.info(f"  → Status: {response.status_code}, Duration: {duration:.3f}s")
        
        # Calculate and log statistics
        successful = sum(1 for r in results if r["success"])
        avg_duration = sum(r["duration"] for r in results) / len(results)
        min_duration = min(r["duration"] for r in results)
        max_duration = max(r["duration"] for r in results)
        
        logger.info("=" * 60)
        logger.info("PERFORMANCE METRICS:")
        logger.info(f"  Total conversions: {len(results)}")
        logger.info(f"  Successful: {successful}/{len(results)}")
        logger.info(f"  Average time: {avg_duration:.3f}s")
        logger.info(f"  Min time: {min_duration:.3f}s")
        logger.info(f"  Max time: {max_duration:.3f}s")
        logger.info("=" * 60)
        
        assert successful == len(results)
        logger.info("✓ Performance test PASSED")
    
    def test_large_csv_conversion(self):
        """Test conversion of large CSV file (500+ rows)"""
        logger.info("Starting large CSV conversion test")
        
        # Generate CSV with 500 rows
        csv_lines = ["ID,Name,Email,Age"]
        for i in range(500):
            csv_lines.append(f"{i},User{i},user{i}@example.com,{20+i%50}")
        
        csv_content = "\n".join(csv_lines)
        csv_base64 = base64.b64encode(csv_content.encode()).decode()
        
        logger.info(f"CSV size: {len(csv_content)} bytes, {len(csv_lines)} rows")
        
        conversion_request = {
            "async": False,
            "filetype": "csv",
            "key": f"test_large_csv_{int(time.time())}",
            "outputtype": "xlsx",
            "title": "large_data.csv",
            "url": f"data:text/csv;base64,{csv_base64}"
        }
        
        start = time.time()
        response = requests.post(
            CONVERTER_URL,
            json=conversion_request,
            timeout=TIMEOUT
        )
        duration = time.time() - start
        
        assert response.status_code == 200
        logger.info(f"✓ Large CSV conversion successful in {duration:.2f}s")
    
    def test_concurrent_healthchecks(self):
        """Test server handles concurrent requests"""
        logger.info("Starting concurrent requests test")
        
        import concurrent.futures
        
        num_requests = 10
        
        def make_healthcheck():
            """Perform a single healthcheck request"""
            start = time.time()
            response = requests.get(f"{BASE_URL}/healthcheck", timeout=TIMEOUT)
            duration = time.time() - start
            return {
                "status": response.status_code,
                "duration": duration,
                "success": response.text.strip() == "true"
            }
        
        # Execute concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_healthcheck) for _ in range(num_requests)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # Calculate metrics
        successful = sum(1 for r in results if r["success"])
        avg_duration = sum(r["duration"] for r in results) / len(results)
        
        logger.info(f"Concurrent requests: {num_requests}")
        logger.info(f"Successful: {successful}/{num_requests}")
        logger.info(f"Average response time: {avg_duration:.3f}s")
        
        assert successful == num_requests
        logger.info("✓ Concurrent requests test PASSED")


class TestErrorHandling:
    """Test error handling for invalid inputs"""
    
    def test_invalid_filetype(self):
        """Test server rejects unsupported file types"""
        logger.info("Testing invalid filetype handling")
        
        conversion_request = {
            "async": False,
            "filetype": "invalid_format",
            "key": f"test_invalid_{int(time.time())}",
            "outputtype": "pdf",
            "title": "test.invalid",
            "url": "data:text/plain;base64,dGVzdA=="
        }
        
        response = requests.post(
            CONVERTER_URL,
            json=conversion_request,
            timeout=TIMEOUT
        )
        
        # Should return error status
        assert response.status_code in [400, 500]
        logger.info(f"✓ Invalid filetype properly rejected with status {response.status_code}")
    
    def test_missing_parameters(self):
        """Test server rejects requests with missing parameters"""
        logger.info("Testing missing parameters handling")
        
        # Request with only filetype (missing required params)
        conversion_request = {"filetype": "txt"}
        
        response = requests.post(
            CONVERTER_URL,
            json=conversion_request,
            timeout=TIMEOUT
        )
        
        # Should return validation error
        assert response.status_code in [400, 500]
        logger.info(f"✓ Missing parameters properly rejected with status {response.status_code}")
    
    def test_malformed_json(self):
        """Test server handles malformed JSON"""
        logger.info("Testing malformed JSON handling")
        
        response = requests.post(
            CONVERTER_URL,
            data="this is not valid json",
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        # Should return parsing error
        assert response.status_code in [400, 500]
        logger.info(f"✓ Malformed JSON properly rejected with status {response.status_code}")


class TestStaticResources:
    """Test availability of static resources"""
    
    def test_fonts_available(self):
        """Check if fonts resources are accessible"""
        logger.info("Testing fonts availability")
        
        response = requests.get(
            f"{BASE_URL}/sdkjs/common/AllFonts.js",
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            logger.info(f"✓ Fonts resource loaded ({len(response.content)} bytes)")
        else:
            logger.warning(f"⚠ Fonts resource returned {response.status_code}")
    
    def test_localization_available(self):
        """Check if localization files are accessible"""
        logger.info("Testing localization availability")
        
        response = requests.get(
            f"{BASE_URL}/web-apps/apps/documenteditor/main/locale/en.json",
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            content = response.json()
            assert isinstance(content, dict)
            logger.info(f"✓ Localization resource loaded ({len(content)} keys)")
        else:
            logger.warning(f"⚠ Localization resource returned {response.status_code}")


class TestCommandService:
    """Test Command Service API"""
    
    def test_version_command(self):
        """Get version info via Command Service"""
        logger.info("Testing version command")
        
        command_request = {"c": "version"}
        
        response = requests.post(
            f"{BASE_URL}/coauthoring/CommandService.ashx",
            json=command_request,
            timeout=TIMEOUT
        )
        
        logger.info(f"Version command response: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        
        assert response.status_code in [200, 400]
        logger.info("✓ Version command executed")
    
    def test_info_command(self):
        """Get document info via Command Service"""
        logger.info("Testing info command")
        
        command_request = {
            "c": "info",
            "key": f"test_doc_{int(time.time())}"
        }
        
        response = requests.post(
            f"{BASE_URL}/coauthoring/CommandService.ashx",
            json=command_request,
            timeout=TIMEOUT
        )
        
        logger.info(f"Info command response: {response.status_code}")
        assert response.status_code in [200, 400]
        logger.info("✓ Info command executed")


if __name__ == "__main__":
    # Run with verbose output and HTML report
    pytest.main([
        __file__, 
        "-v", 
        "-s", 
        "--tb=short", 
        "--html=report.html", 
        "--self-contained-html"
    ])
