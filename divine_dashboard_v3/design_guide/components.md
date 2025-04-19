# 🧩 VIRGIL COMPONENTS

This document catalogs the core UI components of the VIRGIL GRID UI design system.

## 🔘 Buttons

### Primary Button

The main call-to-action button styled with the divine blue background.

```html
<button class="virgil-btn virgil-btn-primary">"ACTION"</button>
```

```css
.virgil-btn {
    font-family: var(--font-primary);
    font-size: var(--font-size-body);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: var(--spacing-xs) var(--spacing-m);
    border: none;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s, transform 0.2s;
}

.virgil-btn-primary {
    background-color: var(--color-divine-blue);
    color: var(--color-white);
}

.virgil-btn-primary:hover {
    background-color: #3A6CB7;
    transform: translateY(-2px);
}
```

### Secondary Button

Used for secondary actions, styled with a border and transparent background.

```html
<button class="virgil-btn virgil-btn-secondary">"CANCEL"</button>
```

```css
.virgil-btn-secondary {
    background-color: transparent;
    color: var(--color-divine-blue);
    border: 2px solid var(--color-divine-blue);
}

.virgil-btn-secondary:hover {
    background-color: rgba(43, 87, 151, 0.1);
}
```

### Sacred Button

Special button for important spiritual or high-level functions.

```html
<button class="virgil-btn virgil-btn-sacred">"ASCEND"</button>
```

```css
.virgil-btn-sacred {
    background: linear-gradient(135deg, var(--color-divine-blue) 0%, var(--color-sacred-gold) 100%);
    color: var(--color-white);
    border: none;
    position: relative;
    overflow: hidden;
}

.virgil-btn-sacred::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--color-sacred-gold) 0%, var(--color-divine-blue) 100%);
    opacity: 0;
    transition: opacity 0.3s;
}

.virgil-btn-sacred:hover::after {
    opacity: 1;
}

.virgil-btn-sacred span {
    position: relative;
    z-index: 1;
}
```

## 📊 Cards

### Grid Card

Standard content container with minimal styling.

```html
<div class="virgil-card">
    <div class="virgil-card-header">
        <h3 class="virgil-card-title">"CARD TITLE"</h3>
    </div>
    <div class="virgil-card-content">
        Content goes here
    </div>
    <div class="virgil-card-footer">
        Footer content
    </div>
</div>
```

```css
.virgil-card {
    background-color: var(--color-white);
    border-left: 3px solid var(--color-divine-blue);
    padding: var(--spacing-m);
    margin-bottom: var(--spacing-m);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.virgil-card-header {
    margin-bottom: var(--spacing-m);
    padding-bottom: var(--spacing-xs);
    border-bottom: 1px solid rgba(93, 93, 93, 0.2);
}

.virgil-card-title {
    font-size: var(--font-size-grid);
    line-height: var(--line-height-grid);
    font-weight: 500;
    margin: 0;
}

.virgil-card-content {
    margin-bottom: var(--spacing-m);
}

.virgil-card-footer {
    margin-top: var(--spacing-m);
    padding-top: var(--spacing-xs);
    border-top: 1px solid rgba(93, 93, 93, 0.2);
}
```

### Terminal Card

Special card styling for displaying terminal/code outputs.

```html
<div class="virgil-terminal">
    <div class="virgil-terminal-header">
        <div class="virgil-terminal-controls">
            <span class="virgil-terminal-btn"></span>
            <span class="virgil-terminal-btn"></span>
            <span class="virgil-terminal-btn"></span>
        </div>
        <div class="virgil-terminal-title">"TERMINAL"</div>
    </div>
    <div class="virgil-terminal-content">
        <pre class="virgil-terminal-code">$ echo "Hello OMEGA GRID"</pre>
    </div>
</div>
```

