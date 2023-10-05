PATH_TO_SONAR=$1
coverage run ./manage.py test src && coverage report -m && coverage xml
$PATH_TO_SONAR/sonar-scanner \
-Dsonar.projectKey=physical-verification-system \
-Dsonar.sources=src/ \
-Dsonar.exclusions=**/migrations/** \
-Dsonar.coverage.exclusions=**/tests/**,**/test*.py,manage.py,**/physical_verification_project/**,**/apps.py, \
-Dsonar.python.coverage.reportPaths=coverage.xml \
-Dsonar.login=sqp_fa234517e3b80e943a233261e2e0ab2d367ab7df \
-Dsonar.host.url=http://localhost:9000 \