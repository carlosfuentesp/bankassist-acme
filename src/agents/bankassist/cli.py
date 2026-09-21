from __future__ import annotations

import argparse
import json

from agents.bankassist.async_utils import run_sync
from agents.bankassist.prompts import DEFAULT_QUESTION
from agents.bankassist.service import ask_bankassist


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a grounded BankAssist question.")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    result = run_sync(ask_bankassist(args.question))
    if args.as_json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, default=str))
    else:
        print(result.answer)


if __name__ == "__main__":
    main()
