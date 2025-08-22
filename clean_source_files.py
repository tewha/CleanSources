#!/usr/bin/env python3

import os
import sys
import argparse

class FriendlyParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"❌ {message}\n", file=sys.stderr)
        self.print_help(sys.stderr)
        sys.exit(1)

def clean_file(filepath, *, bare=False, verbose=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    if '\r' in original_content:
        print(f'❌ Error: Carriage return (\\r) detected in file: {filepath}', file=sys.stderr)
        sys.exit(1)

    lines = original_content.splitlines()
    cleaned_lines = [line.rstrip() for line in lines]

    while cleaned_lines and cleaned_lines[-1] == '':
        cleaned_lines.pop()

    cleaned_content = '\n'.join(cleaned_lines) + '\n'

    if cleaned_content != original_content:
        if bare:
            print(filepath)
        else:
            print(f'🧹 Cleaning: {filepath}')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
    elif verbose and not bare:
        print(f'➖ Skipped:  {filepath}')

def clean_project_files(root_dir, *, bare=False, verbose=False):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(('.swift', '.py', '.sh', '.json')):
                full_path = os.path.join(dirpath, filename)
                clean_file(full_path, bare=bare, verbose=verbose)

def main():
    parser = FriendlyParser(
        description="Clean trailing whitespace and fix EOF in Swift, Python, Shell (.sh), and JSON files."
    )
    parser.add_argument(
        'directory',
        metavar='DIR',
        help='Root directory to scan for .swift and .python files'
    )
    parser.add_argument(
        '-b', '--bare',
        action='store_true',
        help='Only print paths of cleaned files (no labels)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Also print skipped files'
    )

    args = parser.parse_args()

    root_path = os.path.abspath(args.directory)

    if not os.path.isdir(root_path):
        print(f"❌ Error: '{args.directory}' is not a valid directory.\n", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    clean_project_files(
        root_path,
        bare=args.bare,
        verbose=args.verbose
    )

if __name__ == '__main__':
    main()
