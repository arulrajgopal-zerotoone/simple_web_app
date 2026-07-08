# Infrastructure setup



terraform init -var-file="../config/dev.tfvars"
terraform plan -var-file="../config/dev.tfvars"
terraform apply -var-file="../config/dev.tfvars"
terraform destroy -var-file="../config/dev.tfvars"