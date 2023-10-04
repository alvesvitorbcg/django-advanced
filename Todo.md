## Boilerplate

- OK Create Django application
- OK Install Rest framework

## Models

- OK Create Customer Model
- OK Create Employee Model
- OK Create Role Model
- OK Create Verification Document Model
- OK Create Loan Application Model
- OK Create Loan Application History Model

## Endpoints

- OK Implement ModelViewSet for all models

- WIP Endpoint For inserting new Loan Application

  - OK status should be set to new
  - OK verification_status should be set to pending

- WIP Endpoint For updating Loan Application:
  - OK can only set verification status to 'Assigned' if verifier is defined
  - OK can only set verification status to 'Verified' or 'Failed' if a Verifier had been previously assigned
  - OK can only set status to 'Approved' or 'Rejected' if a reviewer and a verifier had been previouly assigned and the verification status is 'Verified'
  - WIP assign Verifier should change status to Assigned
  - WIP can only set verification status to Verified if there is Verification Document
  - it should save a history of changes
