#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import frontmatter
import re

# Get the project root - need to handle both direct run and test-sync run.
SCRIPT_PATH = Path(__file__).resolve()

if 'test-sync/source' in str(SCRIPT_PATH):
    # Running from test-sync/source/scripts/md2mdx.py.
    PROJECT_ROOT = SCRIPT_PATH.parent.parent.parent.parent
else:
    # Running directly from scripts/md2mdx.py.
    PROJECT_ROOT = SCRIPT_PATH.parent.parent

SOURCE_FILE = str(PROJECT_ROOT / 'README.md')
TARGET_FILE = str(PROJECT_ROOT / 'test-sync/target/src/content/pages/index.mdx')

print(f'  Script location: {__file__}')
print(f'  Project root: {PROJECT_ROOT}')
print(f'  Source file: {SOURCE_FILE}')
print(f'  Target file: {TARGET_FILE}')

ASTRO_IMPORTS = '''import { Picture } from 'astro:assets';

import CodeExample from '../../components/CodeExample.astro';
import CodeSwitcher from '../../components/CodeSwitcher.astro';
import Diagram from '../../components/Diagram.astro';
import GitHubHeader from '../../components/GitHubHeader.astro';'''


def remove_table_of_contents(content: str) -> str:
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
    print('\n󰋼  Adding GitHub header...')
    print('  ⭮  Adding GitHub header')
    
    return re.sub(
        r'(#\s+[^\n]*\n)(\n?)',
        r'\1\n<GitHubHeader repoUrl="https://github.com/apify/actor-whitepaper" />\n\n',
        content,
        count=1
    )


def remove_bold_formatting(content: str) -> str:
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
    1. CodeSwitcher and CodeExample components, removing redundant titles
    2. Illustration, Diagram and Picture components
    
    Args:
        content: The source Markdown content
        
    Returns:
        Content with ASTRO comments converted to component tags
    """
    print('\n󰋼  Transforming ASTRO blocks...')
    
    def replace_astro_block(match):
        # Get the component definition but preserve internal whitespace
        component = match.group(1).strip()
        
        # Handle CodeSwitcher
        if component == '<CodeSwitcher>':
            print('  ⭮  Adding CodeSwitcher opening tag')
            return '<CodeSwitcher>'
        elif component == '</CodeSwitcher>':
            print('  ⭮  Adding CodeSwitcher closing tag')
            return '</CodeSwitcher>'
            
        # Handle CodeExample
        code_example_match = re.match(r'<CodeExample\s+title="([^"]+)">', component)
        if code_example_match:
            title = code_example_match.group(1)
            print(f'  ⭮  Adding CodeExample tag with title: {title}')
            return f'<CodeExample title="{title}">'
        elif component == '</CodeExample>':
            print('  ⭮  Adding CodeExample closing tag')
            return '</CodeExample>'
            
        # Handle Illustration, Diagram, and Picture
        if (component.startswith('<Illustration') or 
            component.startswith('<Diagram') or 
            component.startswith('<Picture')):
            print(f'  ⭮  {component[:120]}')
            return component
            
        # Return unchanged if not a matching component
        return f'<!-- ASTRO: {match.group(1)} -->'
    
    # First transform all ASTRO comments to components
    content = re.sub(
        r'<!--\s*ASTRO:\s*(.*?)\s*-->',
        replace_astro_block,
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # Then remove redundant titles inside CodeExample blocks
    def remove_redundant_titles(match):
        block = match.group(0)
        # Remove any heading that appears right after the CodeExample opening tag
        block = re.sub(
            r'(<CodeExample[^>]+>)(\s*\n)*\s*#{3,4}[^\n]+\n',
            lambda m: print(f'  ⭮  Removing heading after CodeExample') or m.group(1) + '\n',
            block,
            count=1
        )
        return block
    
    content = re.sub(
        r'<CodeExample[^>]+>[\s\S]+?</CodeExample>',
        remove_redundant_titles,
        content
    )
    
    return content


def transform_schema_links(content: str) -> str:
    print('\n󰋼  Transforming schema links...')
    
    def replace_link(match, suffix_lower):
        text, path = match.groups()
        new_path = f'/{path.lower().replace("_", "-")}-{suffix_lower}'
        print(f'  ⭮  {text} →  {new_path}')
        return f'[{text}]({new_path})'
    
    replacements = {
        r'\[([^]]+)\]\(./pages/([^)]+)_SCHEMA\.md\)': 
            lambda m: replace_link(m, 'schema'),
        r'\[([^]]+)\]\(./pages/([^)]+)_FILE\.md\)': 
            lambda m: replace_link(m, 'file')
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)
    
    return content


def transform_markdown_to_mdx(content: str) -> str:
    print('\n󰋼  Parsing frontmatter...')
    post = frontmatter.loads(content)

    transformed = remove_table_of_contents(post.content)
    transformed = transform_image_references(transformed)
    transformed = remove_picture_components(transformed)
    transformed = transform_astro_blocks(transformed)
    transformed = add_github_header(transformed)
    transformed = remove_bold_formatting(transformed)
    transformed = transform_schema_links(transformed)

    print('\n󰋼  Combining with Astro imports...')
    return f'{ASTRO_IMPORTS}\n\n{transformed}'


def process_files():
    try:
        print('\n󰋼  Reading source file...')
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f'  Source file size: {len(content)} bytes')

        print('\n󰋼  Transforming content...')
        transformed_content = transform_markdown_to_mdx(content)
        print(f'  ⭮  {len(transformed_content)} bytes')

        print('\n󰋼  Writing target file...')
        os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
        with open(TARGET_FILE, 'w', encoding='utf-8') as f:
            f.write(transformed_content)
        print(f'  ⭮  {SOURCE_FILE} →  {TARGET_FILE}')

        print('\n󰋼  Formatting MDX file...')
        os.system('npm run format-sync')
        
        print('\n  Done')
        
    except Exception as error:
        print('\n❌ Error processing files:', str(error))
        sys.exit(1)


if __name__ == '__main__':
    process_files()