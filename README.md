# Australia Political Governance Map 2025

🌏 **Live Site:** [https://anacondy.github.io/3--Aussie-Political-MAP/](https://anacondy.github.io/3--Aussie-Political-MAP/)

## Overview

An interactive, responsive map visualization of Australian political governance showing legislative control and seat distribution across all states and territories as of November 2025. Built with Leaflet.js and optimized for both desktop and mobile devices.

![Desktop View](https://github.com/user-attachments/assets/13fd00cb-cf5e-4b15-8e75-333533ecaf06)

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

The site has been tested on:
- ✅ Desktop browsers (1920x1080, 2560x1440, 4K displays)
- ✅ Mobile devices (16:9 and 20:9 aspect ratios)
- ✅ Tablets (iPad, Android tablets)
- ✅ Various orientations (portrait and landscape)
- ✅ Touch and mouse interactions
- ✅ High DPI/Retina displays

## Screenshots

### Desktop View
The full desktop experience with glass-morphism design and comprehensive data display.

### Mobile View
Optimized mobile interface with full-screen sidebar and touch-friendly controls.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Repository

GitHub: [https://github.com/anacondy/3--Aussie-Political-MAP](https://github.com/anacondy/3--Aussie-Political-MAP)

## Contributing

Feel free to submit issues or pull requests for improvements or data updates.

---

**Last Updated:** November 2025  
**Version:** 2.0 - Mobile Optimized