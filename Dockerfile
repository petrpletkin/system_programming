FROM debian
COPY script.sh .
RUN chmod +x script.sh
RUN touch test_file.txt  # To check the script functionality
CMD ./script.sh