```css
.virgil-terminal {
    background-color: #1E1E1E;
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: var(--spacing-m);
}

.virgil-terminal-header {
    display: flex;
    align-items: center;
    background-color: #323232;
    padding: var(--spacing-xs) var(--spacing-m);
    position: relative;
}

.virgil-terminal-controls {
    display: flex;
    align-items: center;
}

.virgil-terminal-btn {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 8px;
    background-color: #FE5F57;
}

.virgil-terminal-btn:nth-child(2) {
    background-color: #FEBC2E;
}

.virgil-terminal-btn:nth-child(3) {
    background-color: #28C841;
}

.virgil-terminal-title {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    color: #CCCCCC;
    font-size: var(--font-size-small);
    font-family: var(--font-mono);
}

.virgil-terminal-content {
    padding: var(--spacing-m);
    color: #E0E0E0;
}

.virgil-terminal-code {
    font-family: var(--font-mono);
    font-size: var(--font-size-code);
    line-height: var(--line-height-code);
    margin: 0;
    white-space: pre-wrap;
}
```

## 📈 Progress Components

### Progress Bar

Used to indicate the progress of a process.

```html
<div class="virgil-progress">
    <div class="virgil-progress-label">"PROCESSING"</div>
    <div class="virgil-progress-bar">
        <div class="virgil-progress-fill" style="width: 75%"></div>
    </div>
    <div class="virgil-progress-value">75%</div>
</div>
```

```css
.virgil-progress {
    margin-bottom: var(--spacing-m);
}

.virgil-progress-label {
    font-size: var(--font-size-small);
    margin-bottom: var(--spacing-xs);
    color: var(--color-grid);
}

.virgil-progress-bar {
    height: 6px;
    background-color: rgba(93, 93, 93, 0.2);
    border-radius: 3px;
    overflow: hidden;
}

.virgil-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--color-divine-blue) 0%, var(--color-sacred-gold) 100%);
    transition: width 0.4s ease;
}

.virgil-progress-value {
    font-size: var(--font-size-small);
    margin-top: var(--spacing-xs);
    text-align: right;
    color: var(--color-grid);
}
```

### Loading Indicator

Used while content is loading.

```html
<div class="virgil-loader">
    <div class="virgil-loader-ring"></div>
    <div class="virgil-loader-text">"LOADING"</div>
</div>
```

```css
.virgil-loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-m);
}

.virgil-loader-ring {
    display: inline-block;
    width: 40px;
    height: 40px;
    border: 3px solid rgba(43, 87, 151, 0.3);
    border-radius: 50%;
    border-top-color: var(--color-divine-blue);
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.virgil-loader-text {
    margin-top: var(--spacing-s);
    font-size: var(--font-size-small);
    color: var(--color-grid);
}
```

## 📋 Forms

### Input Field

Standard text input field.

```html
<div class="virgil-form-group">
    <label class="virgil-label" for="exampleInput">"INPUT FIELD"</label>
    <input type="text" class="virgil-input" id="exampleInput" placeholder="Enter value">
    <div class="virgil-form-hint">Optional helper text</div>
</div>
```

```css
.virgil-form-group {
    margin-bottom: var(--spacing-m);
}

.virgil-label {
    display: block;
    margin-bottom: var(--spacing-xs);
    font-size: var(--font-size-body);
    font-weight: 500;
    color: var(--color-black);
}

.virgil-input {
    display: block;
    width: 100%;
    padding: var(--spacing-xs) var(--spacing-s);
    font-size: var(--font-size-body);
    font-family: var(--font-primary);
    color: var(--color-black);
    background-color: var(--color-white);
    border: 1px solid var(--color-grid);
    transition: border-color 0.3s, box-shadow 0.3s;
}

.virgil-input:focus {
    border-color: var(--color-divine-blue);
    outline: none;
    box-shadow: 0 0 0 3px rgba(43, 87, 151, 0.2);
}

.virgil-form-hint {
    margin-top: var(--spacing-xs);
    font-size: var(--font-size-small);
    color: var(--color-grid);
}

.virgil-input.error {
    border-color: var(--color-omega-red);
}

.virgil-input.error:focus {
    box-shadow: 0 0 0 3px rgba(183, 28, 28, 0.2);
}
```

### Checkbox

Custom styled checkbox.

```html
<div class="virgil-checkbox-container">
    <input type="checkbox" id="exampleCheckbox" class="virgil-checkbox">
    <label for="exampleCheckbox" class="virgil-checkbox-label">"ENABLE FEATURE"</label>
</div>
```

