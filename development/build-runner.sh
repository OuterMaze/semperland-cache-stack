CURPATH="$(dirname "$(realpath "$(pwd)/$0")")"
D="$(dirname "$CURPATH")/events-grabber"
(cd "$D" && docker build . -t semperland-dev/cache-runner)
