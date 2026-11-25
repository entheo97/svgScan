#!/bin/bash

dir="${1:-.}"
out="decoded_output.txt"
list="malicious.txt"

: > "$out"
found=0

for f in "$dir"/*; do
    [ -f "$f" ] || continue

    case "${f,,}" in
        *.svg) ;;
        *) continue ;;
    esac

    file_decoded=""
    while IFS= read -r -d '' comment; do
        cleaned=$(printf '%s' "$comment" | sed -e 's/^<!--//; s/-->$//' | tr -d ' \t\r\n')
        [ -n "$cleaned" ] || continue

        if [[ "$cleaned" =~ ^[A-Za-z0-9+/]+={0,2}$ ]] && (( ${#cleaned} % 4 == 0 )); then
            decoded=$(printf '%s' "$cleaned" | base64 -d 2>/dev/null) || continue
            file_decoded+="$decoded"$'\n'
            printf '%s\n' "$decoded" >> "$out"
        fi
    done < <(grep -Pzo '<!--[\s\S]*?-->' "$f")

    if [ -n "$file_decoded" ] && printf '%s' "$file_decoded" | grep -aFo -f <(grep -v '^[[:space:]]*$' "$list") >/dev/null; then
        echo "Match found in: $f"
        printf '%s' "$file_decoded" | grep -aFo -f <(grep -v '^[[:space:]]*$' "$list")
        found=1
    fi
done

[ "$found" -eq 0 ] && echo "No matches found"
