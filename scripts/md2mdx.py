#!/usr/bin/env python3

"""
Markdown to MDX Transformer
---------------------------

This script transforms a standard Markdown file into an MDX file for use with Astro.
It performs several transformations:

1. Processes ASTRO comments into component tags:
   - CodeSwitcher and CodeExample components.
   - Illustration, Diagram, and Picture components.
   - Removes redundant titles in code blocks.
2. Transforms image references to Astro Picture components
3. Removes table of contents (The Astro site has its own table of contents).
4. Adds GitHub header.
5. Removes bold formatting from fully bold lines.
6. Transforms schema file links to proper paths.

Usage:
    The script reads from README.md in the project root and outputs to:
    test-sync/target/src/content/pages/index.mdx

    $ python3 scripts/md2mdx.py

Dependencies:
    - python-frontmatter
    - pathlib
    - re (regex)
"""

import os
import sys
from pathlib import Path
import frontmatter
import re
import glob

# Get the project root - need to handle both direct run and test-sync run.
SCRIPT_PATH = Path(__file__).resolve()

if 'test-sync/source' in str(SCRIPT_PATH):
    # Running from test-sync/source/scripts/md2mdx.py.
    PROJECT_ROOT = SCRIPT_PATH.parent.parent.parent.parent
    SOURCE_ROOT = SCRIPT_PATH.parent.parent
    TARGET_ROOT = Path(PROJECT_ROOT) / 'test-sync/target'
else:
    # Running directly from scripts/md2mdx.py.
    PROJECT_ROOT = SCRIPT_PATH.parent.parent
    SOURCE_ROOT = PROJECT_ROOT
    TARGET_ROOT = PROJECT_ROOT / 'test-sync/target'

SOURCE_FILE = str(PROJECT_ROOT / 'README.md')
TARGET_FILE = str(PROJECT_ROOT / 'test-sync/target/src/content/pages/index.mdx')

print(f'  Script location: {__file__}')
print(f'  Project root: {PROJECT_ROOT}')
print(f'  Source file: {SOURCE_FILE}')
print(f'  Target file: {TARGET_FILE}')

# Required imports for the MDX file.
ASTRO_IMPORTS = '''import { Picture } from 'astro:assets';
import CodeExample from '../../components/CodeExample.astro';
import CodeSwitcher from '../../components/CodeSwitcher.astro';
import Diagram from '../../components/Diagram.astro';
import GitHubHeader from '../../components/GitHubHeader.astro';
import illuApifyStore from './illu-apify-store@2x.png';
import illuAPIGetInput from './illu-get-input@2x.png';
import illuAPIKeyValueStoreAccess from './illu-api-key-value-store-access@2x.png';
import illuAPIMetamorph from './illu-api-metamorph@2x.gif';
import illuAPIPush from './illu-api-push@2x.gif';
import illuAPIReboot from './illu-api-reboot@2x.png';
import illuAPIStartAnother from './illu-api-start-another@2x.png';
import illuAPIWebServer from './illu-api-webserver@2x.gif';
import illuBasicConceptsInput from './illu-basic-concepts-input@2x.gif';
import illuBasicConceptsIntegrations from './illu-basic-concepts-integrations@2x.png';
import illuBasicConceptsOutput from './illu-basic-concepts-output@2x.gif';
import illuBasicConceptsRunEnvironment from './illu-basic-concepts-docker@2x.gif';
import illuBasicConceptsStorage from './illu-basic-concepts-storage@2x.png';
import illuBasicConceptsStorageDataset from './illu-basic-concepts-storage-dataset@2x.png';
import illuBasicConceptsStorageKeyValueStore from './illu-basic-concepts-storage-key-value-store@2x.png';
import illuDatasetSchema from './illu-dataset-schema@2x.png';
import illuDefinitionFilesInputSchemaFile from './illu-definition-files-input-schema-file@2x.png';
import illuDefinitionFilesOutputSchemaFile from './illu-definition-files-output-schema-file@2x.png';
import illuDevelopmentDeployment from './illu-development-deployment@2x.png';
import illuDevelopmentLocal from './illu-development-local@2x.png';
import illuDiagramHoriz from './illu-diagram-horiz@2x.png';
import illuDiagramVert from './illu-diagram-vert@2x.png';
import illuPhilosophyWhyTheName from './illu-philosophy-why-the-name@2x.png';
import illuSharingChargingMoney from './illu-sharing-charging-money@2x.gif';
import illuSharingMonetization from './illu-sharing-monetization@2x.png';
import Illustration from '../../components/Illustration.astro';
import illuTakerInput from './illu-taker-input@2x.png';'''

