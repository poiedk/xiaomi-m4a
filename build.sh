#!/bin/bash

echo "Simple script to build Openwrt image for the Xiaomi Mi Router 4A Gigabit Router"

echo "Update feeds..."
./scripts/feeds update -a

echo "Install all packages from feeds..."
./scripts/feeds install -a

echo "Copy default custom config to make image"
cp Config-custom .config

echo "Set to use default config"
make defconfig

echo "Download packages before build"
make download

echo "Start build and log to build.log"
make -j$(($(nproc)+1)) V=s CONFIG_DEBUG_SECTION_MISMATCH=y 2>&1 | tee build.log

exit 0
