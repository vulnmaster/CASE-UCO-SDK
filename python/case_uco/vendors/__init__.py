"""Readers for forensic tool output that tolerate layout drift between versions.

Each reader returns a plain record with the fields it recognized, the raw
sections it did not, and a ``warnings`` list naming every assumption it made
(a guessed date order, a missing section). Mapping a record into a
:class:`~case_uco.CASEGraph` is a separate step, so a new tool version that
renames a field breaks one lookup rather than the whole ingest.
"""

__all__ = ["cellebrite", "file_identity", "magnet"]
