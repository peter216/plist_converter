# Plist Converter

A command-line tool for converting `.plist` files to JSON, XML, and YAML formats. The tool supports both binary and XML plist files as input and provides both Python and Bash interfaces for maximum flexibility.

## Features

- ✅ Convert `.plist` files to JSON, XML, and YAML formats
- ✅ Support for both binary and XML plist files as input
- ✅ Batch conversion of multiple files
- ✅ Cross-platform compatibility (Linux, macOS, Windows)
- ✅ Command-line interface with comprehensive options
- ✅ Bash wrapper script for Unix-like systems
- ✅ Detailed error handling and status reporting
- ✅ Preserve data types and structure during conversion

## Requirements

- Python 3.6 or higher
- PyYAML (for YAML conversion support)

### Installation of Dependencies

```bash
# Install PyYAML for YAML support
pip3 install PyYAML

# Or use the bash wrapper to install dependencies
./plist_converter.sh --install-deps
