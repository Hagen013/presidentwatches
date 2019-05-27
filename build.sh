#!/bin/bash

# VUE-CLI admin application
cd ./admin/
npm run build
cd ..
cp -r ./admin/dist/ ./compose/nginx/

# FRONTEND
cd ./client/;
rm -rf /static /static_production;
# npm i;
nvm use 8.12.0
npm  run build;
gulp build;
cd ..;
# BACKEND
source ./server/venv/bin/activate;
cd ./server/;

echo 'yes' | python3 manage.py collectstatic --settings=config.settings.production;
deactivate;
cd ..;
# STATIC_PRODUCTION TO NGINX STATIC
rm -rf ./compose/nginx/static_production;
cp -r ./client/static_production ./compose/nginx/;
# ADD HASH TO STATIC FILE NAMES IN 
# STATIC FILES AND IN TEMPLATES
hash_suffix="$(date | md5sum | cut -c1-7)"
echo "HASH_SUFFIX=${hash_suffix}"

TEMPLATES_PATH="$(cd ./client/templates && pwd && cd ../..)"
echo "TEMPLATES_PATH=${TEMPLATES_PATH}"
# STATIC FILES
cd ./compose/nginx/static_production

STATIC_FILE_PATHS=(
    "css/styles.css"
    "css/profile.css"
    "js/common.js"
    "js/main.js"
    "js/productPage.js"
    "js/catalogPage.js"
    "js/cartPage.js"
)

# REPLACE STATIC FILES AND TEMPLATES
for file_name in ${STATIC_FILE_PATHS[@]}
do
    new_file_name="${file_name%%.*}_${hash_suffix}.${file_name#*.}"
    cp $file_name $new_file_name
    find $TEMPLATES_PATH -name '*.html' -exec sed -i "s/$(sed 's/\//\\\//g' <<< $file_name)/$(sed 's/\//\\\//g' <<< $new_file_name)/g" '{}' \;
    echo "${file_name} hashed"
done

cd ..
