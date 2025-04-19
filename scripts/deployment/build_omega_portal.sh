#!/bin/bash

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸


# "OFF-WHITE™" c/o "VIRGIL ABLOH"
# "DIVINE CLI PORTAL" "BUILD SCRIPT"
# "TECHNICAL INTERFACE" "2025"

# "COLORS" FOR "DIVINE" "OUTPUT"
BLACK='\033[0;30m'
WHITE='\033[1;37m'
ORANGE='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

# "FUNCTION" TO "DISPLAY" "DIVINE" "LOGO"
display_logo() {
    echo -e "${WHITE}"
    echo "  \"OMEGA\""
    echo ""
    echo "      ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗ "
    echo "     ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗"
    echo "     ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║"
    echo "     ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║"
    echo "     ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║"
    echo "      ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝"
    echo ""
    echo "  \"CLI PORTAL\""
    echo ""
    echo -e "${BLACK}${WHITE}                           FOR \"DIVINE CLI PORTAL\" BUILD                          ${RESET}"
    echo -e "${BLACK}${WHITE}                           c/o \"VIRGIL ABLOH\"                                ${RESET}"
    echo ""
    echo -e "${ORANGE}          \"TECHNICAL INTERFACE\" \"2025\" \"OFF-WHITE™\" ${RESET}"
    echo ""
}

# "CHECK" FOR "DOCKER" "INSTALLATION"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}\"ERROR:\" Docker is not installed. Please install Docker to build the \"DIVINE CLI PORTAL\".${RESET}"
    exit 1
fi

# "DISPLAY" "DIVINE" "LOGO"
display_logo

# "BUILD" THE "DIVINE" "CONTAINER"
echo -e "${WHITE}\"BUILDING\" \"DIVINE CLI PORTAL\"...${RESET}"
docker build -t omega_cli_portal:divine -f Dockerfile.omega_portal .

# "CHECK" "BUILD" "STATUS"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}\"SUCCESS:\" \"DIVINE CLI PORTAL\" built successfully!${RESET}"
    echo -e "${ORANGE}\"JAH JAH BLESS\"${RESET}"
    echo -e "${WHITE}\"c/o VIRGIL ABLOH\"${RESET}"
    
    # "ASK" IF "USER" WANTS TO "RUN" THE "CONTAINER"
    read -p $'\033[1;37m\"RUN\" \"DIVINE CLI PORTAL\"? (y/n): \033[0m' run_container
    if [[ $run_container =~ ^[Yy]$ ]]; then
        echo -e "${WHITE}\"STARTING\" \"DIVINE CLI PORTAL\"...${RESET}"
        docker run -it --rm \
            -v $(pwd):/app \
            -p 8080:8080 \
            --name omega_cli_portal \
            omega_cli_portal:divine
    fi
else
    echo -e "${RED}\"ERROR:\" Failed to build \"DIVINE CLI PORTAL\".${RESET}"
    exit 1
fi 