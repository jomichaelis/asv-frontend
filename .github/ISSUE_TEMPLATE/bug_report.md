---
name: Bug report
about: Create a bug report to be fixed
title: ''
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Start with a clean clone of the main branch
2. Set up and activate your venv with `uv venv .venv -p 3.10 && source ./venv/bin/activate`
3. Run `make`
4. Copy file '<scene>.usda' from /mnt/scratch/x to your repository
5. Run the following script:

Ideally, include a short script here to let other developers reproduce the error.

```python
from radarCrater.scene import Scene

scene = Scene.import_from_file("scene.usda")
# ...
```

**Experienced behavior**
Add error logs, plots or screenshots which sufficiently allow for error analysis.

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment (please complete the following information):**
 - OS: [Win/Linux]
 - machine used: [fived03, fived10] (if relevant, add the GPU model here, too)
 - radarCrater version/branch/tag used [e.g. v1.5.2]
 - any other additions made to your environment (e.g. environment variables like $PYTHONPATH, python packages, etc.)

**Additional context**
Add any other context about the problem here.
