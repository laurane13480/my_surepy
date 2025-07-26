import configparser
import logging
import pprint
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from surepy import Surepy
from surepy.enums import LockState

token_file = Path("~/.surepy.token").expanduser()
old_token_file = token_file.with_suffix(".old_token")
auth_file = Path("~/.surepy.auth").expanduser()
config = configparser.ConfigParser()
config.read(str(auth_file))


def file_older_then(file: Path, delta: timedelta) -> bool:
    return datetime.fromtimestamp(file.stat().st_mtime) < (datetime.now() - delta)


async def get_surepy() -> Surepy | None:
    return Surepy(
        email=config.get("Login", "email"),
        password=config.get("Login", "password"),
    )

@pytest.mark.asyncio
async def test_get_entities() -> None:
    spy = await get_surepy()

    response = await spy.get_entities(refresh=True)

    with open("response.txt", "w") as file:
        file.write(pprint.pformat(response))

    assert len(response) > 0

@pytest.mark.asyncio
async def test_set_lock_state_tag() -> None:
    spy = await get_surepy()

    response = await spy.sac._set_lock_state_for_tag(device_id=1103637, tag_id=1932540, mode=LockState.UNLOCKED)

    with open("response.txt", "w") as file:
        file.write(pprint.pformat(response))

    assert len(response) > 0


@pytest.mark.asyncio
async def test_get_actions() -> None:
    spy = await get_surepy()

    response = await spy.get_actions(household_id=config.get("IDs", "household"))

    assert len(response) > 0


@pytest.mark.asyncio
async def test_get_latest_anonymous_drinks() -> None:
    spy = await get_surepy()

    response = await spy.get_latest_anonymous_drinks(household_id=config.get("IDs", "household"))

    assert len(response) > 0
