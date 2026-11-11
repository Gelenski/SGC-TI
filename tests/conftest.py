import sys
from pathlib import Path

# Garante que os testes encontrem a pasta 'src'
src_path = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_path))