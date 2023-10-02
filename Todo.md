## Boilerplate

- Create Django application
- Install Rest framework

## Models

- Create Customer Model
- Create Employee Model
- Create Role Model
- Create Verification Document Model
- Create Loan Application Model
- Create Loan Application History Model

## Endpoints

- Create Endpoint For inserting new Customer
  -
- Create Endpoint For inserting new Loan Application
  - status: new
  - verification_status: pending
- Create Endpoint to list Loan Applications

- Create Endpoint For updating Loan Application (should save history of changes):
  - assign Verifier
    - change status to Assigned
  - change Verification Status to Verified and insert Verification Document
  - assign Reviewer
  - Change Status to Approved, Rejected or New