IGNORED_FILES = {
    'license.md',  # ignore case-insensitive
    # Add more files here as needed, e.g.:
    # 'contributing.md',
    # 'changelog.md',
}

def should_process_file(path: Path) -> bool:
    """Determine if a file should be processed based on ignore rules."""
    
    # Case-insensitive filename check.
    if path.name.lower() in IGNORED_FILES:
        print(f'\n󰋼  Skipping ignored file: {path.name}')
        return False
    return True

def remove_table_of_contents(content: str) -> str:
    """Remove the table of contents section from the markdown content."""

    print('\n󰋼  Removing table of contents...')

    def replace_toc(match):
        print('  ⭮  Removed table of contents section')
        return ''

    return re.sub(
        r'## Contents\n\n<!-- toc -->[\s\S]*?<!-- tocstop -->',
        replace_toc,
        content
    )


def transform_image_references(content: str) -> str:
    """Transform markdown image references to Astro Picture components."""

    print('\n󰋼  Transforming image references...')

    def replace_image(match):
        alt, src = match.groups()
        print(f'  ⭮  {src}')
        basename = os.path.basename(src)
        return f'<Picture src={basename} alt="{alt}" width={800} height={600} />'

    return re.sub(
        r'!\[(.*?)\]\((.*?)\)',
        replace_image,
        content
    )


def add_github_header(content: str) -> str:
    """Add GitHub header component after the first heading."""

    print('\n󰋼  Adding GitHub header...')
    print('  ⭮  Adding GitHub header')

    return re.sub(
        r'(#\s+[^\n]*\n)(\n?)',
        r'\1\n<GitHubHeader repoUrl="https://github.com/apify/actor-whitepaper" />\n\n',
        content,
        count=1
    )


def remove_bold_formatting(content: str) -> str:
    """Remove bold formatting from lines that are entirely bold."""

    print('\n󰋼  Removing bold formatting...')

    def replace_bold(match):
        text = match.group(1)
        print(f'  ⭮  {text[:120]}')
        return text

    return re.sub(
        r'^\*\*(.*?)\*\*$',
        replace_bold,
        content,
        flags=re.MULTILINE
    )


def remove_picture_components(content: str) -> str:
    """Remove Picture components that aren't preceded by ASTRO comments."""

    print('\n󰋼  Removing Picture components...')

    def replace_picture(match):
        picture = re.sub(r'\s+', ' ', match.group(0))
        print(f'  ⭮  {picture[:120]}')
        return ''

    return re.sub(
        r'(?<!<!-- ASTRO: )<Picture[\s\S]*?/>',
        replace_picture,
        content,
        flags=re.MULTILINE | re.DOTALL
    )


