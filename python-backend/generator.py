import os
import json
from groq import Groq


class MarkdownSpecGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set in environment variables.")
        self.client = Groq(api_key=api_key)
        # Use a currently available Groq model (check Groq console if this changes)
        # See: https://console.groq.com/docs/text-chat
        self.model_name = "openai/gpt-oss-120b"

    def generate_all_documents(self, target_url, telemetry, copy_corpus):
        os.makedirs("outputs", exist_ok=True)

        combined_payload = {
            "target_url": target_url,
            "current_system_calendar_year": "2026",
            "current_system_date_full": "July 1, 2026",
            "architecture_telemetry": telemetry,
            "extracted_content_samples": copy_corpus,
        }

        payload_str = json.dumps(combined_payload, indent=2)

        failures = []

        # STRUCTURE.MD
        print("[AI Generator] Compiling structure.md...")
        ok = self._write_doc(
            filename="outputs/structure.md",
            system_instruction=(
                "You are an Elite Enterprise Solutions Architect. Analyze the provided payload and compile a highly rigorous structure.md engineering spec.\n\n"
                "CRITICAL CORRECTION MATRIX RULES:\n"
                "1. STRICEST BOUNDARY SEPARATION: You must explicitly label every entry with one of three vocabulary markers: [Confirmed], [Inferred], or [Not Verified]. No blending fact and assumption.\n"
                "2. INTRODUCTORY DISCLAIMER: Begin the document with an explicit architectural note stating: "
                "'This structural architecture is derived purely from client-side rendered behavior and visible page content footprint telemetry; it is not compiled from back-end server codebase inspections.'\n"
                "3. ROUTES ENGINE: Group the mapped routes into a clear breakdown of Confirmed Pages vs Inferred Pages. For instance, if a target route link exists in the HTML footer or menu structure (like /terms) but has empty text/telemetry context data in the payload, explicitly flag it as [Not Verified - Stubbed Link].\n"
                "4. FORM MECHANISMS: If form actions or methods return null or empty spaces, do NOT guess. Print exactly 'Not confirmed from telemetry' and explicitly state that the submission behavior could not be determined from client-side traces.\n"
                "5. FRAMEWORK FOOTPRINTS: Frame assertions like tech stack markers strictly as: "
                "'Next.js/React Asset Traces observed in layout metadata strings, implying a high probability of this stack profile, but unverified at a source-code level.'"
            ),
            prompt=(
                "Build an uncompromisingly accurate structure.md engineering spec using this trace data:\n\n"
                f"{payload_str}"
            ),
        )
        if not ok:
            failures.append("structure.md")

        # DESIGN.MD
        print("[AI Generator] Compiling design.md...")
        ok = self._write_doc(
            filename="outputs/design.md",
            system_instruction=(
                "You are a Senior Design Systems Engineer. Process the real-time computed runtime variables to compile design.md.\n\n"
                "CRITICAL CORRECTION MATRIX RULES:\n"
                "1. DATE SYNCHRONIZATION: The metadata 'Last Updated' date MUST match the current time context exactly: July 1, 2026. Absolutely no future placeholders or generic months allowed.\n"
                "2. STRICT STYLING LABELS: Rename the styles section to explicitly separate reality from inference using these exact terms:\n"
                "   - Use '[Observed in Live Rendering]' for layout font strings, colors, background properties, and elements present in the active DOM.\n"
                "   - Use '[Inferred from Rendered Output]' for structural rules like bento-grid assumptions, modularity configurations, framework styles, or components.\n"
                "3. ACCURATE LAYOUT DENSITY: Do not default to calling a site 'media-rich'. Read the media_density property per URL.\n"
                "   - If it states 'Text-dominant with minimal blocks', explicitly document that the page layout relies on typography hierarchies and clean functional blocks over images or illustrations.\n"
                "   - Only use the phrase 'Illustrated / Media-rich' when the media_density property for that URL exactly states 'Illustrated / Media-rich'. Do not invent or soften this classification.\n"
                "4. NAVIGATION REALISM: Do not state that elements like headers are 'fixed or sticky' unless explicitly verified by computed layout tracking data; label such descriptions as '[Inferred from Rendered Output]'. "
                "Document the 'Back Navigation' buttons precisely based on the detected subpage traces, noting if a subpage link's body contents were not fetched.\n"
                "5. NON-SPECULATIVE LANGUAGE: Avoid verbs like 'appears', 'likely', or 'probably' when describing directly observed styles. Reserve '[Inferred from Rendered Output]' sections for any necessary cautious wording, and clearly mark them as such."
            ),
            prompt=(
                "Build a precision design.md UI system tracking file using this trace data:\n\n"
                f"{payload_str}"
            ),
        )
        if not ok:
            failures.append("design.md")

        # USECASE.MD
        print("[AI Generator] Compiling usecase.md...")
        ok = self._write_doc(
            filename="outputs/usecase.md",
            system_instruction=(
                "You are a Senior Product Management Director. Your objective is to formulate a high-fidelity usecase.md document. "
                "DO NOT repeat technology stacks, routing grids, component abstractions, or coding details from structure.md.\n\n"
                "CRITICAL CORRECTION MATRIX RULES:\n"
                "1. ZERO PROMOTIONAL FLUFF: Strip away all marketing, promotional, and corporate hyping language from the opening section. "
                "State the product's mission and objective in clean, highly objective, standard enterprise prose.\n"
                "2. STRICT PAGE SCOPE: You MUST restrict all scenarios and references to the pages explicitly confirmed in the telemetry:\n"
                "   - Home page: '/'\n"
                "   - Future Plans page: '/future-plans'\n"
                "   - Privacy Policy page: '/privacy'\n"
                "   - Terms of Use page: '/terms'\n"
                "   Do NOT invent any additional pages (e.g., 'Services' page, 'Dashboard', 'Admin console').\n"
                "3. PERSONA MATRIX RULES: Build the 'User Persona Matrix & Scenarios' table using exactly these columns:\n"
                "   | Persona | Goal | Entry Point | Pages Used | Action Taken |\n"
                "   | --- | --- | --- | --- | --- |\n"
                "   Each row MUST:\n"
                "   - Reference only the confirmed URLs ('/', '/future-plans', '/privacy', '/terms').\n"
                "   - Describe a short, realistic scenario grounded in the extracted content (e.g., 'Get In Touch', 'The Road to 2030', privacy/terms review).\n"
                "   - Use single-sentence, concise cells (no multi-paragraph cells, no very long explanations).\n"
                "   The table MUST have at least three fully populated rows.\n"
                "4. TELEMETRY-GROUNDED SCENARIOS ONLY: Every scenario you describe must be directly supported by phrases or concepts present in the extracted content samples, such as:\n"
                "   - 'Precision Crop Logistics'\n"
                "   - 'Soil & Science Consulting'\n"
                "   - 'Agro-Tech Integration'\n"
                "   - 'The Road to 2030'\n"
                "   - 'Phase 01 IoT Expansion'\n"
                "   - 'Phase 02 AI Analytics'\n"
                "   - 'Phase 03 National Logistics'\n"
                "   Do NOT introduce new product names, modules, pages, or capabilities beyond these.\n"
                "5. REVENUE MONETIZATION LOGIC: Clearly label all monetization flow models, billing setups, and financial streams as "
                "'[Business Model Inference/Economic Hypotheses]'. Do not mention prices, fees, or exact contract structures; describe only general patterns inferred from the visible services. "
                "Keep this section concise and explicitly marked as inference.\n"
                "6. RISK & METRICS SCOPE: If you include success metrics or risks, they must logically follow from the observed content and remain generic (no fabricated numeric targets that are not implied by the text). "
                "Avoid generic consulting boilerplate; keep it tethered to the visible phases and services.\n"
                "7. TABLE COMPLETENESS & VALIDITY: Do not stop after writing only the header row. Ensure the markdown table includes the header, exactly one separator row "
                "('| --- | --- | --- | --- | --- |'), and at least three body rows with proper closing pipe delimiters so the table renders correctly."
            ),
            prompt=(
                "Build a professional product management usecase.md utilizing this text payload. "
                "Focus on real user interactions with the confirmed pages ('/', '/future-plans', '/privacy', '/terms'), "
                "the observed contact form, and the roadmap phases. "
                "Do not invent new pages or product modules.\n\n"
                f"{payload_str}"
            ),
        )
        if not ok:
            failures.append("usecase.md")

        return failures

    def _write_doc(self, filename, system_instruction, prompt):
        """
        Calls Groq chat completions API and writes the response to filename.
        Returns True on success, False on failure.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_instruction,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.1,
            )
            text = completion.choices[0].message.content
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            return True
        except Exception as e:
            print(f"[Generation Error] Failed on writing target artifact {filename}: {e}")
            return False
        
    # generator.py (add this new method next to generate_all_documents)

    async def generate_documents_in_memory(self, target_url, telemetry, copy_corpus):
        """
        Generates structure.md, design.md, usecase.md and returns them
        as a dict of strings instead of writing to disk.
        """
        combined_payload = {
            "target_url": target_url,
            "current_system_calendar_year": "2026",
            "current_system_date_full": "July 1, 2026",
            "architecture_telemetry": telemetry,
            "extracted_content_samples": copy_corpus,
        }

        payload_str = json.dumps(combined_payload, indent=2)

        results = {
            "structure_md": None,
            "design_md": None,
            "usecase_md": None,
        }

        # STRUCTURE.MD
        print("[AI Generator] Compiling structure.md (memory)...")
        results["structure_md"] = self._generate_text(
            system_instruction=(
                "You are an Elite Enterprise Solutions Architect. Analyze the provided payload and compile a highly rigorous structure.md engineering spec.\n\n"
                "CRITICAL CORRECTION MATRIX RULES:\n"
                "1. STRICEST BOUNDARY SEPARATION: You must explicitly label every entry with one of three vocabulary markers: [Confirmed], [Inferred], or [Not Verified]. No blending fact and assumption.\n"
                "2. INTRODUCTORY DISCLAIMER: Begin the document with an explicit architectural note stating: "
                "'This structural architecture is derived purely from client-side rendered behavior and visible page content footprint telemetry; it is not compiled from back-end server codebase inspections.'\n"
                "3. ROUTES ENGINE: Group the mapped routes into a clear breakdown of Confirmed Pages vs Inferred Pages. For instance, if a target route link exists in the HTML footer or menu structure (like /terms) but has empty text/telemetry context data in the payload, explicitly flag it as [Not Verified - Stubbed Link].\n"
                "4. FORM MECHANISMS: If form actions or methods return null or empty spaces, do NOT guess. Print exactly 'Not confirmed from telemetry' and explicitly state that the submission behavior could not be determined from client-side traces.\n"
                "5. FRAMEWORK FOOTPRINTS: Frame assertions like tech stack markers strictly as: "
                "'Next.js/React Asset Traces observed in layout metadata strings, implying a high probability of this stack profile, but unverified at a source-code level.'"
            ),
            prompt=(
                "Build an uncompromisingly accurate structure.md engineering spec using this trace data:\n\n"
                f"{payload_str}"
            ),
        )

        # DESIGN.MD
        print("[AI Generator] Compiling design.md (memory)...")
        results["design_md"] = self._generate_text(
            system_instruction=(
                "You are a Senior Design Systems Engineer. Process the real-time computed runtime variables to compile design.md.\n\n"
                "CRITICAL CORRECTION MATRIX RULES:\n"
                "1. DATE SYNCHRONIZATION: The metadata 'Last Updated' date MUST match the current time context exactly: July 1, 2026. Absolutely no future placeholders or generic months allowed.\n"
                "2. STRICT STYLING LABELS: Rename the styles section to explicitly separate reality from inference using these exact terms:\n"
                "   - Use '[Observed in Live Rendering]' for layout font strings, colors, background properties, and elements present in the active DOM.\n"
                "   - Use '[Inferred from Rendered Output]' for structural rules like bento-grid assumptions, modularity configurations, framework styles, or components.\n"
                "3. ACCURATE LAYOUT DENSITY: Do not default to calling a site 'media-rich'. Read the media_density property per URL.\n"
                "   - If it states 'Text-dominant with minimal blocks', explicitly document that the page layout relies on typography hierarchies and clean functional blocks over images or illustrations.\n"
                "   - Only use the phrase 'Illustrated / Media-rich' when the media_density property for that URL exactly states 'Illustrated / Media-rich'. Do not invent or soften this classification.\n"
                "4. NAVIGATION REALISM: Do not state that elements like headers are 'fixed or sticky' unless explicitly verified by computed layout tracking data; label such descriptions as '[Inferred from Rendered Output]'. "
                "Document the 'Back Navigation' buttons precisely based on the detected subpage traces, noting if a subpage link's body contents were not fetched.\n"
                "5. NON-SPECULATIVE LANGUAGE: Avoid verbs like 'appears', 'likely', or 'probably' when describing directly observed styles. Reserve '[Inferred from Rendered Output]' sections for any necessary cautious wording, and clearly mark them as such."
            ),
            prompt=(
                "Build a precision design.md UI system tracking file using this trace data:\n\n"
                f"{payload_str}"
            ),
        )

        # USECASE.MD
        print("[AI Generator] Compiling usecase.md (memory)...")
        results["usecase_md"] = self._generate_text(
            system_instruction=(
                "You are a Senior Product Management Director. Your objective is to formulate a high-fidelity usecase.md document. "
                "DO NOT repeat technology stacks, routing grids, component abstractions, or coding details from structure.md.\n\n"
                "CRITICAL CORRECTION MATRIX RULES:\n"
                "1. ZERO PROMOTIONAL FLUFF: Strip away all marketing, promotional, and corporate hyping language from the opening section. "
                "State the product's mission and objective in clean, highly objective, standard enterprise prose.\n"
                "2. STRICT PAGE SCOPE: You MUST restrict all scenarios and references to the pages explicitly confirmed in the telemetry:\n"
                "   - Home page: '/'\n"
                "   - Future Plans page: '/future-plans'\n"
                "   - Privacy Policy page: '/privacy'\n"
                "   - Terms of Use page: '/terms'\n"
                "   Do NOT invent any additional pages.\n"
                "3. PERSONA MATRIX RULES: Build the 'User Persona Matrix & Scenarios' table using exactly these columns:\n"
                "   | Persona | Goal | Entry Point | Pages Used | Action Taken |\n"
                "   | --- | --- | --- | --- | --- |\n"
                "   Each row MUST:\n"
                "   - Reference only the confirmed URLs ('/', '/future-plans', '/privacy', '/terms').\n"
                "   - Describe a short, realistic scenario grounded in the extracted content.\n"
                "   - Use single-sentence, concise cells.\n"
                "   The table MUST have at least three fully populated rows.\n"
                "4. TELEMETRY-GROUNDED SCENARIOS ONLY: Every scenario must be directly supported by phrases or concepts present in the extracted content samples.\n"
                "5. REVENUE MONETIZATION LOGIC: Clearly label all monetization flow models as "
                "'[Business Model Inference/Economic Hypotheses]'. Keep this section concise.\n"
                "6. TABLE COMPLETENESS & VALIDITY: Ensure the markdown table includes the header, exactly one separator row "
                "('| --- | --- | --- | --- | --- |'), and at least three body rows."
            ),
            prompt=(
                "Build a professional product management usecase.md utilizing this text payload. "
                "Focus on real user interactions with the confirmed pages ('/', '/future-plans', '/privacy', '/terms'), "
                "the observed contact form, and the roadmap phases. "
                "Do not invent new pages or product modules.\n\n"
                f"{payload_str}"
            ),
        )

        return results

    def _generate_text(self, system_instruction, prompt):
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"[Generation Error] Failed in _generate_text: {e}")
            return ""