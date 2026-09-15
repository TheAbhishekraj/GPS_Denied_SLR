import os

checks = [
    # Phase 0
    ('00_scope', True),
    ('01_data_raw', True),
    ('02_data_processed', True),
    ('03_prompts', True),
    ('04_ai_responses', True),
    ('05_papers_fulltext', True),
    ('06_analysis/output/figures_v2', True),
    ('06_analysis/output/tables', True),
    ('06_analysis/scripts', True),
    ('07_manuscript', True),
    ('08_docs', True),
    ('09_prompts', True),
    ('supplementary', True),
    ('requirements.txt', False),
    ('.gitignore', False),
    ('08_docs/FOLDER_GUIDE.md', False),
    # Phase 1
    ('00_scope/PROTOCOL.md', False),
    ('00_scope/SEARCH_STRINGS.md', False),
    ('00_scope/REGISTRATION.md', False),
    # Phase 2
    ('01_data_raw/ieee_xplore_raw.csv', False),
    ('01_data_raw/scopus_raw.csv', False),
    ('01_data_raw/SEARCH_LOG.md', False),
    # Phase 3
    ('02_data_processed/deduplicated_master.csv', False),
    ('02_data_processed/dedup_log.csv', False),
    ('02_data_processed/DEDUP_REPORT.md', False),
    # Phase 4
    ('03_prompts/screening_prompts.jsonl', False),
]
base = r'E:\GPS_Denied_SLR'
for path, is_dir in checks:
    full = os.path.join(base, path)
    exists = os.path.isdir(full) if is_dir else os.path.isfile(full)
    status = 'OK' if exists else 'MISSING'
    print(f'{status}: {path}')
