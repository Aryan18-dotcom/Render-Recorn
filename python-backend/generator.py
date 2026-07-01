import os
import json
from groq import Groq


class MarkdownSpecGenerator:
    def __init__(self):
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise RuntimeError("GROQ_API_KEY is not set in environment variables.")

            self.client = Groq(api_key=api_key)
            # Use a currently available Groq model (check Groq console if this changes)
            # See: https://console.groq.com/docs/text-chat
            groq_model = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")
            self.model_name = groq_model

            print("[Generator] Initialized Groq client and model successfully.")
        except Exception as e:
            # This will show up in Render logs
            print(f"[Generator] Initialization error: {e}")
            # Re-raise so FastAPI can catch and convert to HTTP error
            raise

    def generate_all_documents(self, target_url, telemetry, copy_corpus):
        """
        Legacy disk-based generator. You probably don't use this on Render anymore,
        but we keep it defensive.
        """
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
                "3. ROUTES ENGINE: Group the mapped routes into a clear breakdown of Confirmed Pages vs Inferred Pages.\n"
                "4. FORM MECHANISMS: If form actions or methods return null or empty spaces, do NOT guess.\n"
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
                "1. DATE SYNCHRONIZATION: The metadata 'Last Updated' date MUST match the current time context exactly: July 1, 2026.\n"
                "2. STRICT STYLING LABELS: Rename the styles section to explicitly separate reality from inference.\n"
                "3. ACCURATE LAYOUT DENSITY: Do not default to calling a site 'media-rich'.\n"
                "4. NAVIGATION REALISM: Do not state that elements like headers are 'fixed or sticky' unless explicitly verified.\n"
                "5. NON-SPECULATIVE LANGUAGE: Avoid verbs like 'appears', 'likely', or 'probably' when describing directly observed styles."
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
                "1. ZERO PROMOTIONAL FLUFF.\n"
                "2. STRICT PAGE SCOPE.\n"
                "3. PERSONA MATRIX RULES.\n"
                "4. TELEMETRY-GROUNDED SCENARIOS ONLY.\n"
                "5. REVENUE MONETIZATION LOGIC.\n"
                "6. RISK & METRICS SCOPE.\n"
                "7. TABLE COMPLETENESS & VALIDITY."
            ),
            prompt=(
                "Build a professional product management usecase.md utilizing this text payload.\n\n"
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
            # Detailed logging for Render
            print(f"[Generation Error] Failed on writing target artifact {filename}: {e}")
            return False

    async def generate_documents_in_memory(self, target_url, telemetry, copy_corpus):
        """
        Generates structure.md, design.md, usecase.md and returns them
        as a dict of strings instead of writing to disk.
        Raises RuntimeError with a descriptive message if generation fails.
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
                "..."
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
                "..."
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
                "You are a Senior Product Management Director. Your objective is to formulate a high-fidelity usecase.md document.\n\n"
                "..."
            ),
            prompt=(
                "Build a professional product management usecase.md utilizing this text payload.\n\n"
                f"{payload_str}"
            ),
        )

        # Validate outputs; if missing, raise with clear message
        missing = [k for k, v in results.items() if not v]
        if missing:
            msg = f"AI generation returned empty outputs for: {', '.join(missing)}"
            print(f"[AI Generator] {msg}")
            raise RuntimeError(msg)

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
            # Return empty string so caller can detect failure
            return ""