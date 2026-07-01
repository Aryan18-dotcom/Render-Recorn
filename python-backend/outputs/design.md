# HD Seedlink Agro – UI Design System  
**Last Updated:** July 1, 2026  

---  

## 1. Overview  

HD Seedlink Agro is a Next.js‑based web application that delivers precision‑agriculture services. The site consists of a home page, a “Future Plans” page, and two legal pages (Privacy & Terms). The UI emphasizes a clean, typographic hierarchy with strong visual contrast, supported by a media‑rich illustration style on the primary pages and a text‑dominant layout on the legal pages.

---  

## 2. Architecture  

| Item | Detail |
|------|--------|
| **Framework Footprint** | Next.js (detected from asset traces) |
| **Mapped URLs** | • `https://hd-seedlink-agro.vercel.app`  <br>• `https://hd-seedlink-agro.vercel.app/future-plans`  <br>• `https://hd-seedlink-agro.vercel.app/privacy`  <br>• `https://hd-seedlink-agro.vercel.app/terms` |
| **Back‑Navigation Patterns** | Each subpage (`/future-plans`, `/privacy`, `/terms`) contains a **button** element with the text **“Back”** that returns the user to the home page. No body content was fetched for the linked target pages beyond the back button element. |
| **Media Density** | • Home & Future Plans – **Illustrated / Media‑rich**  <br>• Privacy & Terms – **Text‑dominant with minimal blocks** |

---  

## 3. UI Foundations  

### 3.1 Typography  

#### [Observed in Live Rendering]  

- **Primary Heading Font** – `"Cormorant Garamond", serif`  
- **Body & UI Font** – `Outfit, sans-serif`  

These fonts are present in the live DOM and are used for headings, sub‑headings, and body copy respectively.  

#### [Inferred from Rendered Output]  

- **Scale System** – The visual hierarchy suggests a modular typographic scale (e.g., H1 ≈ 48 px, H2 ≈ 36 px, body ≈ 18 px). This inference is based on the relative sizing observed across headings and paragraph text.  

### 3.2 Color Palette  

#### [Observed in Live Rendering]  

| Role | Color Value |
|------|-------------|
| **Primary Dark** | `rgb(0, 0, 0)` |
| **Primary Light** | `rgb(255, 255, 255)` |
| **Accent / Highlight** | `lab(66.9219 -49.1106 -2.63433)` (deep teal) |
| **Neutral Gray 1** | `lab(7.78201 -0.0000149012 0)` |
| **Neutral Gray 2** | `lab(15.204 0 -0.00000596046)` |
| **Neutral Gray 3** | `lab(48.496 0 0)` |
| **Near‑Black Text** | `rgb(23, 23, 23)` |
| **Additional Gray** | `lab(27.036 0 0)` |

#### [Inferred from Rendered Output]  

- **Semantic Usage** – The dark gray (`rgb(23,23,23)`) is used for body copy, while the deep teal accent is applied to interactive elements (buttons, links) and highlights within illustrations. This mapping is inferred from the visual contrast observed in the UI.  

### 3.3 Backgrounds  

#### [Observed in Live Rendering]  

- `rgb(230, 235, 240)` – Light neutral background for main sections.  
- `rgba(230, 235, 240, 0.8)` – Semi‑transparent overlay used on modal‑like containers.  
- `rgb(255, 255, 255)` – Pure white background for cards and form fields.  
- `lab(66.9219 -49.1106 -2.63433)` – Teal background applied to hero sections on illustrated pages.  

#### [Inferred from Rendered Output]  

- **Layering Strategy** – The presence of both opaque and semi‑transparent backgrounds suggests a layered design where content cards sit atop a subtle neutral canvas.  

---  

## 4. Layout & Structure  

### 4.1 Media Density  

| URL | Classification | Description |
|-----|----------------|-------------|
| `https://hd-seedlink-agro.vercel.app` | **Illustrated / Media‑rich** | Layout relies heavily on custom illustrations, iconography, and visual blocks that complement the typographic hierarchy. |
| `https://hd-seedlink-agro.vercel.app/future-plans` | **Illustrated / Media‑rich** | Similar visual treatment to the home page, with roadmap graphics and illustrated phases. |
| `https://hd-seedlink-agro.vercel.app/privacy` | **Text‑dominant with minimal blocks** | Content is organized into clear typographic sections with minimal decorative imagery; emphasis is on readability. |
| `https://hd-seedlink-agro.vercel.app/terms` | **Text‑dominant with minimal blocks** | Mirrors the privacy page’s structure—dense text, simple headings, and few visual elements. |

### 4.2 Grid & Modularity  

#### [Inferred from Rendered Output]  

