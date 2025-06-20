#!/bin/bash

# Plist Converter - Bash Wrapper Script
# A convenient wrapper around the Python plist converter tool

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/plist_converter.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if Python script exists
check_python_script() {
    if [[ ! -f "$PYTHON_SCRIPT" ]]; then
        print_error "Python script not found: $PYTHON_SCRIPT"
        exit 1
    fi
}

# Function to check Python installation
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
}

# Function to check PyYAML installation
check_pyyaml() {
    if ! python3 -c "import yaml" 2>/dev/null; then
        print_warning "PyYAML is not installed. YAML conversion will be unavailable."
        print_info "Install with: pip3 install PyYAML"
        return 1
    fi
    return 0
}

# Function to display usage information
show_usage() {
    cat << EOF
Plist Converter - Convert .plist files to JSON, XML, and YAML formats

USAGE:
    $(basename "$0") [OPTIONS] <plist_files...>

OPTIONS:
    -j, --json          Convert to JSON format
    -x, --xml           Convert to XML format
    -y, --yaml          Convert to YAML format (requires PyYAML)
    -a, --all           Convert to all supported formats
    -o, --output-dir    Output directory for converted files
    -h, --help          Show this help message
    -v, --version       Show version information
    --install-deps      Install Python dependencies

EXAMPLES:
    $(basename "$0") --json --xml file.plist
    $(basename "$0") --all *.plist
    $(basename "$0") --yaml --output-dir ./converted file.plist
    $(basename "$0") -j -x -y file1.plist file2.plist

NOTES:
    - Supports both binary and XML plist files as input
    - Output files are created with appropriate extensions (.json, .xml, .yaml)
    - If no output directory is specified, files are saved in the same location as input

EOF
}

# Function to install Python dependencies
install_dependencies() {
    print_info "Installing Python dependencies..."
    
    if command -v pip3 &> /dev/null; then
        pip3 install PyYAML
        print_success "Dependencies installed successfully"
    elif command -v pip &> /dev/null; then
        pip install PyYAML
        print_success "Dependencies installed successfully"
    else
        print_error "pip is not available. Please install PyYAML manually:"
        print_info "  pip3 install PyYAML"
        exit 1
    fi
}

# Function to convert arguments to Python script format
convert_args() {
    local python_args=()
    local files=()
    local output_dir=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -j|--json)
                python_args+=("--json")
                shift
                ;;
            -x|--xml)
                python_args+=("--xml")
                shift
                ;;
            -y|--yaml)
                python_args+=("--yaml")
                shift
                ;;
            -a|--all)
                python_args+=("--all")
                shift
                ;;
            -o|--output-dir)
                if [[ -n "$2" && "$2" != -* ]]; then
                    python_args+=("--output-dir" "$2")
                    shift 2
                else
                    print_error "Option --output-dir requires a directory path"
                    exit 1
                fi
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--version)
                python3 "$PYTHON_SCRIPT" --version
                exit 0
                ;;
            --install-deps)
                install_dependencies
                exit 0
                ;;
            -*)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                # Check if it's a plist file
                if [[ "$1" == *.plist ]]; then
                    files+=("$1")
                else
                    print_warning "File does not have .plist extension: $1"
                    files+=("$1")
                fi
                shift
                ;;
        esac
    done
    
    # Check if any files were provided
    if [[ ${#files[@]} -eq 0 ]]; then
        print_error "No plist files specified"
        show_usage
        exit 1
    fi
    
    # Check if any format was specified
    if [[ ${#python_args[@]} -eq 0 ]] || ! printf '%s\n' "${python_args[@]}" | grep -qE '^(--json|--xml|--yaml|--all)$'; then
        print_error "No output format specified. Use --json, --xml, --yaml, or --all"
        show_usage
        exit 1
    fi
    
    # Run the Python script
    python3 "$PYTHON_SCRIPT" "${python_args[@]}" "${files[@]}"
}

# Function to handle file expansion
expand_files() {
    local expanded_files=()
    
    for arg in "$@"; do
        if [[ "$arg" == *.plist ]]; then
            # Check if it's a glob pattern that didn't match
            if [[ "$arg" == *"*"* ]] && [[ ! -f "$arg" ]]; then
                # Expand the glob
                local matches=()
                while IFS= read -r -d '' file; do
                    matches+=("$file")
                done < <(find . -maxdepth 1 -name "$arg" -print0 2>/dev/null)
                
                if [[ ${#matches[@]} -eq 0 ]]; then
                    print_warning "No files match pattern: $arg"
                else
                    expanded_files+=("${matches[@]}")
                fi
            else
                expanded_files+=("$arg")
            fi
        else
            expanded_files+=("$arg")
        fi
    done
    
    printf '%s\n' "${expanded_files[@]}"
}

# Main function
main() {
    # Check if no arguments provided
    if [[ $# -eq 0 ]]; then
        show_usage
        exit 1
    fi
    
    # Perform checks
    check_python
    check_python_script
    
    # Check for PyYAML if YAML conversion might be needed
    for arg in "$@"; do
        if [[ "$arg" == "--yaml" || "$arg" == "-y" || "$arg" == "--all" || "$arg" == "-a" ]]; then
            check_pyyaml
            break
        fi
    done
    
    # Convert and run
    convert_args "$@"
}

# Run main function with all arguments
main "$@"
