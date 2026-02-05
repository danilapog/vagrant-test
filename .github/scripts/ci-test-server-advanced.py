"""
Advanced DocumentServer Functional Tests
Tests the actual functionality of conversion and document handling
"""
import pytest
import requests
import time
import base64
import json
from io import BytesIO
from pathlib import Path


BASE_URL = "http://127.0.0.1:8200"
TIMEOUT = 60


class TestDocumentConversion:
    """Real-World Document Conversion Tests"""
    
    def test_text_to_pdf_conversion(self):
        """Convert a text document to PDF"""
        # Make simple text document
        text_content = "Hello ONLYOFFICE DocumentServer!\nThis is a test document.\n\nLine 3"
        text_base64 = base64.b64encode(text_content.encode()).decode()
        
        conversion_request = {
            "async": False,
            "filetype": "txt",
            "key": f"test_txt_to_pdf_{int(time.time())}",
            "outputtype": "pdf",
            "title": "test_document.txt",
            "url": f"data:text/plain;base64,{text_base64}"
        }
        
        response = requests.post(
            f"{BASE_URL}/ConversionService.ashx",
            json=conversion_request,
            timeout=TIMEOUT
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        assert response.status_code == 200
        result = response.json()
        
        # Check convertation result
        assert "endConvert" in result or "fileUrl" in result or "percent" in result
        print(f"✓ Text to PDF conversion successful")
        print(f"Result: {result}")
    
    def test_html_to_docx_conversion(self):
        """Convert HTML to DOCX"""
        html_content = """
        <html>
        <head><title>Test Document</title></head>
        <body>
            <h1>Test Header</h1>
            <p>This is a <b>test</b> paragraph with <i>formatting</i>.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ul>
        </body>
        </html>
        """
        html_base64 = base64.b64encode(html_content.encode()).decode()
        
        conversion_request = {
            "async": False,
            "filetype": "html",
            "key": f"test_html_to_docx_{int(time.time())}",
            "outputtype": "docx",
            "title": "test.html",
            "url": f"data:text/html;base64,{html_base64}"
        }
        
        response = requests.post(
            f"{BASE_URL}/ConversionService.ashx",
            json=conversion_request,
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        result = response.json()
        print(f"✓ HTML to DOCX conversion successful")
        print(f"Result: {result}")
    
    def test_csv_to_xlsx_conversion(self):
        """Convert CSV to XLSX"""
        csv_content = """Name,Age,City,Salary
John Doe,30,New York,75000
Jane Smith,25,Los Angeles,65000
Bob Johnson,35,Chicago,80000
Alice Williams,28,Houston,70000"""
        
        csv_base64 = base64.b64encode(csv_content.encode()).decode()
        
        conversion_request = {
            "async": False,
            "filetype": "csv",
            "key": f"test_csv_to_xlsx_{int(time.time())}",
            "outputtype": "xlsx",
            "title": "test_data.csv",
            "url": f"data:text/csv;base64,{csv_base64}"
        }
        
        response = requests.post(
            f"{BASE_URL}/ConversionService.ashx",
            json=conversion_request,
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        result = response.json()
        print(f"✓ CSV to XLSX conversion successful")
        print(f"Result: {result}")
    
    def test_markdown_to_docx_conversion(self):
        """Convert Markdown to DOCX"""
        markdown_content = """# Test Document

## Introduction

This is a **test** document written in *Markdown*.

### Features

- Feature 1
- Feature 2
- Feature 3

### Code Example

```python
def hello():
    print("Hello, World!")
```

### Conclusion

This concludes our test document.
"""
        
        md_base64 = base64.b64encode(markdown_content.encode()).decode()
        
        conversion_request = {
            "async": False,
            "filetype": "md",
            "key": f"test_md_to_docx_{int(time.time())}",
            "outputtype": "docx",
            "title": "test.md",
            "url": f"data:text/markdown;base64,{md_base64}"
        }
        
        response = requests.post(
            f"{BASE_URL}/ConversionService.ashx",
            json=conversion_request,
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        result = response.json()
        print(f"✓ Markdown to DOCX conversion successful")
        print(f"Result: {result}")


class TestDocumentBuilder:
    """Тесты Document Builder API"""
    
    def test_builder_simple_document(self):
        """Creating a Simple Document with the Builder API"""
        builder_script = """
        builder.CreateFile("docx");
        var oDocument = Api.GetDocument();
        var oParagraph = oDocument.GetElement(0);
        oParagraph.AddText("Hello from Document Builder!");
        builder.SaveFile("docx", "test_output.docx");
        builder.CloseFile();
        """
        
        builder_request = {
            "async": False,
            "key": f"test_builder_{int(time.time())}",
            "url": f"data:text/plain;base64,{base64.b64encode(builder_script.encode()).decode()}"
        }
        
        response = requests.post(
            f"{BASE_URL}/ConversionService.ashx",
            json=builder_request,
            timeout=TIMEOUT
        )
        
        print(f"Builder response: {response.status_code}")
        print(f"Builder result: {response.text[:500]}")


class TestEditorAPI:
    """Тесты Editor API (Checking the generation of editor pages)"""
    
    def test_document_editor_page(self):
        """Checking the loading of a text editor page"""
        response = requests.get(
            f"{BASE_URL}/web-apps/apps/documenteditor/main/index.html",
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        content = response.text
        
        # Checking for the presence of key elements
        assert "documenteditor" in content.lower()
        assert len(content) > 1000  # The page must be large enough
        print(f"✓ Document editor page loaded ({len(content)} bytes)")
    
    def test_spreadsheet_editor_page(self):
        """Checking the loading of the table editor page"""
        response = requests.get(
            f"{BASE_URL}/web-apps/apps/spreadsheeteditor/main/index.html",
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        content = response.text
        assert "spreadsheeteditor" in content.lower()
        print(f"✓ Spreadsheet editor page loaded ({len(content)} bytes)")
    
    def test_presentation_editor_page(self):
        """Checking the loading of the presentation editor page"""
        response = requests.get(
            f"{BASE_URL}/web-apps/apps/presentationeditor/main/index.html",
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        content = response.text
        assert "presentationeditor" in content.lower()
        print(f"✓ Presentation editor page loaded ({len(content)} bytes)")
    
    def test_api_js_loads(self):
        """Checking the loading of the main API file"""
        response = requests.get(
            f"{BASE_URL}/web-apps/apps/api/documents/api.js",
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        content = response.text
        
        # Checking for the availability of key API functions
        assert "DocsAPI" in content
        assert "DocEditor" in content
        print(f"✓ API.js loaded ({len(content)} bytes)")
        
        # Let's check that this is valid JavaScript.
        assert content.strip().endswith(";") or content.strip().endswith("}")
        print("✓ API.js appears to be valid JavaScript")


class TestStressAndPerformance:
    """Stress tests and performance tests"""
    
    def test_multiple_sequential_conversions(self):
        """Multiple consecutive conversions"""
        text_content = "Test document content"
        text_base64 = base64.b64encode(text_content.encode()).decode()
        
        num_conversions = 5
        results = []
        
        for i in range(num_conversions):
            start_time = time.time()
            
            conversion_request = {
                "async": False,
                "filetype": "txt",
                "key": f"test_sequential_{i}_{int(time.time())}",
                "outputtype": "pdf",
                "title": f"test_{i}.txt",
                "url": f"data:text/plain;base64,{text_base64}"
            }
            
            response = requests.post(
                f"{BASE_URL}/ConversionService.ashx",
                json=conversion_request,
                timeout=TIMEOUT
            )
            
            duration = time.time() - start_time
            results.append({
                "iteration": i,
                "status": response.status_code,
                "duration": duration
            })
            
            assert response.status_code == 200
        
        avg_duration = sum(r["duration"] for r in results) / len(results)
        print(f"✓ Completed {num_conversions} sequential conversions")
        print(f"Average duration: {avg_duration:.2f}s")
        print(f"Results: {results}")
    
    def test_concurrent_healthchecks(self):
        """Parallel healthcheck queries"""
        import concurrent.futures
        
        num_requests = 20
        
        def make_healthcheck():
            start = time.time()
            response = requests.get(f"{BASE_URL}/healthcheck", timeout=TIMEOUT)
            duration = time.time() - start
            return {
                "status": response.status_code,
                "duration": duration,
                "success": response.text.strip() == "true"
            }
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_healthcheck) for _ in range(num_requests)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        successful = sum(1 for r in results if r["success"])
        avg_duration = sum(r["duration"] for r in results) / len(results)
        
        assert successful == num_requests
        print(f"✓ All {num_requests} concurrent requests successful")
        print(f"Average response time: {avg_duration:.3f}s")
    
    def test_large_csv_conversion(self):
        """Converting a large CSV file"""
        # Generating a CSV with 1000 rows
        csv_lines = ["ID,Name,Email,Age,Salary"]
        for i in range(1000):
            csv_lines.append(f"{i},User{i},user{i}@example.com,{20+i%50},{30000+i*100}")
        
        csv_content = "\n".join(csv_lines)
        csv_base64 = base64.b64encode(csv_content.encode()).decode()
        
        print(f"CSV size: {len(csv_content)} bytes, {len(csv_lines)} rows")
        
        start_time = time.time()
        
        conversion_request = {
            "async": False,
            "filetype": "csv",
            "key": f"test_large_csv_{int(time.time())}",
            "outputtype": "xlsx",
            "title": "large_data.csv",
            "url": f"data:text/csv;base64,{csv_base64}"
        }
        
        response = requests.post(
            f"{BASE_URL}/ConversionService.ashx",
            json=conversion_request,
            timeout=TIMEOUT
        )
        
        duration = time.time() - start_time
        
        assert response.status_code == 200
        print(f"✓ Large CSV conversion successful in {duration:.2f}s")


class TestErrorHandling:
    """Error handling tests"""
    
    def test_invalid_filetype(self):
        """Test with unsupported file type"""
        conversion_request = {
            "async": False,
            "filetype": "invalid_format",
            "key": f"test_invalid_{int(time.time())}",
            "outputtype": "pdf",
            "title": "test.invalid",
            "url": "data:text/plain;base64,dGVzdA=="
        }
        
        response = requests.post(
            f"{BASE_URL}/ConversionService.ashx",
            json=conversion_request,
            timeout=TIMEOUT
        )
        
        # Should be error
        assert response.status_code in [400, 500]
        print(f"✓ Invalid filetype properly rejected with status {response.status_code}")
    
    def test_missing_parameters(self):
        """Tests with missed parameters"""
        conversion_request = {
            "filetype": "txt"
            # We intentionally skip mandatory parameters
        }
        
        response = requests.post(
            f"{BASE_URL}/ConversionService.ashx",
            json=conversion_request,
            timeout=TIMEOUT
        )
        
        # There must be a validation error
        assert response.status_code in [400, 500]
        print(f"✓ Missing parameters properly rejected with status {response.status_code}")
    
    def test_malformed_json(self):
        """Test with invalid JSON"""
        response = requests.post(
            f"{BASE_URL}/ConversionService.ashx",
            data="this is not json",
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        # There must be a parsing error
        assert response.status_code in [400, 500]
        print(f"✓ Malformed JSON properly rejected with status {response.status_code}")


class TestCommandServiceOperations:
    """Command Service Tests for Document Management"""
    
    def test_version_command(self):
        """Obtaining a version via Command Service"""
        command_request = {
            "c": "version"
        }
        
        response = requests.post(
            f"{BASE_URL}/coauthoring/CommandService.ashx",
            json=command_request,
            timeout=TIMEOUT
        )
        
        print(f"Version command response: {response.status_code}")
        print(f"Response body: {response.text}")
        
        assert response.status_code in [200, 400]
    
    def test_info_command(self):
        """Obtaining information about a document"""
        command_request = {
            "c": "info",
            "key": f"test_doc_{int(time.time())}"
        }
        
        response = requests.post(
            f"{BASE_URL}/coauthoring/CommandService.ashx",
            json=command_request,
            timeout=TIMEOUT
        )
        
        print(f"Info command response: {response.status_code}")
        assert response.status_code in [200, 400]


class TestStaticResources:
    """Static resource loading tests"""
    
    def test_fonts_available(self):
        """Checking font availability"""
        # We are trying to get a list of fonts or a specific font
        response = requests.get(
            f"{BASE_URL}/sdkjs/common/AllFonts.js",
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            print(f"✓ Fonts resource loaded ({len(response.content)} bytes)")
        else:
            print(f"⚠ Fonts resource returned {response.status_code}")
    
    def test_themes_available(self):
        """Checking the availability of topics"""
        response = requests.get(
            f"{BASE_URL}/web-apps/apps/common/main/resources/themes/theme-classic-light.json",
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            print(f"✓ Theme resource loaded")
        else:
            print(f"⚠ Theme resource returned {response.status_code}")
    
    def test_localization_available(self):
        """Checking the availability of localization files"""
        response = requests.get(
            f"{BASE_URL}/web-apps/apps/documenteditor/main/locale/en.json",
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            content = response.json()
            assert isinstance(content, dict)
            print(f"✓ Localization resource loaded ({len(content)} keys)")
        else:
            print(f"⚠ Localization resource returned {response.status_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
