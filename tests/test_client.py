import configparser
import logging
import pprint
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from surepylhn import Surepy
from surepylhn.enums import LockState

token_file = Path("~/.surepylhn.token").expanduser()
old_token_file = token_file.with_suffix(".old_token")
auth_file = Path("~/.surepylhn.auth").expanduser()
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
async def test_set_profile_for_tag() -> None:
    spy = await get_surepy()

    response = await spy.sac.set_profile_for_tag(device_id=1103637, tag_id=1932540, mode=LockState.UNLOCKED)

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
