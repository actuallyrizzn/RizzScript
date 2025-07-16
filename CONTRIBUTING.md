# Contributing to RizzScript

Thank you for your interest in contributing to RizzScript! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Submitting Changes](#submitting-changes)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of PyQt5 and Python
- AssemblyAI and OpenAI API keys for testing

### Development Environment

1. **Fork the Repository**
   ```bash
   git fork https://github.com/actuallyrizzn/rizzscript.git
   cd rizzscript
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv dev-env
   source dev-env/bin/activate  # On Windows: dev-env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Configuration**
   - Copy `config.json.example` to `config.json` (if available)
   - Add your API keys for testing
   - Never commit your actual API keys

## Development Setup

### Project Structure

```
rizzscript/
├── app.py                    # Main application file
├── requirements.txt          # Python dependencies
├── RizzScript.spec          # PyInstaller configuration
├── config.json              # API configuration (not in git)
├── README.md                # Main documentation
├── CONTRIBUTING.md          # This file
├── API_SETUP_GUIDE.md       # API configuration guide
├── LICENSE                  # MIT license
├── .gitignore              # Git ignore rules
├── dist/                   # Built distributions
├── build/                  # Build artifacts
└── old/                    # Legacy code
```

### Key Components

- **MainWindow**: Primary GUI controller
- **TranscriptionThread**: Background audio processing
- **MappingWorker**: OpenAI integration for speaker mapping
- **SpeakerMappingWidget**: Interactive speaker mapping interface
- **SettingsDialog**: API key configuration

### Running the Application

```bash
python app.py
```

## Code Style Guidelines

### Python Code Style

We follow PEP 8 with some specific preferences:

1. **Line Length**: Maximum 88 characters (Black formatter standard)
2. **Indentation**: 4 spaces (no tabs)
3. **Imports**: Group imports in this order:
   - Standard library
   - Third-party packages
   - Local application imports

```python
# Standard library
import sys
import os
import json

# Third-party
from PyQt5.QtCore import Qt, QThread
import assemblyai as aai

# Local
from .utils import helper_function
```

### PyQt5 Conventions

1. **Class Names**: Use CamelCase for Qt classes
   ```python
   class TranscriptionThread(QThread):
       pass
   ```

2. **Signal Names**: Use camelCase
   ```python
   transcriptionFinished = pyqtSignal(object)
   ```

3. **Widget Names**: Use descriptive names
   ```python
   self.speaker_mapping_dock = QDockWidget("Speaker Mapping", self)
   ```

### Documentation Standards

1. **Docstrings**: Use Google-style docstrings
   ```python
   def extract_json(text):
       """Extract JSON object from text response.
       
       Args:
           text (str): Text containing JSON data
           
       Returns:
           dict: Parsed JSON object
           
       Raises:
           ValueError: If no valid JSON found
       """
   ```

2. **Comments**: Explain complex logic, not obvious code
   ```python
   # Convert milliseconds to seconds for timestamp formatting
   sec_time = utt.start / 1000.0
   ```

3. **Type Hints**: Use where helpful
   ```python
   def seconds_to_hhmmss(seconds: float) -> str:
       """Convert seconds to HH:MM:SS format."""
   ```

## Submitting Changes

### Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clear, focused commits
   - Follow the code style guidelines
   - Add tests if applicable

3. **Test Your Changes**
   - Run the application manually
   - Test with different audio files
   - Verify UI functionality

4. **Update Documentation**
   - Update README.md if needed
   - Add docstrings for new functions
   - Update API_SETUP_GUIDE.md if API changes

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Guidelines

Use clear, descriptive commit messages:

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

Examples:
```
feat: Add timestamp toggle functionality
fix: Resolve speaker mapping error handling
docs: Update API setup instructions
refactor: Extract transcription logic into separate class
```

### Pull Request Guidelines

1. **Title**: Clear, descriptive title
2. **Description**: Explain what changes were made and why
3. **Testing**: Describe how you tested the changes
4. **Screenshots**: Include UI changes if applicable
5. **Breaking Changes**: Note any breaking changes

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested with sample audio files
- [ ] Verified UI functionality
- [ ] Tested error handling

## Screenshots (if applicable)
Add screenshots here.

## Additional Notes
Any additional information.
```

## Bug Reports

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Test with latest version** to ensure bug still exists
3. **Gather system information** (OS, Python version, etc.)

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug.

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 10, macOS 11.6, Ubuntu 20.04]
- Python Version: [e.g., 3.9.7]
- RizzScript Version: [e.g., 2.0.0]

