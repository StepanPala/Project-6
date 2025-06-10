"""
Test suite for Alza.cz website using Playwright.
This suite includes tests for searching a product,
verifying product alt text, and downloading product instructions.
"""
import os

import pytest
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ALZA_HOMEPAGE = "https://www.alza.cz/"
TEST_PRODUCT_URL = (
    "https://www.alza.cz/alzapower-a101-fast-charge-20w-bila-d7855172.htm"
)

@pytest.fixture(params=["chromium", "firefox", "webkit"])
def browser(request):
    """
    Pytest fixture to launch and manage Playwright browser instance.
    It yields the instance and ensures it is closed after the test.
    The browser type (chromium, firefox, webkit) is parameterized.
    Supported browsers: chromium, firefox, webkit.
    """
    browser_type = request.param
    print(f"[Fixture] Launching {browser_type} browser...")
    with sync_playwright() as playwright:
        browser_instance = getattr(playwright, browser_type).launch(
            headless=False, # Set to True to run in headless mode
            slow_mo=500, # Adjust the speed of the browser actions
        )
        print(
            f"[Fixture] {browser_type.capitalize()} browser launched."
        )
        yield browser_instance
        print(f"[Fixture] Closing {browser_type} browser...")
        browser_instance.close()
        print(
            f"[Fixture] {browser_type.capitalize()} browser closed."
        )


@pytest.fixture()
def page(browser):
    """
    Pytest fixture to create and manage a new browser page.
    It yields the instance and ensures it is closed after the test.
    It sets a consistent viewport size for testing.
    """
    print("[Fixture] Creating new page...")
    page = browser.new_page()
    # Set the viewport size for consistent testing
    viewport_size = {"width": 1920, "height": 1080}
    print(f"[Fixture] Setting viewport size to: {viewport_size}")
    page.set_viewport_size(viewport_size)
    print(f"[Fixture] New page created with viewport: {viewport_size}.")
    yield page
    print("[Fixture] Closing page...")
    page.close()
    print("[Fixture] Page closed.")


def refuse_cookies(page: Page):
    """
    Refuse cookies on the Alza.cz website.
    This function attempts to find and click the refuse cookies button.
    If the button is not found or not visible within the timeout,
    a screenshot is taken and the test continues.
    """
    print(f"Attempting to refuse cookies on page {page.url}...")
    button_refuse_selector = ".js-cookies-info-reject"
    try:
        button_refuse = page.locator(button_refuse_selector)
        button_refuse.wait_for(state="visible", timeout=10000)
        button_refuse.click()
        print("Cookie banner refused.")
    except PlaywrightTimeoutError:
        # Cookie banner may not load in headless mode
        screenshot_path = "alza_cookie_banner_timeout.png"
        page.screenshot(path=screenshot_path)
        print(
            f"Cookie banner ('{button_refuse_selector}') not found or not "
            f"visible on {page.url}. "
            f"Screenshot saved as {screenshot_path}. Trying to continue..."
        )


def navigate_and_refuse_cookies(page: Page, url: str):
    """
    Navigates the page to a given URL and attempts to refuse cookies.
    """
    print(f"Navigating to {url}...")
    try:
        page.goto(url, timeout=20000)
        print(f"Navigation to {url} successful.")
        print(f"Current URL after navigation: {page.url}")
    except PlaywrightTimeoutError:
        print(f"Navigation to {url} timed out.")
        raise # Re-raise the exception after printing
    refuse_cookies(page)


