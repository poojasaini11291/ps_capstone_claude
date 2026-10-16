
#!/usr/bin/env bash

INPUT=$(cat)

if printf '%s' "$INPUT" | grep -Eq '(^|[^[:alnum:]_])\.env([^[:alnum:]_]|$)'; then
  echo "Secret file access requires review." >&2
  exit 2
fi

exit 0
