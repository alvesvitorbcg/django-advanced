class Errors:
    ROLE_NOT_VALID = "Employee role is not valid"
    USER_IS_NOT_EMPLOYEE = "User is not employee"
    VERIFICATION_STATUS_CANT_BE_ASSIGNED_WITHOUT_VERIFIER = "Verification status can only be 'Assigned' if a Verifier is assigned to the Loan Application."
    VERIFICATION_STATUS_CANT_BE_DECIDED_WITHOUT_VERIFIER = "Verification status can only be 'Verified' or 'Failed' if a Verifier had been previously assigned."
    STATUS_CANT_BE_DECIDED_WITHOUT_REVIEWER = "Status can only be 'Approved' or 'Rejected' if a reviewer and a verifier had been previously assigned and the verification status is 'Verified'."
    REVIEWER_CANT_BE_ASSIGNED_IS_NOT_VERIFIED = "Reviewer can only be assigned if the verification status is 'Verified'."
    VERIFICATION_STATUS_CANT_BE_VERIFIER_WITHOUT_DOCUMENTS = "Verification status can only be 'Verified' if there is at least one verification document."
