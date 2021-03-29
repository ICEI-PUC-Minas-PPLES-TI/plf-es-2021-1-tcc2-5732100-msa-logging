from json import loads

import pytest

from app.models import GQL, Repository, repository


def test_gql_init():
    # Variable setup
    endpoint = "https://api.github.com/graphql"
    headers = dict(Accept="abc/xyz", Authorization="bearer token")

    # Object init
    gql = GQL(headers=headers)

    # Tests
    assert gql.endpoint == endpoint
    assert gql.headers == headers
    assert gql.query == ""
    assert gql.query_results == {}
    assert gql.query_template == ""
    assert gql.paging.has_next_page is False
    assert gql.paging.end_cursor == "null"
    assert gql.template_path == "app/queries"
    assert gql.template_variables == dict(
        AFTER_CURSOR="after: null",
    )


def test_gql_setup_manual():
    # Variables setup
    endpoint = "https://api.github.com/v4"
    headers = dict(Accept="abc/xyz", Authorization="bearer token")
    query = "{search(query:query)}"
    results = dict(
        data=dict(search=dict(pageInfo=dict(hasNextPage=True, endCursor="123abc")))
    )
    variables = dict(VAR_A="value 1", VAR_B="value 2")

    # Object init
    gql = GQL(endpoint=endpoint, headers={"a": "b"})

    # Object attributes setup
    gql.set_headers(headers)
    gql.set_query(query)
    gql.set_query_results(results)
    gql.set_template_variables(**variables)

    # Tests
    assert gql.endpoint == endpoint
    assert gql.headers == headers
    assert gql.query == query
    assert gql.query_results == results["data"]["search"]
    assert gql.template_variables == variables
    assert gql.paging.has_next_page is True
    assert gql.paging.end_cursor == '"123abc"'


def test_gql_run_query_ok(response_mock, mock_query_pull_requests):
    gql = GQL({})

    with response_mock(
        f"""
            POST https://api.github.com/graphql
    
            Allow: POST, HEAD
            Content-Language: en
            X-RateLimit-Remaining: 4987
    
            -> 200 :{mock_query_pull_requests}
            """
    ):
        r = gql.run_query()

    assert type(r) is dict


def test_gql_run_query_forbidden(response_mock, mock_query_pull_requests):
    gql = GQL({})

    with response_mock(
        f"""
            POST https://api.github.com/graphql
    
            Allow: POST, HEAD
            Content-Language: en
            X-RateLimit-Remaining: 4987
    
            -> 403 :{mock_query_pull_requests}
            """
    ):
        with pytest.raises(ConnectionRefusedError) as expt:
            r = gql.run_query()


def test_repository_constructor(response_mock, mock_query_repositories):
    gql = GQL({})

    with response_mock(
        f"""
            POST https://api.github.com/graphql
    
            Allow: POST, HEAD
            Content-Language: en
            X-RateLimit-Remaining: 4987
    
            -> 200 :{mock_query_repositories}
            """
    ):
        r = gql.run_query()
    repo = repository(r["nodes"][0])
    assert type(repo) is Repository


def test_repository_init():
    # Object init
    repo = Repository()

    # Tests
    assert repo.id == ""
    assert repo.owner == ""
    assert repo.name == ""
    assert repo.name_with_owner == "/"
    assert repo.url == ""
    assert repo.created_at == ""
    assert repo.updated_at == ""
    assert repo.primary_language_name == ""
    assert repo.license_info_name == ""
    assert repo.stargazers_total_count == -1
    assert repo.forks_total_count == -1
    assert repo.releases_total_count == -1
    assert repo.pull_requests == []
    assert repo.pull_requests_total_count == -1
    assert repo.pull_requests_open_count == -1
    assert repo.issues_total_count == -1
    assert repo.issues_open_count == -1
    assert repo.issues_open_old_count == -1


