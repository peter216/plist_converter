#!/usr/bin/env python3
"""
Plist Converter Tool

A command-line utility to convert .plist files to JSON, XML, and YAML formats.
Supports both binary and XML plist files as input.
"""

import argparse
import json
import os
import plistlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    yaml = None
    print("Warning: PyYAML not installed. YAML conversion will be unavailable.")
    print("Install with: pip install PyYAML")


class PlistConverter:
    """Main converter class for handling plist file conversions."""
    
    def __init__(self):
        self.supported_formats = ['json', 'xml', 'yaml']
        if yaml is None:
            self.supported_formats.remove('yaml')
    
    def load_plist(self, file_path: str) -> Dict[str, Any]:
        """
        Load a plist file (binary or XML format).
        
        Args:
            file_path: Path to the plist file
            
        Returns:
            Dictionary containing the plist data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not a valid plist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                return plistlib.load(f)
        except Exception as e:
            raise ValueError(f"Invalid plist file '{file_path}': {str(e)}")
    
    def convert_to_json(self, data: Dict[str, Any], output_path: str) -> None:
        """
        Convert plist data to JSON format.
        
        Args:
            data: Dictionary containing plist data
            output_path: Output file path
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            raise ValueError(f"Failed to write JSON file '{output_path}': {str(e)}")
    
    def convert_to_xml(self, data: Dict[str, Any], output_path: str) -> None:
        """
        Convert plist data to XML format.
        
        Args:
            data: Dictionary containing plist data
            output_path: Output file path
        """
        try:
            # Use plistlib to write as XML plist format
            with open(output_path, 'wb') as f:
                plistlib.dump(data, f, fmt=plistlib.FMT_XML)
        except Exception as e:
            raise ValueError(f"Failed to write XML file '{output_path}': {str(e)}")
    
    def convert_to_yaml(self, data: Dict[str, Any], output_path: str) -> None:
        """
        Convert plist data to YAML format.
        
        Args:
            data: Dictionary containing plist data
            output_path: Output file path
        """
        if yaml is None:
            raise ValueError("PyYAML is not installed. Cannot convert to YAML format.")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            raise ValueError(f"Failed to write YAML file '{output_path}': {str(e)}")
    
    def get_output_path(self, input_path: str, format_type: str, output_dir: str = None) -> str:
        """
        Generate output file path based on input file and format.
        
        Args:
            input_path: Path to input file
            format_type: Target format (json, xml, yaml)
            output_dir: Optional output directory
            
        Returns:
            Output file path
        """
        input_file = Path(input_path)
        base_name = input_file.stem
        
        if output_dir:
            output_path = Path(output_dir) / f"{base_name}.{format_type}"
        else:
            output_path = input_file.parent / f"{base_name}.{format_type}"
        
        return str(output_path)
    
    def convert_file(self, input_path: str, formats: List[str], output_dir: str = None) -> Dict[str, bool]:
        """
        Convert a single plist file to specified formats.
        
        Args:
            input_path: Path to input plist file
            formats: List of target formats
            output_dir: Optional output directory
            
        Returns:
            Dictionary with format as key and success status as value
        """
        results = {}
        
        try:
            # Load the plist file
            print(f"Loading: {input_path}")
            data = self.load_plist(input_path)
            
            # Convert to each requested format
            for format_type in formats:
                if format_type not in self.supported_formats:
                    print(f"  ❌ {format_type.upper()}: Unsupported format")
                    results[format_type] = False
                    continue
                
                try:
                    output_path = self.get_output_path(input_path, format_type, output_dir)
                    
                    if format_type == 'json':
                        self.convert_to_json(data, output_path)
                    elif format_type == 'xml':
                        self.convert_to_xml(data, output_path)
                    elif format_type == 'yaml':
                        self.convert_to_yaml(data, output_path)
                    
                    print(f"  ✅ {format_type.upper()}: {output_path}")
                    results[format_type] = True
                    
                except Exception as e:
                    print(f"  ❌ {format_type.upper()}: {str(e)}")
                    results[format_type] = False
            
        except Exception as e:
            print(f"  ❌ Failed to load file: {str(e)}")
            for format_type in formats:
                results[format_type] = False
        
        return results
    
    def convert_files(self, input_paths: List[str], formats: List[str], output_dir: str = None) -> None:
        """
        Convert multiple plist files to specified formats.
        
        Args:
            input_paths: List of input plist file paths
            formats: List of target formats
            output_dir: Optional output directory
        """
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"Created output directory: {output_dir}")
            except Exception as e:
                print(f"❌ Failed to create output directory '{output_dir}': {str(e)}")
                return
        
        total_files = len(input_paths)
        successful_conversions = 0
        
        print(f"\nConverting {total_files} file(s) to {', '.join(formats).upper()} format(s)...")
        print("-" * 60)
        
        for i, input_path in enumerate(input_paths, 1):
            print(f"\n[{i}/{total_files}] Processing: {os.path.basename(input_path)}")
            
            results = self.convert_file(input_path, formats, output_dir)
            
            if any(results.values()):
                successful_conversions += 1
        
        print(f"\n{'='*60}")
        print(f"Conversion complete: {successful_conversions}/{total_files} files processed successfully")


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description="Convert .plist files to JSON, XML, and YAML formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file.plist --json --xml
  %(prog)s *.plist --all
  %(prog)s file.plist --yaml --output-dir ./converted
  %(prog)s file1.plist file2.plist --json --xml --yaml
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        help='Plist file(s) to convert'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Convert to JSON format'
    )
    
    parser.add_argument(
        '--xml',
        action='store_true',
        help='Convert to XML format'
    )
    
    parser.add_argument(
        '--yaml',
        action='store_true',
        help='Convert to YAML format (requires PyYAML)'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Convert to all supported formats'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Output directory for converted files (default: same as input)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Determine target formats
    formats = []
    if args.all:
        converter = PlistConverter()
        formats = converter.supported_formats
    else:
        if args.json:
            formats.append('json')
        if args.xml:
            formats.append('xml')
        if args.yaml:
            formats.append('yaml')
    
    if not formats:
        print("❌ Error: No output format specified. Use --json, --xml, --yaml, or --all")
        parser.print_help()
        sys.exit(1)
    
    # Validate input files
    valid_files = []
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"❌ Warning: File not found: {file_path}")
            continue
        if not file_path.lower().endswith('.plist'):
            print(f"❌ Warning: Not a .plist file: {file_path}")
            continue
        valid_files.append(file_path)
    
    if not valid_files:
        print("❌ Error: No valid .plist files found")
        sys.exit(1)
    
    # Perform conversion
    converter = PlistConverter()
    try:
        converter.convert_files(valid_files, formats, args.output_dir)
    except KeyboardInterrupt:
        print("\n❌ Conversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
