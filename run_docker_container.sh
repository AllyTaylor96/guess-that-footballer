#!/bin/bash


docker run --rm -it -v ${PWD}:${PWD} \
	-w ${PWD} \
	guess-that-footballer bash
