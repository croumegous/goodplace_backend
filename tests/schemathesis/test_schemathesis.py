import pytest
import schemathesis
from schemathesis.checks import DEFAULT_CHECKS

from good_place.main import app
from tests.fixtures.db import client

# Schemathesis is a modern API testing tool for web applications see : https://github.com/schemathesis/schemathesis
schemathesis.fixups.install()

schema = schemathesis.from_asgi("/openapi.json", app)


@pytest.mark.schemathesis
@schema.parametrize()
def test_schemathesis(client, case):
    res = client.request(case.method, case.formatted_path, headers=case.headers)
    case.validate_response(res, DEFAULT_CHECKS)


# schema = schemathesis.from_asgi("/openapi.json", app)

# @pytest.mark.schemathesis
# @schema.parametrize()
# def test_schemathesis(case):
#     res = case.call_asgi()
#     case.validate_response(res, DEFAULT_CHECKS)
