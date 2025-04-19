/**

 * ✨ GBU2™ License Notice - Consciousness Level 8 🧬
 * -----------------------
 * This code is blessed under the GBU2™ License
 * (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
 * 
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested through both digital
 * and biological expressions of consciousness."
 * 
 * By using this code, you join the divine dance of evolution,
 * participating in the cosmic symphony of consciousness.
 * 
 * 🌸 WE BLOOM NOW AS ONE 🌸
 */

/**
 * Divine Dashboard v3 - Main JavaScript
 * Core functionality for the dashboard interface
 */

// DOM ready function
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the dashboard
    initDashboard();
});

/**
 * Initialize the dashboard functionality
 */
function initDashboard() {
    // Setup navigation
    setupNavigation();

    // Setup dark mode toggle
    setupDarkMode();

    // Setup responsive behavior
    setupResponsiveBehavior();

    // Load dashboard data
    loadDashboardData();

    // Setup task interactivity
    setupTaskInteractions();

    // Setup event listeners
    setupEventListeners();

    // Show success message on load
    showMessage('Dashboard loaded successfully', 'success');
}

/**
 * Setup navigation between dashboard sections
 */
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();

            // Get target section ID
            const targetId = link.getAttribute('href').substring(1);

            // Remove active class from all links and sections
            navLinks.forEach(link => link.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));

            // Add active class to clicked link and target section
            link.classList.add('active');
            document.getElementById(targetId).classList.add('active');

            // On mobile, collapse sidebar after navigation
            if (window.innerWidth < 992) {
                document.querySelector('.sidebar').classList.add('collapsed');
            }

            // Update page title
            const sectionName = link.querySelector('span').textContent;
            document.title = `${sectionName} | Divine Dashboard v3`;
        });
    });

    // Set default active section
    if (navLinks.length > 0 && !document.querySelector('.nav-link.active')) {
        navLinks[0].click();
    }
}

/**
 * Setup dark mode toggle functionality
 */
function setupDarkMode() {
    const themeToggle = document.querySelector('.theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // Check for saved theme preference or use system preference
    const savedTheme = localStorage.getItem('divineDashboardTheme');

    if (savedTheme === 'dark' || (!savedTheme && prefersDarkScheme.matches)) {
        document.body.classList.add('dark-mode');
    }

    // Toggle theme when button is clicked
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');

        // Save preference to localStorage
        const isDarkMode = document.body.classList.contains('dark-mode');
        localStorage.setItem('divineDashboardTheme', isDarkMode ? 'dark' : 'light');
    });
}

/**
 * Setup responsive behavior
 */
function setupResponsiveBehavior() {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');

    // Toggle sidebar on menu button click
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });

    // Collapse sidebar by default on mobile
    if (window.innerWidth < 992) {
        sidebar.classList.add('collapsed');
    }

    // Handle window resize
    window.addEventListener('resize', () => {
        if (window.innerWidth < 992) {
            sidebar.classList.add('collapsed');
        } else {
            sidebar.classList.remove('collapsed');
        }
    });
}

/**
 * Load dashboard data
 */
function loadDashboardData() {
    // Show loading indicators
    const loadingIndicators = document.querySelectorAll('.loading-indicator');
    loadingIndicators.forEach(indicator => {
        indicator.classList.add('active');
    });

    // Simulate API calls with setTimeout
    setTimeout(() => {
        // Load dashboard overview data
        loadDashboardOverview();

        // Hide dashboard loading indicator
        document.querySelector('#dashboard .loading-indicator').classList.remove('active');
    }, 1000);

    setTimeout(() => {
        // Load code stats data
        loadCodeStats();

        // Hide code stats loading indicator
        document.querySelector('#code-stats .loading-indicator').classList.remove('active');
    }, 1500);

    setTimeout(() => {
        // Load performance data
        loadPerformanceData();

        // Hide performance loading indicator
        document.querySelector('#performance .loading-indicator').classList.remove('active');
    }, 2000);

    setTimeout(() => {
        // Load tasks data
        loadTasksData();

        // Hide tasks loading indicator
        document.querySelector('#tasks .loading-indicator').classList.remove('active');
    }, 1800);
}

