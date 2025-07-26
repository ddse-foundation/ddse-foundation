#!/usr/bin/env python3
"""
Copyright (c) 2025 DDSE Foundation
Licensed under the MIT License

TDR Validator - DDSE Compliance Checker

This validator ensures Technical Decision Records (TDRs) comply with DDSE specifications.
It validates YAML frontmatter, required sections, cross-references, and AI context.

Usage:
    python tdr_validator.py <file_or_directory> [--strict] [--output json|text]
    
Example:
    python tdr_validator.py ../tdr-templates/adr-template.md
    python tdr_validator.py ../examples/ --strict --output json
"""

import argparse
import json
import os
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


class TDRValidationError(Exception):
    """Custom exception for TDR validation errors."""
    pass


class TDRValidator:
    """Validates Technical Decision Records against DDSE specifications."""
    
    # TDR type configurations with required sections
    TDR_TYPES = {
        'MDD': {
            'name': 'Major Design Decision',
            'required_sections': [
                'Status', 'Context', 'Decision', 'Rationale', 
                'Consequences', 'Implementation', 'Alternatives Considered'
            ],
            'optional_sections': [
                'Assumptions', 'Constraints', 'Risks', 'Timeline',
                'Success Metrics', 'Review Schedule'
            ]
        },
        'ADR': {
            'name': 'Architectural Decision Record',
            'required_sections': [
                'Status', 'Context', 'Decision', 'Consequences'
            ],
            'optional_sections': [
                'Rationale', 'Alternatives Considered', 'Implementation',
                'Assumptions', 'Constraints', 'Related Decisions'
            ]
        },
        'EDR': {
            'name': 'Engineering Decision Record',
            'required_sections': [
                'Status', 'Context', 'Decision', 'Implementation'
            ],
            'optional_sections': [
                'Rationale', 'Consequences', 'Alternatives Considered',
                'Technical Details', 'Testing Approach', 'Performance Impact'
            ]
        },
        'IDR': {
            'name': 'Implementation Decision Record',
            'required_sections': [
                'Status', 'Context', 'Decision', 'Implementation'
            ],
            'optional_sections': [
                'Rationale', 'Code Examples', 'Testing Notes',
                'Performance Notes', 'Dependencies', 'Rollback Plan'
            ]
        },
        'TDM': {
            'name': 'Technical Decision Memo',
            'required_sections': [
                'Context', 'Decision', 'Rationale'
            ],
            'optional_sections': [
                'Implementation', 'Consequences', 'Next Steps',
                'Follow-up Required', 'Related Work'
            ]
        }
    }
    
    # Valid status values
    VALID_STATUSES = [
        'proposed', 'accepted', 'rejected', 'superseded', 
        'deprecated', 'under-review', 'implemented'
    ]
    
    def __init__(self, strict_mode: bool = False):
        """Initialize the validator.
        
        Args:
            strict_mode: If True, enforce stricter validation rules
        """
        self.strict_mode = strict_mode
        self.errors = []
        self.warnings = []
        
    def validate_file(self, file_path: Union[str, Path]) -> Dict:
        """Validate a single TDR file.
        
        Args:
            file_path: Path to the TDR file
            
        Returns:
            Dictionary containing validation results
        """
        file_path = Path(file_path)
        self.errors = []
        self.warnings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            return self._create_error_result(f"File not found: {file_path}")
        except UnicodeDecodeError:
            return self._create_error_result(f"Invalid UTF-8 encoding: {file_path}")
        
        # Parse frontmatter and content
        frontmatter, markdown_content = self._parse_frontmatter(content)
        
        if not frontmatter:
            self.errors.append("Missing or invalid YAML frontmatter")
            return self._create_result(file_path, frontmatter, {})
        
        # Validate frontmatter
        self._validate_frontmatter(frontmatter)
        
        # Parse sections
        sections = self._parse_sections(markdown_content)
        
        # Validate sections based on TDR type
        if 'type' in frontmatter:
            self._validate_sections(frontmatter['type'], sections)
        
        # Additional validations
        self._validate_cross_references(markdown_content)
        self._validate_ai_context(frontmatter)
        
        return self._create_result(file_path, frontmatter, sections)
    
    def validate_directory(self, dir_path: Union[str, Path]) -> List[Dict]:
        """Validate all TDR files in a directory.
        
        Args:
            dir_path: Path to directory containing TDR files
            
        Returns:
            List of validation results for each file
        """
        dir_path = Path(dir_path)
        if not dir_path.is_dir():
            return [self._create_error_result(f"Directory not found: {dir_path}")]
        
        results = []
        tdr_files = list(dir_path.glob("*.md"))
        
        if not tdr_files:
            return [self._create_error_result(f"No .md files found in: {dir_path}")]
        
        for file_path in sorted(tdr_files):
            results.append(self.validate_file(file_path))
        
        return results
    
    def _parse_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Parse YAML frontmatter from markdown content.
        
        Args:
            content: Full markdown content
            
        Returns:
            Tuple of (frontmatter dict, remaining markdown content)
        """
        if not content.startswith('---\n'):
            return None, content
        
        try:
            # Find the closing ---
            end_marker = content.find('\n---\n', 4)
            if end_marker == -1:
                return None, content
            
            yaml_content = content[4:end_marker]
            markdown_content = content[end_marker + 5:]
            
            frontmatter = yaml.safe_load(yaml_content)
            return frontmatter, markdown_content
            
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML frontmatter: {e}")
            return None, content
    
    def _validate_frontmatter(self, frontmatter: Dict) -> None:
        """Validate YAML frontmatter structure and content.
        
        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        required_fields = ['type', 'title', 'status', 'date', 'decision_owner']
        
        for field in required_fields:
            if field not in frontmatter:
                self.errors.append(f"Missing required frontmatter field: {field}")
        
        # Validate TDR type
        if 'type' in frontmatter:
            tdr_type = frontmatter['type'].upper()
            if tdr_type not in self.TDR_TYPES:
                self.errors.append(f"Invalid TDR type: {frontmatter['type']}. "
                                 f"Valid types: {', '.join(self.TDR_TYPES.keys())}")
        
        # Validate status
        if 'status' in frontmatter:
            status = frontmatter['status'].lower()
            if status not in self.VALID_STATUSES:
                self.errors.append(f"Invalid status: {frontmatter['status']}. "
                                 f"Valid statuses: {', '.join(self.VALID_STATUSES)}")
        
        # Validate date format
        if 'date' in frontmatter:
            try:
                datetime.fromisoformat(str(frontmatter['date']))
            except ValueError:
                self.errors.append(f"Invalid date format: {frontmatter['date']}. "
                                 "Use ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS")
        
        # Validate decision-owner
        if 'decision_owner' in frontmatter:
            if not isinstance(frontmatter['decision_owner'], str):
                self.errors.append("decision_owner must be a string")
            elif not frontmatter['decision_owner'].strip():
                self.errors.append("decision_owner cannot be empty")
        
        # Validate optional fields
        optional_fields = ['tdr_id', 'supersedes', 'reviewers']
        for field in ['tdr_id', 'supersedes']:
            if field in frontmatter and not isinstance(frontmatter[field], (int, str)):
                try:
                    int(frontmatter[field]) if field != 'tdr_id' else str(frontmatter[field])
                except (ValueError, TypeError):
                    self.warnings.append(f"Field '{field}' should be numeric or string")
        
        # Validate reviewers if present
        if 'reviewers' in frontmatter:
            if not isinstance(frontmatter['reviewers'], list):
                self.warnings.append("reviewers should be a list")
    
    def _parse_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown sections from content.
        
        Args:
            content: Markdown content without frontmatter
            
        Returns:
            Dictionary mapping section names to content
        """
        sections = {}
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Check for section headers (## or ###)
            header_match = re.match(r'^(#{2,3})\s+(.+)$', line)
            if header_match:
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = header_match.group(2).strip()
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _validate_sections(self, tdr_type: str, sections: Dict[str, str]) -> None:
        """Validate sections based on TDR type requirements.
        
        Args:
            tdr_type: Type of TDR (MDD, ADR, etc.)
            sections: Dictionary of section names to content
        """
        tdr_type = tdr_type.upper()
        if tdr_type not in self.TDR_TYPES:
            return
        
        config = self.TDR_TYPES[tdr_type]
        required_sections = config['required_sections']
        
        # Check for required sections
        for required_section in required_sections:
            if required_section not in sections:
                self.errors.append(f"Missing required section: {required_section}")
            elif not sections[required_section].strip():
                self.errors.append(f"Required section is empty: {required_section}")
        
        # In strict mode, warn about unknown sections
        if self.strict_mode:
            known_sections = set(required_sections + config['optional_sections'])
            for section_name in sections.keys():
                if section_name not in known_sections:
                    self.warnings.append(f"Unknown section for {tdr_type}: {section_name}")
    
    def _validate_cross_references(self, content: str) -> None:
        """Validate cross-references to other TDRs.
        
        Args:
            content: Full markdown content
        """
        # Look for TDR references like ADR-001, MDD-5, etc.
        ref_pattern = r'\b([A-Z]{3})-(\d+)\b'
        references = re.findall(ref_pattern, content)
        
        for ref_type, ref_id in references:
            if ref_type not in self.TDR_TYPES:
                self.warnings.append(f"Reference to unknown TDR type: {ref_type}-{ref_id}")
        
        # In strict mode, could validate that referenced TDRs exist
        # This would require a registry or file system scanning
    
    def _validate_ai_context(self, frontmatter: Dict) -> None:
        """Validate AI context section if present.
        
        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        if 'ai-context' in frontmatter:
            ai_context = frontmatter['ai-context']
            
            if not isinstance(ai_context, dict):
                self.errors.append("ai-context must be a dictionary")
                return
            
            # Validate AI context fields
            recommended_fields = ['summary', 'keywords', 'related-patterns', 'complexity-level']
            
            if 'summary' in ai_context:
                if not isinstance(ai_context['summary'], str) or len(ai_context['summary']) < 20:
                    self.warnings.append("AI context summary should be a descriptive string (20+ chars)")
            
            if 'keywords' in ai_context:
                if not isinstance(ai_context['keywords'], list):
                    self.warnings.append("AI context keywords should be a list")
            
            if 'complexity-level' in ai_context:
                valid_levels = ['low', 'medium', 'high', 'critical']
                if ai_context['complexity-level'] not in valid_levels:
                    self.warnings.append(f"AI context complexity-level should be one of: {valid_levels}")
    
    def _create_result(self, file_path: Path, frontmatter: Dict, sections: Dict) -> Dict:
        """Create validation result dictionary.
        
        Args:
            file_path: Path to validated file
            frontmatter: Parsed frontmatter
            sections: Parsed sections
            
        Returns:
            Validation result dictionary
        """
        return {
            'file': str(file_path),
            'valid': len(self.errors) == 0,
            'errors': self.errors.copy(),
            'warnings': self.warnings.copy(),
            'metadata': {
                'frontmatter': frontmatter,
                'section_count': len(sections),
                'sections': list(sections.keys()),
                'has_ai_context': 'ai-context' in frontmatter if frontmatter else False
            }
        }
    
    def _create_error_result(self, error_message: str) -> Dict:
        """Create an error result for file-level failures.
        
        Args:
            error_message: Description of the error
            
        Returns:
            Error result dictionary
        """
        return {
            'file': 'unknown',
            'valid': False,
            'errors': [error_message],
            'warnings': [],
            'metadata': {}
        }


