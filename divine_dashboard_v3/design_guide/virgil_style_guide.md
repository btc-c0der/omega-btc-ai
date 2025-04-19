# 🔤 VIRGIL STYLE GUIDE

This document defines the foundational visual elements of the VIRGIL GRID UI design system.

## 🎨 Color Palette

### Primary Colors

| Name | Hex | RGB | Description |
|------|-----|-----|-------------|
| **"WHITE"** | `#F5F5F5` | `245, 245, 245` | Base background, not pure white; slightly off |
| **"BLACK"** | `#0F0F0F` | `15, 15, 15` | Primary text, not pure black; slightly off |
| **"GRID"** | `#5D5D5D` | `93, 93, 93` | Secondary text, borders |

### Accent Colors

| Name | Hex | RGB | Description |
|------|-----|-----|-------------|
| **"DIVINE BLUE"** | `#2B5797` | `43, 87, 151` | Primary accent, links, buttons |
| **"SACRED GOLD"** | `#FFD700` | `255, 215, 0` | Highlights, important actions |
| **"OMEGA RED"** | `#B71C1C` | `183, 28, 28` | Warnings, critical actions |
| **"QUANTUM GREEN"** | `#1E8E3E` | `30, 142, 62` | Success, positive feedback |

### Gradient

Sacred Gradient: Linear blend of DIVINE BLUE to SACRED GOLD

```css
background: linear-gradient(135deg, #2B5797 0%, #FFD700 100%);
```

## 📝 Typography

### Font Stacks

#### Primary Font: Helvetica Neue

```css
font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
```

#### Monospace Font: SF Mono

```css
font-family: "SF Mono", Monaco, Menlo, Consolas, "Courier New", monospace;
```

### Type Scale (Fibonacci-based)

| Name | Size | Line Height | Weight | Usage |
|------|------|-------------|--------|-------|
| **"DIVINE HEADING"** | `34px` | `55px` | `500` | Main page headings |
| **"GRID HEADING"** | `21px` | `34px` | `500` | Section headings |
| **"SUBHEADING"** | `18px` | `29px` | `500` | Card headings |
| **"BODY"** | `16px` | `26px` | `400` | Main text |
| **"SMALL"** | `13px` | `21px` | `400` | Secondary text, captions |
| **"TINY"** | `11px` | `18px` | `400` | Metadata, timestamps |
| **"CODE"** | `14px` | `21px` | `400` | Code, terminal outputs (monospace) |

### Text Styling

```css
/* Divine Heading */
.divine-heading {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 34px;
    line-height: 55px;
    font-weight: 500;
    letter-spacing: -0.5px;
    text-transform: uppercase;
}

/* Quotation styling */
.virgil-quote {
    position: relative;
    padding: 0 8px;
}

.virgil-quote::before {
    content: """;
    position: absolute;
    left: -5px;
}

.virgil-quote::after {
    content: """;
    position: absolute;
    right: -5px;
}
```

## 📏 Spacing System (Fibonacci-based)

| Name | Size | Usage |
|------|------|-------|
| **"SACRED UNIT"** | `8px` | Base unit for all spacing |
| **"SPACING XS"** | `8px` | Smallest spacing, tight elements |
| **"SPACING S"** | `13px` | Small spacing between related elements |
| **"SPACING M"** | `21px` | Medium spacing, standard padding |
| **"SPACING L"** | `34px` | Large spacing, section padding |
| **"SPACING XL"** | `55px` | Extra large spacing, page sections |
| **"SPACING XXL"** | `89px` | Double extra large, major page breaks |

### Margins and Padding

```css
/* Basic spacing examples */
.container {
    padding: var(--spacing-m);
    margin-bottom: var(--spacing-l);
}

.card {
    padding: var(--spacing-m);
    margin-bottom: var(--spacing-m);
    border-radius: var(--spacing-xs);
}
```

## 📦 Layout System

### Grid System

Based on a 13-column grid (Fibonacci 13)

- Standard container width: `1597px` (Fibonacci 1597)
- Column width: `89px` (Fibonacci 89)
- Gutter width: `21px` (Fibonacci 21)

```css
.grid-container {
    display: grid;
    grid-template-columns: repeat(13, 1fr);
    grid-gap: 21px;
    max-width: 1597px;
    margin: 0 auto;
    padding: 0 34px;
}

.grid-8 {
    grid-column: span 8;
}

.grid-5 {
    grid-column: span 5;
}
```

### Sacred Proportions

- Golden Ratio (1:1.618) for card dimensions
- Fibonacci sequence for layout rhythm

## 📱 Responsiveness

### Breakpoints

| Name | Size | Description |
|------|------|-------------|
| **"MOBILE"** | `< 610px` | Mobile devices |
| **"TABLET"** | `610px - 987px` | Tablets, small laptops |
| **"DESKTOP"** | `988px - 1597px` | Standard desktops |
| **"WIDE"** | `> 1597px` | Wide screens |

```css
/* Mobile first approach */
.container {
    padding: var(--spacing-s);
}

/* Tablet */
@media (min-width: 610px) {
    .container {
        padding: var(--spacing-m);
    }
}

/* Desktop */
@media (min-width: 988px) {
    .container {
        padding: var(--spacing-l);
    }
}
```

## 🧱 Component Design Principles

### Cards

- Cards use subtle shadows and borders
- 3px border on the left side for category indication
- Consistent internal padding (21px)

### Buttons

- Uppercase text
- Clear hover states
- No rounded corners for primary actions
- Soft rounded corners (3px) for secondary actions

### Form Elements

- Simple, minimal styling
- Focus states with sacred gold accent
- Error states with omega red
- Success states with quantum green

## 📄 CSS Variables Implementation

```css
:root {
    /* Colors */
    --color-white: #F5F5F5;
    --color-black: #0F0F0F;
    --color-grid: #5D5D5D;
    --color-divine-blue: #2B5797;
    --color-sacred-gold: #FFD700;
    --color-omega-red: #B71C1C;
    --color-quantum-green: #1E8E3E;
    
    /* Typography */
    --font-primary: "Helvetica Neue", Helvetica, Arial, sans-serif;
    --font-mono: "SF Mono", Monaco, Menlo, Consolas, "Courier New", monospace;
    
    /* Font Sizes */
    --font-size-divine: 34px;
    --font-size-grid: 21px;
    --font-size-subheading: 18px;
    --font-size-body: 16px;
    --font-size-small: 13px;
    --font-size-tiny: 11px;
    --font-size-code: 14px;
    
    /* Line Heights */
    --line-height-divine: 55px;
    --line-height-grid: 34px;
    --line-height-subheading: 29px;
    --line-height-body: 26px;
    --line-height-small: 21px;
    --line-height-tiny: 18px;
    --line-height-code: 21px;
    
    /* Spacing */
    --spacing-xs: 8px;
    --spacing-s: 13px;
    --spacing-m: 21px;
    --spacing-l: 34px;
    --spacing-xl: 55px;
    --spacing-xxl: 89px;
}
```

---

**"Typography is Voice. Space is Silence." — OMEGA DESIGN AXIOM 02**