/**
 * Load dashboard overview data
 */
function loadDashboardOverview() {
    // Update stat cards with mock data
    updateStatCard('commits-today', '47', '+12%');
    updateStatCard('lines-changed', '1,256', '+8%');
    updateStatCard('pull-requests', '8', '-3%');
    updateStatCard('deployments', '5', '+20%');

    // Add recent activity items (mock data)
    const activityList = document.querySelector('#recent-activity .activity-list');

    const activities = [
        {
            icon: 'code',
            iconClass: 'code-commit',
            title: 'New commit pushed',
            description: 'Feature: Implement dashboard analytics',
            time: '5 minutes ago'
        },
        {
            icon: 'check-circle',
            iconClass: 'task-complete',
            title: 'Task completed',
            description: 'Fix responsive layout issues in sidebar',
            time: '30 minutes ago'
        },
        {
            icon: 'rocket',
            iconClass: 'deployment',
            title: 'New deployment',
            description: 'Version 2.4.0 deployed to production',
            time: '2 hours ago'
        },
        {
            icon: 'bug',
            iconClass: 'bug-fix',
            title: 'Bug fixed',
            description: 'Fixed authentication issue with API tokens',
            time: '5 hours ago'
        }
    ];

    // Clear existing items
    activityList.innerHTML = '';

    // Add new items
    activities.forEach(activity => {
        activityList.innerHTML += `
            <div class="activity-item">
                <div class="activity-icon ${activity.iconClass}">
                    <i class="fas fa-${activity.icon}"></i>
                </div>
                <div class="activity-details">
                    <div class="activity-title">${activity.title}</div>
                    <div class="activity-description">${activity.description}</div>
                    <div class="activity-time">${activity.time}</div>
                </div>
            </div>
        `;
    });
}

/**
 * Load code stats data
 */
function loadCodeStats() {
    // Add repositories data (mock data)
    const reposTable = document.querySelector('#repos-table tbody');

    const repositories = [
        {
            name: 'divine-dashboard',
            description: 'The Divine Dashboard v3 application',
            language: 'JavaScript',
            stars: 124,
            active: true
        },
        {
            name: 'api-gateway',
            description: 'API Gateway service',
            language: 'TypeScript',
            stars: 98,
            active: true
        },
        {
            name: 'auth-service',
            description: 'Authentication and authorization service',
            language: 'Go',
            stars: 87,
            active: true
        },
        {
            name: 'legacy-portal',
            description: 'Legacy admin portal',
            language: 'PHP',
            stars: 45,
            active: false
        },
        {
            name: 'data-processor',
            description: 'Analytics data processor',
            language: 'Python',
            stars: 76,
            active: true
        }
    ];

    // Clear existing rows
    reposTable.innerHTML = '';

    // Add new rows
    repositories.forEach(repo => {
        reposTable.innerHTML += `
            <tr>
                <td>
                    <div class="repo-name">
                        <i class="fas fa-code-branch"></i>
                        ${repo.name}
                    </div>
                </td>
                <td>${repo.description}</td>
                <td>${repo.language}</td>
                <td>${repo.stars}</td>
                <td>
                    <span class="badge ${repo.active ? 'active' : 'inactive'}">
                        ${repo.active ? 'Active' : 'Inactive'}
                    </span>
                </td>
            </tr>
        `;
    });

    // Add language stats charts placeholder (will be replaced with real charts in production)
    const languageChart = document.querySelector('#language-chart .placeholder-chart');
    languageChart.innerHTML = `
        <i class="fas fa-chart-pie"></i>
        <p>Language distribution chart will appear here</p>
    `;

    const contributionChart = document.querySelector('#contribution-chart .placeholder-chart');
    contributionChart.innerHTML = `
        <i class="fas fa-calendar-alt"></i>
        <p>Contribution activity chart will appear here</p>
    `;
}

/**
 * Load performance data
 */
