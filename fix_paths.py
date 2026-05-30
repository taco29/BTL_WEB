
import os
import glob

# File mapping: file_path -> prefix to replace /udu_clone/ with
# docs/index.html is at docs/ level, so /udu_clone/ maps to nothing (empty string relative to docs/)
# Actually for relative paths, we need to go from the file to the docs root

files_and_prefixes = [
    # (file_path, replacement_for_/udu_clone/)
    ('docs/index.html', ''),
    ('docs/components/header.html', '../'),
    ('docs/components/footer.html', '../'),
    ('docs/pages/aiot.html', '../'),
    ('docs/pages/club.html', '../'),
    ('docs/pages/contact.html', '../'),
    ('docs/pages/event.html', '../'),
    ('docs/pages/hoat-dong-sinh-vien.html', '../'),
    ('docs/pages/nckh.html', '../'),
    ('docs/pages/popup_modal.html', '../'),
    ('docs/pages/research.html', '../'),
    ('docs/pages/udu.html', '../'),
    ('docs/pages/gioi-thieu-html/co-cau.html', '../../'),
    ('docs/pages/gioi-thieu-html/giang-vien.html', '../../'),
    ('docs/pages/gioi-thieu-html/gioi-thieu-chung.html', '../../'),
    ('docs/pages/gioi-thieu-html/lich-su.html', '../../'),
    ('docs/pages/gioi-thieu-html/triet-ly.html', '../../'),
    ('docs/pages/tin-tuc-html/cchoa.html', '../../'),
    ('docs/pages/tin-tuc-html/dnhoa.html', '../../'),
    ('docs/pages/tin-tuc-html/qthoa.html', '../../'),
    ('docs/pages/tin-tuc-html/ttin.html', '../../'),
]

for file_path, prefix in files_and_prefixes:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = content.replace('/udu_clone/', prefix)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count = content.count('/udu_clone/')
        print(f'Fixed {count} paths in: {file_path}')
    else:
        print(f'NOT FOUND: {file_path}')

print('All done!')