def test_repository_setup_manual():
    # Variables setup
    id_ = "id"
    owner = "owner"
    name = "name"
    url = "https://github.com/"
    created = "1970-01-01"
    updated = "2020-12-31"
    language = "Python"
    license = "Unlicense"
    stargazers = 42
    forks = 4
    releases = 1
    pr_total = 32
    pr_open = 16
    issues_total = 64
    issues_open = 8
    issues_open_old = 4

    # Object init
    repo = Repository()

    # Object attributes setup
    repo.set_id(id_)
    repo.set_owner(owner)
    repo.set_name(name)
    repo.set_url(url)
    repo.set_created_at(created)
    repo.set_updated_at(updated)
    repo.set_primary_language_name(language)
    repo.set_license_info_name(license)
    repo.set_stargazers_total_count(stargazers)
    repo.set_forks_total_count(forks)
    repo.set_releases_total_count(releases)
    repo.set_pull_requests_total_count(pr_total)
    repo.set_pull_requests_open_count(pr_open)
    repo.set_issues_total_count(issues_total)
    repo.set_issues_open_count(issues_open)
    repo.set_issues_open_old_count(issues_open_old)

    # Tests
    assert repo.id == id_
    assert type(repo.owner) is str
    assert repo.owner == owner
    assert type(repo.name) is str
    assert repo.name == name
    assert type(repo.name_with_owner) is str
    assert repo.name_with_owner == f"{owner}/{name}"
    assert type(repo.url) is str
    assert repo.url == url
    assert type(repo.created_at) is str
    assert repo.created_at == created
    assert type(repo.updated_at) is str
    assert repo.updated_at == updated
    assert type(repo.primary_language_name) is str
    assert repo.primary_language_name == language
    assert type(repo.license_info_name) is str
    assert repo.license_info_name == license
    assert type(repo.stargazers_total_count) is int
    assert repo.stargazers_total_count >= 0
    assert repo.stargazers_total_count == stargazers
    assert type(repo.forks_total_count) is int
    assert repo.forks_total_count >= 0
    assert repo.forks_total_count == forks
    assert type(repo.releases_total_count) is int
    assert repo.releases_total_count >= 0
    assert repo.releases_total_count == releases
    assert type(repo.pull_requests_total_count) is int
    assert repo.pull_requests_total_count >= 0
    assert repo.pull_requests_total_count == pr_total
    assert type(repo.pull_requests_open_count) is int
    assert repo.pull_requests_open_count >= 0
    assert repo.pull_requests_open_count == pr_open
    assert type(repo.issues_total_count) is int
    assert repo.issues_total_count >= 0
    assert repo.issues_total_count == issues_total
    assert type(repo.issues_open_count) is int
    assert repo.issues_open_count >= 0
    assert repo.issues_open_count == issues_open
    assert type(repo.issues_open_old_count) is int
    assert repo.issues_open_old_count >= 0
    assert repo.issues_open_old_count == issues_open_old

    # Killing mutants
    repo.set_stargazers_total_count(0)
    repo.set_forks_total_count(0)
    repo.set_releases_total_count(0)
    repo.set_pull_requests_total_count(0)
    repo.set_pull_requests_open_count(0)
    repo.set_issues_total_count(0)
    repo.set_issues_open_count(0)
    repo.set_issues_open_old_count(0)
    repo.set_stargazers_total_count(5.555)
    repo.set_forks_total_count(5.555)
    repo.set_releases_total_count(5.555)
    repo.set_pull_requests_total_count(5.555)
    repo.set_pull_requests_open_count(5.555)
    repo.set_issues_total_count(5.555)
    repo.set_issues_open_count(5.555)
    repo.set_issues_open_old_count(5.555)
    assert type(repo.stargazers_total_count) is int
    assert repo.stargazers_total_count == 0
    assert type(repo.forks_total_count) is int
    assert repo.forks_total_count == 0
    assert type(repo.releases_total_count) is int
    assert repo.releases_total_count == 0
    assert type(repo.pull_requests_total_count) is int
    assert repo.pull_requests_total_count == 0
    assert type(repo.pull_requests_open_count) is int
    assert repo.pull_requests_open_count == 0
    assert type(repo.issues_total_count) is int
    assert repo.issues_total_count == 0
    assert type(repo.issues_open_count) is int
    assert repo.issues_open_count == 0
    assert type(repo.issues_open_old_count) is int
    assert repo.issues_open_old_count == 0
    assert repo.issues_open_old_count == 0


