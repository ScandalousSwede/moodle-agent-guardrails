# Changelog

All notable changes to the Moodle Calendar Sync project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2025-03-14

### Added
- Enhanced logging system with centralized configuration:
  - Created `src/utils/logging_config.py` with unified logging setup
  - Added `get_logger` function for consistent logger creation
  - Implemented file logging with customizable paths and rotation
  - Added support for different log levels across components
- Comprehensive test suite for core components:
  - Created `tests/unit/test_calendar_event.py` for CalendarEvent class testing
  - Added `tests/unit/test_logging_config.py` for logging system verification
  - Implemented `tests/unit/test_moodle_agents.py` for agent functionality testing
  - Created `tests/unit/test_simple_moodle_scraper.py` for scraper testing
- Improved error handling with standardized approaches:
  - Implemented graceful degradation for non-critical failures
  - Added detailed error context for easier debugging
  - Created recovery mechanisms for common failure scenarios

### Changed
- Refactored CalendarEvent class with improved validation:
  - Enhanced field validation for required attributes
  - Added better string representation for debugging
  - Implemented comprehensive dictionary conversion methods
- Updated documentation to reflect the new structure:
  - Enhanced README.md with detailed logging examples
  - Updated project structure documentation
  - Added code examples for key components
- Improved test organization with dedicated unit test directory

### Fixed
- Resolved file cleanup issues in logging tests
- Fixed import errors in test modules
- Corrected parameter handling in logging configuration

## [1.3.0] - 2025-03-14

### Added
- Project organization script (`organize_project.py`) for maintaining a clean codebase
- Comprehensive directory structure for better code organization
- Improved error handling with detailed logging and stack traces
- Asynchronous support for better performance

### Changed
- Reorganized project structure for better maintainability:
  - Moved scraper modules to `src/scrapers/` directory
  - Moved calendar modules to `src/calendar/` directory
  - Moved utility functions to `src/utils/` directory
  - Separated tests into `tests/unit/` and `tests/integration/` directories
  - Created `scripts/` directory for utility scripts
  - Created `examples/` directory for example code
- Refactored import statements to match the new structure
- Enhanced main sync process to use async/await patterns
- Improved status management with batched updates and file locking

### Removed
- Redundant and duplicate files (106 files removed)
- Unnecessary test backups and temporary files

## [1.2.0] - 2025-03-14

### Added
- Performance monitoring and optimization:
  - Created `src/performance.py` module for monitoring extraction tasks
  - Implemented caching mechanisms for frequently accessed data
  - Added decorators for timing functions and caching results
  - Created performance metrics logging and analysis
- Enhanced testing capabilities:
  - Developed `tests/test_edge_cases.py` for edge case testing
  - Created `tests/test_real_moodle_integration.py` for integration tests
  - Added tests for empty contexts, maximum item limits, error handling
  - Implemented performance measurement and caching verification tests
- Comprehensive documentation:
  - Added `docs/performance_and_testing.md` with detailed information
  - Created `docs/agents_sdk_integration_guide.md` for SDK usage
  - Updated README with performance and testing information

### Changed
- Enhanced `SimpleMoodleScraper` class with performance optimizations
- Improved error handling and recovery mechanisms
- Updated README with performance best practices
- Refactored test suite for better organization and coverage

## [1.1.1] - 2025-03-13

### Fixed
- Resolved issues with Agents-Based Slack Notification Integration:
  - Fixed parameter mismatch in SlackNotifier.send_message calls
  - Removed direct passing of channel, username, and icon_emoji parameters
  - Implemented proper state management for SlackNotifier properties
  - Corrected asynchronous calls to synchronous methods
  - Enhanced error handling with try/finally blocks
  - Improved logging for notification attempts
- All integration tests now pass successfully

## [1.1.0] - 2025-03-15

### Added
- Created `src/integrations.py` to manage integrations with external services
- Added unified integration manager for Google Calendar and Slack
- Implemented calendar event syncing with Google Calendar
- Added Slack notifications for calendar events and course resources
- Added command-line arguments for integration control:
  - `--enable-integrations`: Enable integrations with Google Calendar and Slack
  - `--notify`: Send notifications via Slack
  - `--sync-calendar`: Sync events with Google Calendar
- Enhanced test suite to verify integration functionality
- Updated documentation with integration setup instructions

### Changed
- Refactored `run.py` to support integration features
- Improved date and time parsing for better compatibility with Google Calendar
- Enhanced error handling for integration failures
- Updated README with detailed integration usage examples

## [1.0.0] - 2025-03-13

### Added
- Initial release of the simplified Moodle Calendar Sync
- Created `simple_moodle_scraper.py` focusing solely on OpenAI tools
- Added support for both Computer Use model and Agents SDK
- Implemented calendar event extraction functionality
- Added course resource extraction functionality
- Created test script for the simple implementation
- Added comprehensive documentation

### Changed
- Updated `run.py` to support both simple and hybrid implementations
- Simplified requirements.txt to focus on core dependencies
- Updated README with clear instructions for the simplified approach

### Removed
- Removed dependencies on Puppeteer and HTML scrapers
- Eliminated complex integrations to improve maintainability
- Removed Google Calendar and Slack notification features from the simple implementation

## [0.2.0] - 2025-03-18
### Added
- Enhanced agent orchestration system with proper handoffs
- Structured schema models using Pydantic
- Comprehensive tracing support with visualization capabilities
- Function-to-schema conversion utility
- Guardrails for data validation
- New agent tools registry

### Changed
- Refactored agents_integration.py to use functional patterns
- Improved error handling with discriminated unions
- Enhanced notification processing with better validation
- Updated exception handling system with trace support

### Fixed
- Proper cleanup in async operations
- Better type safety throughout the codebase
- More robust error handling in agent operations

## [0.2.0] - 2025-03-01

### Added
- Hybrid implementation combining OpenAI tools with traditional web scraping
- Support for Google Calendar integration
- Slack notification capabilities
- Comprehensive error handling and retry mechanisms

### Changed
- Enhanced browser automation with Playwright
- Improved credential management
- Updated documentation with detailed setup instructions

## [0.1.0] - 2025-02-15

### Added
- Initial prototype with basic Moodle scraping functionality
- Support for calendar event extraction
- Basic authentication mechanisms
- Preliminary documentation
