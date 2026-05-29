"""
Smoke test for the Forensic Intelligence Dashboard.
Assumes the server is running: uvicorn dashboard.backend.main:app --port 8000

Run: pytest dashboard/tests/smoke_test.py -v
"""

import pytest
from playwright.sync_api import sync_playwright, expect


BASE_URL = "http://localhost:8000"


def test_dashboard_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL, wait_until="domcontentloaded")

        # Title and top-bar branding
        assert "FORENSIC INTELLIGENCE" in page.title()
        expect(page.locator(".tb-logo")).to_have_text("SENTINEL")

        # Core UI panels are present
        expect(page.locator("#search-input")).to_be_visible()
        expect(page.locator("#graph-svg")).to_be_visible()
        expect(page.locator("#timeline-svg")).to_be_visible()
        expect(page.locator("#panel-details")).to_be_visible()

        browser.close()


def test_search_returns_results():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL, wait_until="domcontentloaded")

        # Initial load populates the sidebar with all entities
        page.wait_for_selector(".result-item", timeout=5000)
        all_items = page.locator(".result-item").count()
        assert all_items > 0, "Sidebar should show entities on load"

        # Typing filters results
        page.fill("#search-input", "LJM")
        page.wait_for_timeout(400)  # debounce
        page.wait_for_selector(".result-item", timeout=3000)
        filtered = page.locator(".result-item").count()
        assert filtered < all_items, "Search should reduce result count"
        assert filtered >= 1, "Should find at least one LJM entity"

        browser.close()


def test_select_entity_populates_graph_and_timeline():
    """
    Uses LJM Cayman L.P. — a shell company with direct Enron transactions,
    so we can verify both the network graph (3 nodes) and timeline (14 txns).
    Note: executive personal accounts (e.g. Andrew Fastow) have no synthetic
    transactions and would show only 1 node and 0 timeline dots.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL, wait_until="domcontentloaded")

        # Search for LJM Cayman (shell company with known connections)
        page.wait_for_selector(".result-item", timeout=5000)
        page.fill("#search-input", "LJM Cayman")
        page.wait_for_timeout(400)
        page.wait_for_selector(".result-item", timeout=3000)

        results = page.locator(".result-item")
        assert results.count() >= 1
        expect(results.first.locator(".ri-name")).to_contain_text("LJM Cayman")

        # Click the entity
        results.first.click()

        # Network graph should populate with multiple nodes
        page.wait_for_selector("#graph-svg .g-node", timeout=8000)
        page.wait_for_timeout(600)  # let force simulation settle
        nodes = page.locator("#graph-svg .g-node")
        assert nodes.count() > 1, "Graph should show LJM Cayman + connected entities"

        # Graph placeholder should be hidden
        placeholder = page.locator("#graph-placeholder")
        assert placeholder.evaluate("el => el.style.display") == "none"

        # Timeline should show transaction dots
        page.wait_for_selector("#timeline-svg circle.txn", timeout=5000)
        dots = page.locator("#timeline-svg circle.txn")
        assert dots.count() > 0, "Timeline should show transactions"

        # Entity details panel should show the name
        expect(page.locator("#details-scroll")).to_contain_text("LJM Cayman")

        # Flag controls should appear
        expect(page.locator("#flag-bar")).to_be_visible()

        browser.close()


def test_click_different_graph_node_updates_timeline():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL, wait_until="domcontentloaded")

        # Select Enron Corp (the central node)
        page.wait_for_selector(".result-item", timeout=5000)
        page.fill("#search-input", "Enron Corp")
        page.wait_for_timeout(400)
        page.wait_for_selector(".result-item", timeout=3000)
        page.locator(".result-item").first.click()

        # Wait for graph with many nodes (Enron has lots of connections)
        page.wait_for_selector("#graph-svg .g-node", timeout=8000)
        initial_node_count = page.locator("#graph-svg .g-node").count()
        assert initial_node_count > 5

        # Timeline entity label should reference Enron Corp
        expect(page.locator("#tl-entity-name")).to_contain_text("Enron Corp")

        browser.close()