def test_repository_setup_dict():
    # Variables setup
    json = dict(
        id="id",
        nameWithOwner="owner/name",
        owner="owner",
        name="name",
        url="https://github.com/",
        createdAt="1970-01-01",
        updatedAt="2020-12-31",
        primaryLanguage=dict(name="Python"),
        licenseInfo=dict(name="Unlicense"),
        stargazers=dict(totalCount=42),
        forks=dict(totalCount=4),
        releases=dict(totalCount=1),
        pullRequests=dict(totalCount=32),
        pullRequestsOpen=dict(totalCount=16),
        issues=dict(totalCount=64),
        issuesOpen=dict(totalCount=8),
    )

    # Object init
    repo = Repository()

    # Object attributes setup
    repo.setup_via_json(json)

    # Tests
    assert repo.owner == json["owner"]
    assert repo.name == json["name"]
    assert repo.name_with_owner == f"{json['nameWithOwner']}"
    assert repo.url == json["url"]
    assert repo.primary_language_name == json["primaryLanguage"]["name"]
    assert repo.stargazers_total_count == json["stargazers"]["totalCount"]
    assert repo.stargazers_total_count >= 0


def test_export_repo_info_as_json():
    # Variables setup
    jin = loads(
        """{
      "id": "MDEwOlJlcG9zaXRvcnkyODQ1NzgyMw==",
      "nameWithOwner": "freeCodeCamp/freeCodeCamp",
      "url": "https://github.com/freeCodeCamp/freeCodeCamp",
      "createdAt": "2014-12-24T17:49:19Z",
      "updatedAt": "2021-01-30T17:00:45Z",
      "primaryLanguage": {
        "name": "JavaScript"
      },
      "licenseInfo": {
        "name": "BSD 3-Clause 'New' or 'Revised' License"
      },
      "stargazers": {
        "totalCount": 319121
      },
      "forks": {
        "totalCount": 24475
      },
      "releases": {
        "totalCount": 0
      },
      "pullRequests": {
        "totalCount": 25253
      },
      "pullRequestsOpen": {
        "totalCount": 57
      },
      "issues": {
        "totalCount": 15059
      },
      "issuesOpen": {
        "totalCount": 227
      }
    }"""
    )

    # Object init
    pr = Repository()

    # Object attributes setup
    pr.setup_via_json(jin)
    pr.set_issues_open_old_count(16)
    jout = pr.export_repo_info_as_json()

    # Tests
    assert "repository" in jout
    assert "full_name" in jout["repository"]
    assert "id" in jout["repository"]
    assert "owner" in jout["repository"]
    assert "name" in jout["repository"]
    assert "url" in jout["repository"]
    assert "created_at" in jout["repository"]
    assert "updated_at" in jout["repository"]
    assert "primary_language_name" in jout["repository"]
    assert "license_info_name" in jout["repository"]
    assert "stargazers_total_count" in jout["repository"]
    assert "forks_total_count" in jout["repository"]
    assert "releases_total_count" in jout["repository"]
    assert "pull_requests_total_count" in jout["repository"]
    assert "pull_requests_open_count" in jout["repository"]
    assert "issues_total_count" in jout["repository"]
    assert "issues_open_count" in jout["repository"]
    assert "issues_open_old_count" in jout["repository"]
    assert jout["repository"]["issues_open_old_count"] == 16