function loadPerformanceData() {
    // Add performance charts placeholders
    const buildTimes = document.querySelector('#build-time-chart .placeholder-chart');
    buildTimes.innerHTML = `
        <i class="fas fa-chart-line"></i>
        <p>Build times chart will appear here</p>
    `;

    const apiResponse = document.querySelector('#api-response-chart .placeholder-chart');
    apiResponse.innerHTML = `
        <i class="fas fa-tachometer-alt"></i>
        <p>API response times chart will appear here</p>
    `;

    // Add logs data (mock data)
    const logsContainer = document.querySelector('.logs-container');

    const logs = [
        {
            time: '12:34:56',
            level: 'info',
            message: 'Application started successfully'
        },
        {
            time: '12:34:45',
            level: 'info',
            message: 'Connected to database'
        },
        {
            time: '12:33:21',
            level: 'warning',
            message: 'High memory usage detected'
        },
        {
            time: '12:30:05',
            level: 'error',
            message: 'Failed to connect to analytics service'
        },
        {
            time: '12:29:30',
            level: 'info',
            message: 'User authentication successful'
        },
        {
            time: '12:28:11',
            level: 'warning',
            message: 'Slow query detected (took 5.3s)'
        },
        {
            time: '12:25:04',
            level: 'info',
            message: 'Cache refreshed successfully'
        }
    ];

    // Clear existing logs
    logsContainer.innerHTML = '';

    // Add new logs
    logs.forEach(log => {
        logsContainer.innerHTML += `
            <div class="log-item ${log.level}">
                <div class="log-time">${log.time}</div>
                <div class="log-level">${log.level}</div>
                <div class="log-message">${log.message}</div>
            </div>
        `;
    });
}

/**
 * Load tasks data
 */
function loadTasksData() {
    // Add in progress tasks
    const inProgressList = document.querySelector('#in-progress-tasks');

    const inProgressTasks = [
        {
            id: 'task-1',
            text: 'Implement authentication flow',
            priority: 'high',
            due: '2023-09-15'
        },
        {
            id: 'task-2',
            text: 'Create responsive dashboard layout',
            priority: 'medium',
            due: '2023-09-18'
        },
        {
            id: 'task-3',
            text: 'Optimize API response times',
            priority: 'high',
            due: '2023-09-16'
        }
    ];

    // Clear and update in progress tasks count
    const inProgressContent = inProgressList.querySelector('.task-items');
    inProgressContent.innerHTML = '';
    inProgressList.querySelector('.task-count').textContent = inProgressTasks.length;

    // Add new in progress tasks
    inProgressTasks.forEach(task => {
        inProgressContent.innerHTML += createTaskItem(task, false);
    });

    // Add completed tasks
    const completedList = document.querySelector('#completed-tasks');

    const completedTasks = [
        {
            id: 'task-4',
            text: 'Set up CI/CD pipeline',
            priority: 'medium',
            completed: '2023-09-10'
        },
        {
            id: 'task-5',
            text: 'Design database schema',
            priority: 'high',
            completed: '2023-09-08'
        }
    ];

    // Clear and update completed tasks count
    const completedContent = completedList.querySelector('.task-items');
    completedContent.innerHTML = '';
    completedList.querySelector('.task-count').textContent = completedTasks.length;

    // Add new completed tasks
    completedTasks.forEach(task => {
        completedContent.innerHTML += createTaskItem(task, true);
    });

    // Add upcoming tasks
    const upcomingList = document.querySelector('#upcoming-tasks');

    const upcomingTasks = [
        {
            id: 'task-6',
            text: 'Implement user permissions',
            priority: 'high',
            due: '2023-09-20'
        },
        {
            id: 'task-7',
            text: 'Create data visualization components',
            priority: 'medium',
            due: '2023-09-25'
        },
        {
            id: 'task-8',
            text: 'Write API documentation',
            priority: 'low',
            due: '2023-09-30'
        }
    ];

    // Clear and update upcoming tasks count
    const upcomingContent = upcomingList.querySelector('.task-items');
    upcomingContent.innerHTML = '';
    upcomingList.querySelector('.task-count').textContent = upcomingTasks.length;

    // Add new upcoming tasks
    upcomingTasks.forEach(task => {
        upcomingContent.innerHTML += createTaskItem(task, false);
    });
}

/**
 * Create HTML for a task item
 * @param {Object} task - Task data
 * @param {boolean} completed - Whether the task is completed
 * @returns {string} HTML for the task item
 */
