FROM debian
COPY file_deskriptor_checker.sh .
RUN chmod +x file_deskriptor_checker.sh
RUN touch test_file.txt  # To check the script functionality
CMD ./file_deskriptor_checker.sh
