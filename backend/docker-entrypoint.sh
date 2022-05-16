#!/bin/bash

echo "Waiting for DB to start..."
./wait-for db:5432