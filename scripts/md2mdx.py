#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import frontmatter
import re

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
SOURCE_FILE = str(PROJECT_ROOT / 'README.md')  # Source is in project root
TARGET_FILE = str(PROJECT_ROOT / 'test-sync/target/src/content/pages/index.mdx')

ASTRO_IMPORTS = '''import { Picture } from 'astro:assets';

import CodeExample from '../../components/CodeExample.astro';
import CodeSwitcher from '../../components/CodeSwitcher.astro';
import Diagram from '../../components/Diagram.astro';
import GitHubHeader from '../../components/GitHubHeader.astro';'''


def remove_table_of_contents(content: str) -> str:
    print('\n󰋼  Removing table of contents...')
    return re.sub(
        r'## Contents\n\n<!-- toc -->[\s\S]*?<!-- tocstop -->',
        '',
        content
    )


def transform_code_blocks(content: str) -> str:
    print('\n󰋼  Transforming code blocks...')

    def replace_code_block(match):
        language, code = match.groups()
        if language in ['bash', 'javascript', 'python']:
            print(f'  Found {language} code block')
            return f'<CodeExample title="{language.upper()}">\n{language}{code}</CodeExample>'
        return match.group(0)

    return re.sub(
        r'`{3}(\w+)([\s\S]*?)`{3}',
        replace_code_block,
        content
    )


def transform_image_references(content: str) -> str:
    print('\n󰋼  Transforming image references...')

    def replace_image(match):
        alt, src = match.groups()
        print(f'  Found image: {src}')
        basename = os.path.basename(src)
        return f'''<Picture
    src={basename}
    alt="{alt}"
    width={800}
    height={600}
/>'''

    return re.sub(
        r'!\[(.*?)\]\((.*?)\)',
        replace_image,
        content
    )


def transform_markdown_to_mdx(content: str) -> str:
    print('\n󰋼  Parsing frontmatter...')
    post = frontmatter.loads(content)

    transformed = remove_table_of_contents(post.content)
    transformed = transform_code_blocks(transformed)
    transformed = transform_image_references(transformed)

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
        print(f'  Transformed size: {len(transformed_content)} bytes')

        print('\n󰋼  Writing target file...')
        os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
        with open(TARGET_FILE, 'w', encoding='utf-8') as f:
            f.write(transformed_content)
        print(f'  Successfully transformed: {SOURCE_FILE} → {TARGET_FILE}')

        print('\n󰋼  Formatting MDX file...')
        os.system('npm run format-sync')
        
        print('\n  Done')
        
    except Exception as error:
        print('\n❌ Error processing files:', str(error))
        sys.exit(1)


if __name__ == '__main__':
    process_files()