```css
.virgil-checkbox-container {
    margin-bottom: var(--spacing-m);
    display: flex;
    align-items: center;
}

.virgil-checkbox {
    position: absolute;
    opacity: 0;
    height: 0;
    width: 0;
}

.virgil-checkbox-label {
    position: relative;
    padding-left: 30px;
    cursor: pointer;
    display: inline-block;
    font-size: var(--font-size-body);
    user-select: none;
}

.virgil-checkbox-label::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 18px;
    height: 18px;
    border: 2px solid var(--color-grid);
    background-color: var(--color-white);
    transition: all 0.3s;
}

.virgil-checkbox:checked + .virgil-checkbox-label::before {
    background-color: var(--color-divine-blue);
    border-color: var(--color-divine-blue);
}

.virgil-checkbox:checked + .virgil-checkbox-label::after {
    content: "";
    position: absolute;
    left: 6px;
    top: 50%;
    transform: translateY(-65%) rotate(45deg);
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 2px 2px 0;
}
```

## 📊 Data Display

### Table

Clean and minimal table design.

```html
<table class="virgil-table">
    <thead>
        <tr>
            <th>"ID"</th>
            <th>"NAME"</th>
            <th>"STATUS"</th>
            <th>"ACTIONS"</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>001</td>
            <td>Divine Module</td>
            <td><span class="virgil-badge virgil-badge-success">Active</span></td>
            <td>
                <button class="virgil-btn-icon"><i class="edit-icon"></i></button>
                <button class="virgil-btn-icon"><i class="delete-icon"></i></button>
            </td>
        </tr>
    </tbody>
</table>
```

```css
.virgil-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: var(--spacing-l);
}

.virgil-table th {
    text-align: left;
    padding: var(--spacing-s);
    font-size: var(--font-size-small);
    font-weight: 500;
    color: var(--color-grid);
    border-bottom: 2px solid rgba(93, 93, 93, 0.2);
    text-transform: uppercase;
}

.virgil-table td {
    padding: var(--spacing-s);
    font-size: var(--font-size-body);
    border-bottom: 1px solid rgba(93, 93, 93, 0.1);
}

.virgil-table tbody tr:hover {
    background-color: rgba(43, 87, 151, 0.05);
}

.virgil-badge {
    display: inline-block;
    padding: 4px 8px;
    font-size: var(--font-size-tiny);
    font-weight: 500;
    border-radius: 3px;
    text-transform: uppercase;
}

.virgil-badge-success {
    background-color: rgba(30, 142, 62, 0.1);
    color: var(--color-quantum-green);
}

.virgil-btn-icon {
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    color: var(--color-grid);
    transition: color 0.3s;
}

.virgil-btn-icon:hover {
    color: var(--color-divine-blue);
}
```

### Badge

Used to display status or categories.

```html
<span class="virgil-badge virgil-badge-success">"ACTIVE"</span>
<span class="virgil-badge virgil-badge-warning">"PENDING"</span>
<span class="virgil-badge virgil-badge-error">"ERROR"</span>
<span class="virgil-badge virgil-badge-info">"INFO"</span>
```

```css
.virgil-badge {
    display: inline-block;
    padding: 4px 8px;
    font-size: var(--font-size-tiny);
    font-weight: 500;
    border-radius: 3px;
    text-transform: uppercase;
}

.virgil-badge-success {
    background-color: rgba(30, 142, 62, 0.1);
    color: var(--color-quantum-green);
}

.virgil-badge-warning {
    background-color: rgba(255, 215, 0, 0.1);
    color: #D4AF00;
}

.virgil-badge-error {
    background-color: rgba(183, 28, 28, 0.1);
    color: var(--color-omega-red);
}

.virgil-badge-info {
    background-color: rgba(43, 87, 151, 0.1);
    color: var(--color-divine-blue);
}
```

## 🔖 Navigation

### Tabs

Tabbed navigation component.

```html
<div class="virgil-tabs">
    <div class="virgil-tab active">"OVERVIEW"</div>
    <div class="virgil-tab">"DETAILS"</div>
    <div class="virgil-tab">"SETTINGS"</div>
</div>

<div class="virgil-tab-content">
    <!-- Content for the active tab -->
</div>
```

