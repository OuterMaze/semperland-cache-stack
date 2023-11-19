CURPATH="$(dirname "$(realpath "$(pwd)/$0")")"
D="$(dirname "$CURPATH")/cache-server"
(cd "$D" && docker build . -t semperland-dev/cache-server)
