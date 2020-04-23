#!/usr/bin/env python3

import os
from io import BytesIO

import pytest

from app import application


@pytest.fixture(scope="session")
def client():
    with application.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def valid_apk_path():
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "test_resources",
        "InsecureBankv2.apk",
    )


class TestApp(object):
    def test_home_page(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"<b>RiskInDroid</b> is a tool for quantitative risk" in response.data

    def test_results_page(self, client):
        response = client.get("/results")
        assert response.status_code == 200

    def test_get_apk_list(self, client):
        response = client.get("/apks")
        assert response.status_code == 200
        assert response.json["current_page"] == 1

    def test_get_apk_details(self, client):
        response = client.get(
            "/details", query_string={"md5": "56dc73999fae5aa5bcb26844d245b826"}
        )
        assert response.status_code == 200
        assert response.json["name"] == "com.spotify.music.apk"

    def test_apk_upload(self, client, valid_apk_path):
        with open(valid_apk_path, "rb") as apk_file:
            apk_file_bytes = BytesIO(apk_file.read())
        response = client.post(
            "/upload", data={"file": (apk_file_bytes, "InsecureBankv2.apk")}
        )
        assert response.status_code == 200
        assert response.json["name"] == "InsecureBankv2.apk"
        assert (
            len([x for x in response.json["permissions"] if x["cat"] == "Declared"])
            == 12
        )
