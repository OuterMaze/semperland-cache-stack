SOURCE_FILE="$(dirname "$0")/.env-client"
TARGET_FILE=$(mktemp)
MY_LAN_IP=$1
sed "s/my-lan-ip/$MY_LAN_IP/g" "$SOURCE_FILE" > "$TARGET_FILE"
docker run --rm --env-file "$TARGET_FILE" -p 8080:8080 semperland-dev/cache-server
