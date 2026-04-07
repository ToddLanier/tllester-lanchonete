#!/usr/bin/env python3
"""
Complete URL fixes for tllester-lanchonete.
Fixes all remaining legacy lanchonete.org domain URLs to local Hugo paths.
Handles 170+ remaining URLs across all content files.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

# Domain to content section mapping
DOMAIN_PATTERNS = {
    r'lanchonete\.org': 'posts',
    r'cidadequeer\.lanchonete\.org': 'cidadequeer',
    r'paim\.lanchonete\.org': 'paim',
    r'zdm2016\.lanchonete\.org': 'zonadamata',
    r'episodiohaiti\.lanchonete\.org': 'episodiohaiti',
    r'arquivo\.lanchonete\.org': 'arquivo',
    r'cuiaba\.lanchonete\.org': 'arquivo',
}


class URLFixer:
    def __init__(self, content_dir):
        self.content_dir = Path(content_dir)
        self.fixes = defaultdict(int)
        self.unfixed = []
        self.files_processed = 0
        self.total_urls_found = 0
        self.modified_files = 0

    def extract_slug_from_path(self, path):
        """Extract slug from URL path like /YYYY/MM/slug/ or /YYYY/MM/slug"""
        match = re.search(r'/(\d{4})/(\d{2})/([^/?#]+)', path)
        if match:
            return match.group(3)
        return None

    def resolve_url(self, url, domain_section):
        """Attempt to resolve a legacy lanchonete URL to a Hugo path."""

        # Handle wp-content/uploads URLs
        if 'wp-content/uploads' in url:
            match = re.search(r'wp-content/uploads/(?:\d{4}/\d{2}/)?([^/?#]+)$', url)
            if match:
                filename = match.group(1)
                return f"/uploads/{filename}"

        # Parse the URL path
        parsed = urlparse(url)
        path = parsed.path

        # Extract slug from WordPress date-based URL
        slug = self.extract_slug_from_path(path)
        if slug:
            # Internal link to a post
            return f"/{domain_section}/{slug}/"

        # Handle /textos/ sections (zona da mata custom pages)
        if '/textos/' in path:
            match = re.search(r'/textos/([^/?#]+)', path)
            if match:
                text_slug = match.group(1)
                return f"/{domain_section}/textos/{text_slug}/"
            return f"/{domain_section}/"

        # Handle specific section pages with full paths
        if '/projetos-projects/' in path:
            # Extract the project slug if it exists
            match = re.search(r'/projetos-projects/([^/?#]+)', path)
            if match:
                project_slug = match.group(1)
                return f"/{domain_section}/projetos-projects/{project_slug}/"
            return f"/{domain_section}/"

        if '/calendario-events' in path:
            return f"/{domain_section}/"

        if '/2016/08/26/' in path:
            # Handle specific post path
            match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/([^/?#]+)', path)
            if match:
                slug = match.group(4)
                return f"/{domain_section}/{slug}/"

        # Handle root or section pages
        if path == '/' or path == '/en/' or path == '':
            if domain_section == 'paim':
                return '/paim/'
            elif domain_section == 'cidadequeer':
                return '/cidadequeer/'
            elif domain_section == 'zonadamata':
                return '/zonadamata/'
            elif domain_section == 'episodiohaiti':
                return '/episodiohaiti/'
            elif domain_section == 'arquivo':
                return '/arquivo/'
            else:
                return '/'

        # Handle about/sobre pages
        if '/sobre' in path or '/about' in path:
            return '/about/'

        # Couldn't resolve
        return None

    def fix_urls_in_content(self, content, filepath='unknown'):
        """Find and fix all legacy URLs in content."""
        fixed_content = content
        urls_fixed_here = 0

        # Build a comprehensive regex to find all lanchonete.org URLs
        # This pattern matches URLs and includes hyphens and slashes in the path
        # Stops at closing parenthesis, bracket, quote, or whitespace
        url_pattern = r'https?://(?:www\.)?(?:lanchonete\.org|cidadequeer\.lanchonete\.org|paim\.lanchonete\.org|zdm2016\.lanchonete\.org|episodiohaiti\.lanchonete\.org|arquivo\.lanchonete\.org|cuiaba\.lanchonete\.org)(?:/[a-zA-Z0-9._~:/?#\[\]@!$&\'()*+,;=-]*[a-zA-Z0-9./])?'

        for match in re.finditer(url_pattern, content):
            url = match.group(0)
            self.total_urls_found += 1

            # Determine section from domain
            section = 'posts'  # default
            for domain_pattern, sect in DOMAIN_PATTERNS.items():
                if re.search(domain_pattern, url):
                    section = sect
                    break

            local_path = self.resolve_url(url, section)

            if local_path:
                # Replace in content
                fixed_content = fixed_content.replace(url, local_path)
                urls_fixed_here += 1
                if 'wp-content/uploads' in url:
                    self.fixes['wp_upload'] += 1
                elif re.search(r'/\d{4}/\d{2}/', url):
                    self.fixes['internal_link'] += 1
                elif '/textos/' in url:
                    self.fixes['textos_page'] += 1
                else:
                    self.fixes['section_link'] += 1
            else:
                # Could not resolve
                self.unfixed.append({
                    'url': url,
                    'section': section,
                    'file': filepath
                })
                self.fixes['unresolvable'] += 1

        return fixed_content, urls_fixed_here

    def process_file(self, filepath):
        """Process a single markdown file."""
        self.files_processed += 1

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            fixed_content, urls_fixed = self.fix_urls_in_content(
                content,
                str(filepath.relative_to(self.content_dir))
            )

            # Write back if changed
            if fixed_content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                self.modified_files += 1
                return urls_fixed

            return 0

        except Exception as e:
            print(f"ERROR processing {filepath}: {e}")
            return 0

    def run(self):
        """Run the complete URL fixer."""
        print("=" * 70)
        print("LANCHONETE LEGACY URL FIXER - Complete Pass")
        print("=" * 70)

        print("\nScanning for markdown files...")
        md_files = list(self.content_dir.glob('**/*.md'))
        print(f"Found {len(md_files)} markdown files\n")

        print("Processing files...")
        total_urls_fixed = 0
        for i, filepath in enumerate(md_files, 1):
            urls_fixed = self.process_file(filepath)
            total_urls_fixed += urls_fixed

            if i % 50 == 0:
                print(f"  Processed {i}/{len(md_files)} files... ({total_urls_fixed} URLs fixed so far)")

        print(f"\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Files processed:           {self.files_processed}")
        print(f"Files modified:            {self.modified_files}")
        print(f"\nTotal legacy URLs found:   {self.total_urls_found}")
        print(f"WordPress uploads fixed:   {self.fixes['wp_upload']}")
        print(f"Internal links fixed:      {self.fixes['internal_link']}")
        print(f"Textos pages fixed:        {self.fixes['textos_page']}")
        print(f"Section links fixed:       {self.fixes['section_link']}")
        print(f"Unresolvable URLs:         {self.fixes['unresolvable']}")

        if self.unfixed:
            print(f"\n" + "=" * 70)
            print(f"UNRESOLVABLE URLs ({len(self.unfixed)} total)")
            print("=" * 70)

            # Group by file
            by_file = defaultdict(list)
            for item in self.unfixed:
                by_file[item['file']].append(item['url'])

            for filepath in sorted(by_file.keys())[:15]:  # Show first 15 files
                print(f"\n{filepath}:")
                for url in by_file[filepath][:5]:  # Show first 5 URLs per file
                    print(f"  - {url}")
                if len(by_file[filepath]) > 5:
                    print(f"  ... and {len(by_file[filepath]) - 5} more")

            if len(by_file) > 15:
                print(f"\n... and {len(by_file) - 15} more files with unresolvable URLs")

        print(f"\n" + "=" * 70)


def main():
    content_dir = Path(__file__).parent / 'content'

    if not content_dir.exists():
        print(f"ERROR: Content directory not found: {content_dir}")
        return 1

    fixer = URLFixer(content_dir)
    fixer.run()
    return 0


if __name__ == '__main__':
    exit(main())