def transform_astro_blocks(content: str) -> str:
    """Transform ASTRO comments into component tags.

    This function processes:
    1. CodeSwitcher and CodeExample components, removing redundant titles.
    2. Illustration, Diagram and Picture components.
    """

    print('\n󰋼  Transforming ASTRO blocks...')

    def replace_astro_block(match):
        # Get the component definition but preserve internal whitespace.
        component = match.group(1).strip()

        # Handle CodeSwitcher tags.
        if component == '<CodeSwitcher>':
            print('  ⭮  Adding CodeSwitcher opening tag')
            return '<CodeSwitcher>'
        elif component == '</CodeSwitcher>':
            print('  ⭮  Adding CodeSwitcher closing tag')
            return '</CodeSwitcher>'

        # Handle CodeExample tags with titles.
        code_example_match = re.match(r'<CodeExample\s+title="([^"]+)">', component)

        if code_example_match:
            title = code_example_match.group(1)
            print(f'  ⭮  Adding CodeExample tag with title: {title}')
            return f'<CodeExample title="{title}">'
        elif component == '</CodeExample>':
            print('  ⭮  Adding CodeExample closing tag')
            return '</CodeExample>'

        # Handle media components (Illustration, Diagram, Picture).
        if (component.startswith('<Illustration') or
            component.startswith('<Diagram') or
            component.startswith('<Picture')):
            print(f'  ⭮  {component[:120]}')
            return component

        # Return unchanged if not a matching component.
        return f'<!-- ASTRO: {match.group(1)} -->'

    # First transform all ASTRO comments to their respective components.
    content = re.sub(
        r'<!--\s*ASTRO:\s*(.*?)\s*-->',
        replace_astro_block,
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # Then remove redundant h3/h4 titles that appear right after CodeExample tags.
    def remove_redundant_titles(match):
        block = match.group(0)

        # Match any h3 or h4 heading after the opening tag, including across newlines.
        block = re.sub(
            r'(<CodeExample[^>]+>)(\s*\n)*\s*#{3,4}[^\n]+\n',
            lambda m: print(f'  ⭮  Removing heading after CodeExample') or m.group(1) + '\n',
            block,
            count=1  # Only remove the first heading found
        )

        return block

    # Process each CodeExample block to remove redundant titles.
    content = re.sub(
        r'<CodeExample[^>]+>[\s\S]+?</CodeExample>',
        remove_redundant_titles,
        content
    )

    return content


def transform_schema_links(content: str) -> str:
    """Transform schema file links to their proper paths."""

    print('\n󰋼  Transforming schema links...')

    def replace_link(match, suffix_lower):
        text, path = match.groups()
        new_path = f'/{path.lower().replace("_", "-")}-{suffix_lower}'
        print(f'  ⭮  {text} →  {new_path}')
        return f'[{text}]({new_path})'

    # Define patterns for both schema and file links.
    replacements = {
        r'\[([^]]+)\]\(./pages/([^)]+)_SCHEMA\.md\)':
            lambda m: replace_link(m, 'schema'),
        r'\[([^]]+)\]\(./pages/([^)]+)_FILE\.md\)':
            lambda m: replace_link(m, 'file')
    }

    # Apply each replacement pattern.
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    return content


def remove_html_comments(content: str) -> str:
    """Remove all HTML comments from the content."""

    print('\n󰋼  Removing HTML comments...')

    def replace_comment(match):
        comment = match.group(0)
        print(f'  ⭮  Removing comment: {comment[:120]}')
        return ''

    return re.sub(
        r'<!--[\s\S]*?-->',
        replace_comment,
        content,
        flags=re.MULTILINE | re.DOTALL
    )


def transform_markdown_to_mdx(content: str) -> str:
    """Main transformation pipeline to convert markdown to MDX format."""
    print('\n󰋼  Parsing frontmatter...')
    post = frontmatter.loads(content)

    # Apply transformations in sequence.
    transformed = remove_table_of_contents(post.content)
    transformed = transform_image_references(transformed)
    transformed = remove_picture_components(transformed)
    transformed = transform_astro_blocks(transformed)
    transformed = add_github_header(transformed)
    transformed = remove_bold_formatting(transformed)
    transformed = transform_schema_links(transformed)
    transformed = remove_html_comments(transformed)  # Added as final cleanup step

    print('\n󰋼  Combining with Astro imports...')
    return f'{ASTRO_IMPORTS}\n\n{transformed}'


def get_target_path(source_path: Path) -> Path:
    """Convert source path to target path using the required transformations."""
    
    # Get relative path from source root.
    rel_path = source_path.relative_to(SOURCE_ROOT)
    
    # Transform filename.
    stem = rel_path.stem.lower().replace('_', '-')
    new_name = f"{stem}.mdx"
    
    # Construct target path.
    if source_path.name == 'README.md':
        # Special case for README.md -> index.mdx.
        return TARGET_ROOT / 'src/content/pages/index.mdx'
    else:
        # For files in pages directory.
        return TARGET_ROOT / 'src/content/pages' / new_name


def process_files():
    """Main function to process all markdown files."""
    
    try:
        # Find all markdown files to process.
        source_files = [
            Path(p) for p in [
                *glob.glob(str(SOURCE_ROOT / '*.md')),  # root md files
                *glob.glob(str(SOURCE_ROOT / 'pages/*.md'))  # files in pages directory
            ]
            
            if should_process_file(Path(p))  # filter out ignored files
        ]
        
        print(f'\n󰋼  Found {len(source_files)} markdown files to process')
        
        for source_file in source_files:
            target_file = get_target_path(source_file)
            print(f'\n󰋼  Processing: {source_file.name} → {target_file.name}')
            
            # Read source content.
            print(f'  Reading source file: {source_file}')
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f'  Source file size: {len(content)} bytes')
            
            # Transform content.
            print('\n󰋼  Transforming content...')
            transformed_content = transform_markdown_to_mdx(content)
            print(f'  ⭮  {len(transformed_content)} bytes')
            
            # Write target file.
            print(f'\n󰋼  Writing target file: {target_file}')
            os.makedirs(target_file.parent, exist_ok=True)
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(transformed_content)
            print(f'  ⭮  {source_file.name} → {target_file.name}')
        
        print('\n󰋼  Formatting MDX files...')
        os.system('npm run format-sync')
        
        print('\n  Done')
        
    except Exception as error:
        print('\n❌ Error processing files:', str(error))
        sys.exit(1)


if __name__ == '__main__':
    process_files()