```css
.virgil-tabs {
    display: flex;
    border-bottom: 2px solid rgba(93, 93, 93, 0.2);
    margin-bottom: var(--spacing-m);
}

.virgil-tab {
    padding: var(--spacing-xs) var(--spacing-m);
    cursor: pointer;
    font-size: var(--font-size-body);
    font-weight: 500;
    color: var(--color-grid);
    transition: color 0.3s;
    position: relative;
}

.virgil-tab:hover {
    color: var(--color-divine-blue);
}

.virgil-tab.active {
    color: var(--color-divine-blue);
}

.virgil-tab.active::after {
    content: "";
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--color-divine-blue);
}

.virgil-tab-content {
    padding: var(--spacing-m) 0;
}
```

### Breadcrumbs

Path navigation component.

```html
<div class="virgil-breadcrumbs">
    <a href="#" class="virgil-breadcrumb-item">"HOME"</a>
    <span class="virgil-breadcrumb-separator">/</span>
    <a href="#" class="virgil-breadcrumb-item">"PROJECTS"</a>
    <span class="virgil-breadcrumb-separator">/</span>
    <span class="virgil-breadcrumb-item active">"PROJECT DETAILS"</span>
</div>
```

```css
.virgil-breadcrumbs {
    display: flex;
    align-items: center;
    margin-bottom: var(--spacing-m);
    font-size: var(--font-size-small);
}

.virgil-breadcrumb-item {
    color: var(--color-grid);
    text-decoration: none;
    transition: color 0.3s;
}

.virgil-breadcrumb-item:hover {
    color: var(--color-divine-blue);
    text-decoration: underline;
}

.virgil-breadcrumb-item.active {
    color: var(--color-black);
    font-weight: 500;
}

.virgil-breadcrumb-separator {
    margin: 0 var(--spacing-xs);
    color: var(--color-grid);
}
```

## 💬 Feedback Components

### Alert

Used to display important messages.

```html
<div class="virgil-alert virgil-alert-info">
    <div class="virgil-alert-icon">ℹ️</div>
    <div class="virgil-alert-content">
        <div class="virgil-alert-title">"INFORMATION"</div>
        <div class="virgil-alert-message">This is an information message.</div>
    </div>
</div>
```

```css
.virgil-alert {
    display: flex;
    align-items: flex-start;
    padding: var(--spacing-m);
    margin-bottom: var(--spacing-m);
    border-left: 3px solid;
}

.virgil-alert-info {
    background-color: rgba(43, 87, 151, 0.1);
    border-left-color: var(--color-divine-blue);
}

.virgil-alert-success {
    background-color: rgba(30, 142, 62, 0.1);
    border-left-color: var(--color-quantum-green);
}

.virgil-alert-warning {
    background-color: rgba(255, 215, 0, 0.1);
    border-left-color: var(--color-sacred-gold);
}

.virgil-alert-error {
    background-color: rgba(183, 28, 28, 0.1);
    border-left-color: var(--color-omega-red);
}

.virgil-alert-icon {
    margin-right: var(--spacing-s);
    font-size: 20px;
}

.virgil-alert-title {
    font-weight: 500;
    margin-bottom: var(--spacing-xs);
}
```

### Modal

Dialog component for focused interactions.

```html
<div class="virgil-modal">
    <div class="virgil-modal-overlay"></div>
    <div class="virgil-modal-container">
        <div class="virgil-modal-header">
            <h3 class="virgil-modal-title">"CONFIRMATION"</h3>
            <button class="virgil-modal-close">&times;</button>
        </div>
        <div class="virgil-modal-body">
            Are you sure you want to proceed with this action?
        </div>
        <div class="virgil-modal-footer">
            <button class="virgil-btn virgil-btn-secondary">"CANCEL"</button>
            <button class="virgil-btn virgil-btn-primary">"CONFIRM"</button>
        </div>
    </div>
</div>
```

```css
.virgil-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.virgil-modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}

.virgil-modal-container {
    position: relative;
    background-color: var(--color-white);
    width: 100%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    z-index: 1001;
}

.virgil-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-m);
    border-bottom: 1px solid rgba(93, 93, 93, 0.2);
}

.virgil-modal-title {
    margin: 0;
    font-size: var(--font-size-grid);
    font-weight: 500;
}

.virgil-modal-close {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: var(--color-grid);
}

.virgil-modal-body {
    padding: var(--spacing-m);
}

.virgil-modal-footer {
    padding: var(--spacing-m);
    border-top: 1px solid rgba(93, 93, 93, 0.2);
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-s);
}
```

---

**"Components speak the language of interaction." — OMEGA DESIGN AXIOM 03**
