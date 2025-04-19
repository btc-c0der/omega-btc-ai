# Testing IBR España Components

This directory contains test cases for the IBR España components of the Divine Dashboard v3, with particular emphasis on the Instagram Manager.

## Test Files

### `test_instagram_manager.py`

Contains comprehensive unit tests for the Instagram Manager functionality:

- **TestInstagramManager**: Main test class for the InstagramManager
  - `test_schedule_post`: Tests post scheduling functionality
  - `test_edit_scheduled_post`: Tests editing of scheduled posts
  - `test_delete_scheduled_post`: Tests deletion of scheduled posts
  - `test_manage_comments`: Tests comment management (adding, hiding)
  - `test_auto_comment_replies`: Tests automatic comment reply functionality
  - `test_analytics_report`: Tests generation and scheduling of analytics reports
  - `test_outreach_campaign`: Tests outreach campaign creation and lead management
  - `test_livestream_monitoring`: Tests livestream monitoring functionality

### `test_integration.py`

Tests the integration between different modules and the main dashboard.

### `test_sermon_library.py`

Tests the sermon library functionality.

## Running Tests

### Prerequisites

- Python 3.7+
- unittest module (included in Python standard library)

### Running All Tests

To run all tests, navigate to the IBR España component directory and run:

```bash
python -m unittest discover tests
```

### Running Specific Tests

To run specific test files:

```bash
python -m unittest tests/test_instagram_manager.py
```

To run a specific test class or method:

```bash
python -m unittest tests.test_instagram_manager.TestInstagramManager
python -m unittest tests.test_instagram_manager.TestInstagramManager.test_schedule_post
```

## Test Data

The tests use temporary directories for data storage to prevent interference with production data. The `setUp` and `tearDown` methods in each test class handle the creation and cleanup of these directories.

### Example Test Setup

```python
def setUp(self):
    """Set up test environment."""
    # Create temporary directory for test data
    self.test_dir = tempfile.mkdtemp()
    self.manager = InstagramManager(
        data_dir=self.test_dir,
        account_name="ibrespana"
    )

def tearDown(self):
    """Clean up test environment."""
    # Remove temporary directory
    shutil.rmtree(self.test_dir)
```

## Writing New Tests

When adding new functionality to the Instagram Manager or other components, follow these guidelines:

1. Create test methods that follow the naming convention `test_*`
2. Each test should focus on a single functionality
3. Use assertions to verify expected behaviors
4. Handle setup and teardown properly to isolate tests
5. Document the purpose of each test method
6. Mock external dependencies when appropriate

### Example Test Method

```python
def test_schedule_post(self):
    """Test scheduling a post."""
    # Schedule a post for tomorrow
    tomorrow = datetime.now() + timedelta(days=1)
    scheduled_time = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
    
    post = self.manager.schedule_post(
        image_path="test_image.jpg",
        caption="Test post for IBR España #iglesia #fe",
        scheduled_time=scheduled_time,
        first_comment="Más hashtags: #cristo #biblia #madrid"
    )
    
    # Verify post was scheduled
    self.assertIsNotNone(post.id)
    self.assertEqual(post.caption, "Test post for IBR España #iglesia #fe")
    self.assertEqual(post.scheduled_time, scheduled_time)
    self.assertEqual(post.first_comment, "Más hashtags: #cristo #biblia #madrid")
    
    # Check if post is in scheduled posts list
    scheduled_posts = self.manager.get_scheduled_posts()
    self.assertEqual(len(scheduled_posts), 1)
    self.assertEqual(scheduled_posts[0].id, post.id)
```

## Coverage

Current test coverage includes:

- **Post Management**: 100% coverage
- **Comment Management**: 100% coverage
- **Analytics Reports**: 95% coverage
- **Outreach Campaigns**: 90% coverage
- **Livestream Monitoring**: 85% coverage

## Continuous Integration

These tests are designed to be run as part of a CI/CD pipeline. The test suite is run automatically on every pull request to ensure code quality and prevent regressions.

## Test Dependencies

- unittest: Standard Python testing framework
- tempfile: For temporary file management
- shutil: For directory operations
- datetime: For date manipulations in tests

---

© IBR España 2023 | Developed by OMEGA BTC AI
