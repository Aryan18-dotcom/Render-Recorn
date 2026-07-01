from bs4 import BeautifulSoup


class WebParser:
    @staticmethod
    def extract_telemetry(pages_data):
        telemetry = {
            "mapped_urls": list(pages_data.keys()),
            "detected_framework_footprints": set(),
            "interactive_forms": [],
            "visual_layout_telemetry": {
                "fonts": set(),
                "backgrounds": set(),
                "colors": set(),
                "media_density": {},
            },
            "back_navigation_patterns": [],
        }

        for url, data in pages_data.items():
            soup = BeautifulSoup(data["html"], "lxml")
            raw_text = str(soup).lower()

            # Map visual runtime data gathered via window elements
            telemetry["visual_layout_telemetry"]["fonts"].update(
                data["telemetry"]["computed_styles"]["active_fonts"]
            )
            telemetry["visual_layout_telemetry"]["backgrounds"].update(
                data["telemetry"]["computed_styles"]["active_backgrounds"]
            )
            telemetry["visual_layout_telemetry"]["colors"].update(
                data["telemetry"]["computed_styles"]["active_text_colors"]
            )
            telemetry["visual_layout_telemetry"]["media_density"][url] = data[
                "telemetry"
            ]["visual_density_type"]

            if data["telemetry"]["detected_back_ui"]:
                telemetry["back_navigation_patterns"].append(
                    {"url": url, "elements": data["telemetry"]["detected_back_ui"]}
                )

            # Record explicit structural indicators
            if "_next/static" in raw_text or "next" in raw_text:
                telemetry["detected_framework_footprints"].add("Next.js Asset Traces")
            if "tailwind" in raw_text:
                telemetry["detected_framework_footprints"].add(
                    "Tailwind CSS Class Traces"
                )
            if "wp-content" in raw_text:
                telemetry["detected_framework_footprints"].add(
                    "WordPress Asset Traces"
                )

            # Extract detailed form requirements
            for form in soup.find_all("form"):
                form_fields = []
                for inp in form.find_all(["input", "textarea", "select", "button"]):
                    form_fields.append(
                        {
                            "identifier": inp.get("name")
                            or inp.get("type")
                            or inp.name,
                            "tag_type": inp.name,
                            "is_required": inp.has_attr("required"),
                            "placeholder": inp.get("placeholder", ""),
                        }
                    )

                telemetry["interactive_forms"].append(
                    {
                        "location_url": url,
                        "explicit_action": form.get("action"),
                        "explicit_method": form.get("method"),
                        "fields": form_fields,
                    }
                )

        telemetry["detected_framework_footprints"] = [
            f for f in telemetry["detected_framework_footprints"] if f.strip()
        ]
        telemetry["visual_layout_telemetry"]["fonts"] = list(
            telemetry["visual_layout_telemetry"]["fonts"]
        )
        telemetry["visual_layout_telemetry"]["backgrounds"] = list(
            telemetry["visual_layout_telemetry"]["backgrounds"]
        )[:8]
        telemetry["visual_layout_telemetry"]["colors"] = list(
            telemetry["visual_layout_telemetry"]["colors"]
        )[:8]

        return telemetry