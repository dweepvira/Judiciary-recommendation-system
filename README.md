# Judiciary Recommendation System

### Project Overview

This repository contains the source code for the Judiciary Recommendation System project, designed to facilitate judicial recommendations using AI-driven insights. The project is structured into two main components:

1. jrs/ - This directory contains the frontend of the application, built using React. The UI is designed for a seamless user experience, allowing users to interact with the judiciary recommendation system efficiently.

2. Judiciary System/ - This directory houses the backend, implemented in Python. The backend processes user inputs, trains a machine learning model, and serves the appropriate recommendations based on legal data.

### Data and Model

The system utilizes a machine learning model trained specifically for judiciary-related tasks. A crucial component of the project is the pickle file (file.pkl), which stores the trained model. This file is not included in the repository but can be downloaded from the following link:

[Download file.pkl](https://drive.google.com/file/d/19cxCtuvdGeQNQ31uLy0nuneW8Rac33kG/view?usp=sharing)

The backend loads this pickle file to perform inference, generating recommendations based on user queries and input case details.
