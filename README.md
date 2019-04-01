To set up, place Dockerfile, bucket\_actions.py, copyscript.py, and env in the same folder

To operate:

1) Run 'docker build .', note final successful build id
2) Edit the 'env' file to add your credentials with format VAR=VAL
3) Run 'docker run -it --env-file env \<build-id> \<from-bucket> \<to-bucket> \<threshold>'


The 'tests.py' file is not needed to run the script, but is included to show my work.
