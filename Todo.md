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

- OK Implement ModelViewSet for all models

- WIP Endpoint For inserting new Loan Application

  - status can't be an input, OK it should be set to new
  - verification_status can't be an input, OK it should be set to pending

- WIP Endpoint For updating Loan Application:
  - assign Verifier should change status to Assigned
  - change Verification Status to Verified and insert Verification Document
  - it should save a history of changes
