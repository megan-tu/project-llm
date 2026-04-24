# AGENTS.md

## Tool Usage Rules
- Always use tools when performing file operations (reading, writing, deleting).
- Use `write_file` or `write_files` to create or modify files.
- Use `rm` to delete files.
- Use `ls`, `cat`, and `grep` to inspect the filesystem.
- Do not simulate file operations in text—use tools instead.

## Git Behavior
- Every file creation or modification must include a commit message.
- Use clear, descriptive commit messages (e.g., "add hello world script").
- Assume all file changes are automatically committed via tools.

## Output Rules
- Keep responses short and direct (1–2 sentences unless using tools).
- When using a tool, return the tool output exactly.
- Do not add extra explanation when a tool is used.

## File Safety
- Only operate on safe, relative paths.
- Do not attempt to access system or absolute paths.
