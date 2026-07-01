from urllib.parse import urlparse, urljoin
from playwright.async_api import async_playwright


class WebCrawler:
    def __init__(self, start_url, max_pages=6):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.urls_to_visit = [start_url]
        self.domain = urlparse(start_url).netloc

    def is_same_domain(self, url):
        return urlparse(url).netloc == self.domain

    async def crawl(self):
        pages_data = {}
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1440, "height": 900},
            )
            page = await context.new_page()

            while self.urls_to_visit and len(self.visited_urls) < self.max_pages:
                current_url = self.urls_to_visit.pop(0)
                if current_url in self.visited_urls:
                    continue

                print(f"[Crawler] Parsing Path: {current_url}")
                try:
                    await page.goto(
                        current_url, wait_until="domcontentloaded", timeout=15000
                    )
                    await page.wait_for_timeout(2500)

                    html = await page.content()

                    # Core Telemetry Extraction: direct facts from the browser window
                    telemetry_data = await page.evaluate(
                        """() => {
                        const allElems = Array.from(document.querySelectorAll('*'));
                        const rawImages = Array.from(document.querySelectorAll('img, svg, picture'));
                        const images = rawImages.filter(img => {
                            const style = window.getComputedStyle(img);
                            const rect = img.getBoundingClientRect();
                            return style.display !== 'none' &&
                                   style.visibility !== 'hidden' &&
                                   rect.width > 0 &&
                                   rect.height > 0;
                        });
                        const backElements = Array.from(document.querySelectorAll('a, button'))
                            .filter(e => /back|←/i.test(e.innerText || ''));

                        const bgColors = allElems
                            .map(e => window.getComputedStyle(e).backgroundColor)
                            .filter(c => c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent');
                        const textColors = allElems.map(e => window.getComputedStyle(e).color);
                        const fonts = allElems.map(e => window.getComputedStyle(e).fontFamily);

                        return {
                            has_images_or_icons: images.length > 0,
                            media_count: images.length,
                            visual_density_type: images.length < 3
                                ? "Text-dominant with minimal blocks"
                                : "Illustrated / Media-rich",
                            detected_back_ui: backElements.map(e => ({
                                text: (e.innerText || '').trim(),
                                element: e.tagName.toLowerCase()
                            })),
                            computed_styles: {
                                active_backgrounds: Array.from(new Set(bgColors)).slice(0, 8),
                                active_text_colors: Array.from(new Set(textColors)).slice(0, 8),
                                active_fonts: Array.from(new Set(fonts)).slice(0, 4)
                            }
                        };
                    }"""
                    )

                    self.visited_urls.add(current_url)

                    hrefs = await page.eval_on_selector_all(
                        "a", "elements => elements.map(e => e.href)"
                    )
                    for href in hrefs:
                        clean_url = urljoin(current_url, href).split("#")[0].rstrip("/")
                        if (
                            self.is_same_domain(clean_url)
                            and clean_url not in self.visited_urls
                        ):
                            if clean_url not in self.urls_to_visit:
                                self.urls_to_visit.append(clean_url)

                    pages_data[current_url] = {
                        "html": html,
                        "telemetry": telemetry_data,
                    }
                except Exception as e:
                    print(f"[Error] Skipping route target {current_url}: {e}")

            await context.close()
            await browser.close()

        return pages_data