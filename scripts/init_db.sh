#!/bin/bash

set -e
set -u

export PGPASSWORD=postgres

psql \
    -X \
    -U postgres \
    -h 0.0.0.0 \
    -p 6432 \
    -f ./scripts/create_db.sql \
    --echo-all \
    --set AUTOCOMMIT=off \
    --set ON_ERROR_STOP=on

psql_exit_status = $?

if [ $psql_exit_status != 0 ]; then
    echo "psql failed while trying to run this sql script" 1>&2
    exit $psql_exit_status
fi

echo "sql script successful"
exit 0