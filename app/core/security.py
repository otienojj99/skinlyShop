from pathlib import Path

PUBLIC_KEY = Path("keys/public.pem").read_text
JWT_ALGORITHM = "RS256"
