# Graph Report - F:\workspace\smart-comfyui-gallery  (2026-04-22)

## Corpus Check
- Large corpus: 48 files · ~781,074 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 212 nodes · 392 edges · 24 communities detected
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 34 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_External Folder Mounting, ai_indexing_add_files|External Folder Mounting, ai_indexing_add_files]]
- [[_COMMUNITY_Collections Screenshot, Comments Panel Screenshot|Collections Screenshot, Comments Panel Screenshot]]
- [[_COMMUNITY_clean_prompt_text, ComfyMetadataParser|clean_prompt_text, ComfyMetadataParser]]
- [[_COMMUNITY_Workflow Recall, download_file|Workflow Recall, download_file]]
- [[_COMMUNITY_check_rescan_status, check_zip_status|check_rescan_status, check_zip_status]]
- [[_COMMUNITY_check_exhibition_requirements, cleanup_invalid_watched_folde|check_exhibition_requirements, cleanup_invalid_watched_folde]]
- [[_COMMUNITY_User Management Screenshot, User Management and ACL|User Management Screenshot, User Management and ACL]]
- [[_COMMUNITY_create_thumbnail, extract_workflow_files_string|create_thumbnail, extract_workflow_files_string]]
- [[_COMMUNITY_api_search_options, collection_view|api_search_options, collection_view]]
- [[_COMMUNITY_filter_enabled_nodes, generate_node_summary|filter_enabled_nodes, generate_node_summary]]
- [[_COMMUNITY_delete_batch, delete_file|delete_batch, delete_file]]
- [[_COMMUNITY_analyze_file_metadata, format_duration|analyze_file_metadata, format_duration]]
- [[_COMMUNITY_Serves input files directly from the ComfyUI Input folder.,|Serves input files directly from the ComfyUI Input folder., ]]
- [[_COMMUNITY_load_or_create_encryption_key, Loads the system encryption k|load_or_create_encryption_key, Loads the system encryption k]]
- [[_COMMUNITY_Shows a non-blocking warning message for missing FFmpeg., sh|Shows a non-blocking warning message for missing FFmpeg., sh]]
- [[_COMMUNITY_print_configuration, Prints the current configuration in a n|print_configuration, Prints the current configuration in a n]]
- [[_COMMUNITY_check_metadata, Lightweight endpoint to check real-time stat|check_metadata, Lightweight endpoint to check real-time stat]]
- [[_COMMUNITY_check_for_updates, Checks the GitHub repo for a newer versio|check_for_updates, Checks the GitHub repo for a newer versio]]
- [[_COMMUNITY_System Health Check with user advice and cross-platform wait|System Health Check with user advice and cross-platform wait]]
- [[_COMMUNITY_management_api_only, Security Decorator Blocks access to de|management_api_only, Security Decorator: Blocks access to de]]
- [[_COMMUNITY_Shows a critical error message and exits the program., show_|Shows a critical error message and exits the program., show_]]
- [[_COMMUNITY_ai_check_status, Checks the status of a specific search sess|ai_check_status, Checks the status of a specific search sess]]
- [[_COMMUNITY_ai_queue_search, Receives a search query from the frontend a|ai_queue_search, Receives a search query from the frontend a]]
- [[_COMMUNITY_check_port_available, Checks if the specified port is availa|check_port_available, Checks if the specified port is availa]]

## God Nodes (most connected - your core abstractions)
1. `get_db_connection()` - 52 edges
2. `get_dynamic_folder_config()` - 21 edges
3. `ComfyMetadataParser` - 13 edges
4. `get_file_info_from_db()` - 10 edges
5. `Exhibition Portal` - 10 edges
6. `Virtual Collections` - 10 edges
7. `extract_workflow()` - 9 edges
8. `initialize_gallery()` - 9 edges
9. `Ratings and Comments` - 8 edges
10. `get_standardized_path()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Exhibition Portal` --conceptually_related_to--> `exhibition_login()`  [INFERRED]
  README.md → F:\workspace\smart-comfyui-gallery\smartgallery.py
