import asyncio
import os
from colorama import init, Fore
from dotenv import load_dotenv

from crawler import WebCrawler
from parser import WebParser
from extractor import ContentExtractor
from generator import MarkdownSpecGenerator


load_dotenv()
init(autoreset=True)


async def main():
    print(Fore.CYAN + "=========================================================")
    print(Fore.GREEN + "   🚀 REVERSE-ENGINEERING AGENT WORKSPACE ACTIVATED 🚀   ")
    print(Fore.CYAN + "=========================================================\n")

    if not os.getenv("GROQ_API_KEY"):
        print(Fore.RED + "[Critical Error] GROQ_API_KEY missing from system environments.")
        return

    target_url = input(Fore.YELLOW + "Enter the target web application address: ").strip()
    if not target_url:
        print(Fore.RED + "[Error] No URL provided.")
        return

    if not target_url.startswith(("http://", "https://")):
        print(Fore.RED + "[Error] Please provide a valid target schema (http:// or https://).")
        return

    print(Fore.BLUE + "\n[*] Launching browser cluster crawler to map pages...")
    crawler = WebCrawler(start_url=target_url, max_pages=6)
    pages_data = await crawler.crawl()

    if not pages_data:
        print(Fore.RED + "[Error] Failed to read resource traces or route target.")
        return

    print(Fore.BLUE + "\n[*] Processing runtime telemetry, styles, and layouts...")
    telemetry = WebParser.extract_telemetry(pages_data)

    print(Fore.BLUE + "[*] Aggregating editorial content, copywriting, and legal identities...")
    copy_corpus = ContentExtractor.extract_copy_block(pages_data)

    print(Fore.MAGENTA + "\n[*] Submitting processed data models to Gemini Core Engines...")
    generator = MarkdownSpecGenerator()
    failures = generator.generate_all_documents(target_url, telemetry, copy_corpus)

    output_path = os.path.abspath("outputs")

    if failures:
        print(
            Fore.YELLOW
            + "\n⚠️  Partial success. "
            + "The following artifacts could not be generated due to model availability or other errors:"
        )
        for name in failures:
            print(Fore.YELLOW + f"   - {name}")
        print(
            Fore.CYAN
            + f"\nAvailable artifacts are in your website-agent/outputs/ folder at: {output_path}"
        )
    else:
        print(
            Fore.GREEN
            + f"\n🎉 Success! All artifacts (structure.md, design.md, usecase.md) are ready in your website-agent/outputs/ folder at: {output_path}"
        )


if __name__ == "__main__":
    asyncio.run(main())