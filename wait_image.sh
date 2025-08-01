#!/bin/bash


IMAGE="$1"          
INTERVAL=10         
TIMEOUT=300         
ELAPSED=0

echo "⏳ Wait untill present '$IMAGE' в registry..."

while true; do
  
    OUTPUT=$(docker buildx imagetools inspect "$IMAGE" --format '{{ json .SBOM.SPDX }}' 2>&1)
    

    if [[ $? -eq 0 && "$OUTPUT" != *"not found"* && "$OUTPUT" != *"ERROR:"* ]]; then
        INSTALLED=$(docker buildx imagetools inspect "$IMAGE" --format '{{ range .SBOM.SPDX.packages }}{{ println .name .versionInfo }}{{ end }}' | sort)
        CVE=$(docker buildx imagetools inspect "$IMAGE" --format '{{ json .SBOM.SPDX }}' | grype)
        echo "✅ Image found!"
        echo "$OUTPUT" | jq . 
        echo "INSTALLED PACKAGES:"
        echo "$INSTALLED"
        echo "CVE:"
        echo "$CVE"
        break
    else
        echo "❌ Image still is not exist. Wait $INTERVAL seconds..."
        sleep $INTERVAL
        ELAPSED=$((ELAPSED + INTERVAL))
        
        if [ $ELAPSED -ge $TIMEOUT ]; then
            echo "⏰ Awaiting time is gone ($TIMEOUT sec)."
            exit 1
        fi
    fi
done