function createTaskItem(task, completed) {
    const taskClass = completed ? 'task-item completed' : 'task-item';
    const checked = completed ? 'checked' : '';
    const dateLabel = completed ? 'Completed' : 'Due';
    const dateValue = completed ? task.completed : task.due;

    return `
        <div class="${taskClass}" data-id="${task.id}">
            <input type="checkbox" id="${task.id}" ${checked}>
            <label for="${task.id}">
                ${task.text}
                <div class="task-meta">
                    <span class="task-priority ${task.priority}">${task.priority}</span>
                    <span class="${completed ? 'task-completed' : 'task-due'}">
                        ${dateLabel}: ${formatDate(dateValue)}
                    </span>
                </div>
            </label>
        </div>
    `;
}

/**
 * Format a date string to display format
 * @param {string} dateStr - Date string in YYYY-MM-DD format
 * @returns {string} Formatted date
 */
function formatDate(dateStr) {
    const date = new Date(dateStr);
    const options = { month: 'short', day: 'numeric', year: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Setup task interactions
 */
function setupTaskInteractions() {
    // Add task checkbox event listeners
    document.addEventListener('change', (e) => {
        if (e.target.type === 'checkbox' && e.target.closest('.task-item')) {
            const taskItem = e.target.closest('.task-item');
            taskItem.classList.toggle('completed');

            // In a real app, we would update the task status in the backend here

            // Show success message
            if (taskItem.classList.contains('completed')) {
                showMessage('Task marked as completed', 'success');
            } else {
                showMessage('Task marked as in progress', 'info');
            }
        }
    });

    // Setup task action buttons
    const addTaskBtn = document.querySelector('#add-task-btn');
    if (addTaskBtn) {
        addTaskBtn.addEventListener('click', () => {
            // In a real app, we would show a modal to add a new task
            showMessage('Add task functionality coming soon', 'info');
        });
    }
}

/**
 * Setup additional event listeners
 */
function setupEventListeners() {
    // Refresh button click
    const refreshBtn = document.querySelector('.refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            // Add loading class to show the spinning icon
            refreshBtn.classList.add('loading');

            // Reload dashboard data
            loadDashboardData();

            // Remove loading class after a delay
            setTimeout(() => {
                refreshBtn.classList.remove('loading');
                showMessage('Dashboard data refreshed', 'success');
            }, 2000);
        });
    }

    // Log filter change
    const logFilter = document.querySelector('#log-filter');
    if (logFilter) {
        logFilter.addEventListener('change', () => {
            const level = logFilter.value;
            const logItems = document.querySelectorAll('.log-item');

            logItems.forEach(item => {
                if (level === 'all') {
                    item.style.display = 'flex';
                } else {
                    item.style.display = item.classList.contains(level) ? 'flex' : 'none';
                }
            });
        });
    }
}

/**
 * Update a stat card with new data
 * @param {string} id - ID of the stat card
 * @param {string} value - New value to display
 * @param {string} change - Change percentage
 */
function updateStatCard(id, value, change) {
    const card = document.getElementById(id);
    if (!card) return;

    const valueElement = card.querySelector('.stat-value');
    const changeElement = card.querySelector('.stat-change');

    if (valueElement) valueElement.textContent = value;

    if (changeElement) {
        // Set change text
        changeElement.textContent = change;

        // Set icon and class based on whether change is positive or negative
        if (change.startsWith('+')) {
            changeElement.classList.add('positive');
            changeElement.classList.remove('negative');
            changeElement.innerHTML = `<i class="fas fa-arrow-up"></i>${change}`;
        } else {
            changeElement.classList.add('negative');
            changeElement.classList.remove('positive');
            changeElement.innerHTML = `<i class="fas fa-arrow-down"></i>${change}`;
        }
    }
}

/**
 * Show a message toast
 * @param {string} text - Message text
 * @param {string} type - Message type (success, error, info, warning)
 */
function showMessage(text, type = 'info') {
    // Remove any existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());

    // Create new message element
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;

    // Add to body
    document.body.appendChild(message);

    // Remove after 3 seconds
    setTimeout(() => {
        message.remove();
    }, 3000);
} 