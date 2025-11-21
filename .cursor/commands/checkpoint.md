# checkpoint

Create a checkpoint commit right now. Stage all current changes and commit them with a checkpoint message. This is for saving progress during debugging - tests do NOT need to pass.

## Behavior

1. Check what files have been modified/added
2. Stage all current changes (or use user-specified files if provided in the prompt)
3. Create a commit with message format: `checkpoint(scope): brief description`
4. **Do NOT run `poetry run poe check:fix`** - checkpoint commits are intermediate saves during debugging
5. The commit message should briefly describe the current debugging state or what was attempted

## Commit Message Format

Use: `checkpoint(scope): brief description`

**Examples:**
- `checkpoint(debug): attempt to fix level number resolution issue`
- `checkpoint(test): partial fix for handler configuration tests`
- `checkpoint(logger): debugging custom level registration`

## Important Notes

- This creates the commit immediately - do not ask for permission
- Checkpoint commits are intermediate saves and don't need to pass all checks
- The commit should still be meaningful and describe what state you're in
- If the user provides additional context in the prompt, incorporate it into the commit message

