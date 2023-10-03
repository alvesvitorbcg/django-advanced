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

- OK Create Endpoint For inserting new Customer
- WIP Create Endpoint For inserting new Loan Application
  - status can't be an input, it should be set to new
  - verification_status can't be an input, it should be set to pending
- OK Create Endpoint to list Loan Applications

- WIP Create Endpoint For updating Loan Application:
  - assign Verifier
    - change status to Assigned
  - change Verification Status to Verified and insert Verification Document
  - assign Reviewer
  - Change Status to Approved, Rejected or New
  - it shuold save a history of changes
