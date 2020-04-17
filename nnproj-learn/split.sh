#!/usr/bin/env zsh

split_set_impl() {
  src_dir="$PWD/data/type/$2/$1_$3"
  dst_dir="$PWD/data/split/raw/$2"

  mkdir -p $dst_dir
  ls -d $src_dir/* | xargs -L1 -I{} python split.py $1 {} $dst_dir
}

split_set() {
  split_set_impl $@ 1
  split_set_impl $@ 2
}

split_set 1992 train
split_set 1992 test
split_set 2016 train
split_set 2016 test