- `Exhibition Portal` --conceptually_related_to--> `exhibition_logout()`  [INFERRED]
  README.md → F:\workspace\smart-comfyui-gallery\smartgallery.py
- `Compare Mode` --conceptually_related_to--> `compare_files_api()`  [INFERRED]
  README.md → F:\workspace\smart-comfyui-gallery\smartgallery.py
- `Focus Mode` --conceptually_related_to--> `gallery_view()`  [INFERRED]
  README.md → F:\workspace\smart-comfyui-gallery\smartgallery.py
- `Video Storyboard` --conceptually_related_to--> `serve_storyboard_frame()`  [INFERRED]
  README.md → F:\workspace\smart-comfyui-gallery\smartgallery.py

## Hyperedges (group relationships)
- **DAM Collaboration Surface** — concept_dam_mode, concept_virtual_collections, concept_status_tags, concept_ratings_comments, concept_user_management, concept_exhibition_portal [INFERRED 0.84]
- **Advanced Media Inspection** — concept_workflow_recall, concept_compare_mode, concept_storyboard, smartgallery_extract_workflow, smartgallery_compare_files_api, smartgallery_get_storyboard [INFERRED 0.86]
- **Main Workspace Shell** — concept_main_workspace, tpl_index, asset_sidebar_tabs, asset_top_toolbar, asset_focus_on [EXTRACTED 1.00]

## Communities

### Community 0 - "External Folder Mounting, ai_indexing_add_files"
Cohesion: 0.06
Nodes (48): External Folder Mounting, ai_indexing_add_files(), ai_indexing_add_folder(), ai_indexing_control(), ai_indexing_reset(), ai_indexing_status(), ai_watched_folders(), background_rescan_worker() (+40 more)

### Community 1 - "Collections Screenshot, Comments Panel Screenshot"
Cohesion: 0.09
Nodes (31): Collections Screenshot, Comments Panel Screenshot, Compare Mode Screenshot, Exhibition Portal Screenshot, Focus Mode Screenshot, Sidebar Tabs Screenshot, Statuses Screenshot, Storyboard Screenshot (+23 more)

### Community 2 - "clean_prompt_text, ComfyMetadataParser"
Cohesion: 0.13
Nodes (13): clean_prompt_text(), ComfyMetadataParser, Cleans a raw prompt string: removes LoRA tags, normalizes whitespace,     and e, Advanced parser that traces the workflow graph to find real generation parameter, Main parsing method. Returns a standardized dictionary., Finds the main KSampler node ID., Follows links recursively to find the actual value.         Improved to handle, Traces the latent image link.          If direct tracing fails, it attempts to (+5 more)

### Community 3 - "Workflow Recall, download_file"
Cohesion: 0.15
Nodes (18): Workflow Recall, download_file(), download_workflow(), extract_workflow(), get_file_info_from_db(), get_node_summary(), Generator that yields all valid JSON objects found in the byte stream.     Sear, Extracts workflow JSON from image/video files.          Args:         filepat (+10 more)

### Community 4 - "check_rescan_status, check_zip_status"
Cohesion: 0.13
Nodes (5): Colors, # NOTE: A full ffmpeg installation is highly recommended., # IMPORTANT:, # NOTE: This usually requires Developer Mode enabled OR running ComfyUI as Admin, # IMPORTANT: If your paths contain SPACES, you MUST use quotes around them!

### Community 5 - "check_exhibition_requirements, cleanup_invalid_watched_folde"
Cohesion: 0.22
Nodes (11): check_exhibition_requirements(), cleanup_invalid_watched_folders(), find_ffprobe_path(), full_sync_database(), init_db(), initialize_gallery(), initialize_gallery_fast_no_db_check(), pregenerate_exhibition_cache() (+3 more)

### Community 6 - "User Management Screenshot, User Management and ACL"
Cohesion: 0.22
Nodes (8): User Management Screenshot, User Management and ACL, admin_manage_users(), decrypt_password(), encrypt_password(), ensure_admin_user(), exhibition_login(), Checks for admin user and applies password from startup config.

