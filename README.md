# RizzScript - AI-Powered Audio Transcription Suite

**RizzScript** is a professional-grade PyQt5 desktop application designed for intelligent audio transcription, speaker diarization, and automated speaker identification. It combines the power of AssemblyAI's transcription services with OpenAI's language models to deliver accurate, speaker-attributed transcripts with intelligent name mapping.

## 🚀 Key Features

### Core Transcription Capabilities
- **Multi-format Audio Support**: Processes `.mp3`, `.wav`, and `.ogg` audio files
- **Advanced Speaker Diarization**: Automatically separates and labels different speakers
- **High-Quality Transcription**: Powered by AssemblyAI's state-of-the-art speech-to-text engine
- **Real-time Processing**: Background transcription with progress tracking

### AI-Powered Speaker Intelligence
- **Automatic Speaker Identification**: Uses OpenAI's language models to intelligently map speaker labels to real names
- **Context-Aware Analysis**: Analyzes conversation patterns, dialogue structure, and contextual clues
- **Candidate Name Suggestions**: Accepts user-provided name lists for more accurate mapping
- **Interactive Progress Logging**: Real-time feedback during AI processing

### Professional Editing Suite
- **Dynamic Timestamp Management**: Toggle timestamps on/off with precise `[HH:MM:SS]` formatting
- **Advanced Search & Replace**: Powerful text manipulation tools
- **Professional Text Editor**: Fixed-width font, word wrap controls, and standard editing shortcuts
- **File Management**: Save/load transcript files in standard text format

### Enterprise-Ready Architecture
- **Fully Asynchronous Processing**: No UI blocking during intensive operations
- **Secure API Key Management**: Encrypted storage in local configuration files
- **Modular Design**: Clean separation between UI, API services, and business logic
- **Cross-Platform Compatibility**: Runs on Windows, macOS, and Linux

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended for large audio files)
- **Storage**: At least 1GB free space for application and temporary files

