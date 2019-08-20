#!/bin/bash

qstat -u $USER | grep -E "(Q|R)" | tail -n +3 | cut -c1-10 | xargs qdel
