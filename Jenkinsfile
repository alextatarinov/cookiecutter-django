node {
    def branches = [
        'develop': [
            'host': '1.1.1.1',
            'url': 'https://clevergames-develop.enkonix.com',
            'pem': '',
        ],
        'master': [
            'host': '1.1.1.1',
            'url': 'https://4challenge-games.nl',
            'pem': '',
        ],
    ]

    def branch = branches[env.BRANCH_NAME]
    def host = branch['host']
    def url = branch['url']
    def pem = branch['pem']

    stage('Build') {
        result = sh (script: """
            ssh -T -i ${pem} ubuntu@${host} << EOF
            cd clever_backend

            source venv/bin/activate
            poetry install --no-dev || exit 1

            # Running linting for all python files in the project:
            flake8 || exit 1

            # Lint .env file
            dotenv-linter .env || exit 1

            # Run checks to be sure settings are correct (production flag is required):
            python manage.py check --deploy --fail-level WARNING || exit 1

            # Check that staticfiles app is working fine:
            python manage.py collectstatic --no-input --dry-run --verbosity=0 || exit 1

            # Check that all migrations worked fine:
            python manage.py makemigrations --dry-run --check || exit 1

            # Checking if all the dependencies are secure and do not have any
            # known vulnerabilities:
            safety check --bare --full-report || exit 1

            python manage.py drop_test_database --noinput
            python manage.py test --settings=config.settings.local --failfast || exit 1

            python manage.py migrate || exit 1
            python manage.py collectstatic --noinput || exit 1

            sudo venv/bin/python deploy/build_config.py || exit 1

            sudo nginx -t || exit 1
            sudo service nginx reload

            sudo supervisorctl update
            sudo supervisorctl restart all
        """, returnStatus: true)
    }

    stage('Slack') {
        if (result == 0) {
            currentBuild.result = 'SUCCESS'
            slackSend color: 'good', message: "Backend Deploy " + url + " is success!", channel: "#clevergames_jenkins"
        } else {
            currentBuild.result = 'FAILURE'
            slackSend color: 'bad', message: "Backend Deploy " + url + " is FAILED!!! See console log in " + env.BUILD_URL + "console", channel: "#clevergames_jenkins"
        }
    }
}
