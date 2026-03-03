#!/bin/bash

# Risk Assessment Engine - Setup Script
# Run this script to set up the environment

echo "=================================="
echo "Risk Assessment Engine Setup"
echo "=================================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if Python 3.10+
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "ERROR: Python 3.10+ is required"
    exit 1
fi

echo ""
echo "Creating virtual environment (.venv)..."
python3 -m venv .venv

echo ""
echo "Installing dependencies..."
.venv/bin/pip install --upgrade pip setuptools wheel
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install pytest
.venv/bin/pip install -e .

echo ""
echo "Creating necessary directories..."
mkdir -p assessments

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Quick Start:"
echo "  1. Activate venv: source .venv/bin/activate"
echo "  2. Generate sample: python -m risk_assessment_engine sample -o my-merchant.json"
echo "  3. Edit my-merchant.json with your research findings"
echo "  4. Run assessment: python -m risk_assessment_engine assess my-merchant.json -r report.md"
echo ""
echo "Documentation:"
echo "  - README.md"
echo "  - docs/BI-LICENSE-VERIFICATION-GUIDE.md"
echo ""
