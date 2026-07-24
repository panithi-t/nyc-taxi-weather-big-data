# Project Plan

**Course:** CS-675 Big Data Analytics at Cloud Scale  
**Project Title:** Cloud-Scale Analysis of NYC Taxi Operations Under Different Weather Conditions  
**Author:** Panithi Tawethipong

---

# 1. Project Overview

## Background

New York City generates millions of taxi trips every month, producing one of the largest publicly available urban transportation datasets. At the same time, weather conditions such as heavy rain, snow, extreme temperatures, and reduced visibility can significantly influence travel demand, traffic conditions, and passenger behavior. Understanding these relationships can help transportation agencies, fleet operators, and city planners better anticipate demand and improve operational efficiency.

This project will analyze large-scale NYC Yellow Taxi trip records together with historical New York City weather observations using Apache Spark. The analysis will first be developed locally using a small subset of the data and then deployed to AWS cloud infrastructure to process more than 100 million taxi trip records.

## Project Objectives

The primary objectives of this project are:

- Build a scalable Spark analytics pipeline for large transportation datasets.
- Integrate multiple public datasets through meaningful joins.
- Evaluate how weather conditions influence taxi demand and trip characteristics.
- Deploy the same analytics pipeline to AWS using cloud-native storage and query services.
- Demonstrate reproducible cloud infrastructure using Terraform.
