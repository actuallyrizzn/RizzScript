# Changelog

All notable changes to RizzScript will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation suite
- API setup guide
- Contributing guidelines
- Requirements.txt for dependency management

## [2.0.0] - 2024

### Added
- **Complete PyQt5 Rewrite**: Migrated from tkinter to PyQt5 for modern UI
- **AI-Powered Speaker Identification**: OpenAI integration for intelligent speaker mapping
- **Professional Text Editor**: Fixed-width font, advanced editing features
- **Dynamic Timestamp Management**: Toggle timestamps on/off with precise formatting
- **Asynchronous Processing**: Non-blocking UI during transcription and AI processing
- **Interactive Progress Logging**: Real-time feedback during AI analysis
- **Advanced Speaker Mapping Panel**: User-friendly interface for speaker name assignment
- **Candidate Name Suggestions**: Accept user-provided names for better AI mapping
- **Contextual Analysis**: Sophisticated AI prompts for speaker identification
- **Professional Menu System**: Standard file operations and editing tools
- **Search and Replace Functionality**: Powerful text manipulation tools
- **Word Wrap Controls**: Toggle word wrapping for better text viewing
- **Status Bar with Progress**: Real-time status updates and progress indicators
- **Secure Configuration Management**: Local storage of API keys in config.json
- **Error Handling**: Comprehensive exception management and user feedback
- **Keyboard Shortcuts**: Standard shortcuts for copy, cut, paste, save operations
- **Dockable Speaker Panel**: Flexible UI layout with movable panels
- **Settings Dialog**: Easy API key configuration interface
- **File Save/Load**: Export transcripts as text files

### Changed
- **Complete UI Overhaul**: Modern PyQt5 interface replacing tkinter
- **Enhanced Audio Processing**: Improved AssemblyAI integration with better error handling
- **Improved User Experience**: More intuitive workflow and better visual feedback
- **Better Thread Management**: Robust background processing with proper cleanup
- **Enhanced Speaker Detection**: More accurate speaker separation and labeling

### Technical Improvements
- **Modular Architecture**: Clean separation of concerns with dedicated classes
- **Better Exception Handling**: Graceful error recovery and user notifications
- **Improved Memory Management**: Efficient handling of large audio files
- **Enhanced API Integration**: Robust error handling for external services
- **Cross-Platform Compatibility**: Better support for Windows, macOS, and Linux

### Security
- **API Key Protection**: Secure local storage and .gitignore protection
- **Input Validation**: Proper validation of user inputs and API responses
- **Error Message Sanitization**: Safe error reporting without exposing sensitive data

## [1.0.0] - Previous Version

### Added
- **Basic Transcription**: AssemblyAI integration for speech-to-text
- **Speaker Diarization**: Basic speaker separation
- **Simple UI**: tkinter-based interface
- **File Operations**: Basic audio file loading and text saving
- **Configuration**: Basic API key management

### Features
- Audio file transcription (MP3, WAV, OGG)
- Speaker separation and labeling
- Basic text editing
- Progress bar for transcription
- Simple settings dialog

---

## Version History Summary

| Version | Release Date | Key Features |
|---------|-------------|--------------|
| 2.0.0   | 2024        | PyQt5 rewrite, AI speaker mapping, advanced UI |
| 1.0.0   | Previous    | Basic transcription, tkinter UI, speaker diarization |

---

## Future Roadmap

### Planned Features (v2.1.0)
- **Audio Format Conversion**: Built-in support for additional formats
- **Batch Processing**: Process multiple files simultaneously
- **Export Options**: Multiple output formats (JSON, SRT, VTT)
- **Advanced Search**: Regex support in search functionality
- **Themes**: Dark mode and custom UI themes

### Planned Features (v2.2.0)
- **Cloud Storage Integration**: Direct save to cloud services
- **Collaboration Features**: Share and collaborate on transcripts
- **Advanced AI Features**: Summary generation, key point extraction
- **Performance Optimization**: Faster processing for large files
- **Plugin System**: Extensible architecture for custom features

### Long-term Goals (v3.0.0)
- **Real-time Transcription**: Live audio processing
- **Multi-language Support**: International language support
- **Advanced Analytics**: Speaker statistics and analysis
- **API Server Mode**: Use RizzScript as a transcription service
- **Machine Learning**: Custom speaker identification models

---

## Migration Guide

### Upgrading from v1.0.0 to v2.0.0

1. **New Dependencies**: Install PyQt5 and OpenAI packages
   ```bash
   pip install pyqt5 openai
   ```

2. **Configuration Changes**: 
   - Old config files are not compatible
   - Reconfigure API keys in the new settings dialog

3. **UI Changes**:
   - Complete interface redesign
   - New speaker mapping workflow
   - Enhanced editing features

4. **New Features Available**:
   - AI-powered speaker identification
   - Dynamic timestamp management
   - Advanced text editing tools

---

## Support and Feedback

### Reporting Issues
- Use GitHub Issues for bug reports
- Include version number and system information
- Provide detailed reproduction steps

### Feature Requests
- Submit feature requests via GitHub Issues
- Use the "enhancement" label
- Describe use case and expected behavior

### Community
- Contribute to discussions in GitHub Issues
- Submit pull requests for improvements
- Help improve documentation

### Contact
- **Developer**: Mark Rizzn Hopkins
- **Email**: guesswho@rizzn.com
- **Twitter**: [@rizzn](https://twitter.com/rizzn)
- **GitHub**: [@actuallyrizzn](https://github.com/actuallyrizzn)

---

**Note**: This changelog is maintained manually. For a complete list of changes, see the [GitHub commit history](https://github.com/actuallyrizzn/rizzscript/commits).