# CSCE3550JWKServerEXTENSION
# Student Name: Hasti Rathod
# Subject: CSCE 3550
# Student ID: 11448416
# EUID- hhr0013
# Project2: Extending JWKS Server

**Overview of JWT JWKS Server**

Welcome to the JWT JWKS Server, a comprehensive Node.js application crafted to serve public keys linked to unique identifiers (kid) for the validation of JSON Web Tokens (JWTs). This server emphasizes security through key expiry management and provides an authentication endpoint for JWT issuance.

## Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Using the Server](#using-the-server)
- [Configuration Options](#configuration-options)
- [Starting the Server](#starting-the-server)
- [Available Endpoints](#available-endpoints)
  - [/jwks](#jwks-endpoint)
  - [/auth](#auth-endpoint)
- [Testing Your Setup](#testing-your-setup)
- [Contributing to the Project](#contributing-to-the-project)
- [Licensing Information](#licensing-information)

## Introduction

This project aims to facilitate the verification of JWTs by providing a secure way to manage and serve public keys. It’s built using Node.js and focuses on maintaining a secure environment for JWT management.

## Prerequisites

Before you start, ensure you have the following software installed on your machine:

- Node.js (version 14 or later)
- npm (Node Package Manager)

## Installation Steps

1. First, clone the repository to your local environment:

   ```bash
   git clone https://github.com/hasti0013/CSCE3550JWKServer.git
2. Move into the project directory
3. Install the necessary dependencies:
npm install
Configuration Options
The server’s settings and RSA key pair management can be found in the server.js file. Initially, it generates one RSA key pair for demonstration. For production usage, a more comprehensive key management approach is recommended.
To run the jwk.py or test.py files in VS Code, open the terminal and enter one of the following commands:
python3 jwk.py
  or
python3 test.py

Licensing Information
This project is licensed under the MIT License. For more details, refer to the LICENSE file.
