"""Browser integration test for filters, CSV loading, charts, and KPI behavior.

Run from repository root:
  python -m http.server 8765
  python analytics/browser_test.py
Requires: pip install playwright && python -m playwright install chromium
"""
import asyncio
from playwright.async_api import async_playwright

URL="http://127.0.0.1:8765/"

async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True)
        page=await browser.new_page()
        errors=[]
        page.on("pageerror",lambda err: errors.append(str(err)))
        response=await page.goto(URL,wait_until="networkidle")
        assert response and response.status==200
        await page.locator("#load-status").get_by_text("600 synthetic incidents",exact=False).wait_for()
        assert await page.locator("#total").inner_text()=="600"
        assert await page.locator("#trends .trend-col").count()>=10
        assert await page.locator("#teams .team-row").count()==4
        assert await page.locator("#rows tr").count()==50
        await page.locator("#priority").select_option("Critical")
        critical=int(await page.locator("#total").inner_text())
        assert 0<critical<600
        await page.locator("#status").select_option("Open")
        assert int(await page.locator("#total").inner_text())<critical
        assert await page.locator("#sla").inner_text()=="N/A"
        assert await page.locator("#avg").inner_text()=="N/A"
        await page.locator("#resetBtn").click()
        assert await page.locator("#total").inner_text()=="600"
        assert not errors, errors
        await browser.close()
        print("Browser integration checks passed.")

if __name__=="__main__":
    asyncio.run(main())
