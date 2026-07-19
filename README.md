# Australia Political Governance Map 2025

🌏 **Live Site:** [https://anacondy.github.io/3--Aussie-Political-MAP/](https://anacondy.github.io/3--Aussie-Political-MAP/)

## Overview

An interactive, responsive map visualization of Australian political governance showing legislative control and seat distribution across all states and territories as of November 2025. Built with Leaflet.js and optimized for both desktop and mobile devices.

## Features

### 🗺️ Interactive Map
- Click on any state or territory to view detailed political information
- Hover tooltips showing state names
- Color-coded visualization:
  - **Red**: Labor-controlled states
  - **Blue**: Coalition/Liberal-controlled states
- Smooth animations and transitions
- Touch-optimized for mobile devices

### 📊 Political Data (November 2025)
Displays comprehensive information for each state/territory:
- Premier/Chief Minister name
- Governing party
- Government status (Majority/Minority/Coalition)
- Legislative assembly seat breakdown
- Opposition seats
- Crossbench/Other seats
- Total seats in parliament

### 📱 Mobile Optimization
- Fully responsive design for all screen sizes
- Optimized for 16:9 and 20:9 aspect ratio devices
- Touch-friendly interface with appropriate touch targets
- Adaptive layouts for portrait and landscape orientations
- Mobile-specific UI adjustments (close buttons, stacked layouts)
- Performance optimized with lazy loading and debounced events

### 💻 Desktop Experience
- Large, detailed sidebar with comprehensive data
- Glass-morphism UI design
- Smooth hover effects and interactions
- High-resolution display support

## Technical Details

### Performance Optimizations
- Preconnected to CDN resources for faster loading
- Font display swap for immediate text rendering
- Debounced resize handlers
- CSS hardware acceleration with `backdrop-filter`
- Minimal DOM manipulation
- Efficient event handling

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile, Samsung Internet)
- Progressive enhancement approach
- Touch event support for mobile devices

### Responsive Breakpoints
- **Mobile**: ≤768px
  - Compact header and full-width sidebar
  - Optimized font sizes and spacing
  - Touch-optimized controls
- **Tablet**: 769px - 1024px
  - Medium-sized components
  - Balanced layout
- **Desktop**: >1024px
  - Full-featured interface
  - Maximum information density

## Data Sources

Political data reflects the state of Australian governance as of November 2025:
- Western Australia 2025 Election results
- Queensland 2024 Election results
- Northern Territory 2024 Election results
- Australian Capital Territory 2024 Election results
- Current standings for other states

## Development

### Quick Start
1. Clone the repository
2. Open `index.html` in a web browser
3. No build process required - pure HTML/CSS/JS

### Local Development
```bash
# Simple HTTP server
python3 -m http.server 8000

# Or using Node.js
npx http-server
```

Then navigate to `http://localhost:8000`

### File Structure
```
3--Aussie-Political-MAP/
├── index.html          # Main application (single-file)
├── README.md           # Documentation
├── LICENSE             # MIT License
└── .nojekyll          # GitHub Pages configuration
```

## Testing

The interface is **designed and validated for** the following environments. (Automated
checks are provided by the CI workflow; manual device testing should be re-run after any
UI change.)

- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Mobile devices (16:9 and 20:9 aspect ratios)
- Tablets (portrait and landscape)
- Touch and mouse interactions
- High DPI / Retina displays

> Note: the previous agent's README claimed extensive on-device testing that was not
> evidenced. These claims have been removed to avoid overstating verification.

## Screenshots

> Screenshots are intentionally omitted from the repository. The previous agent
> attached binary screenshots (GitHub user-attachment links) directly into the
> docs/commits as "progress"; those references have been removed as clutter.
> To capture a fresh screenshot, run the site locally (see Development) and
> use your browser/device's native capture.

## Deployment

This site is a static, single-file app deployed with **GitHub Pages**. A CI workflow
(`.github/workflows/ci.yml`) validates the HTML and JavaScript on every push and pull
request.

> ⚠️ **Deployment misconfiguration (action required by repo owner):** GitHub Pages is
> currently set to build from the stale feature branch `copilot/optimize-ui-for-mobile`,
> **not** `main`. Until this is changed in *Settings → Pages*, merges to `main` will not
> appear on the live site. See `ANALYSIS.md` (§8) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Repository

GitHub: [https://github.com/anacondy/3--Aussie-Political-MAP](https://github.com/anacondy/3--Aussie-Political-MAP)

## Contributing

Feel free to submit issues or pull requests for improvements or data updates.

---

**Last Updated:** November 2025  
**Version:** 2.0 - Mobile Optimized