**Additional Context**
Any other relevant information.

**Error Messages**
Include any error messages or logs.
```

## Feature Requests

### Before Requesting

1. **Check existing issues** for similar requests
2. **Consider the scope** - is it appropriate for this project?
3. **Think about implementation** - how would it work?

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature.

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Implementation**
How do you think this could be implemented?

**Alternatives Considered**
Other ways to solve this problem.

**Additional Context**
Any other relevant information.
```

## Testing Guidelines

### Manual Testing

1. **Basic Functionality**
   - Audio file loading
   - Transcription process
   - Speaker mapping
   - Timestamp toggling
   - File saving

2. **Error Handling**
   - Invalid API keys
   - Network errors
   - Corrupted audio files
   - Missing dependencies

3. **UI Testing**
   - Menu functionality
   - Keyboard shortcuts
   - Window resizing
   - Dialog interactions

### Audio File Testing

Test with various audio formats and qualities:
- **Formats**: MP3, WAV, OGG
- **Quality**: Different bitrates and sample rates
- **Duration**: Short (< 1 min) to long (> 1 hour)
- **Speakers**: Single speaker to multiple speakers
- **Audio Quality**: Clear to noisy audio

### API Testing

When testing API integrations:
- Use test API keys (not production)
- Test rate limiting scenarios
- Verify error handling for API failures
- Test with different content types

## Documentation

### Types of Documentation

1. **Code Documentation**: Docstrings and comments
2. **User Documentation**: README.md and guides
3. **Developer Documentation**: CONTRIBUTING.md and API docs
4. **Setup Documentation**: Installation and configuration guides

### Documentation Standards

- **Clear and Concise**: Easy to understand
- **Up-to-Date**: Reflects current functionality
- **Examples**: Include code examples where helpful
- **Screenshots**: Visual aids for UI features

### Updating Documentation

When making changes that affect documentation:
1. Update relevant markdown files
2. Include documentation updates in your PR
3. Test documentation instructions
4. Consider if new documentation is needed

## Code Review Process

### For Contributors

- Be responsive to feedback
- Make requested changes promptly
- Ask questions if feedback is unclear
- Test suggested changes

### For Reviewers

- Be constructive and helpful
- Explain reasoning for requested changes
- Test the changes if possible
- Approve when ready

## Community Guidelines

### Be Respectful

- Use inclusive language
- Be patient with new contributors
- Provide constructive feedback
- Help others learn and grow

### Communication

- Use GitHub issues for public discussions
- Tag relevant people when needed
- Be clear and specific in communications
- Follow up on conversations

## Getting Help

### Resources

- **README.md**: Main documentation
- **API_SETUP_GUIDE.md**: API configuration help
- **GitHub Issues**: Search existing issues
- **Code Comments**: Inline documentation

### Asking for Help

When you need help:
1. Search existing documentation
2. Look through GitHub issues
3. Create a new issue with detailed information
4. Be specific about what you've tried

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

## Questions?

If you have questions not covered in this guide:
1. Check the main README.md
2. Search GitHub issues
3. Create a new issue with the "question" label
4. Contact the maintainer directly:
   - **Mark Rizzn Hopkins**: guesswho@rizzn.com
   - **Twitter**: [@rizzn](https://twitter.com/rizzn)
   - **GitHub**: [@actuallyrizzn](https://github.com/actuallyrizzn)

Thank you for contributing to RizzScript!