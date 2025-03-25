# Move data files out of the MacOS subfolder and re-sign
# see https://github.com/Nuitka/Nuitka/issues/2906

for dir in "dependency_licenses_full.txt" "dependency_licenses_summary.txt" "gooey" "icons" "jaraco"; do 
  mv "build/gui.app/Contents/MacOS/$dir" "build/gui.app/Contents/Resources/"
  cd "build/gui.app/Contents/MacOS/" # needs to be a relative symlink
  ln -s "../Resources/$dir" "."
  cd -
done

mv build/gui.app build/panoptes_aggregation.app
/usr/bin/codesign -s - --force --deep --preserve-metadata=entitlements build/panoptes_aggregation.app
