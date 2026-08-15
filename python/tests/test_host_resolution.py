"""Host resolution must treat helper output as the File bundle, not DiskImage."""

from __future__ import annotations

from case_uco.critique.hosts import host_matches, resolve_host
from case_uco.graph import CASEGraph
from case_uco.helpers import file_with_content_hashes, raster_picture_with_hashes


def test_observable_object_with_file_facet_is_file() -> None:
    graph = CASEGraph()
    obj = file_with_content_hashes(graph, file_name="x.bin", hashes=[("SHA256", "cc")])
    assert resolve_host(obj) == "File"
    assert host_matches("File", ("File", "ObservableObject"))


def test_raster_picture_host() -> None:
    graph = CASEGraph()
    pic = raster_picture_with_hashes(graph, file_name="p.jpg", hashes=[("SHA256", "dd")])
    assert resolve_host(pic) == "RasterPicture"


def test_disk_image_never_required() -> None:
    assert resolve_host({"@type": "DiskImage"}, "DiskImage") == "File"