### Community 7 - "create_thumbnail, extract_workflow_files_string"
Cohesion: 0.22
Nodes (9): create_thumbnail(), extract_workflow_files_string(), extract_workflow_prompt_string(), _is_garbage_text(), process_single_file(), Parses workflow and returns a normalized string containing ONLY filenames, Broad extraction for Database Indexing (Searchable Keywords).     This function, Worker function to perform all heavy processing for a single file.     Designed (+1 more)

### Community 8 - "api_search_options, collection_view"
Cohesion: 0.22
Nodes (9): api_search_options(), collection_view(), gallery_view(), get_filter_options_from_db(), normalize_smart_path(), Scans the physical folder to count files and extract metadata.     Supports rec, Extracts extensions and prefixes for dropdowns using a robust      Python-side, Normalizes a path string for search comparison:     1. Converts to lowercase. (+1 more)

### Community 9 - "filter_enabled_nodes, generate_node_summary"
Cohesion: 0.33
Nodes (6): filter_enabled_nodes(), generate_node_summary(), get_node_color(), Generates a unique and consistent color for a node type., Filters and returns only active nodes and links (mode=0) from a workflow., Analyzes a workflow JSON, extracts active nodes, and identifies input media.

### Community 10 - "delete_batch, delete_file"
Cohesion: 0.5
Nodes (4): delete_batch(), delete_file(), Safely delete a file by either moving it to trash (if DELETE_TO is configured), safe_delete_file()

### Community 11 - "analyze_file_metadata, format_duration"
Cohesion: 0.67
Nodes (3): analyze_file_metadata(), format_duration(), is_webp_animated()

### Community 12 - "Serves input files directly from the ComfyUI Input folder., "
Cohesion: 1.0
Nodes (2): Serves input files directly from the ComfyUI Input folder., serve_input_file()

### Community 13 - "load_or_create_encryption_key, Loads the system encryption k"
Cohesion: 1.0
Nodes (2): load_or_create_encryption_key(), Loads the system encryption key if it exists.      Generates a new one only if

### Community 14 - "Shows a non-blocking warning message for missing FFmpeg., sh"
Cohesion: 1.0
Nodes (2): Shows a non-blocking warning message for missing FFmpeg., show_ffmpeg_warning()

### Community 15 - "print_configuration, Prints the current configuration in a n"
Cohesion: 1.0
Nodes (2): print_configuration(), Prints the current configuration in a neat, aligned table.

### Community 16 - "check_metadata, Lightweight endpoint to check real-time stat"
Cohesion: 1.0
Nodes (2): check_metadata(), Lightweight endpoint to check real-time status of metadata.     Now includes Re

### Community 17 - "check_for_updates, Checks the GitHub repo for a newer versio"
Cohesion: 1.0
Nodes (2): check_for_updates(), Checks the GitHub repo for a newer version without external libs.

### Community 18 - "System Health Check with user advice and cross-platform wait"
Cohesion: 1.0
Nodes (2): System Health Check with user advice and cross-platform wait.     Verifies libr, run_integrity_check()

### Community 19 - "management_api_only, Security Decorator: Blocks access to de"
Cohesion: 1.0
Nodes (2): management_api_only(), Security Decorator: Blocks access to destructive or management APIs      when t

### Community 20 - "Shows a critical error message and exits the program., show_"
Cohesion: 1.0
Nodes (2): Shows a critical error message and exits the program., show_config_error_and_exit()

### Community 21 - "ai_check_status, Checks the status of a specific search sess"
Cohesion: 1.0
Nodes (2): ai_check_status(), Checks the status of a specific search session.

### Community 22 - "ai_queue_search, Receives a search query from the frontend a"
Cohesion: 1.0
Nodes (2): ai_queue_search(), Receives a search query from the frontend and adds it to the DB queue.     Also

