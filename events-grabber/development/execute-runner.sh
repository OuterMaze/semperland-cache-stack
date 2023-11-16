SOURCE_FILE="$(dirname "$0")/.env-runner"
TARGET_FILE=$(mktemp)
MY_LAN_IP=$1
sed "s/my-lan-ip/$MY_LAN_IP/g" "$SOURCE_FILE" > "$TARGET_FILE"
docker run --rm --env-file "$TARGET_FILE" semperland-dev/cache-runner