### Required API Keys
- **AssemblyAI API Key**: For audio transcription and speaker diarization
  - Sign up at [AssemblyAI](https://www.assemblyai.com/)
  - Free tier available with usage limits
- **OpenAI API Key**: For intelligent speaker name mapping (optional but recommended)
  - Sign up at [OpenAI](https://platform.openai.com/)
  - Pay-per-use pricing model

## 🔧 Installation

### Method 1: Python Installation (Recommended for Development)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/actuallyrizzn/rizzscript.git
   cd rizzscript
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install pyqt5 assemblyai openai
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

### Method 2: Standalone Executable (Windows)

1. Download the latest `RizzScript.exe` from the `dist/` directory
2. Run the executable directly - no installation required
3. The application will create a `config.json` file on first run

## ⚙️ Configuration

### First-Time Setup

1. **Launch RizzScript**
2. **Access Settings**: Go to `File > Settings`
3. **Enter API Keys**:
   - **AssemblyAI API Key**: Required for all transcription features
   - **OpenAI API Key**: Optional, enables AI-powered speaker mapping
4. **Save Configuration**: Keys are securely stored in `config.json`

### Configuration File Structure

The `config.json` file stores your API credentials:
```json
{
    "assemblyai_api_key": "your_assemblyai_key_here",
    "openai_api_key": "your_openai_key_here"
}
```

**Security Note**: This file contains sensitive API keys. Ensure it's not shared or committed to version control.

## 📖 Usage Guide

### Basic Transcription Workflow

1. **Open Audio File**
   - `File > Open Audio File`
   - Select your audio file (`.mp3`, `.wav`, or `.ogg`)
   - Wait for upload and processing

2. **Review Initial Transcript**
   - Transcript appears with generic speaker labels (`Speaker A`, `Speaker B`, etc.)
   - Each speaker's dialogue is clearly separated

3. **Speaker Mapping** (Optional but Recommended)
   - The Speaker Mapping panel opens automatically for multi-speaker audio
   - Enter candidate names if known (comma-separated)
   - Click "Attempt to Autopopulate" for AI-powered name suggestions
   - Review and modify suggested mappings
   - Click "Apply Changes" to update the transcript

4. **Timestamp Management**
   - Click "Apply Timestamps" to add precise timing information
   - Format: `[HH:MM:SS] Speaker Name: Dialogue`
   - Click again to remove timestamps for clean text

5. **Final Editing**
   - Use the built-in editor for manual corrections
   - Access `Edit > Search and Replace` for bulk changes
   - `View > Toggle Word Wrap` for display preferences

6. **Save Your Work**
   - `File > Save` to export as `.txt` file
   - Compatible with all text editors and document processors

### Advanced Features

#### AI-Powered Speaker Analysis
The application uses sophisticated analysis to identify speakers:
- **Dialogue Pattern Recognition**: Analyzes who initiates vs. responds
- **Contextual Clue Detection**: Looks for name mentions and direct addresses
- **Conversation Role Analysis**: Identifies leaders, participants, and interaction patterns
- **Linguistic Pattern Matching**: Recognizes unique vocabulary and speech patterns

#### Progress Monitoring
- **Real-time Status Updates**: Track transcription progress in the status bar
- **Detailed AI Logging**: Watch the AI reasoning process during speaker mapping
- **Error Handling**: Clear feedback for API issues or processing errors

#### Keyboard Shortcuts
| Action | Shortcut | Description |
|--------|----------|-------------|
| Save | `Ctrl+S` | Save current transcript |
| Copy | `Ctrl+C` | Copy selected text |
| Cut | `Ctrl+X` | Cut selected text |
| Paste | `Ctrl+V` | Paste from clipboard |

## 🏗️ Development & Building

### Development Setup

1. **Clone and Setup Environment**
   ```bash
   git clone https://github.com/actuallyrizzn/rizzscript.git
   cd rizzscript
   python -m venv dev-env
   source dev-env/bin/activate  # Windows: dev-env\Scripts\activate
   ```

2. **Install Development Dependencies**
   ```bash
   pip install pyqt5 assemblyai openai pyinstaller
   ```

3. **Run in Development Mode**
   ```bash
   python app.py
   ```

### Building Executables

#### Windows Executable
```bash
pyinstaller --onefile --windowed --name "RizzScript" app.py
```

#### Using the Provided Spec File
```bash
pyinstaller RizzScript.spec
```

The spec file includes optimized settings:
- **Single File Distribution**: Everything bundled into one executable
- **Windowed Mode**: No console window for end users
- **UPX Compression**: Reduced file size
- **Optimized Build**: Faster startup and smaller footprint

### Project Structure

```
rizzscript/
├── app.py                 # Main application entry point
├── RizzScript.spec        # PyInstaller build configuration
├── config.json           # API key storage (auto-generated)
├── README.md             # This documentation
├── .gitignore           # Git ignore rules
├── dist/                # Built executables and distribution files
│   ├── RizzScript.exe   # Windows executable
│   ├── RizzScript.rar   # Compressed distribution
│   └── config.json      # Example configuration
├── build/               # Temporary build files (auto-generated)
└── old/                 # Legacy versions and backups
    └── app.py          # Previous tkinter-based version
```

## 🔧 Technical Architecture

### Core Components

#### `MainWindow` Class
- **Primary GUI Controller**: Manages the main application interface
- **Menu System**: File operations, editing tools, and view controls
- **Event Coordination**: Handles user interactions and API responses
- **Progress Management**: Real-time feedback and status updates

#### `TranscriptionThread` Class
- **Background Processing**: Non-blocking audio transcription
- **AssemblyAI Integration**: Manages API calls and response handling
- **Speaker Diarization**: Automatic speaker separation and labeling
- **Error Handling**: Robust exception management and user feedback

#### `MappingWorker` Class
- **AI Processing**: OpenAI API integration for speaker identification
- **Contextual Analysis**: Sophisticated prompt engineering for accurate results
- **Asynchronous Operation**: Non-blocking AI processing
- **Result Parsing**: JSON extraction and validation

#### `SpeakerMappingWidget` Class
- **Interactive Mapping Interface**: User-friendly speaker name assignment
- **Candidate Management**: Handles user-provided name suggestions
- **Progress Visualization**: Real-time AI processing feedback
- **Validation Controls**: Ensures mapping accuracy before application

### API Integrations

#### AssemblyAI Integration
- **Endpoint**: AssemblyAI Speech-to-Text API
- **Features Used**: 
  - High-quality transcription
  - Speaker diarization
  - Timestamp precision
- **Configuration**: Speaker labels enabled by default
- **Error Handling**: Comprehensive exception management

#### OpenAI Integration
- **Model**: GPT-4 (via `o1` model identifier)
- **Use Case**: Contextual speaker identification
- **Prompt Engineering**: Sophisticated context analysis
- **Output Format**: Structured JSON for reliable parsing

### Data Flow

1. **Audio Input** → AssemblyAI API → **Raw Transcript with Speaker Labels**
2. **Transcript Analysis** → OpenAI API → **Speaker Name Suggestions**
3. **User Interaction** → **Final Speaker Mapping** → **Updated Transcript**
4. **Timestamp Processing** → **Formatted Output** → **File Export**

## 🚨 Troubleshooting

### Common Issues

#### "AssemblyAI API key is missing"
- **Cause**: No API key configured
- **Solution**: Go to `File > Settings` and enter your AssemblyAI API key

#### "Transcription Failed"
- **Possible Causes**:
  - Invalid or expired API key
  - Unsupported audio format
  - Network connectivity issues
  - File corruption
- **Solutions**:
  - Verify API key validity
  - Convert audio to supported format
  - Check internet connection
  - Try a different audio file

#### "Auto Mapping Error"
- **Possible Causes**:
  - Missing OpenAI API key
  - Insufficient OpenAI credits
  - Network issues
- **Solutions**:
  - Configure OpenAI API key in settings
  - Check OpenAI account balance
  - Use manual speaker mapping as fallback

#### Application Won't Start
- **Possible Causes**:
  - Missing Python dependencies
  - Incompatible Python version
  - Corrupted installation
- **Solutions**:
  - Reinstall dependencies: `pip install pyqt5 assemblyai openai`
  - Verify Python 3.8+ is installed
  - Try running from a fresh virtual environment

### Performance Optimization

#### Large Audio Files
- **Recommendation**: Files larger than 100MB may take significant time
- **Tip**: Consider splitting large files into smaller segments
- **Memory**: Ensure adequate RAM for processing

#### API Rate Limits
- **AssemblyAI**: Respect usage quotas based on your plan
- **OpenAI**: Monitor token usage to avoid overage charges

## 🤝 Contributing

### Development Guidelines

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
3. **Follow Code Style**: PEP 8 compliance
4. **Add Tests**: Ensure new features include appropriate tests
5. **Update Documentation**: Keep README and inline docs current
6. **Submit Pull Request**: Include detailed description of changes

### Code Style Standards
- **Python**: Follow PEP 8 guidelines
- **Qt/PyQt5**: Use Qt naming conventions for UI elements
- **Comments**: Document complex algorithms and API integrations
- **Error Handling**: Implement comprehensive exception management

## 📄 License

This project is licensed under the **Creative Commons Attribution-ShareAlike 4.0 International License**. See the `LICENSE` file for detailed terms and conditions.

You are free to share, adapt, and build upon this work, even commercially, as long as you provide appropriate attribution and distribute any derivatives under the same license.

### Third-Party Licenses
- **PyQt5**: GPL/Commercial License
- **AssemblyAI Python SDK**: MIT License
- **OpenAI Python SDK**: MIT License

## 🙏 Acknowledgments

- **Mark Rizzn Hopkins**: Creator and lead developer of RizzScript
- **AssemblyAI**: For providing high-quality speech-to-text and diarization services
- **OpenAI**: For advanced language model capabilities
- **Qt/PyQt5**: For the robust cross-platform GUI framework
- **Python Community**: For the extensive ecosystem of tools and libraries

## 📞 Support

### Getting Help
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Documentation**: Refer to this README and inline code documentation
- **API Documentation**: 
  - [AssemblyAI Docs](https://www.assemblyai.com/docs/)
  - [OpenAI API Reference](https://platform.openai.com/docs/)

### Contact
- **Developer**: Mark Rizzn Hopkins
- **Email**: guesswho@rizzn.com
- **Twitter**: [@rizzn](https://twitter.com/rizzn)
- **GitHub**: [@actuallyrizzn](https://github.com/actuallyrizzn)

### Version Information
- **Current Version**: 2.0.0
- **Last Updated**: 2024
- **Compatibility**: Python 3.8+, PyQt5, Windows/macOS/Linux

---

**🎉 Ready to Transform Your Audio into Intelligent Transcripts!** 

*RizzScript combines cutting-edge AI with intuitive design to deliver professional transcription results. Whether you're transcribing interviews, meetings, podcasts, or any spoken content, RizzScript provides the accuracy and intelligence you need.*