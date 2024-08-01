# Local Key Vault

Super light weight key vault for local development.  This is not intended for production use. Take the code, modify it, make it your own, I don't care :)

## Overview

Local Key Vault is a Python package that mimics the behavior of Azure KeyVault but operates locally. It uses the `cryptography` package for encryption and decryption, allowing you to securely store and manage secrets on your local machine. Additionally, it provides a local server interface, enabling you to interact with the key vault via HTTPS requests.

## Features

- Create and manage scopes (similar to key vaults)
- Securely store and retrieve secrets
- List and delete secrets
- Local server for HTTPS interaction

## Installation

Install the required dependencies:

```sh
pip install flask pyOpenSSL cryptography
