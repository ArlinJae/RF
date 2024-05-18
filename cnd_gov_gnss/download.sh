#!/bin/bash

# FTP server details
FTP_SERVER="ftp.mrn.gouv.qc.ca"
FTP_USER="anonymous"
FTP_PASS=""

# Directory on the FTP server
FTP_DIR="/Public/GPS"

# Local directory to save the downloaded files
LOCAL_DIR="./gnss_data"

# Create local directory if it doesn't exist
mkdir -p $LOCAL_DIR

# Log into FTP server and download files
ftp -inv $FTP_SERVER <<EOF
user $FTP_USER $FTP_PASS
cd $FTP_DIR

# Get list of directories (e.g., Caplan, Chibougamau, etc.)
dirs=\$(ls)

for dir in \$dirs; do
    lcd $LOCAL_DIR/\$dir
    mkdir -p \$dir
    cd \$dir

    # Get list of subdirectories (e.g., mon20434, mon20444, etc.)
    subdirs=\$(ls)
    for subdir in \$subdirs; do
        lcd $LOCAL_DIR/\$dir/\$subdir
        mkdir -p \$subdir
        cd \$subdir

        # Download all zip files in the subdirectory
        mget *.zip
        cd ..
    done
    cd ..
done
bye
EOF

# Unzip all downloaded files
for dir in $LOCAL_DIR/*/*; do
    for file in \$dir/*.zip; do
        unzip -o \$file -d \$dir
    done
done

echo "Download and extraction complete. Files saved in $LOCAL_DIR"
