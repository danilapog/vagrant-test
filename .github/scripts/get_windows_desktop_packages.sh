#!/bin/bash
set -e

VERSION="${VERSION}"
BUILD="${BUILD}"
BASE_URL="${PACKAGE_URL}/desktop/win"

echo "Checking Windows Desktop packages for version ${VERSION}.${BUILD}..."

MATRIX_ITEMS=()

# Function to check if package exists
check_package() {
    local url=$1
    if curl --output /dev/null --silent --head --fail "${url}"; then
        return 0
    else
        return 1
    fi
}

# Function to build matrix entry for a package type
check_package_type() {
    local type=$1
    local path=$2
    local prefix=$3
    
    echo "Checking ${type} packages..."
    
    local editions=()
    local platforms=()
    
    # Detect available platforms (x64, x86)
    for platform in "x64" "x86"; do
        # Check community edition for this platform
        local ce_file="${prefix}-${VERSION}.${BUILD}-${platform}"
        case $type in
            portable) ce_file+=".zip" ;;
            inno-setup) ce_file+=".exe" ;;
            advanced-installer) ce_file+=".msi" ;;
        esac
        
        if check_package "${BASE_URL}/${path}/${ce_file}"; then
            if [[ ! " ${platforms[@]} " =~ " ${platform} " ]]; then
                platforms+=("${platform}")
            fi
        fi
    done
    
    # If no platforms found, skip this package type
    if [ ${#platforms[@]} -eq 0 ]; then
        echo "  ✗ No platforms found for ${type}"
        return
    fi
    
    # Check editions (community, enterprise, standalone)
    for platform in "${platforms[@]}"; do
        # Community (no suffix)
        local ce_file="${prefix}-${VERSION}.${BUILD}-${platform}"
        case $type in
            portable) ce_file+=".zip" ;;
            inno-setup) ce_file+=".exe" ;;
            advanced-installer) ce_file+=".msi" ;;
        esac
        
        if check_package "${BASE_URL}/${path}/${ce_file}"; then
            if [[ ! " ${editions[@]} " =~ " community " ]]; then
                editions+=("community")
                echo "  ✓ Community edition found"
            fi
        fi
        
        # Enterprise (-Enterprise suffix)
        local ee_file="${prefix}-Enterprise-${VERSION}.${BUILD}-${platform}"
        case $type in
            portable) ee_file+=".zip" ;;
            inno-setup) ee_file+=".exe" ;;
            advanced-installer) ee_file+=".msi" ;;
        esac
        
        if check_package "${BASE_URL}/${path}/${ee_file}"; then
            if [[ ! " ${editions[@]} " =~ " enterprise " ]]; then
                editions+=("enterprise")
                echo "  ✓ Enterprise edition found"
            fi
        fi
        
        # Standalone (only for inno-setup)
        if [ "$type" == "inno-setup" ]; then
            local sa_file="${prefix}-Standalone-${VERSION}.${BUILD}-${platform}.exe"
            if check_package "${BASE_URL}/${path}/${sa_file}"; then
                if [[ ! " ${editions[@]} " =~ " standalone " ]]; then
                    editions+=("standalone")
                    echo "  ✓ Standalone edition found"
                fi
            fi
        fi
    done
    
    # If editions and platforms found, add to matrix
    if [ ${#editions[@]} -gt 0 ] && [ ${#platforms[@]} -gt 0 ]; then
        local editions_json=$(printf '%s\n' "${editions[@]}" | jq -R . | jq -s -c .)
        local platforms_json=$(printf '%s\n' "${platforms[@]}" | jq -R . | jq -s -c .)
        
        local matrix_entry="{\"type\":\"${type}\",\"editions\":${editions_json},\"platforms\":${platforms_json}}"
        MATRIX_ITEMS+=("${matrix_entry}")
        
        echo "  Matrix entry: ${matrix_entry}"
    else
        echo "  ✗ Insufficient packages for ${type}"
    fi
}

# Check all package types
check_package_type "portable" "generic" "ONLYOFFICE-DesktopEditors"
check_package_type "inno-setup" "inno" "ONLYOFFICE-DesktopEditors"
check_package_type "advanced-installer" "advinst" "ONLYOFFICE-DesktopEditors"

# Build final matrix JSON
if [ ${#MATRIX_ITEMS[@]} -eq 0 ]; then
    echo "ERROR: No Windows Desktop packages found!"
    echo "windows-desktop-packages=" >> $GITHUB_OUTPUT
else
    echo "Found ${#MATRIX_ITEMS[@]} package type(s)"
    MATRIX_JSON=$(printf '%s\n' "${MATRIX_ITEMS[@]}" | jq -s -c .)
    echo "windows-desktop-packages=${MATRIX_JSON}" >> $GITHUB_OUTPUT
    echo "Final Matrix: ${MATRIX_JSON}"
fi
