"""Allow running as module: python -m risk_assessment_engine"""

from .main import main
import sys

if __name__ == "__main__":
    sys.exit(main())
