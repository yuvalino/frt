"""Tests for /screenshot endpoint: the view as a PNG."""

import struct

import pytest

from frt_client import FrtClient, FrtError


def _size(png: bytes) -> tuple[int, int]:
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", png[16:24])


async def test_screenshot_png(frt: FrtClient):
    png = await frt.screenshot()
    width, height = _size(png)
    assert width > 0 and height > 0


async def test_screenshot_scale(frt: FrtClient):
    full = _size(await frt.screenshot())
    half = _size(await frt.screenshot(scale=0.5))
    assert abs(half[0] - full[0] / 2) <= 1 and abs(half[1] - full[1] / 2) <= 1


async def test_screenshot_bad_scale(frt: FrtClient):
    with pytest.raises(FrtError) as e:
        await frt.screenshot(scale=0)
    assert e.value.status == 400
