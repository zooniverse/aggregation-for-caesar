cd docs
shopt -s dotglob
make html
rm -r _s*
rm -r ../doctrees
mv build/html/* .
mv build/doctrees ..
cd ..
