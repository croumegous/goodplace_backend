
HEADER="Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTI3MjE0MzAsInN1YiI6Ijg0YTQ5ZTQ5LTc5ZmYtNDdhMS05ZGU4LWJmOTAwNjRhY2RhZSJ9.ZWYnG8OLPn1SPCtAAajpp8WApvUbU8NCZnyqFseSGVQ"

OPEN_API_DOC_URL="http://127.0.0.1:8000/openapi.json"
VERBOSITY="normal" # quiet, normal, verbose, debug
schemathesis run $OPEN_API_DOC_URL --header "$HEADER" --hypothesis-verbosity $VERBOSITY --store-network-log=cassette.yaml --hypothesis-deadline 2000