@pytest.mark.search
def test_search_and_verify_product_by_name(page: Page):
    """
    Test for searching a product on Alza.cz.
    This test navigates to the homepage, performs a search for
    a specific product, and verifies that the product page loads
    correctly. It checks the product URL and name.
    """
    print("\nStarting test_search...")
    navigate_and_refuse_cookies(page, ALZA_HOMEPAGE)

    search_input_selector = ".header-alz-12 input"
    search_product = "nabíječka"
    search_input = page.locator(search_input_selector)
    search_input.fill(search_product)
    print(f"Pressing Enter to search for: '{search_product}'")
    search_input.press("Enter")

    print(f"Current URL after search: {page.url}")
    product_selector = "#img7855172"
    find_product = page.locator(product_selector)
    try:
        print(
            f"Waiting for product ('{product_selector}') to be visible in "
            f"search results..."
            )
        find_product.wait_for(state="visible", timeout=10000)
        print(f"Product ('{product_selector}') is visible.")
    except PlaywrightTimeoutError:
        screen_path = "alza_search_product_not_visible.png"
        page.screenshot(path=screen_path)
        print(
            f"Product ('{product_selector}') not visible in search results "
            f"on page {page.url}. "
            f"Screenshot saved as {screen_path}."
        )
        raise AssertionError(
            f"Product ('{product_selector}') not visible in search results."
        )
    print(f"Clicking product ('{product_selector}')...")
    find_product.click()
    print(f"Product clicked. Current URL: {page.url}")

    # Checks that we are on the correct product page
    h1_selector = "h1"
    h1_locator = page.locator(h1_selector)
    try:
        print(
            f"Waiting for H1 element ('{h1_selector}') to be visible on "
            f"product page...")
        h1_locator.wait_for(state="visible", timeout=10000)
    except PlaywrightTimeoutError:
        screen_path = "alza_product_page_h1_not_visible.png"
        page.screenshot(path=screen_path)
        print(
            f"H1 element ('{h1_selector}') not visible on product page "
            f"{page.url}. "
            f"Screenshot saved as {screen_path}."
        )
        raise AssertionError(
            f"H1 element ('{h1_selector}') not visible on product page."
        )
    print(f"Product page loaded, H1 element ('{h1_selector}') found.")

    # Checks the URL and product name
    print(f"Checking product URL. Expected: {TEST_PRODUCT_URL}")
    print(f"Actual: {page.url}")
    assert page.url == TEST_PRODUCT_URL, (
        f"Expected URL {TEST_PRODUCT_URL}, but got {page.url}"
    )
    expected_h1_text = "AlzaPower A101CA Fast Charge 20W bílá"
    actual_h1_text = h1_locator.text_content()
    print(f"Checking product name. Expected: '{expected_h1_text}'")
    print(f"Actual: '{actual_h1_text}'")
    assert actual_h1_text == expected_h1_text, (
        f"H1 text mismatch. Expected: '{expected_h1_text}', "
        f"Actual: '{actual_h1_text}'"
    )
    print("Product URL and name verified successfully.")
    print("test_search completed successfully.")


@pytest.mark.alt_text
def test_product_image_alt_text(page: Page):
    """
    Test for verifying the alt text of the product image on Alza.cz.
    This test navigates to the product page, checks the visibility
    of the product image, and verifies that the alt text matches
    the expected value.
    """
    print("\nStarting test_product_alt_text...")
    navigate_and_refuse_cookies(page, TEST_PRODUCT_URL)
    product_image_selector = (
        "#detailPicture swiper-slide.swiper-slide-active img"
    )
    product_image = page.locator(product_image_selector)
    try:
        print(
            f"Waiting for product image ('{product_image_selector}') "
            f"to be visible..."
        )
        product_image.wait_for(state="visible", timeout=10000)
        print(f"Product image ('{product_image_selector}') is visible.")
    except PlaywrightTimeoutError:
        screen_path = "alza_product_image_not_visible.png"
        page.screenshot(path=screen_path)
        print(
            f"Product image ('{product_image_selector}') not visible on "
            f"product page {page.url}. "
            f"Screenshot saved as {screen_path}."
        )
        raise AssertionError(
            f"Product image ('{product_image_selector}') not visible."
        )

    print(
        f"Checking visibility of product image ('{product_image_selector}')..."
    )
    assert product_image.is_visible(), (
        f"Product image ('{product_image_selector}') is not visible " 
        f"after wait_for."
    )
    print(f"Product image ('{product_image_selector}') is visible.")

    actual_alt_text = product_image.get_attribute("alt")
    expected_alt_text = (
        "AlzaPower A101CA Fast Charge 20W bílá - Nabíječka do sítě - "
        "Hlavní obrázek"
    )
    print(f"Actual alt text: '{actual_alt_text}'")
    print(f"Expected alt text: '{expected_alt_text}'")
    print("Checking product alt text...")
    assert actual_alt_text == expected_alt_text, (
        f"Product alt text mismatch. Expected: '{expected_alt_text}', "
        f"Actual: '{actual_alt_text}'"
    )
    print("Product alt text verified successfully.")
    print("test_product_alt_text completed successfully.")


