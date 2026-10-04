FROM mcr.microsoft.com/dotnet/sdk:8.0-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# System packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        curl \
        ca-certificates \
        less \
        procps \
        iproute2 \
        bash \
    && rm -rf /var/lib/apt/lists/*

# PowerShell installation
RUN wget -q https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb \
        -O /tmp/packages-microsoft-prod.deb \
    && dpkg -i /tmp/packages-microsoft-prod.deb \
    && rm /tmp/packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends powershell \
    && rm -rf /var/lib/apt/lists/*

# Install PowerShell modules and verify their installation
RUN pwsh -NoLogo -NoProfile -Command \
    '$ErrorActionPreference = "Stop"; \
     Install-Module -Name Az -Scope AllUsers -Repository PSGallery -Force -AllowClobber; \
     Install-Module -Name AADInternals -Scope AllUsers -Repository PSGallery -Force -AllowClobber; \
     Install-Module -Name AADInternals-Endpoints -Scope AllUsers -Repository PSGallery -Force -AllowClobber; \
     Install-Module -Name Microsoft.Entra -Scope AllUsers -Repository PSGallery -Force -AllowClobber; \
     Install-Module -Name Microsoft.Graph -Scope AllUsers -Repository PSGallery -Force -AllowClobber; \
     Get-Module -ListAvailable Az, AADInternals, AADInternals-Endpoints, Microsoft.Entra, Microsoft.Graph'

WORKDIR /workspace