from bs4 import BeautifulSoup
import re


class ContentExtractor:
    @staticmethod
    def extract_copy_block(pages_data):
        corpus_data = {
            "corporate_signatures": set(),
            "social_footprints": set(),
            "semantic_body_text": "",
        }

        social_domains = [
            "twitter.com",
            "linkedin.com",
            "github.com",
            "facebook.com",
            "instagram.com",
        ]
        text_accumulator = []

        # Ensure deterministic ordering
        for url in sorted(pages_data.keys()):
            data = pages_data[url]
            soup = BeautifulSoup(data["html"], "lxml")

            for clean_target in soup(["script", "style", "svg", "path", "noscript"]):
                clean_target.decompose()

            text_content = soup.get_text(separator=" ", strip=True)
            if len(text_content) > 100:
                text_accumulator.append(
                    f"--- Content Map from {url} ---\n{text_content[:3500]}"
                )

            for a in soup.find_all("a", href=True):
                href = a["href"]
                if any(domain in href for domain in social_domains):
                    corpus_data["social_footprints"].add(href)

            footer_text = soup.find("footer").get_text() if soup.find("footer") else text_content
            cr_match = re.search(r"©\s*(?:\d{4}-)?\d{4}\s*([^.\n|•]+)", footer_text)
            if cr_match:
                corpus_data["corporate_signatures"].add(cr_match.group(1).strip())

        corpus_data["corporate_signatures"] = list(corpus_data["corporate_signatures"])
        corpus_data["social_footprints"] = list(corpus_data["social_footprints"])
        corpus_data["semantic_body_text"] = "\n\n".join(text_accumulator)

        return corpus_data