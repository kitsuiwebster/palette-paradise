#!/bin/bash

for i in $(seq -f "%03g" 0 99)
do
  mkdir $i
done
