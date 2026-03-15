# Figma — Collaborative Design, Prototyping & Developer Handoff

Figma is the leading browser-based design tool for UI/UX design, prototyping, and design systems. Its real-time collaboration features make it the industry standard for product teams, enabling designers, developers, and stakeholders to work together in the same file simultaneously.

---

## Table of Contents
1. [What is Figma?](#1-what-is-figma)
2. [Core Features](#2-core-features)
3. [Dev Mode](#3-dev-mode)
4. [Prototyping](#4-prototyping)
5. [Plugins & Community](#5-plugins--community)
6. [Figma-to-Code Workflows](#6-figma-to-code-workflows)
7. [Pricing](#7-pricing)

---

## 1. What is Figma?

### Overview

Figma is a browser-based vector design tool built for collaborative interface design. Unlike traditional design tools that run as desktop applications with local files, Figma operates entirely in the cloud with real-time multiplayer editing.

- **Website:** https://www.figma.com
- **Platform:** Browser (Chrome, Firefox, Safari, Edge), desktop app (Windows, macOS)
- **History:** Founded in 2012, launched publicly in 2016. Adobe announced an acquisition in 2022 for $20 billion, but the deal was terminated in 2023 due to regulatory concerns. Figma remains independent.

### Core Use Cases

- **UI/UX design** — design interfaces for web, mobile, and desktop applications
- **Prototyping** — create interactive prototypes with transitions and animations
- **Design systems** — build and maintain component libraries with variants and tokens
- **Whiteboarding** — brainstorm and diagram with FigJam
- **Developer handoff** — inspect designs, extract code snippets, and measure spacing

---

## 2. Core Features

### Vector Editing & Layout

- **Vector networks** — edit individual points and paths, boolean operations (union, subtract, intersect, exclude)
- **Auto layout** — responsive frames that resize based on content (similar to CSS flexbox)
- **Constraints** — pin elements to edges or centers for responsive behavior
- **Grids and guides** — layout grids (columns, rows, custom) for alignment

### Components & Variants

```
┌─────────────────────────────────────────┐
│  Main Component (source of truth)       │
│  ┌──────────────────────────────────┐   │
│  │  Button                          │   │
│  │  Variants:                       │   │
│  │    Size: Small / Medium / Large  │   │
│  │    Style: Primary / Secondary    │   │
│  │    State: Default / Hover / ...  │   │
│  └──────────────────────────────────┘   │
│           │                             │
│     ┌─────┼─────────┐                   │
│     ▼     ▼         ▼                   │
│  Instance Instance Instance             │
│  (linked, overridable)                  │
└─────────────────────────────────────────┘
```

- **Components** — reusable design elements; edit the main component and all instances update
- **Variants** — multiple states of a component in a single component set (size, color, state)
- **Instance overrides** — customize text, fills, and nested components without detaching

### Design Tokens & Variables

- **Styles** — reusable colors, text styles, effects, and grid definitions
- **Variables** — define design tokens (colors, spacing, booleans, strings) that can be scoped to modes (light/dark theme)
- **Modes** — switch variable sets for themes (light mode, dark mode) or breakpoints

### Real-Time Collaboration

- **Multiplayer editing** — multiple users edit the same file simultaneously with live cursors
- **Comments** — leave feedback directly on the canvas, resolve threads
- **Branching** — create branches of a file for experimentation, merge back when ready
- **Version history** — view and restore any previous version of a file

### FigJam

Figma's collaborative whiteboarding tool for brainstorming, diagramming, and workshops:
- Sticky notes, shapes, connectors, stamps
- Templates for retrospectives, flowcharts, user journeys
- Voting and timer widgets for team activities

---

## 3. Dev Mode

### Overview

Dev Mode is Figma's developer-focused view that translates designs into actionable specifications. It provides code snippets, measurements, and asset exports without requiring designers to prepare handoff documents.

### Inspect Designs

- **Select any element** to see its properties: dimensions, position, padding, border radius, colors, typography
- **Spacing measurements** — hover between elements to see distances (redlines)
- **Layout details** — auto layout properties mapped to CSS flexbox equivalents

### Code Snippets

Dev Mode generates code for selected elements in multiple formats:

```css
/* CSS output for a button */
display: flex;
padding: 12px 24px;
justify-content: center;
align-items: center;
gap: 8px;
border-radius: 8px;
background: #6366F1;
color: #FFFFFF;
font-family: Inter;
font-size: 14px;
font-weight: 600;
line-height: 20px;
```

```swift
// iOS (Swift) output
let button = UIButton()
button.backgroundColor = UIColor(red: 0.39, green: 0.40, blue: 0.95, alpha: 1.0)
button.layer.cornerRadius = 8
button.titleLabel?.font = UIFont.systemFont(ofSize: 14, weight: .semibold)
```

### Handoff Workflow

| Step | Action |
|------|--------|
| 1 | Designer marks frames as "Ready for dev" |
| 2 | Developer opens file in Dev Mode |
| 3 | Inspect elements, copy code snippets |
| 4 | Export assets (SVG, PNG, PDF) at specified scales |
| 5 | Compare design changes across versions |

---

## 4. Prototyping

### Interactive Prototypes

Figma allows you to wire frames together into clickable prototypes without leaving the design tool:

- **Connections** — link any element to another frame (click, hover, drag triggers)
- **Transitions** — dissolve, move in/out, push, slide, smart animate
- **Smart Animate** — automatically animates matching layers between frames (similar to key-frame animation)
- **Overflow scrolling** — define scrollable regions within frames (vertical, horizontal, or both)

### Advanced Interactions

- **Interactive components** — define hover, press, and focus states within component variants
- **Variables in prototypes** — use boolean and string variables to create conditional logic (show/hide, text changes)
- **Video playback** — embed video within prototypes
- **Device preview** — preview prototypes on mobile devices using the Figma Mirror app (iOS, Android)

### Sharing Prototypes

```
Share → Copy prototype link → Anyone with the link can interact
Settings: "Can view" / "Can edit" / "Can view prototypes only"
```

---

## 5. Plugins & Community

### Popular Plugins

| Plugin | Purpose |
|--------|---------|
| **Iconify** | Access 150,000+ icons from popular icon sets |
| **Unsplash** | Insert free stock photos directly into designs |
| **Content Reel** | Populate designs with realistic placeholder data |
| **Figmotion** | Create animations directly within Figma |
| **Stark** | Accessibility checker (contrast, color blindness simulation) |
| **LottieFiles** | Import and preview Lottie animations |
| **Autoflow** | Draw user flow arrows between frames |

### Community Resources

- **Community hub** — browse free templates, UI kits, icon sets, and wireframe libraries
- **Explore files** — duplicate any community file into your own workspace
- **Popular kits:** Material Design 3, iOS Design Kit, Ant Design, Tailwind CSS UI Kit

### Plugin Development

Figma plugins are built with TypeScript and the Figma Plugin API:

```typescript
// Basic plugin structure
figma.showUI(__html__, { width: 300, height: 200 });

figma.ui.onmessage = (msg) => {
  if (msg.type === 'create-rectangle') {
    const rect = figma.createRectangle();
    rect.resize(100, 100);
    rect.fills = [{ type: 'SOLID', color: { r: 0.4, g: 0.4, b: 0.95 } }];
    figma.currentPage.appendChild(rect);
  }
  figma.closePlugin();
};
```

---

## 6. Figma-to-Code Workflows

### Automated Tools

| Tool | Output | Description |
|------|--------|-------------|
| **Builder.io (Visual Copilot)** | React, Vue, Svelte, Angular, HTML | AI-powered Figma to clean code; integrates with Builder.io CMS |
| **Locofy** | React, Next.js, React Native, HTML/CSS | Production-ready code with responsive support |
| **Anima** | React, Vue, HTML/CSS | Design to code with developer-friendly output |
| **TeleportHQ** | React, Vue, Angular, HTML | Visual builder with Figma import |

### Manual Export Workflow

1. **Open Dev Mode** in Figma
2. **Select elements** to inspect CSS properties
3. **Copy code snippets** (CSS, iOS, Android)
4. **Export assets** — select layers, choose format (SVG for icons, PNG for images), set export scale (1x, 2x, 3x)
5. **Extract colors and typography** from the design system styles

### Best Practices for Developer Handoff

- Use auto layout consistently (maps directly to flexbox/CSS Grid)
- Name layers descriptively (they become class names in generated code)
- Define all colors and text styles as shared styles or variables
- Mark sections as "Ready for dev" to signal completion
- Use consistent spacing values that align with your CSS spacing scale

---

## 7. Pricing

| Plan | Price | Key Features |
|------|-------|--------------|
| **Starter** | Free | 3 Figma files, 3 FigJam files, unlimited personal files, unlimited viewers |
| **Professional** | $15/editor/month | Unlimited files, shared libraries, branching, Dev Mode |
| **Organization** | $45/editor/month | Design systems analytics, SSO, private plugins, centralized admin |
| **Enterprise** | $75/editor/month | Advanced security, dedicated support, custom roles, guest access controls |

**Note:** Viewers (inspect, comment, export) are always free on all plans. Only editors who create and modify designs require paid seats.

---

## See Also

- [Editors & IDEs](editors-and-ides.md) — Code editors for implementing designs
- [Docker Essentials](docker-essentials.md) — Containerize front-end builds from Figma designs
- [APIs & Resources](../reference/apis-and-resources.md) — API keys and services for Figma integrations
