# Infra Setup

Steps to deploy the required Azure resources.

> **Note:** These steps describe a local deployment. This can also be automated, but automation is outside the scope of this project/repository.

## 1. Clone the repository and navigate to the Terraform path

```bash
cd IAC/terraform/src
```

## 2. Initialize Terraform

```bash
terraform init -var-file="../config/dev.tfvars"
```

## 3. Plan and apply

```bash
terraform plan -var-file="../config/dev.tfvars"
terraform apply -var-file="../config/dev.tfvars"
```

## 4. Destroy

```bash
terraform destroy -var-file="../config/dev.tfvars"
```
