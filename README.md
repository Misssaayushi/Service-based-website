# ImpactOutdoors - Outdoor Advertising Agency Website

A modern, clean, and professional 5-page service website built for an outdoor advertising agency. 

## 🌟 Features

*   **5-Page Structure:** Home, About, Services, Portfolio, and Contact pages.
*   **Modern Design:** Built with a premium `#800180` (purple) theme, subtle gradients, and soft shadows.
*   **Light/Dark Mode Toggle:** User preference is saved to `localStorage` and automatically defaults to system settings.
*   **Scroll Animations:** Smooth component reveal animations powered by Vanilla JS `IntersectionObserver`.
*   **Fully Responsive:** Fluid layouts built with Flexbox and CSS Grid, equipped with a mobile-friendly hamburger menu.
*   **Zero Dependencies:** Built entirely with Vanilla HTML, CSS, and JavaScript. No bulky frameworks required.

## 📁 Project Structure

```text
/
├── css/
│   └── style.css       # Global styles, variables, dark mode, utilities
├── js/
│   └── main.js         # Mobile menu toggle, dark mode logic, observer animations
├── images/             # Generated placeholder images (billboards, transit wraps)
├── index.html          # Homepage
├── about.html          # Company mission and story
├── services.html       # Detailed service breakdowns
├── portfolio.html      # Image gallery of past campaigns
└── contact.html        # Interactive contact form and details
```

## 🚀 How to Run

Since this is a static site without any build tools, you can run it immediately in your browser:

1.  **Direct Open:** Simply double-click `index.html` to open it in your default web browser.
2.  **Local Server (Recommended for precise testing):** If you have Python installed, open your terminal in the project directory and run:
    ```bash
    python -m http.server 8000
    ```
    Then visit `http://localhost:8000` in your browser.
3.  **VS Code:** Install the "Live Server" extension, right-click `index.html`, and select "Open with Live Server".

## 🎨 Design Tokens

- **Primary Color:** `#800180` (Purple)
- **Primary Fonts:** 
  - `Outfit` (Headings)
  - `Inter` (Body Text)
- **Icons:** Phosphor Icons (loaded via CDN)
