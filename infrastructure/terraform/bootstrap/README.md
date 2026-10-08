# Terraform State Bootstrap

This future root creates only this repository’s encrypted/versioned state bucket,
lock table, and budget alert. It is not applied by this PR. Use a non-committed
`terraform.tfvars` with the expected account and alert email.
