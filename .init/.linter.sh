#!/bin/bash
cd /tmp/kavia/workspace/code-generation/simple-e-commerce-platform-2438-2447/backend_django
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

