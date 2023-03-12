variable "project" {
  description = "Your GCP Project ID"
  type = string
}

variable "region" {
  description = "Your GCP Project region"
  type = string
}

variable "bucket_name" {
  description = "Your google cloud storage bucket name"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket"
  type = string
}

variable "staging_dataset" {
    description = "This is the staging dataset that will reside in BigQuery"
    type = string
}

variable "production_dataset" {
    description = "This is the production dataset that will reside in BigQuery"
    type = string
}
