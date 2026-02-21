#!/bin/bash
rm -rf dist
mkdir -p dist
cp -r en fr fr-old ar icons fonts dist/
cp index.html manifest.json sw.js agpeya.js agpeya-style.css dist/
cp coptic-cross.png cog_wheel.png Avva_Shenouda.ttf og-image.png dist/