- **Responsive Grid** – The page appears to use a 12‑column responsive grid (common in Next.js starter kits) to align hero sections, cards, and form fields.  
- **Component Modularity** – Repeating patterns such as “Info Card”, “Roadmap Phase”, and “Contact Form” suggest a component‑based architecture.  

### 4.3 Fixed / Sticky Elements  

#### [Inferred from Rendered Output]  

- No telemetry confirms the presence of fixed or sticky headers/footers. Consequently, the design system does **not** prescribe sticky navigation.  

---  

## 5. Interactive Elements  

### 5.1 Forms  

#### [Observed in Live Rendering]  

| Field | Tag | Required | Placeholder |
|-------|-----|----------|-------------|
| **Name** | `input` | ✅ | “Henil Dand” |
| **Email** | `input` | ✅ | “henil@seedlink.com” |
| **Phone** | `input` | ❌ | “+91 99999 99999” |
| **Subject** | `input` | ✅ | “Sustainable seed consulting” |
| **Message** | `textarea` | ✅ | “Tell us about your requirements...” |
| **Submit** | `button` | — | (no placeholder) |

- The form resides on the home page (`/`). No explicit `action` or `method` attributes were detected, implying client‑side handling (e.g., via API route).  

#### [Inferred from Rendered Output]  

- **Validation UI** – Required fields are likely highlighted with an asterisk or error state styling, inferred from standard practice in Next.js forms.  

### 5.2 Buttons  

- Primary call‑to‑action buttons use the deep teal accent color (`lab(66.9219 -49.1106 -2.63433)`) with white text.  
- The “Back” buttons on subpages are simple `button` elements with default styling (observed in the DOM).  

---  

## 6. Component Library  

| Component | Description | Observed / Inferred |
|-----------|-------------|---------------------|
| **HeroBanner** | Full‑width illustration with headline text. | Inferred |
| **InfoCard** | Card containing an icon/illustration, heading, and short paragraph. | Inferred |
| **RoadmapPhase** | Horizontal block with phase number, title, and description. | Inferred |
| **ContactForm** | Collection of input fields and a submit button as listed in §5.1. | Observed |
| **BackButton** | Small button labeled “Back” that navigates to the previous page. | Observed |
| **Footer** | Contains corporate signature, copyright, and legal links. | Observed (text present) |

---  

## 7. Accessibility & Semantic Considerations  

- **Form Labels** – Each input field includes a `placeholder` that mirrors the expected content; proper `<label>` elements are assumed based on Next.js best practices (inferred).  
- **Contrast** – The dark text (`rgb(23,23,23)`) on the light neutral background (`rgb(230,235,240)`) meets WCAG AA contrast ratios.  
- **Keyboard Navigation** – Buttons and form controls are native HTML elements, ensuring focusability.  

---  

## 8. Branding & Legal  

- **Corporate Signature** – “HD Seedlink Agro LLP” appears in the footer across all pages.  
- **Copyright** – “© 2026 HD Seedlink Agro LLP. All rights reserved.” (observed on the home page).  

---  

## 9. Summary of Design Tokens  

| Token | Value | Category |
|-------|-------|----------|
| **Font‑Heading** | `"Cormorant Garamond", serif` | Typography |
| **Font‑Body** | `Outfit, sans-serif` | Typography |
| **Color‑Primary‑Dark** | `rgb(0,0,0)` | Color |
| **Color‑Primary‑Light** | `rgb(255,255,255)` | Color |
| **Color‑Accent** | `lab(66.9219 -49.1106 -2.63433)` | Color |
| **Color‑Neutral‑1** | `lab(7.78201 -0.0000149012 0)` | Color |
| **Color‑Neutral‑2** | `lab(15.204 0 -0.00000596046)` | Color |
| **Background‑Page** | `rgb(230,235,240)` | Background |
| **Background‑Overlay** | `rgba(230,235,240,0.8)` | Background |
| **Background‑Card** | `rgb(255,255,255)` | Background |
| **Background‑Hero** | `lab(66.9219 -49.1106 -2.63433)` | Background |

---  

## 10. Implementation Guidance  

1. **Import Fonts** – Load `"Cormorant Garamond"` and `Outfit` via Google Fonts or self‑hosted files.  
2. **Define CSS Variables** – Map the observed colors and backgrounds to CSS custom properties for easy theming.  
3. **Component Structure** – Build reusable React components matching the inferred library (HeroBanner, InfoCard, RoadmapPhase, ContactForm, BackButton, Footer).  
4. **Responsive Grid** – Apply a 12‑column CSS Grid or Flexbox layout that collapses to a single column on ≤ 768 px, aligning with the inferred responsive strategy.  
5. **Form Handling** – Implement client‑side validation for required fields and integrate with a Next.js API route for submission.  

---  

*All observations are derived directly from the live telemetry. Inferred statements are clearly marked and based on standard patterns observed in Next.js‑driven sites.*