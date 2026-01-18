import os
import re

def get_all_files(root_dir):
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Keep relative path for matching
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, '.')
            file_list.append(rel_path)
    return file_list

def check_path_existence(path, defined_in_file, all_files_set):
    # Ignore external links, anchors, etc.
    if path.startswith('http') or path.startswith('#') or path.startswith('mailto:'):
        return
    
    # Clean path (remove query params)
    clean_path = path.split('?')[0].split('#')[0]
    
    # Resolve alias @
    if clean_path.startswith('@'):
        # This is project specific, assuming @ -> src/
        # Adjust logic if config says otherwise, but usually @lib -> src/lib etc.
        # Let's try to map common aliases if we can, or just skip for now if too complex
        # But for images in public, they start with /
        pass

    # Normalize Path for checking
    # If starts with /, likely public
    target_path = None
    if clean_path.startswith('/'):
        # Check in public/
        target_path = os.path.join('public', clean_path.lstrip('/'))
    else:
        # Relative path
        base_dir = os.path.dirname(defined_in_file)
        target_path = os.path.normpath(os.path.join(base_dir, clean_path))
    
    # For imports in code (not starting with /), they might be in src
    # If checking source imports (not public assets)
    if not clean_path.startswith('/'):
         # Simple check: Does target_path exist in our file list?
         # We need to handle extensions if missing (like import X from './X')
         pass # Skipping complex JS module resolution for now, focusing on ASSETS (images)
         
    # Optimization: Only strictly check things that explicitly look like assets (png, jpg, svg) or explicit imports
    if not any(clean_path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.svg', '.json', '.astro']):
        return

    # Check existence
    # We want EXACT match
    if target_path in all_files_set:
        return # OK
    else:
        # Check for case mismatch
        # find closest match
        target_lower = target_path.lower()
        for f in all_files_set:
            if f.lower() == target_lower:
                print(f"CASE MISMATCH: '{path}' in {defined_in_file} -> Found '{f}' on disk")
                return
        
        # If not found at all
        print(f"MISSING: '{path}' in {defined_in_file} -> Not found at '{target_path}'")

def scan_files():
    all_files = get_all_files('.')
    all_files_set = set(all_files)
    
    # Files to scan for references
    extensions = ['.astro', '.md', '.mdx', '.json', '.js', '.jsx', '.ts', '.tsx']
    
    regex_patterns = [
        r'src=["\']([^"\']+)["\']', # src="..."
        r'href=["\']([^"\']+)["\']', # href="..."
        r'url\(([^)]+)\)', # url(...)
        r'image:\s*([^\s\n]+)', # yaml/json image: ...
        r'avatar:\s*([^\s\n]+)', # yaml/json avatar: ...
        r'thumbnail:\s*([^\s\n]+)', # yaml/json thumbnail: ...
    ]
    
    for file_path in all_files:
        if not any(file_path.endswith(ext) for ext in extensions):
            continue
            
        if 'node_modules' in file_path or 'dist' in file_path or '.git' in file_path:
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                for pattern in regex_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        # cleanup quotes if caught by url()
                        match = match.strip("'\"")
                        check_path_existence(match, file_path, all_files_set)
        except Exception as e:
            pass # ignore binary files etc

if __name__ == "__main__":
    scan_files()
