INSERT INTO auth_user ("password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
 VALUES('pbkdf2_sha256$600000$EKfjJ0ouISecHzufImyJvH$JJOrbOsldm9oCt51tsLzu/qK8UU1/VjtjW0CGZeI/ac=', NULL, true, 'admin', '', '', 'admin@admin.com', true, true, NOW());