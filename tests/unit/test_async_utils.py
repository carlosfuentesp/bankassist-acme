import asyncio

from agents.bankassist.async_utils import run_sync


async def _value():
    return 42


def test_run_sync_without_existing_loop():
    assert run_sync(_value()) == 42


def test_run_sync_with_existing_loop():
    async def caller():
        return run_sync(_value())

    assert asyncio.run(caller()) == 42