@pytest.mark.download
def test_download_instructions_and_verify_saved_file(page: Page):
    """
    Test for downloading product instructions from Alza.cz.
    This test navigates to the product page, clicks on the
    Discussion tab, and attempts to download the product manual.
    It verifies that the download link is visible and that the
    downloaded file exists in the expected location.
    """
    print("\nStarting test_download_instructions...")
    navigate_and_refuse_cookies(page, TEST_PRODUCT_URL)

    discussion_tab_selector = "#hlTabDiscussionPosts"
    find_details = page.locator(discussion_tab_selector)
    try:
        print(
            f"Waiting for Discussion tab ('{discussion_tab_selector}') "
            f"to be visible..."
            )
        find_details.wait_for(state="visible", timeout=10000)
        print(f"Discussion tab ('{discussion_tab_selector}') is visible.")
    except PlaywrightTimeoutError:
        screen_path = "alza_discussion_tab_not_visible.png"
        page.screenshot(path=screen_path)
        print(
            f"Discussion tab ('{discussion_tab_selector}') not visible on "
            f"product page {page.url}. "
            f"Screenshot saved as {screen_path}."
        )
        raise AssertionError(
            f"Discussion tab ('{discussion_tab_selector}') not visible."
        )
    print(f"Clicking Discussion tab ('{discussion_tab_selector}')...")
    find_details.click()
    print(f"Discussion tab clicked. Current URL: {page.url}")

    download_link_selector = "#discussionPosts .manualsList-alz-1 a"
    download_link_locator = page.locator(download_link_selector)
    try:
        print(
            f"Waiting for download link ('{download_link_selector}') "
            f"to be visible..."
            )
        download_link_locator.wait_for(state="visible", timeout=10000)
    except PlaywrightTimeoutError:
        screen_path = "alza_download_link_not_visible.png"
        page.screenshot(path=screen_path)
        print(
            f"Download link ('{download_link_selector}') not visible on "
            f"product page {page.url}. "
            f"Screenshot saved as {screen_path}."
        )
        raise AssertionError(
            f"Download link ('{download_link_selector}') not visible."
        )

    print(f"Attempting to download from ('{download_link_selector}')...")
    with page.expect_download() as download_info:
        download_link_locator.click()
        print("Download link clicked, waiting for download to start...")
    download = download_info.value

    download_path = download.suggested_filename
    print(f"Download started. Suggested file name: {download_path}")

    abs_path = os.path.abspath(download_path) if download_path else None

    try:
        if not abs_path:
            # This case means download.suggested_filename was empty or None.
            print(
                "Download did not provide a valid suggested filename. "
                "Cannot save or clean up."
            )
            raise AssertionError(
                "Download failed: No suggested filename provided."
            )

        print(f"Attempting to save downloaded file as: {download_path}")
        download.save_as(download_path) # File is created here
        print(f"File saved successfully to: {abs_path}")

        # Checks if the file exists
        print(f"Verifying if downloaded file exists at: {abs_path}")
        assert os.path.isfile(abs_path), (
            f"Downloaded file does not exist at the expected location: "
            f"{abs_path}"
        )
        print(f"Verified: Downloaded file exists at: {abs_path}")
        print("File download, save, and existence verification successful.")

    finally:
        # Clean-up: Attempt to remove the file if abs_path is valid
        # and the file exists. This ensures cleanup is attempted
        # even if assertions in the try block fail after file creation.
        if abs_path and os.path.isfile(abs_path):
            print(
                f"Initiating cleanup: Attempting to remove downloaded file: "
                f"{abs_path}"
            )
            try:
                os.remove(abs_path)
                print(
                    f"Cleanup successful: Downloaded file {abs_path} removed."
                )
            except OSError as e:
                print(
                    f"Cleanup error: Failed to remove file {abs_path}. "
                    f"Error: {e}"
                )
        elif abs_path: # abs_path defined, but file not found at cleanup
            print(
                f"Cleanup: File {abs_path} not found (was it saved correctly, "
                f"or already removed?)."
            )
