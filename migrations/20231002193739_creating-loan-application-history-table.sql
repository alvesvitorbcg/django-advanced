-- public.loan_applications_loanapplication definition

-- Drop table

-- DROP TABLE loan_applications_loanapplication;

CREATE TABLE loan_applications_loanapplicationhistory (
	id bigserial NOT NULL,
	loan_application_id bigserial NOT NULL,
	datetime_created timestamptz NOT NULL,
	datetime_updated timestamptz NOT NULL,
	status int2 NULL,
	verification_status int2 NULL,
	manager_id int4 NOT NULL,
	reviewer_id int4 NOT NULL,
	loan_amount int4 NOT NULL,
	customer_id int8 NOT NULL,
	verifier_id int8 NOT NULL,
	CONSTRAINT loan_applications_loanapplicationhistory_loan_amount_check CHECK ((loan_amount >= 0)),
	CONSTRAINT loan_applications_loanapplicationhistory_manager_id_check CHECK ((manager_id >= 0)),
	CONSTRAINT loan_applications_loanapplicationhistory_pkey PRIMARY KEY (id),
	CONSTRAINT loan_applications_loanapplicationhistory_reviewer_id_check CHECK ((reviewer_id >= 0)),
	CONSTRAINT loan_applications_loanapplicationhistory_status_check CHECK ((status >= 0)),
	CONSTRAINT loan_applications_loanapplicationhistory_verification_status_check CHECK ((verification_status >= 0))
);
CREATE INDEX loan_applications_loanapplicationhistory_customer_id_c990d2fc ON public.loan_applications_loanapplicationhistory USING btree (customer_id);
CREATE INDEX loan_applications_loanapplicationhistory_verifier_id_6cdcd63f ON public.loan_applications_loanapplicationhistory USING btree (verifier_id);


-- public.loan_applications_loanapplication foreign keys

ALTER TABLE public.loan_applications_loanapplicationhistory ADD CONSTRAINT loan_applications_lohistory_customer_id_c990d2fc_fk_customers FOREIGN KEY (customer_id) REFERENCES customers_customer(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE public.loan_applications_loanapplicationhistory ADD CONSTRAINT loan_applications_lohistory_verifier_id_6cdcd63f_fk_employees FOREIGN KEY (verifier_id) REFERENCES employees_employee(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE public.loan_applications_loanapplicationhistory ADD CONSTRAINT loan_applications_lohistory_loan_id_6cdcd63f_fk_loan_application_id FOREIGN KEY (loan_application_id) REFERENCES employees_employee(id) DEFERRABLE INITIALLY DEFERRED;