terraform {
    required_version = ">= 1.0"
    backend "local" {}
    required_providers {
      google = {
        source = "hashicorp/google"
      }
    }
}

provider "google" {
    project = var.project
    region = var.region 
    credentials = file("gcs_service_acc.json")  
}

#create GCS bucket for my project data

resource "google_storage_bucket" "project_data_bucket" {
    name = "${var.bucket_name}_${var.project}"
    location = var.region  

    storage_class = var.storage_class
    uniform_bucket_level_access = true

    versioning {
      enabled = true
    }
    force_destroy = true
}

#create a staging data set in big uery
resource "google_bigquery_dataset" "staging_dataset" {
  dataset_id = var.staging_dataset
  project   = var.project 
  location = var.region 
}

#create a production data set in big query
resource "google_bigquery_dataset" "production_dataset" {
  dataset_id = var.production_dataset 
  project   = var.project 
  location = var.region 
}