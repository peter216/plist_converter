# Plist Converter

## Overview

The Plist Converter is a command-line utility designed to convert macOS property list (.plist) files between different formats including JSON, XML, and YAML. The application provides both Python and Bash interfaces for maximum flexibility and cross-platform compatibility.

## System Architecture

### Core Architecture
- **Language**: Python 3.11+ with optional Bash wrapper
- **Design Pattern**: Object-oriented with a main `PlistConverter` class
- **Input Support**: Both binary and XML plist formats
- **Output Formats**: JSON, XML, YAML
- **Interface**: Command-line tool with argument parsing

### Package Management
- **Primary**: UV package manager with `pyproject.toml` configuration
- **Fallback**: Traditional pip installation for dependencies
- **Dependencies**: PyYAML for YAML format support (optional but recommended)

## Key Components

### 1. Core Converter (`plist_converter.py`)
- **Purpose**: Main Python module containing the conversion logic
- **Key Class**: `PlistConverter` - handles all format transformations
- **Input Handling**: Uses Python's built-in `plistlib` for parsing plist files
- **Error Handling**: Comprehensive exception handling for file operations and format validation

### 2. Bash Wrapper (`plist_converter.sh`)
- **Purpose**: Unix-friendly interface with enhanced user experience
- **Features**: 
  - Colored output for better readability
  - Dependency checking and installation
  - Error reporting with status codes
  - Convenience functions for common operations

### 3. Configuration Files
- **`pyproject.toml`**: Modern Python project configuration
- **`uv.lock`**: Dependency lock file for reproducible builds
- **`.replit`**: Replit-specific configuration for cloud development

## Data Flow

1. **Input**: User provides .plist file path and target format
2. **Parsing**: Application detects and parses binary or XML plist format
3. **Conversion**: Data is transformed to target format (JSON/XML/YAML)
4. **Output**: Converted data is written to specified output file or stdout
5. **Validation**: Error checking ensures successful conversion and proper file handling

## External Dependencies

### Required Dependencies
- **Python 3.11+**: Core runtime environment
- **plistlib**: Built-in Python library for plist parsing (no external dependency)

### Optional Dependencies
- **PyYAML**: Required only for YAML output format support
- **xml.etree.ElementTree**: Built-in Python library for XML processing

### Development Dependencies
- **UV**: Modern Python package manager for dependency management
- **argparse**: Built-in library for command-line argument parsing

## Deployment Strategy

### Local Development
- Uses UV for dependency management and virtual environment handling
- Supports direct Python script execution or Bash wrapper usage
- Cross-platform compatibility (Linux, macOS, Windows)

### Replit Environment
- Configured with Python 3.11 module
- Automatic dependency installation via workflows
- Nix package manager integration for system-level dependencies

### Distribution Options
- Standalone Python script (no installation required)
- Package distribution via pyproject.toml for pip installation
- Bash wrapper for Unix-like systems requiring no Python knowledge

## Changelog
- June 20, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.