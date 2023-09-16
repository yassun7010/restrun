#!/bin/sh

set -e

cd "$(dirname "$0")/../examples/petstore"

restrun --verbose generate
