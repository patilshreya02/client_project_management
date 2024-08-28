**Django API Design - Machine Test**
This repository contains the implementation of a machine test where I designed RESTful APIs using Django.

# Overview
Task Details
Entities: User, Client, Project.
# APIs Implemented:
# Clients:
List all clients (GET /clients/)
Register a new client (POST /clients/)
Retrieve client info with projects (GET /clients/:id)
Update client info (PUT/PATCH /clients/:id)
Delete a client (DELETE /clients/:id)
# Projects:
Add a new project for a client and assign users (POST /clients/:id/projects/)
List all projects assigned to the logged-in user (GET /projects/)
# Key Considerations
1. The system supports multiple users and clients.

2. Clients can have multiple projects.

3. Projects can be assigned to multiple users.
