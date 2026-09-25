# Deployment instruction

- When the user sends `Deploy` or `d` as a deployment command, deploy this project to GitHub.
- Stage and commit all current repository changes, including modified and untracked files, then push the current branch to its existing GitHub `origin` remote.
- Do not deploy to Cloudflare or another hosting provider unless the user explicitly requests it.
- After pushing, verify that the local commit matches the corresponding remote branch and report the commit ID.
