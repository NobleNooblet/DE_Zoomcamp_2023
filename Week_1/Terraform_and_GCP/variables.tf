locals {
    data_lake_bucket = "dtc_data_lake"
}

variable "project" {
  description = "Your GCP Project ID"
}

variable "region" {
  description = "Region for GCP resource"
  default = "europe-west6"
  type = string
}

variable "bucket_name" {
    description = "The name of the Google Cloud Storage Bucket.  Globally Unique"
    default = ""
}

variable "storage_class" {
  description = "Storage class type for your bucket"
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "bigquery dataset that raw data will be written to"
  type = string
  default = "trips_data_all"
}

variable "TABLE_NAME" {
  description = "bigquery table"
  type = string
  default = "ny_trips"
}