### Community 23 - "check_port_available, Checks if the specified port is availa"
Cohesion: 1.0
Nodes (2): check_port_available(), Checks if the specified port is available on the host machine.     Returns True

## Ambiguous Edges - Review These
- `Exhibition Portal` → `Video Storyboard`  [AMBIGUOUS]
  README.md · relation: semantically_similar_to

## Knowledge Gaps
- **68 isolated node(s):** `Colors`, `System Health Check with user advice and cross-platform wait.     Verifies libr`, `Converts path to absolute, forces forward slashes, and handles case sensitivity`, `Normalizes a path string for search comparison:     1. Converts to lowercase.`, `Prints the current configuration in a neat, aligned table.` (+63 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Serves input files directly from the ComfyUI Input folder., `** (2 nodes): `Serves input files directly from the ComfyUI Input folder.`, `serve_input_file()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `load_or_create_encryption_key, Loads the system encryption k`** (2 nodes): `load_or_create_encryption_key()`, `Loads the system encryption key if it exists.      Generates a new one only if`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shows a non-blocking warning message for missing FFmpeg., sh`** (2 nodes): `Shows a non-blocking warning message for missing FFmpeg.`, `show_ffmpeg_warning()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `print_configuration, Prints the current configuration in a n`** (2 nodes): `print_configuration()`, `Prints the current configuration in a neat, aligned table.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `check_metadata, Lightweight endpoint to check real-time stat`** (2 nodes): `check_metadata()`, `Lightweight endpoint to check real-time status of metadata.     Now includes Re`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `check_for_updates, Checks the GitHub repo for a newer versio`** (2 nodes): `check_for_updates()`, `Checks the GitHub repo for a newer version without external libs.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `System Health Check with user advice and cross-platform wait`** (2 nodes): `System Health Check with user advice and cross-platform wait.     Verifies libr`, `run_integrity_check()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `management_api_only, Security Decorator: Blocks access to de`** (2 nodes): `management_api_only()`, `Security Decorator: Blocks access to destructive or management APIs      when t`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shows a critical error message and exits the program., show_`** (2 nodes): `Shows a critical error message and exits the program.`, `show_config_error_and_exit()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ai_check_status, Checks the status of a specific search sess`** (2 nodes): `ai_check_status()`, `Checks the status of a specific search session.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ai_queue_search, Receives a search query from the frontend a`** (2 nodes): `ai_queue_search()`, `Receives a search query from the frontend and adds it to the DB queue.     Also`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `check_port_available, Checks if the specified port is availa`** (2 nodes): `check_port_available()`, `Checks if the specified port is available on the host machine.     Returns True`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Exhibition Portal` and `Video Storyboard`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **Why does `ComfyMetadataParser` connect `clean_prompt_text, ComfyMetadataParser` to `Workflow Recall, download_file`, `check_rescan_status, check_zip_status`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **Why does `get_db_connection()` connect `External Folder Mounting, ai_indexing_add_files` to `Collections Screenshot, Comments Panel Screenshot`, `Workflow Recall, download_file`, `check_rescan_status, check_zip_status`, `check_exhibition_requirements, cleanup_invalid_watched_folde`, `User Management Screenshot, User Management and ACL`, `api_search_options, collection_view`, `delete_batch, delete_file`, `check_metadata, Lightweight endpoint to check real-time stat`, `ai_check_status, Checks the status of a specific search sess`, `ai_queue_search, Receives a search query from the frontend a`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `tag_batch()` connect `Collections Screenshot, Comments Panel Screenshot` to `External Folder Mounting, ai_indexing_add_files`, `check_rescan_status, check_zip_status`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Exhibition Portal` (e.g. with `exhibition_login()` and `exhibition_logout()`) actually correct?**
  _`Exhibition Portal` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Colors`, `System Health Check with user advice and cross-platform wait.     Verifies libr`, `Converts path to absolute, forces forward slashes, and handles case sensitivity` to the rest of the system?**
  _68 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `External Folder Mounting, ai_indexing_add_files` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._