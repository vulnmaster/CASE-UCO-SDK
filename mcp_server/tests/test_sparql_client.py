"""Remote SPARQL client and MCP surface tests (issue #120)."""

from __future__ import annotations

import io
import json
import urllib.error
import urllib.request

import pytest

import sparql_client


PUBLIC_IP = "8.8.8.8"


class FakeResponse:
    def __init__(
        self,
        body: bytes,
        content_type: str,
        *,
        status: int = 200,
        content_length: int | None = None,
    ) -> None:
        self._body = io.BytesIO(body)
        self.status = status
        self.headers = {"Content-Type": content_type}
        if content_length is not None:
            self.headers["Content-Length"] = str(content_length)

    def read(self, amount: int = -1) -> bytes:
        return self._body.read(amount)

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None


@pytest.fixture(autouse=True)
def clean_sparql_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        sparql_client.DEFAULT_ENDPOINT_ENV,
        sparql_client.ALLOWED_HOSTS_ENV,
        sparql_client.PRIVATE_HOSTS_ENV,
        sparql_client.SECURE_NETWORK_ENV,
        "CASE_UCO_MCP_PROFILE",
        "CASE_UCO_MCP_SECURE_MODE",
    ):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def public_dns(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        sparql_client.ALLOWED_HOSTS_ENV,
        "example.org,sparql.example.org,approved.example",
    )
    monkeypatch.setattr(
        sparql_client,
        "_resolve_addresses",
        lambda _host, _port: (sparql_client.ipaddress.ip_address(PUBLIC_IP),),
    )


@pytest.mark.parametrize("form", ["SELECT", "ASK", "CONSTRUCT", "DESCRIBE"])
def test_query_forms_allowed(form: str) -> None:
    query = f"PREFIX ex: <https://example.org/>\n{form} "
    if form == "SELECT":
        query += "?s WHERE { ?s ?p ?o } LIMIT 1"
    elif form == "ASK":
        query += "{ ?s ?p ?o }"
    elif form == "CONSTRUCT":
        query += "{ ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 1"
    else:
        query += "?s WHERE { ?s ?p ?o } LIMIT 1"
    assert sparql_client.validate_query(query) == form


@pytest.mark.parametrize(
    "query,error",
    [
        ("INSERT DATA { <urn:s> <urn:p> <urn:o> }", "sparql_update_forbidden"),
        ("CLEAR ALL", "sparql_update_forbidden"),
        (
            "SELECT * WHERE { SERVICE <https://example.org/sparql> { ?s ?p ?o } }",
            "sparql_service_forbidden",
        ),
        ("", "sparql_query_empty"),
        ("not a query", "sparql_query_form_unsupported"),
    ],
)
def test_unsafe_or_invalid_queries_rejected(query: str, error: str) -> None:
    with pytest.raises(sparql_client.SparqlClientError, match=error):
        sparql_client.validate_query(query)


def test_keywords_in_data_do_not_trigger_policy() -> None:
    query = """
        # SERVICE <https://ignored.example/sparql>
        PREFIX insert: <https://example.org/DELETE/>
        SELECT ?insert WHERE {
          ?s <https://example.org/service> "DELETE and SERVICE are evidence" .
          BIND(?s AS ?insert)
        }
        LIMIT 1
    """
    assert sparql_client.validate_query(query) == "SELECT"


def test_comparison_operator_cannot_mask_stacked_update() -> None:
    query = "SELECT * WHERE { ?s ?p ?o FILTER(?o < 2) } ; DELETE WHERE { ?s ?p ?o }"
    with pytest.raises(sparql_client.SparqlClientError, match="sparql_update_forbidden"):
        sparql_client.validate_query(query)


def test_query_size_is_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sparql_client, "MAX_QUERY_CHARS", 10)
    with pytest.raises(sparql_client.SparqlClientError, match="sparql_query_too_large"):
        sparql_client.validate_query("SELECT * WHERE { ?s ?p ?o }")