def format_results(results: List[Dict], output_format: str = 'text') -> str:
    """Format validation results for output.
    
    Args:
        results: List of validation result dictionaries
        output_format: 'text' or 'json'
        
    Returns:
        Formatted results string
    """
    if output_format == 'json':
        return json.dumps(results, indent=2)
    
    # Text format
    output = []
    total_files = len(results)
    valid_files = sum(1 for r in results if r['valid'])
    
    output.append(f"TDR Validation Report")
    output.append(f"{'='*50}")
    output.append(f"Files processed: {total_files}")
    output.append(f"Valid files: {valid_files}")
    output.append(f"Files with errors: {total_files - valid_files}")
    output.append("")
    
    for result in results:
        file_name = Path(result['file']).name
        status = "✓ VALID" if result['valid'] else "✗ INVALID"
        
        output.append(f"{status} - {file_name}")
        
        if result['errors']:
            output.append("  Errors:")
            for error in result['errors']:
                output.append(f"    • {error}")
        
        if result['warnings']:
            output.append("  Warnings:")
            for warning in result['warnings']:
                output.append(f"    • {warning}")
        
        # Show metadata for valid files
        if result['valid'] and result['metadata']:
            metadata = result['metadata']
            if 'frontmatter' in metadata and metadata['frontmatter']:
                fm = metadata['frontmatter']
                tdr_type = fm.get('type', 'Unknown')
                status = fm.get('status', 'Unknown')
                output.append(f"  Type: {tdr_type} | Status: {status} | Sections: {metadata['section_count']}")
        
        output.append("")
    
    return '\n'.join(output)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Validate Technical Decision Records (TDRs) for DDSE compliance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.md
  %(prog)s documents/ --strict
  %(prog)s documents/ --output json > validation_report.json
        """
    )
    
    parser.add_argument(
        'path',
        help='Path to TDR file or directory containing TDR files'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Enable strict validation mode with additional checks'
    )
    
    parser.add_argument(
        '--output',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = TDRValidator(strict_mode=args.strict)
    
    # Validate path
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)
    
    # Run validation
    if path.is_file():
        results = [validator.validate_file(path)]
    else:
        results = validator.validate_directory(path)
    
    # Output results
    output = format_results(results, args.output)
    print(output)
    
    # Exit with error code if any files failed validation
    has_errors = any(not r['valid'] for r in results)
    sys.exit(1 if has_errors else 0)


if __name__ == '__main__':
    main()
