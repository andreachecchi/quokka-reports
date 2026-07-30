import os
import asyncio
from pathlib import Path
from playwright.sync_api import sync_playwright


def _html_to_pdf_sync(html_path: str) -> str:
    """
    Synchronous function to convert HTML to PDF using Playwright.
    This will be run in a thread pool to avoid blocking the asyncio loop.
    """
    html_path = Path(html_path)
    pdf_path = html_path.with_suffix(".pdf")
    
    with sync_playwright() as p:
        # Launch browser in headless mode with appropriate args for headless environment
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ]
        )
        
        try:
            # Create a new page
            page = browser.new_page()
            
            # Set a reasonable timeout
            page.set_default_timeout(30000)
            
            # Load the HTML file
            page.goto(f"file://{html_path.absolute()}", wait_until="networkidle")
            
            # Generate PDF
            page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                margin={
                    "top": "1cm",
                    "right": "1cm",
                    "bottom": "1cm",
                    "left": "1cm",
                }
            )
            
            return str(pdf_path)
            
        finally:
            browser.close()


async def html_to_pdf(html_path: str) -> str:
    """
    Convert an HTML file to PDF using Playwright (async wrapper).
    
    Args:
        html_path: Path to the HTML file to convert
        
    Returns:
        Path to the generated PDF file
    """
    # Run the synchronous function in a thread pool
    return await asyncio.to_thread(_html_to_pdf_sync, html_path)
