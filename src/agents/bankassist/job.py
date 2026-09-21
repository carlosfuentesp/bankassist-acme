from __future__ import annotations

import json

from agents.bankassist.async_utils import run_sync
from agents.bankassist.prompts import DEFAULT_QUESTION
from agents.bankassist.service import ask_bankassist


def main() -> None:
    result = run_sync(ask_bankassist(DEFAULT_QUESTION))
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
