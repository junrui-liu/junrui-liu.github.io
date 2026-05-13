KEY_HEX=$(echo -n "Loremipsumdolorsitamet/consecteturadipiscing" | shasum -a 256 | awk '{print $1}')
IV_HEX=$(echo -n '0123456789abcdef' | xxd -p -c 256)
echo -n $1 | openssl enc -aes-256-cbc -K "$KEY_HEX" -iv "$IV_HEX" -base64 -A