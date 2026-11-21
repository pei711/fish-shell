#!/usr/bin/env python3
import os
import pexpect
from pexpect_helper import SpawnedProc

env = os.environ.copy()
env["TERM"] = "xterm"
env["FISH_TEST_NO_RECURRENT_QUERIES"] = ""
sp = SpawnedProc(env=env)
sp.expect_prompt()
sp.send_cursor_position_report(y=1, x=1)
sp.send("\x1b]11;rgb:0000/0000/0000\x07")
sp.send_primary_device_attribute()

# Recurrent queries are disabled by default in the pexpect tests. Enable them
# and exit from the next fish_prompt event to ensure Fish does not leave a
# terminal query unanswered as it exits.
sp.sendline(
    "set -e FISH_TEST_NO_RECURRENT_QUERIES; "
    "function exit_at_prompt --on-event fish_prompt; exit; end"
)
sp.spawn.expect(pexpect.EOF)
assert "\x1b[6n" not in sp.spawn.before
