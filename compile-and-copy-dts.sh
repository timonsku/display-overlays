#!/bin/bash

cd panels
for d in * ; do
    cd $d
    echo "Compiling $d"
    dtc -@ -I dts -O dtb -o $d.dtbo -b 0 -@ $d.dts
    cp $d.dtbo /boot/overlays/
    cd ..
done
