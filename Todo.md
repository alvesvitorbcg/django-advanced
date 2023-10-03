## Boilerplate

- OK Create Django application
- OK Install Rest framework

## Models

- OK Create Customer Model
- OK Create Employee Model
- OK Create Role Model
- OK Create Verification Document Model
- OK Create Loan Application Model
- TODO Create Loan Application History Model

## Endpoints

- Create Endpoint For inserting new Customer
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
