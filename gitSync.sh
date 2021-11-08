git checkout main
git remote add remoter-repo https://github.com/odoo/odoo.git
git fetch remoter-repo 14.0
git merge remoter-repo/14.0  --allow-unrelated-histories "merge grom remote"
# git remote rm remoter-repo