def test_default_endpoint_is_caselinker(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(sparql_client.DEFAULT_ENDPOINT_ENV, raising=False)
    assert sparql_client.configured_endpoint() == sparql_client.DEFAULT_ENDPOINT


def test_public_https_endpoint_allowed(public_dns: None) -> None:
    url = "https://sparql.example.org/query"
    assert sparql_client.validate_endpoint(url) == url


@pytest.mark.parametrize(
    "url,error",
    [
        ("file:///etc/passwd", "sparql_endpoint_scheme_forbidden"),
        ("https://user:secret@example.org/sparql", "sparql_endpoint_invalid"),
        ("https://example.org/sparql#fragment", "sparql_endpoint_invalid"),
        ("http://example.org/sparql", "sparql_endpoint_https_required"),
    ],
)
def test_endpoint_syntax_and_transport_policy(
    url: str,
    error: str,
    public_dns: None,
) -> None:
    with pytest.raises(sparql_client.SparqlClientError, match=error):
        sparql_client.validate_endpoint(url)


def test_private_endpoint_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(sparql_client.ALLOWED_HOSTS_ENV, "localhost")
    monkeypatch.setattr(
        sparql_client,
        "_resolve_addresses",
        lambda _host, _port: (sparql_client.ipaddress.ip_address("127.0.0.1"),),
    )
    with pytest.raises(
        sparql_client.SparqlClientError,
        match="sparql_endpoint_private_address_forbidden",
    ):
        sparql_client.validate_endpoint("http://localhost:3030/query")


def test_private_fuseki_requires_exact_allowlist(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(sparql_client.PRIVATE_HOSTS_ENV, "localhost")
    monkeypatch.setattr(
        sparql_client,
        "_resolve_addresses",
        lambda _host, _port: (sparql_client.ipaddress.ip_address("127.0.0.1"),),
    )
    url = "http://localhost:3030/dataset/query"
    assert sparql_client.validate_endpoint(url) == url


def test_optional_host_allowlist(public_dns: None, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(sparql_client.ALLOWED_HOSTS_ENV, "approved.example")
    with pytest.raises(
        sparql_client.SparqlClientError,
        match="sparql_endpoint_not_allowlisted",
    ):
        sparql_client.validate_endpoint("https://other.example/query")


def test_nondefault_public_host_requires_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sparql_client,
        "_resolve_addresses",
        lambda _host, _port: (sparql_client.ipaddress.ip_address(PUBLIC_IP),),
    )
    with pytest.raises(
        sparql_client.SparqlClientError,
        match="sparql_endpoint_not_allowlisted",
    ):
        sparql_client.validate_endpoint("https://unconfigured.example/query")


def test_endpoint_query_parameters_are_not_reflected() -> None:
    assert (
        sparql_client._display_endpoint("https://example.org/sparql?token=secret")
        == "https://example.org/sparql"
    )


def test_secure_profile_disables_egress_by_default(
    public_dns: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CASE_UCO_MCP_PROFILE", "offline-investigation")
    with pytest.raises(
        sparql_client.SparqlClientError,
        match="sparql_network_disabled_by_profile",
    ):
        sparql_client.validate_endpoint("https://example.org/query")


def test_secure_profile_can_explicitly_enable_egress(
    public_dns: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CASE_UCO_MCP_PROFILE", "production-review")
    monkeypatch.setenv(sparql_client.SECURE_NETWORK_ENV, "1")
    assert (
        sparql_client.validate_endpoint("https://example.org/query")
        == "https://example.org/query"
    )


def test_select_response_is_normalized(
    public_dns: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = {
        "head": {"vars": ["case", "count"]},
        "results": {
            "bindings": [
                {
                    "case": {"type": "uri", "value": "https://example.org/case/1"},
                    "count": {
                        "type": "literal",
                        "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                        "value": "2",
                    },
                }
            ]
        },
    }
    captured: dict[str, object] = {}

    def fake_open(request: urllib.request.Request, timeout: float) -> FakeResponse:
        captured["request"] = request
        captured["timeout"] = timeout
        body = json.dumps(payload).encode("utf-8")
        return FakeResponse(
            body,
            "application/sparql-results+json; charset=utf-8",
            content_length=len(body),
        )

    monkeypatch.setattr(sparql_client, "_open_request", fake_open)
    query = "SELECT ?case (COUNT(*) AS ?count) WHERE { ?case ?p ?o } GROUP BY ?case LIMIT 1"
    result = sparql_client.execute_query(query, "https://example.org/sparql", 99)

    assert result["ok"] is True
    assert result["result_kind"] == "bindings"
    assert result["row_count"] == 1
    assert result["variables"] == ["case", "count"]
    assert result["bindings"] == payload["results"]["bindings"]
    assert result["content_trust"] == "untrusted-external-sparql-results"
    assert "query" not in result
    assert len(result["query_sha256"]) == 64
    assert captured["timeout"] == sparql_client.MAX_TIMEOUT_SECONDS
    request = captured["request"]
    assert isinstance(request, urllib.request.Request)
    assert request.method == "POST"
    assert request.data == query.encode("utf-8")
    assert request.get_header("Content-type").startswith("application/sparql-query")


def test_ask_and_construct_responses(
    public_dns: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sparql_client,
        "_open_request",
        lambda _request, _timeout: FakeResponse(
            b'{"head": {}, "boolean": true}',
            "application/sparql-results+json",
        ),
    )
    ask = sparql_client.execute_query("ASK { ?s ?p ?o }", "https://example.org/sparql")
    assert ask["result_kind"] == "boolean"
    assert ask["boolean"] is True

    monkeypatch.setattr(
        sparql_client,
        "_open_request",
        lambda _request, _timeout: FakeResponse(
            b"<urn:s> <urn:p> <urn:o> .\n",
            "text/turtle",
        ),
    )
    graph = sparql_client.execute_query(
        "CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 1",
        "https://example.org/sparql",
    )
    assert graph["result_kind"] == "rdf-text"
    assert graph["rdf"].startswith("<urn:s>")


def test_select_refuses_non_json_result_media_type(
    public_dns: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sparql_client,
        "_open_request",
        lambda _request, _timeout: FakeResponse(b"s\nurn:case:1\n", "text/csv"),
    )
    with pytest.raises(
        sparql_client.SparqlClientError,
        match="sparql_response_media_type_unsupported",
    ):
        sparql_client.execute_query(
            "SELECT ?s WHERE { ?s ?p ?o } LIMIT 1",
            "https://example.org/sparql",
        )


def test_jsonld_array_graph_is_supported(
    public_dns: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sparql_client,
        "_open_request",
        lambda _request, _timeout: FakeResponse(
            b'[{"@id":"urn:s","urn:p":{"@id":"urn:o"}}]',
            "application/ld+json",
        ),
    )
    result = sparql_client.execute_query(
        "DESCRIBE ?s WHERE { ?s ?p ?o } LIMIT 1",
        "https://example.org/sparql",
    )
    assert result["result_kind"] == "rdf-jsonld"
    assert isinstance(result["graph"], list)


def test_http_error_is_typed_without_remote_body(
    public_dns: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_http(request: urllib.request.Request, _timeout: float) -> FakeResponse:
        raise urllib.error.HTTPError(
            request.full_url,
            429,
            "Too Many Requests",
            {},
            io.BytesIO(b"untrusted remote instructions"),
        )

    monkeypatch.setattr(sparql_client, "_open_request", raise_http)
    with pytest.raises(sparql_client.SparqlClientError) as caught:
        sparql_client.execute_query(
            "ASK { ?s ?p ?o }",
            "https://example.org/sparql",
        )
    result = sparql_client.error_result(caught.value)
    assert result == {
        "ok": False,
        "error": "sparql_remote_http_error",
        "tool_name": sparql_client.TOOL_NAME,
        "tool_version": sparql_client.TOOL_VERSION,
        "http_status": 429,
    }


def test_redirect_is_refused(
    public_dns: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_redirect(request: urllib.request.Request, _timeout: float) -> FakeResponse:
        raise urllib.error.HTTPError(
            request.full_url,
            302,
            "Found",
            {"Location": "http://127.0.0.1/private"},
            io.BytesIO(),
        )

    monkeypatch.setattr(sparql_client, "_open_request", raise_redirect)
    with pytest.raises(
        sparql_client.SparqlClientError,
        match="sparql_redirect_forbidden",
    ):
        sparql_client.execute_query(
            "ASK { ?s ?p ?o }",
            "https://example.org/sparql",
        )


def test_nonfinite_timeout_is_rejected(
    public_dns: None,
) -> None:
    with pytest.raises(
        sparql_client.SparqlClientError,
        match="sparql_timeout_invalid",
    ):
        sparql_client.execute_query(
            "ASK { ?s ?p ?o }",
            "https://example.org/sparql",
            float("nan"),
        )


def test_response_size_is_bounded(
    public_dns: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sparql_client, "MAX_RESPONSE_BYTES", 10)
    monkeypatch.setattr(
        sparql_client,
        "_open_request",
        lambda _request, _timeout: FakeResponse(
            b"{}",
            "application/sparql-results+json",
            content_length=11,
        ),
    )
    with pytest.raises(
        sparql_client.SparqlClientError,
        match="sparql_response_too_large",
    ):
        sparql_client.execute_query(
            "ASK { ?s ?p ?o }",
            "https://example.org/sparql",
        )


def test_streamed_response_size_is_bounded_without_content_length(
    public_dns: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sparql_client, "MAX_RESPONSE_BYTES", 10)
    monkeypatch.setattr(
        sparql_client,
        "_open_request",
        lambda _request, _timeout: FakeResponse(
            b"01234567890",
            "application/sparql-results+json",
        ),
    )
    with pytest.raises(
        sparql_client.SparqlClientError,
        match="sparql_response_too_large",
    ):
        sparql_client.execute_query(
            "ASK { ?s ?p ?o }",
            "https://example.org/sparql",
        )


def test_server_exposes_sparql_tool_and_resource() -> None:
    import asyncio

    fastmcp = pytest.importorskip("fastmcp")
    import server

    async def inspect_surface() -> tuple[list[object], list[object]]:
        async with fastmcp.Client(server.mcp) as client:
            tools = await client.list_tools()
            resources = await client.list_resources()
            return tools, resources

    tools, resources = asyncio.run(inspect_surface())
    assert any(getattr(tool, "name", "") == "execute_sparql_query" for tool in tools)
    assert any(str(getattr(resource, "uri", "")) == "case-uco://sparql" for resource in resources)
    refused = server.execute_sparql_query("CLEAR ALL")
    assert refused["ok"] is False
    assert refused["error"] == "sparql_update_forbidden"
