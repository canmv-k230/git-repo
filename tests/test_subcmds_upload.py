# Copyright (C) 2020 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unittests for the subcmds/init.py module."""

import unittest

from unittest import mock
from subcmds import upload
from error import UploadError, GitError


class UnexpectedException(Exception):
    """An exception not expected by upload command."""


class UploadCommand(unittest.TestCase):
    """Check registered all_commands."""

    def setUp(self):
        self.cmd = upload.Upload()
        self.branch = mock.MagicMock()
        self.people = mock.MagicMock()
        self.opt, _ = self.cmd.OptionParser.parse_args([])
        mock.patch.object(
            self.cmd, "_AppendAutoList", return_value=None
        ).start()
        mock.patch.object(self.cmd, "git_event_log").start()

    def test_UploadAndReport_UploadError(self):
        """Check UploadExitError raised when UploadError encoutered."""
        side_effect = UploadError("upload error")
        with mock.patch.object(
            self.cmd, "_UploadBranch", side_effect=side_effect
        ):
            with self.assertRaises(upload.UploadExitError):
                self.cmd._UploadAndReport(self.opt, [self.branch], self.people)

    def test_UploadAndReport_GitError(self):
        """Check UploadExitError raised when UploadError encoutered."""
        side_effect = GitError("some git error")
        with mock.patch.object(
            self.cmd, "_UploadBranch", side_effect=side_effect
        ):
            with self.assertRaises(upload.UploadExitError):
                self.cmd._UploadAndReport(self.opt, [self.branch], self.people)

    def test_UploadAndReport_UnhandledError(self):
        """Check UploadExitError raised when UploadError encoutered."""
        side_effect = UnexpectedException("some os error")
        with mock.patch.object(
            self.cmd, "_UploadBranch", side_effect=side_effect
        ):
            with self.assertRaises(type(side_effect)):
                self.cmd._UploadAndReport(self.opt, [self.branch], self.people)
