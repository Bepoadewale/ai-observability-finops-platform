#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
terraform fmt -check -recursive infrastructure/terraform
make terraform-validate
make cloud-contracts-validate
make kustomize-validate
