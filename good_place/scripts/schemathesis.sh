OPEN_API_DOC_URL="http://127.0.0.1:8000/openapi.json"
VERBOSITY="normal" # quiet, normal, verbose, debug
schemathesis run $OPEN_API_DOC_URL --hypothesis-verbosity $VERBOSITY --store-network-log=cassette.yaml --hypothesis-deadline 2000
